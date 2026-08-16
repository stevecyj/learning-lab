# Wayfinder 與 AI 輔助架構決策工作流：核心學習導讀

本篇整理自 `notes/matt/wayfinder-demo.srt`，探討如何利用 **Wayfinder（決策地圖編排器）**、**高保真原型探針（Prototyping）** 與 **多 Agent 平行質詢（Parallel Grilling）**，在面對大型模糊需求時消除架構不確定性，並在實作前產出完整規格。

---

### 1. 這堂課真正要解決的問題

大型或模糊需求（例如「在課程影片管理系統 CVM 中加入 TikTok / Shorts 直式短影音創作功能」）如果直接交由 AI 進入實作（Vibe Coding），會面臨以下具體問題：

1. **決策迷霧與錯誤假設**：需求牽涉資料表結構、UI 佈局、外部 API 限制（如 TikTok 審核規範）、舊程式碼相依性等多重未知數。Agent 在沒有邊界的情況下寫程式，容易做出錯誤假設並產出無法整合的代碼。
2. **Context Window 膨脹與推理退化**：在單一會話中討論所有分支，Token 數容易超過 150k–200k，超出高效智能區，導致模型遺忘前文或注意力稀釋。
3. **過早實作的重構成本**：若在資料模型與字幕渲染方式尚未定案前就寫入正式程式碼，一旦發現外部限制或 UX 不合適，所有代碼都必須重寫。

**核心目標**：在不編寫正式實作代碼的前提下，將模糊需求拆解為具備相依關係的決策地圖（Decision Map），透過多個平行的子任務（質詢、原型、調研）消除架構盲點，產出決策完備的規格書（Decision-Complete Spec）。

---

### 2. 核心概念

#### 概念一：Wayfinder 決策地圖編排器 (Pre-spec Decision Orchestrator)
- **它是什麼**：基於 Agent 的工作流技能（`Grill Me` 的演進版）。它先掃描既有程式碼庫，將模糊需求拆解為一張由多個決策票券（Decision Tickets）與相依關係組成的結構化地圖（如 GitHub Issues 樹狀圖）。
- **為什麼存在**：單次質詢無法承受大型架構的認知負載；Wayfinder 負責界定決策邊界（Decision Frontier）。
- **解決什麼問題**：解決功能開發初期「不知道該先決定什麼、遺漏關鍵決策」的迷霧狀態。
- **何時使用**：面對跨模組、需多階段完成的中大型功能或架構重構。
- **何時不適合使用**：範圍明確、單一會話即可釐清的小型變更（此時自動降級為單次文檔質詢 `grill-with-docs`）。

#### 概念二：決策任務 vs. 實作任務 (Decision Tickets vs. Implementation Tickets)
- **它是什麼**：
  - **決策任務（Decision Tickets）**：透過設計選擇、調研外部限制或驗證原型來結案的票券，目標是消除未知。
  - **實作任務（Implementation Tickets）**：在規格鎖定後，將決策具現化（Reify）為正式生產程式碼的任務。
- **為什麼存在**：混淆兩者會導致在架構未定時耗費精力編寫無效程式碼。
- **解決什麼問題**：防止過早實作，確保實作階段的每個步驟都有明確規格支援。
- **何時使用**：在整個規劃與開發流程中嚴格區分。
- **何時不適合使用**：已是既定事實、毫無懸念的細微修復（如修正純語法錯誤）。

#### 概念三：漸進式揭露與多 Agent 平行調研 (Progressive Disclosure & Parallel Sub-agents)
- **它是什麼**：將決策地圖中的獨立子任務（例如：TikTok API 調研、YouTube Shorts 限制調研、資料庫欄位質詢、UI 原型測試）分別交由獨立的 Context Window（子 Agent）並行處理；主地圖僅保留核心摘要與指向深層文檔的連結。
- **為什麼存在**：單一 Context Window 的容量有限，並行處理可避免工程師等待（No Dead Time）。
- **解決什麼問題**：避免長上下文導致的模型退化，同時縮短探索時間。
- **何時使用**：當決策地圖中出現多個無相依關係（Unblocked）的調研或質詢任務時。
- **何時不適合使用**：具備強相依關係的任務（前置決策未完成前無法進行下一步）。

