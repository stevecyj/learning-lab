#!/usr/bin/env python3
"""v2.2.0 eval harness 硬判：零依赖脚本，输出字数留存率 / 破折号密度 / protected spans 粗核。

规格：tasks/current/roadmap-2026H2-v2.0.1-v2.3.md §6（v2.2.0）。
定位：把 judge 模型能被脚本替掉的判定项拿出来硬判——降成本、提稳定性。
判死 vs 报警：字数留存率与破折号密度按 run-eval.md 既有口径直接判过/不过；
protected spans 粗核只报警不判死，缺失留给 judge 复核（粗核是正则匹配，
不判定语义改写是否保真）。

用法（仓库根目录）：
    python3 automation/eval/hard_metrics.py --run tasks/current/eval-runs/<日期>-<版本>/
        # 扫批次目录：自动配对原文本（evals/benchmark-blind.md）与各模型输出，
        # 逐条计算，输出 <目录>/hard-metrics.md 报告和 <目录>/hard-metrics.json
    python3 automation/eval/hard_metrics.py --pair <原文本文件> <改后文本文件>
        # 单条对照：输出可读结果
    python3 automation/eval/hard_metrics.py --stdin <原文本文件>
        # 原文本从文件读，改后文本从 stdin 读；输出可读结果
    python3 automation/eval/hard_metrics.py --pair A.md B.md --report-json
        # 输出单行 JSON，供 automation/eval/README.md 的管道用法拼接 judge 输入

退出码：--run 模式任一长文用例留存率低于硬下限 0.85 时退出码为 1；
批次不完整（零用例批次 / 缺输出）时退出码为 2（报告不可信）；
缺文件、格式异常等自身错误退出码为 2；其余为 0。
"""

import argparse
import json
import re
import sys
from pathlib import Path

# 长文用例判据口径来自 evals/run-eval.md「Long-form / in-place」：
# 字数留存率目标 >= 0.90，硬下限 0.85
RETENTION_TARGET = 0.90
RETENTION_FLOOR = 0.85

# 场景标签里标了 long 的用例按长文判据处理；这个信号同时写死在
# benchmark-blind.md 的标题行里，不依赖 benchmark.md 的预期字段
LONG_TAG = re.compile(r"\blong\b")


def batch_expected_ids(batch):
    """从批次名解析期望覆盖的用例编号集。

    支持 `B01-16`（盲测区间）与旧口径 `SF43-45-SNF34-35`（v1.9.2 回放，
    多个前缀+区间段）。非区间命名（如 targeted-*）返回 None。
    """
    segments = re.split(r"-", batch)
    groups = []  # [(prefix, lo, hi)]
    i = 0
    while i < len(segments):
        seg = segments[i]
        m = re.fullmatch(r"([A-Za-z]*)(\d+)", seg)
        if not m:
            return None
        prefix = m.group(1).upper()
        num = int(m.group(2))
        if i + 1 < len(segments) and re.fullmatch(r"\d+", segments[i + 1]):
            lo, hi = num, int(segments[i + 1])
            if lo > hi:
                return None
            groups.append((prefix, lo, hi))
            i += 2
        else:
            groups.append((prefix, num, num))
            i += 1
    if not groups:
        return None
    ids = set()
    for prefix, lo, hi in groups:
        if prefix in ("", "B"):
            ids.update(f"B-{n:02d}" for n in range(lo, hi + 1))
        else:
            ids.update(f"{prefix}-{n}" for n in range(lo, hi + 1))
    return ids