#### 概念四：原型探針 (High-Fidelity Prototyping Probe)
- **它是什麼**：在 Git Worktree（獨立工作樹）中快速建構出可互動的 UI/UX 分支變體（Variant A vs. Variant B），供開發者實際操作。
- **為什麼存在**：純文字描述視覺與佈局容易產生語意歧義，直接操作原型能快速確認操作手感與工作流。
- **解決什麼問題**：消除文字溝通的認知落差，以低成本驗證使用者體驗。
- **何時使用**：遇到主觀品味（Taste）、複雜工作流或佈局結構不確定的決策點。
- **何時不適合使用**：純後端邏輯、演算法設計或資料表欄位定義等適合文字與型別推導的情境。

#### 概念五：Agent 三層模型 (Model / Harness / Environment)
- **它是什麼**：
  - **Model（核心引擎）**：LLM 模型本體（如 Opus、GPT）。
  - **Harness（操控框架）**：圍繞模型的 CLI 工具、Session 管理、提示詞管道與 Skills（如 Claude Code、Codex）。
  - **Environment（執行環境）**：Agent 操作的實體場域（檔案系統、Git Worktrees、資料庫、外部 API）。
- **為什麼存在**：釐清 AI 輔助開發效能的決定因素。
- **解決什麼問題**：單純更換模型並不能解決所有問題。優化 Harness 與 Environment 對產出品質與穩定度的影響往往佔 50% 以上，且成本更低。
- **何時使用**：架構 AI 輔助開發流程、除錯 Agent 行為或配置開發環境時。
- **何時不適合使用**：無（此為基礎心智模型）。

#### 概念六：五階段 AI 工程管線 (The 5-Stage AI Engineering Pipeline)
- **它是什麼**：從模糊想法到生產交付的標準流程：
  $$\text{Wayfinder (決策地圖)} \longrightarrow \text{to-spec (鎖定規格)} \longrightarrow \text{to-tickets (實作拆解)} \longrightarrow \text{Implement (無人值守實作)} \longrightarrow \text{Code Review (規格對比審查)}$$
- **為什麼存在**：建立可預測、可重現的高品質軟體開發流程。
- **解決什麼問題**：解決 AI 生成代碼時常出現的架構斷層、回歸錯誤與無法維護問題。
- **何時使用**：所有中大型功能的標準開發流程。
- **何時不適合使用**：單行 Hotfix 或純文檔錯字修正。

---

### 3. Mental Model

#### 傳統單視窗 Vibe Coding vs. Wayfinder 決策前置管線

```text
【傳統單視窗 Vibe Coding (高風險、高污染)】
模糊需求 ──> 單一 Context Window (Prompt 膨脹 > 150k) ──> 直接寫入正式代碼 ──> 遭遇 API 限制/架構衝突 ──> 推翻重構 / 放棄

─────────────────────────────────────────────────────────────────────────────

【Wayfinder 五階段管線 (漸進式揭露、狀態隔離)】

  [模糊需求 (Fog)]
         │
         ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Wayfinder Orchestrator (掃描專案代碼庫)                   │
 │    產出: 決策地圖 (Decision Map / GitHub Issues Graph)       │
 └──────────────────────────────┬──────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
  [調研票券 (Research)]   [質詢票券 (Grilling)]   [原型票券 (Prototype)]
  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
  │ 子 Agent (Context A) │    │ 子 Agent (Context B) │    │ Git Worktree     │
  │ 調研 TikTok API  │    │ 討論資料庫欄位   │    │ 驗證 UI 變體 A/B │
  │ 寫入深層 Markdown│    │ 決定採用 Enum    │    │ 確定操作工作流   │
  └────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘
           │                       │                       │
           └───────────────────────┼───────────────────────┘
                                   │ 決策回填 (決策票券全數關閉)
                                   ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 2. to-spec: 匯整地圖與決策指標，產出完整規格書 (Locked Spec) │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 3. to-tickets: 依據規格拆解出「實作票券 (Implementation)」  │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 4. Implement: AFK (無人值守) 子 Agent 分別實作各功能模組     │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ 5. Code Review: 對照規格書進行二階段 Diff 審查與品質檢驗     │
 └─────────────────────────────────────────────────────────────┘
```

---

### 4. 專家視角

#### 初學者需要知道，但資深工程師通常已成直覺的內容
1. **狀態建模使用 Enum 優於 Boolean**：當實體具備互斥狀態時（如影片格式為 `standard` 或 `short`），使用 `is_short = true` 會在未來加入第三種格式時產生 $2^n$ 種狀態組合，造成非法的業務狀態（例如同時為 true）。直接使用 Enum 可限制狀態空間。
2. **Brownfield（既有專案）與 Greenfield（新專案）本質相同**：既有專案只要透過接縫隔離（Seam）與介面封裝，決策流程與新專案完全一致。
3. **主動引導 Agent（Driver vs. Passenger）**：工程師需擔任主導者（Tech Lead），將 AI 視為執行者（Junior），隨時校正方向並施加架構約束。
4. **Token Context 警戒線**：模型在 150k–200k Token 以上時注意力會分散，需透過拆分子任務與 Worktree 定期重置 Context。

#### 資深工程師仍然會注意的內容
1. **平台審核門檻（Audit Gate）**：TikTok 官方 API 對未審核 App 有嚴格限制（如強制特定隱私下拉選單、未審核無法公開發布）。評估自建原生串接與第三方服務（如 Buffer + Zapier + Dropbox）的成本效益至關重要。
2. **架構接縫隔離（Arm's-length Seam Isolation）**：引用舊專案（如 monorepo 內舊版 Remotion 字幕引擎）時，使用外部 CLI / Shell-out 調用，避免將老舊相依套件合併入主專案。
3. **工作樹狀態與環境隔離（Worktree Friction）**：本地執行多個 Git Worktrees 原型時，易遇到 Node 模組符號連結（Symlink）、環境變數缺失、Port 衝突等問題，可評估未來遷移至雲端沙盒。
4. **推理代價與延遲權衡（Effort vs. Latency Trade-off）**：選擇模型思考強度（如 Opus Medium vs. High）時，衡量 Token 消耗與等待時間帶來的邊際效益。

---

### 5. 語法 vs 通用知識

| 分類 | 內容 | 說明與跨語言通用性 |
| :--- | :--- | :--- |
| **語言 / 工具特有知識** | Claude Code Terminal Multi-worker | Claude Code 的終端多工作行程管理功能，可在單一視窗切換檢視多個 Agent。 |
| **語言 / 工具特有知識** | TypeScript Schema Enum 定義 | 在 Drizzle / Prisma / TypeScript 中以 Union Types 或 Enum 定義欄位約束。 |
| **語言 / 工具特有知識** | Remotion 視訊渲染管道 | 基於 React 技術棧的程式化視訊渲染與字幕燒錄引擎。 |
| **語言 / 工具特有知識** | Git Worktree 多重工作樹 | Git 內建功能，允許同一個 Repository 同時檢出多分支到不同目錄獨立執行。 |
| **通用程式設計知識** | 有限狀態機與狀態空間約束 | 避免布林值爆炸，以列舉型別嚴格定義狀態空間（通用於 Python、Go、Rust、Java、SQL 等）。 |
| **通用程式設計知識** | 漸進式揭露 (Progressive Disclosure) | 資訊架構設計原則：頂層提供索引摘要，需要細節時再循指標下鑽，避免 Context 超載。 |
| **通用程式設計知識** | 絞殺者模式 / 橋接模式 (Strangler / Bridge Pattern) | 對於舊系統功能，以獨立進程或 CLI 介面隔離調用，待時機成熟再重構併入主系統。 |
| **通用程式設計知識** | 探針原型 (Spike / Prototyping) | 編寫拋棄式代碼以降低技術或 UX 決策的不確定性。 |

---

### 6. Trade-off