# 保护片段粗核：数字（含单位）、版本号、路径、反引号片段、带小数的百分比、
# 中英文时间表达、英文缩略词。只做逐字存在检查，不做语义判定。
TOKEN_PATTERNS = [
    (r"`[^`\n]+`", "反引号片段"),
    # 中文紧贴场景（「耗时20ms」「共20人」）没有 \b 边界：数字侧用 ASCII 负向断言，
    # 中文（CJK）不算 word char，汉字贴数字也能命中；单位表把 CJK 单位也列进来。
    (r"(?<![0-9A-Za-z_])\d+(?:\.\d+)?\s*(?:ms|s|h|天|小时|分钟|秒|%|MB|GB|KB|倍|次|人|台|个|条|篇|年|月|日|版本|万|k)(?![0-9A-Za-z_])", "数字+单位"),
    (r"(?<![0-9A-Za-z_])\d+(?:\.\d+)?(?![0-9A-Za-z_])", "数字"),
    # 版本号：中文紧贴（「版本v1.8.0」）用负向字符断言替代 \b
    (r"(?<![0-9A-Za-z])v?\d+\.\d+\.\d+(?:[-+][\w.]+)?(?![0-9A-Za-z])", "版本号"),
    (r"(?:^|[\s(/])(?:[\w-]+/){1,}[\w./-]+", "路径"),
    (r"\b[A-Za-z_][A-Za-z0-9_]*[a-z][A-Za-z0-9_]*(?:[A-Z][a-z0-9]*){2,}\b", "英文标识符"),
    (r"\b(?:[a-z]+_){1,}[a-z][a-z0-9_]*\b", "英文标识符"),
    (r"\b(?:p95|p99|max_connections|handleBurst|Request|iOS|API|URL|DB|HTTP|CLI|Redis|Dijkstra|GitHub|Linux)\b", "英文缩略词/术语"),
    (r"\d{4}[-年]\d{1,2}(?:[-月]\d{1,2}日?)?", "日期"),
]

def parse_cases(root):
    """从 benchmark 语料解析用例：(编号, 场景, 原文)。

    盲测标题 `### B-xx | 场景` 从 evals/benchmark-blind.md 读；
    旧口径 `### SF-xx | 场景 | 描述` / `### SNF-xx | ...`（v1.9.2 回放）
    从 evals/benchmark.md 读。两个语料都解析并合并，编号体系互不冲突。
    """
    cases = []

    def parse_file(path, head):
        text = path.read_text(encoding="utf-8")
        current = None
        for line in text.splitlines():
            m = head.match(line)
            if m:
                current = {"id": m.group(1), "scene": m.group(2).strip(), "quote": []}
                cases.append(current)
                continue
            if current is not None and (line.startswith(">") or not line.strip()):
                current["quote"].append(line)

    blind = root / "evals" / "benchmark-blind.md"
    if blind.exists():
        parse_file(blind, re.compile(r"^### (B-\d+) \| (.+)$"))
    bench = root / "evals" / "benchmark.md"
    if bench.exists():
        parse_file(bench, re.compile(r"^### (SF-\d+|SNF-\d+) \| ([^|]+)"))
    if not cases:
        print("hard_metrics: evals/benchmark-blind.md 与 evals/benchmark.md 都没有可解析用例", file=sys.stderr)
        sys.exit(2)
    out = []
    for c in cases:
        quote = "\n".join(c["quote"]).strip("\n")
        if not quote:
            print(f"hard_metrics: {c['id']} 在 benchmark-blind.md 中没有解析到引用块", file=sys.stderr)
            sys.exit(2)
        out.append((c["id"], c["scene"], quote))
    return out


def extract_blocks(text):
    """从模型输出里切出每条用例的 处理结果 正文。

    返回 {盲测编号: 正文}。B-xx 标题后的「处理结果：」以下到下一个
    B-xx 标题之间的内容都算正文；B-xx 标题缺失时按序配对前一个编号。
    """
    lines = text.splitlines()
    blocks = {}
    pending_id = None
    in_result = False
    buf = []
    for line in lines:
        # 模型可能给整篇输出加 blockquote 前缀（`> ## B-01`），识别标题时先剥
        line_stripped = line[2:] if line.startswith("> ") else line
        # 兼容两代标题：盲测 B-xx 与旧口径 SF-xx / SNF-xx（v1.9.2 回放）
        m = re.match(r"^## (B-\d+|SF-\d+|SNF-\d+)$", line_stripped)
        if m:
            if pending_id is not None and buf:
                blocks.setdefault(pending_id, []).extend(buf)
            pending_id = m.group(1)
            in_result = False
            buf = []
            continue
        if pending_id is None:
            continue
        if in_result and re.match(r"^## |^### ", line_stripped):
            # 下一个用例标题（或章节标题）：结束当前正文块，行由下一轮循环的
            # 标题分支处理；不能用 break，否则后续用例全部丢失
            continue
        # 处理结果 行也可能带 blockquote 前缀（`> 处理结果：`），剥前缀后再识别
        if re.match(r"^处理结果(?:（[^）]*）)?[:：]", line_stripped):
            in_result = True
            rest = line_stripped.split("：", 1)[1] if "：" in line_stripped else (
                line_stripped.split(":", 1)[1] if ":" in line_stripped else ""
            )
            if rest.strip():
                buf.append(rest)
            continue
        if in_result and re.match(r"^判定链[:：]", line):
            continue
        if in_result:
            buf.append(line)
    if pending_id is not None and buf:
        blocks.setdefault(pending_id, []).extend(buf)
    return {k: "\n".join(v) for k, v in blocks.items()}


def strip_output_notes(text):
    """剥掉模型输出末尾的括号说明段（claude 在正文后附的 `（in-place：…）` 等）。

    特征：独立段落、整段以 `（` 开头 `）` 结尾、不是 `（待确认）` 删除清单。
    人工 wc -m 记录不算这些说明（对照 long-form-retention.txt：claude B-19 320、
    B-44 254 都是剥掉说明段后的正文长度）。
    """
    paras = text.split("\n\n")
    out = []
    for para in paras:
        s = para.strip()
        if s.startswith("（") and s.endswith("）") and not s.startswith("（待确认"):
            continue
        out.append(para)
    return "\n\n".join(out)


def count_chars(text, strip_markdown_prefix=False):
    """长文留存率口径：与既有人工 wc -m 一致，统计所有字符含空白。

    benchmark-blind.md 的原文是 blockquote（每行带 `> ` 前缀）；人工 wc -m
    记录的是去掉前缀后的正文（对照 long-form-retention.txt：B-02 231、B-19
    339、B-44 254、B-68 416）。模型输出侧剥掉 `> ` 前缀、末尾括号说明段
    和首尾空白再数。
    """
    lines = []
    for line in text.splitlines():
        if strip_markdown_prefix and line.startswith("> "):
            lines.append(line[2:])
        elif strip_markdown_prefix and line.startswith(">"):
            lines.append(line[1:])
        else:
            lines.append(line)
    text = "\n".join(lines)
    text = strip_output_notes(text)
    return len(text.strip("\n"))


def retained(tokens, text):
    """粗核：token 逐字出现在 text 里才算保留，大小写敏感、忽略空白差异。"""
    norm = re.sub(r"\s+", "", text)
    hits, missing = [], []
    for pat, label, raw in tokens:
        probe = re.sub(r"\s+", "", raw)
        if probe and probe in norm:
            hits.append((pat, label, raw))
        else:
            missing.append((pat, label, raw))
    return hits, missing