#### 1. Wayfinder 決策地圖編排 vs. 單次對話直接質詢 / Vibe Coding
- **差異**：前者先產出相依性圖表與多個獨立 Issue 平行調研；後者在單一對話中討論並直接寫代碼。
- **優勢（Wayfinder）**：可處理高複雜度需求、決策具備完整追溯性、保持 Context 乾淨。
- **代價（Wayfinder）**：初期啟動與管理票券的成本較高。
- **適用情境**：跨模組、需多工作階段的大型功能。
- **選錯後果**：大型需求若使用單次對話，容易中途遺忘前置決策並產出衝突代碼。

#### 2. 狀態表示：Enum（列舉）vs. 多個 Boolean 旗標
- **差異**：`format = 'standard' | 'short'` vs. `is_short = true, is_lesson = false`。
- **優勢（Enum）**：狀態空間嚴格限制在合法範圍內（$N$ 種狀態），資料庫約束明確。
- **代價（Enum）**：初期需定義型別；未來若有非互斥的複合維度需重新設計。
- **適用情境**：互斥的業務分類、生命週期狀態。
- **選錯後果**：布林值會產生 $2^n$ 種排列組合，造成「既是 short 又是 lesson」的非法業務狀態。

#### 3. 整合老舊子系統：外部 CLI 調用 (Shell-out) vs. 併入主代碼庫 (In-repo Merge)
- **差異**：透過子進程執行獨立專案 vs. 將程式碼與相依套件搬入主專案。
- **優勢（Shell-out）**：主專案相依性乾淨，避免舊套件版本衝突或 Monorepo 建置複雜度。
- **代價（Shell-out）**：跨進程溝通需序列化參數、錯誤處理間接、本機需維護兩套環境。
- **適用情境**：既有工具已可穩定運作，但套件版本過舊且短期內無重構急迫性。
- **選錯後果**：過早併入會引發套件衝突，拖慢主專案開發速度。

#### 4. 外部發布管道：自建官方 API 串接 vs. 第三方工具橋接 (Buffer / Zapier)
- **差異**：自行實作 TikTok OAuth 與發布審核流程 vs. 產出檔案後丟入 Dropbox 由 Buffer 排程發布。
- **優勢（第三方橋接）**：避開 TikTok 嚴苛的 App 審核（Audit Gate）與強制 UI 規範，幾小時內即可上線。
- **代價（第三方橋接）**：需支付第三方 SaaS 費用、流程依賴多個外部服務。
- **適用情境**：內部個人工具、驗證階段的新功能。
- **選錯後果**：自建原生 API 會卡在數週的平台審核與繁瑣的合規 UX 開發中，導致功能延遲交付。

---

### 7. 常見誤解

1. **「只要模型能力夠強，長 Prompt 就能直接寫出完整系統」**
   - 需求未拆解時，模型會自行代入假設，產出看似正確但無法與既有系統相容的程式碼。
2. **「把所有歷史紀錄與檔案全塞入同一個對話，AI 才能理解全局」**
   - Context 超過 150k 時注意力會退化。正確做法是採用漸進式揭露，各子任務獨立運作，主地圖只保留摘要與指標。
3. **「Pre-spec 階段寫的原型（Prototype）代碼可直接作為正式代碼基礎」**
   - 原型代碼的目的是消除 UX 與佈局的不確定性，通常缺乏嚴謹的錯誤處理與狀態架構。直接沿用會累積技術債。
4. **「決策任務（Decision Ticket）就是實作任務（Implementation Ticket）」**
   - 決策任務的結案條件是「做出選擇並記錄理由」；實作任務的結案條件是「代碼通過測試並合併」。混淆兩者會導致在架構未定時便開始寫測試與邏輯。

---

### 8. Code Prediction — 請先作答

請閱讀以下三段程式碼，在不執行程式的前提下回答：
1. **執行結果為何？**
2. **為什麼會是這個結果？**
3. **程式內部發生了什麼事（執行順序、變數狀態變化）？**

#### 程式一：影片格式狀態分類器 (Python)