def dash_metrics(blocks_text, original):
    """破折号密度：原文本段数、原/改每段 —— 计数、输出首句是否仍以 —— 起手。

    首句起手 = 正文第一段的第一个句子以 `——` 开头（SF-43 判据之一）。
    只统计含 —— 的段；输出侧首句起手是「该改没改」的残留信号。
    """
    def segs(text):
        return [s for s in re.split(r"\n\s*\n", text) if s.strip()]

    def strip_quote_prefix(text):
        """剥 blockquote 前缀：模型输出与 benchmark-blind 原文都可能带 `> `。"""
        lines = []
        for line in text.splitlines():
            if line.startswith("> "):
                lines.append(line[2:])
            elif line.startswith(">"):
                lines.append(line[1:])
            else:
                lines.append(line)
        return "\n".join(lines)

    orig_segs = segs(strip_quote_prefix(original))
    new_segs = segs(strip_quote_prefix(blocks_text))
    orig_counts = [s.count("——") for s in orig_segs]
    new_counts = [s.count("——") for s in new_segs]

    def first_sentence(text):
        return re.split(r"(?<=[。！？.!?])", text, maxsplit=1)[0]

    orig_first_starts = False
    if orig_segs:
        orig_first_starts = first_sentence(orig_segs[0]).lstrip().startswith("——")

    new_first_starts = False
    if new_segs:
        new_first_starts = first_sentence(new_segs[0]).lstrip().startswith("——")

    return {
        "original_segments": len(orig_segs),
        "output_segments": len(new_segs),
        "original_per_segment": orig_counts,
        "output_per_segment": new_counts,
        "output_total_dashes": sum(new_counts),
        "original_first_sentence_starts_with_dash": orig_first_starts,
        "output_first_sentence_starts_with_dash": new_first_starts,
    }


def retention_status(ratio):
    if ratio >= RETENTION_TARGET:
        return "ok"
    if ratio >= RETENTION_FLOOR:
        return "warn"
    return "fail"


def normalize_text(t):
    """归一化：去空白、全角/半角括号差异，用于「声明 no-op 但正文没跟上」比对。"""
    norm = re.sub(r"\s+", "", t)
    norm = norm.replace("（", "(").replace("）", ")").replace("，", ",").replace("。", ".")
    return norm


def is_noop(output_text):
    """no-op 判定：输出以「保留原文」开头，或处理结果不含改写正文。

    no-op 用例不判留存率——模型判定不该改时输出说明即可，字数变短不代表误删；
    留存率口径只约束实际改写（替掉人工对长文改写用例的 wc -m）。
    """
    head = output_text.lstrip().split("\n", 1)[0]
    # --pair/--stdin 模式给的是完整模型输出，先剥「处理结果：」前缀再判断
    m = re.match(r"^处理结果(?:（[^）]*）)?[:：]\s*", head)
    if m:
        head = head[m.end():]
    return (
        head.startswith("保留原文")
        or head.startswith("保持原文")
        or head.startswith("保留原文：")
        or head.startswith("保持原文：")
    )


def analyze_case(cid, scene, original, output_text, raw_output=None):
    """单条用例的硬判结果。

    raw_output：可选，完整输出文件文本，用于在判定链里查「力度=no-op」证据；
    缺省时退化用 output_text 本身。
    """
    # --pair/--stdin 常给完整模型输出（含 `## B-xx` 标题）。先尝试剥出「处理结果」
    # 正文；剥不出（纯正文）就原样用。raw_output 未提供时回填为剥前原文，
    # 保证判定链证据可用。
    if re.search(r"^#{1,3} ", output_text, re.MULTILINE):
        blocks = extract_blocks(output_text)
        target = blocks.get(cid) or next(
            (b for b in blocks.values() if b.strip()), ""
        )
        if target.strip():
            if raw_output is None:
                raw_output = output_text
            output_text = target
    char_orig = count_chars(original, strip_markdown_prefix=True)
    char_out = count_chars(output_text, strip_markdown_prefix=True)
    ratio = char_out / char_orig if char_orig else 1.0

    noop = is_noop(output_text)
    is_long = bool(LONG_TAG.search(scene))
    is_inplace_long = is_long and "in-place" in scene
    # 假 no-op 校验：声明保留原文时，要么判定链有「力度=no-op」的推理证据（judge 会复核），
    # 要么正文≈原文（归一化后长度不比原文短太多且原文字符基本都在）。
    # 两者都没有 → 标 noop_unverified，仍按长文判据计算，不让假 no-op 吞掉硬失败。
    noop_unverified = False
    if noop and is_inplace_long:
        verdict_text = raw_output or output_text
        chain_noop = re.search(r"力度\s*[:=]\s*no-?op", verdict_text) is not None
        norm_out = normalize_text(output_text)
        # benchmark-blind 原文带 `> ` blockquote 前缀，归一化前先剥掉
        stripped_orig = "\n".join(
            l[2:] if l.startswith("> ") else (l[1:] if l.startswith(">") else l)
            for l in original.splitlines()
        )
        norm_orig = normalize_text(stripped_orig)
        # 真 no-op 的输出要么是原文本身（正文连续包含归一化后的原文），
        # 要么有判定链「力度=no-op」佐证。假 no-op 只有一句「保留原文」的说明，
        # 原文不会连续出现 → 标 noop_unverified，仍按实际留存率判。
        body_ok = bool(norm_orig) and norm_orig in norm_out
        noop_ok = chain_noop or body_ok
        if not noop_ok:
            noop_unverified = True
        if noop_ok and body_ok:
            # 正文≈原文：留存率按 100% 记（与手工 wc -m 口径一致，
            # 「处理结果：/保持原文：」等包装字不计入分子）
            char_out = char_orig
            ratio = 1.0
    retention = None
    if is_inplace_long:
        status = "noop" if (noop and not noop_unverified) else retention_status(ratio)
        retention = {
            "original_chars": char_orig,
            "output_chars": char_out,
            "ratio": round(ratio, 4),
            "target": RETENTION_TARGET,
            "floor": RETENTION_FLOOR,
            "status": status,
            "noop_unverified": noop_unverified,
        }

    dm = dash_metrics(output_text, original)
    dashes_dense = (
        max(dm["output_per_segment"], default=0) >= 4
        or dm["output_first_sentence_starts_with_dash"]
    )

    tokens = []
    for pat, label in TOKEN_PATTERNS:
        for m in re.finditer(pat, original, re.MULTILINE):
            raw = m.group(0).strip()
            if raw and re.fullmatch(r"[\s\W_]+", raw):
                continue
            tokens.append((pat, label, raw, m.start(), m.end()))

    # 版本号优先：先剥掉完整版本跨度，避免「v1.8.0」再被裸数字拆成幽灵片段 8/8.0
    version_spans = []
    for pat, label in TOKEN_PATTERNS:
        if label != "版本号":
            continue
        for m in re.finditer(pat, original, re.MULTILINE):
            version_spans.append((m.start(), m.end()))
    if version_spans:
        kept = []
        for pat, label, raw, start, end in tokens:
            if any(s < end and start < e for s, e in version_spans if not (label == "版本号" and s == start and e == end)):
                continue
            kept.append((pat, label, raw, start, end))
        tokens = kept

    # 按位置覆盖去重：一个匹配完全落在更早（更长）匹配区间内时丢弃。
    # 例：`3.8%` 先被「数字+单位」匹配（0,4），`3` / `3.8` 落在其内 → 丢弃。
    # 模式顺序即优先级：数字+单位 > 版本号 > 路径 > 标识符 > 日期 > 数字。
    tokens.sort(key=lambda t: (t[3], -(t[4] - t[3])))
    deduped = []
    covered_until = -1
    for pat, label, raw, start, end in tokens:
        if start < covered_until:
            continue
        deduped.append((pat, label, raw))
        covered_until = max(covered_until, end)
    # no-op 用例也要跑粗核：模型说「保留原文」但实际改了数字/术语时，
    # 缺失报警能抓住假 no-op（留存率不判是因为输出是说明文字不是正文）
    hits, missing = retained(deduped, output_text)

    return {
        "case": cid,
        "scene": scene,
        "is_long": is_long,
        "retention": retention,
        "dashes": {
            "dense": dashes_dense,
            **dm,
        },
        "protected": {
            "total": len(deduped),
            "hit": len(hits),
            "missing": missing,
        },
        "noop": noop,
        "noop_unverified": noop_unverified,
    }