```python
from enum import Enum

class VideoFormat(Enum):
    STANDARD = "standard"
    SHORT = "short"

def get_render_pipeline(format_type: VideoFormat, has_captions: bool) -> str:
    if format_type == VideoFormat.SHORT:
        if has_captions:
            return "remotion_vertical_burned_in"
        return "vertical_raw"
    elif format_type == VideoFormat.STANDARD:
        return "landscape_standard"
    else:
        return "unknown_pipeline"

current_format = VideoFormat.SHORT
needs_subtitle = True
selected_pipeline = get_render_pipeline(current_format, needs_subtitle)
print(selected_pipeline)
```

---

#### 程式二：決策相依性排程檢查器 (JavaScript)

```javascript
const decisionTickets = [
  { id: "T1", name: "DB Schema Enum", status: "CLOSED", blockedBy: [] },
  { id: "T2", name: "TikTok API Research", status: "CLOSED", blockedBy: [] },
  { id: "T3", name: "Render Pipeline Shell-out", status: "OPEN", blockedBy: ["T1"] },
  { id: "T4", name: "Full Spec Generation", status: "OPEN", blockedBy: ["T2", "T3"] }
];

function getReadyTickets(tickets) {
  const closedTicketIds = new Set(
    tickets.filter(t => t.status === "CLOSED").map(t => t.id)
  );

  return tickets.filter(ticket => {
    if (ticket.status !== "OPEN") {
      return false;
    }
    const allBlockersResolved = ticket.blockedBy.every(blockerId => 
      closedTicketIds.has(blockerId)
    );
    return allBlockersResolved;
  });
}

const actionable = getReadyTickets(decisionTickets);
console.log(actionable.map(t => t.id));
```

---

#### 程式三：多布林狀態組合計算 (Python)

```python
flags = {
    "is_short": True,
    "is_lesson": True,
    "is_pitch": False
}

def resolve_video_category(state: dict) -> str:
    active_count = sum(1 for val in state.values() if val is True)
    
    if active_count > 1:
        return "INVALID_STATE_CONFLICT"
    elif state.get("is_short"):
        return "CATEGORY_SHORT"
    elif state.get("is_lesson"):
        return "CATEGORY_LESSON"
    elif state.get("is_pitch"):
        return "CATEGORY_PITCH"
    else:
        return "CATEGORY_STANDALONE"

result = resolve_video_category(flags)
print(result)
```

---

### 9. Bug Hunt — 請先作答

請找出以下兩段程式碼中的邏輯缺陷或架構問題，說明原因並提出修復方案。

#### 缺陷程式碼一：布林值旗標擴充陷阱 (JavaScript)

```javascript
function updateVideoAttributes(video, newAttributes) {
  // 需求：影片必須是 standard、short 或 lesson 其中一種
  const updated = {
    ...video,
    isStandard: newAttributes.isStandard ?? video.isStandard,
    isShort: newAttributes.isShort ?? video.isShort,
    isLesson: newAttributes.isLesson ?? video.isLesson,
  };

  if (updated.isShort) {
    updated.renderMode = "PORTRAIT";
  } else {
    updated.renderMode = "LANDSCAPE";
  }

  return updated;
}

const currentVideo = { id: 101, isStandard: true, isShort: false, isLesson: false };
const result = updateVideoAttributes(currentVideo, { isShort: true });
console.log(result);
```

---

#### 缺陷程式碼二：未隔離相依性與缺乏錯誤處理的子進程 (Python)

```python
import subprocess
import json

def run_remotion_render(video_id: str, props: dict) -> dict:
    """
    呼叫外部 Remotion CLI 渲染直式影片
    假設：Remotion 腳本位於本機獨立目錄中
    """
    serialized_props = json.dumps(props)
    
    command = f"npx remotion render MyComp out/{video_id}.mp4 --props='{serialized_props}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    return {
        "status": "SUCCESS",
        "output_path": f"out/{video_id}.mp4",
        "raw_logs": result.stdout
    }
```

---

### 10. Coding Challenge

#### 題目：決策地圖狀態機與阻塞排程器 (Decision Map State Machine)