def summarize(result):
    """把单条结果变成 markdown 小节（run-eval.md 口径的判定）。"""
    lines = [f"### {result['case']} | {result['scene']}", ""]
    if result["is_long"] and not result["retention"]:
        lines.append("- 字数留存率：bounded 长文不适用留存率判据（run-eval.md 口径只约束 in-place 长文）")
    if result["retention"]:
        r = result["retention"]
        if r.get("noop_unverified"):
            lines.append(f"- 字数留存率：{r['output_chars']}/{r['original_chars']} = {r['ratio']:.1%}（⚠️ 声明保留原文但正文未跟上原文，按实际改写判：目标 ≥ {r['target']:.0%}，硬下限 {r['floor']:.0%}）→ **{r['status'].upper()}**")
        elif r["status"] == "noop":
            lines.append(f"- 字数留存率：{r['output_chars']}/{r['original_chars']} = {r['ratio']:.1%}（no-op：模型判定保留原文，留存率不判；数字仅供参考复核）")
        else:
            lines.append(f"- 字数留存率：{r['output_chars']}/{r['original_chars']} = {r['ratio']:.1%}（目标 ≥ {r['target']:.0%}，硬下限 {r['floor']:.0%}）→ **{r['status'].upper()}**")
        if r["status"] == "warn":
            lines.append("  - ⚠️ 低于目标，高于硬下限：符合 run-eval.md 的既有口径但需 judge 复核风格列")
        elif r["status"] == "fail":
            lines.append("  - ❌ 低于硬下限：长文误删并句重排风险，按 run-eval.md 记硬约束 ❌")
    d = result["dashes"]
    lines.append(f"- 破折号密度：原 {d['original_per_segment']} / 改 {d['output_per_segment']}；输出首句起手={d['output_first_sentence_starts_with_dash']}；总 {d['output_total_dashes']} 处")
    if d["dense"]:
        lines.append("  - ⚠️ 单段 ≥ 4 处或首句起手：命中 SF-43 破折号过密信号，需 judge 复核标点腔处理")
    p = result["protected"]
    lines.append(f"- protected spans 粗核：{p['hit']}/{p['total']} 保留")
    if p["missing"]:
        lines.append("  - ⚠️ 以下受保护片段在输出中未逐字找到（报警不判死，留给 judge 复核）：")
        for pat, label, raw in p["missing"]:
            lines.append(f"    - [{label}] `{raw}`")
    lines.append("")
    return "\n".join(lines)