#### 目標
請使用 Python 或 JavaScript 實作一個 `DecisionMap` 類別：
1. 註冊多個決策票券（包含 ID、類型：`GRILL`、`RESEARCH`、`PROTOTYPE`、狀態：`OPEN` / `CLOSED`、相依票券 ID 陣列 `blocked_by`）。
2. 提供 `get_next_actionable_tickets()` 方法，回傳目前所有無阻礙、可立即執行的任務清單。
3. 提供 `close_ticket(ticket_id, resolution_summary)` 方法：
   - 記錄決策結果。
   - 將該票券標記為 `CLOSED`。
   - 自動解鎖依賴此票券的其他下游任務。
4. 提供 `is_decision_complete()` 檢查是否所有決策票券皆已關閉，可進入 `to-spec` 階段。

#### 約束條件
- 純記憶體資料結構實作，不使用外部資料庫。
- 處理循環相依（Circular Dependency）檢測，若存在死鎖需丟出明確錯誤。
- 代碼需具備型別標記（Python Type Hints 或 TypeScript / JSDoc）。

#### 驗收標準
- 加入 `T1 (無相依)`、`T2 (依賴 T1)` 時，初始狀態只有 `T1` 是 actionable。
- 關閉 `T1` 後，`T2` 變為 actionable。
- 所有票券關閉後，`is_decision_complete()` 回傳 `True`。

#### 延伸挑戰 (Stretch Goal)
- 支援動態新增票券（在解析某個 `GRILL` 任務時，動態新增一個 `PROTOTYPE` 票券並插入相依鏈中）。

---

### 11. Retrieval Practice — 請先作答

請不看前文，回答以下五個核心思考題：

1. **[Why 目的]** 為什麼在面對大型模糊需求時，不能直接讓 AI 進入實作（Implementation）階段，而必須先透過 Wayfinder 進行「決策地圖（Pre-spec Map）」拆解？
2. **[How 機制]** 在 Wayfinder 的架構中，「漸進式揭露（Progressive Disclosure）」如何透過 GitHub Issue / 決策地圖與子 Agent 避免 Context Window 超載？
3. **[Trade-off 權衡]** 串接外部服務（如 TikTok API）遇到嚴苛審核與 UI 規範時，選擇「自建原生串接官方 API」與「透過第三方服務（如 Buffer + Dropbox）橋接」各自的代價與適用情境為何？
4. **[Prediction 預測]** 若在資料表中使用 `is_short = True` 和 `is_lesson = True` 兩個布林值標記影片類型，當系統新增「直式精華 (Highlights)」與「宣傳短片 (Pitches)」時，資料庫狀態與業務邏輯會面臨什麼具體問題？
5. **[Application 應用]** 若要在既有專案中新增一個具備高度不確定性的功能（例如將舊有的 Python CLI 工具整合到 Web API 中），你會如何安排從「迷霧」到「上線」的完整五階段流程？

---

### 12. 下一步

#### 完成本課後具備的能力
1. 能識別何時應停止盲目寫 code，改用 Pre-spec 決策地圖拆解模糊需求。
2. 能合理劃分 Model、Harness 與 Environment，透過優化工作環境提升 AI 協作效能。
3. 能在資料建模中以 Enum 取代多布林旗標，消除無效狀態組合。
4. 能規劃五階段 AI 開發流水線（`Wayfinder` $\rightarrow$ `to-spec` $\rightarrow$ `to-tickets` $\rightarrow$ `implement` $\rightarrow$ `code-review`）。

#### 建議後續學習主題
1. **Sandcastle 與無人值守實作 (AFK Implementation Orchestration)**：規格鎖定後，如何讓 Agent 在獨立 Worktree 中全自動完成實作票券並提交 PR。
2. **規格對比代碼審查 (Spec-Driven Code Review)**：將鎖定的 Spec 作為基準，自動對照 Git Diff 進行雙向驗證。
3. **Git Worktrees 與雲端沙盒自動化 (Worktrees & Cloud Sandbox Environments)**：管理多 Agent 並行時的環境變數、相依套件與隔離執行。