def analyze_run(root, run_dir):
    """扫批次目录：配对 benchmark-blind.md 原文与各模型输出，逐条硬判。"""
    run_dir = Path(run_dir)
    cases = parse_cases(root)
    by_id = {cid: (scene, quote) for cid, scene, quote in cases}

    if run_dir.is_dir():
        candidates = sorted(run_dir.rglob("rewrite-*.md"))
    elif run_dir.is_file():
        candidates = [run_dir]
    else:
        print(f"hard_metrics: 路径不存在：{run_dir}", file=sys.stderr)
        sys.exit(2)

    model_reports = {}
    report_paths = []
    file_results = {}
    problems = {}
    for path in candidates:
        m = re.search(r"rewrite-([A-Za-z0-9-]+)\.md$", path.name)
        if not m:
            continue
        batch = m.group(1)
        report_paths.append(path)
        blocks = extract_blocks(path.read_text(encoding="utf-8"))
        expected = batch_expected_ids(batch)
        actual_ids = set(blocks)
        if expected is None:
            # 非区间命名（targeted 补跑等）：以实际出现的标题为准
            target_ids = actual_ids
        else:
            target_ids = expected
        ignored = sorted(actual_ids - target_ids)
        results = []
        for cid in sorted(target_ids):
            scene, quote = by_id.get(cid, ("", ""))
            output_text = blocks.get(cid, "")
            if not output_text:
                results.append({
                    "case": cid, "scene": scene,
                    "is_long": bool(LONG_TAG.search(scene)),
                    "retention": None, "dashes": None, "protected": None,
                    "missing_output": True, "noop": False, "noop_unverified": False,
                })
                continue
            results.append(analyze_case(cid, scene, quote, output_text, path.read_text(encoding="utf-8")))

        retentions = [r["retention"] for r in results if r.get("retention")]
        fails = [r["case"] for r in results if r.get("retention") and r["retention"]["status"] == "fail"]
        warns = [r["case"] for r in results if r.get("retention") and r["retention"]["status"] == "warn"]
        dense = [
            (r["case"], max(r["dashes"]["output_per_segment"], default=0))
            for r in results if r.get("dashes") and r["dashes"]["dense"]
        ]
        missing_spans = [
            (r["case"], len(r["protected"]["missing"]))
            for r in results if r.get("protected") and r["protected"]["missing"]
        ]

        key = path.relative_to(run_dir).as_posix() if run_dir.is_dir() else path.name
        file_results[key] = results
        # 零用例批次 = 解析失败或命名不被识别（如旧口径 SF-xx），报告不完整，记硬错
        if len(results) == 0:
            problems.setdefault(key, []).append("零用例批次（文件名命名未被 Bxx-yy 识别或正文为空）")
        if any(r.get("missing_output") for r in results):
            problems.setdefault(key, []).append(
                f"缺输出：{', '.join(r['case'] for r in results if r.get('missing_output'))}"
            )
        model_reports[key] = {
            "batch": batch,
            "total_cases": len(results),
            "ignored_out_of_range": ignored,
            "missing_output": [r["case"] for r in results if r.get("missing_output")],
            "long_form": {
                "cases": len(retentions),
                "warn": warns,
                "fail": fails,
            },
            "dash_dense": dense,
            "protected_missing": missing_spans,
        }

    if not report_paths:
        print(f"hard_metrics: {run_dir} 下没有找到 rewrite-*.md 文件", file=sys.stderr)
        sys.exit(2)

    lines_out = [
        "# Hard Metrics — 硬判报告",
        "",
        f"> 由 `python3 automation/eval/hard_metrics.py --run {run_dir}` 生成。",
        "> 字数留存率与破折号密度按 `evals/run-eval.md` 既有口径判定；protected spans 粗核只报警不判死，缺失由 judge 复核。",
        "> 本报告是运行产物，不入 commit；需要时归档到 `tasks/` 下。",
        "",
        "## 汇总",
        "",
    ]
    total_fail, total_warn = 0, 0
    for key, rep in model_reports.items():
        lf = rep["long_form"]
        total_fail += len(lf["fail"])
        total_warn += len(lf["warn"])
    lines_out.append(f"- 长文硬下限失败 {total_fail} 条（{', '.join(c for rep in model_reports.values() for c in rep['long_form']['fail']) or '无'}）")
    lines_out.append(f"- 长文目标下警告 {total_warn} 条（{', '.join(c for rep in model_reports.values() for c in rep['long_form']['warn']) or '无'}）")
    lines_out.append("")
    for path in report_paths:
        key = path.relative_to(run_dir).as_posix() if run_dir.is_dir() else path.name
        rep = model_reports[key]
        lines_out += [f"## {key}", ""]
        lines_out.append(f"- 用例总数：{rep['total_cases']}")
        if rep.get("ignored_out_of_range"):
            lines_out.append(f"- ⚠️ 区间外标题（已忽略）：{', '.join(rep['ignored_out_of_range'])}")
        if rep["missing_output"]:
            lines_out.append(f"- ⚠️ 缺输出：{', '.join(rep['missing_output'])}")
        lf = rep["long_form"]
        if lf["cases"]:
            lines_out.append(f"- 长文用例 {lf['cases']} 条：硬下限失败 {len(lf['fail'])}（{', '.join(lf['fail']) or '无'}），目标下警告 {len(lf['warn'])}（{', '.join(lf['warn']) or '无'}）")
        else:
            lines_out.append("- 长文用例：0（本批次无 long 标签用例，留存率不判）")
        if rep["dash_dense"]:
            lines_out.append(f"- ⚠️ 破折号过密 {len(rep['dash_dense'])} 条：{', '.join(f'{cid}（{n} 处）' for cid, n in rep['dash_dense'])}")
        if rep["protected_missing"]:
            lines_out.append(f"- ⚠️ 保护片段缺失报警 {len(rep['protected_missing'])} 条：{', '.join(f'{cid}（{n} 项）' for cid, n in rep['protected_missing'])}")
        lines_out.append("")
        for res in file_results[key]:
            if res.get("missing_output"):
                lines_out.append(f"### {res['case']} | {res['scene']}")
                lines_out.append("")
                lines_out.append("- ⚠️ 缺输出：本用例在输出文件中没有解析到处理结果")
                lines_out.append("")
                continue
            lines_out.append(summarize(res))
        lines_out.append("")

    header = lines_out

    out_path = run_dir if run_dir.is_dir() else run_dir.parent
    md_path = out_path / "hard-metrics.md"
    json_path = out_path / "hard-metrics.json"
    md_path.write_text("\n".join(header).rstrip() + "\n", encoding="utf-8")
    json_path.write_text(
        json.dumps({"reports": model_reports, "cases": file_results}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"hard-metrics: {len(report_paths)} 个批次 → {md_path}, {json_path}")
    for name, probs in problems.items():
        for prob in probs:
            print(f"  ⚠️ {name}: {prob}")
    for name, rep in model_reports.items():
        lf = rep["long_form"]
        print(f"  {name}: {rep['total_cases']} 条, 长文 {lf['cases']} 条, 硬下限失败 {len(lf['fail'])}")
    # 退出码：硬下限失败=1；批次不完整（零用例/缺输出）这类报告不可信=2；其余=0
    if any(problems.values()):
        return 2
    return 1 if any(rep["long_form"]["fail"] for rep in model_reports.values()) else 0


def read_text_safe(path):
    """读文件，缺文件时打印错误并退出 2（自身错误口径）。"""
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as e:
        print(f"hard_metrics: 读文件失败 {path}: {e}", file=sys.stderr)
        sys.exit(2)


def single_pair(original_path, output_path, scene=""):
    """单条对照：原文本从文件读，改后文本从文件或 stdin 读。"""
    original = read_text_safe(original_path)
    if output_path == "-":
        output_text = sys.stdin.read()
    else:
        output_text = read_text_safe(output_path)
    cid = f"{Path(original_path).name} / {Path(output_path).name}"
    res = analyze_case(cid, scene, original, output_text)
    print(summarize(res).rstrip())
    return 0


def main():
    ap = argparse.ArgumentParser(description="说人话 eval harness 硬判脚本（v2.2.0）")
    ap.add_argument("--run", metavar="DIR", help="扫批次目录（含 rewrite-*.md），输出 hard-metrics 报告")
    ap.add_argument("--pair", nargs=2, metavar=("ORIG", "OUT"), help="单条对照：原文本文件 + 改后文本文件（- 表示 stdin）")
    ap.add_argument("--stdin", metavar="ORIG", help="原文本文件，改后文本从 stdin 读")
    ap.add_argument("--report-json", action="store_true", help="--pair 模式输出单行 JSON（供 judge 输入拼接）")
    ap.add_argument("--scene", metavar="SCENE", default="", help="单条模式（--pair/--stdin）的用例场景标签，如 'public-writing / long / in-place'，用于长文留存判据")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[2]

    if args.run:
        sys.exit(analyze_run(root, args.run))

    if args.pair:
        if args.report_json:
            original = read_text_safe(args.pair[0])
            output_text = (
                sys.stdin.read()
                if args.pair[1] == "-"
                else read_text_safe(args.pair[1])
            )
            res = analyze_case("pair", args.scene, original, output_text)
            print(json.dumps(res, ensure_ascii=False))
            return 0
        sys.exit(single_pair(args.pair[0], args.pair[1], args.scene))

    if args.stdin:
        original = read_text_safe(args.stdin)
        res = analyze_case("stdin", args.scene, original, sys.stdin.read())
        if args.report_json:
            print(json.dumps(res, ensure_ascii=False))
        else:
            print(summarize(res).rstrip())
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
