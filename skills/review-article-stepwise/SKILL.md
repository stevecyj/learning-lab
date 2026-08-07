---
name: review-article-stepwise
description: Review an article or prose document interactively, one heading, paragraph, list item, or table row at a time, while judging each unit against its surrounding and document-wide context. Use when the user asks for paragraph-by-paragraph review, 逐段檢查, title-by-title editing, contextual line editing, or an approval-gated writing pass paired with a style skill such as shuorenhua.
---

# Review an Article Stepwise

Run an approval-gated editing loop. Read broadly for context, but judge and present exactly one reviewable unit per turn.

## Pair with the style skill

Load and follow the available skill named `shuorenhua` before making style judgments. Let that skill own tone, protected spans, rewrite severity, and fidelity checks. Let this skill own unit boundaries, context selection, sequencing, approval, and file edits.

If the `shuorenhua` skill is unavailable, say so and ask whether to continue with a general clarity review. Do not claim to have applied it.

## Establish the review

1. Resolve the target document. If the user names one file, use it without asking again.
2. Read the whole document once to establish its purpose, audience, structure, terminology, and existing voice. Do not rewrite it during this pass.
3. Build an ordered internal queue of reviewable units. Keep the queue internal unless the user asks to see it.
4. Start with the first unit unless the user specifies a starting point.

Treat these as separate reviewable units:

- each document title and heading at every level;
- each prose or blockquote paragraph;
- each list item;
- a table header and each table row.

Treat fenced code, commands, paths, parameters, error text, and other protected spans according to the `shuorenhua` skill. Skip a code-only unit unless the user asks to review code comments or technical correctness.

## Review one unit

Before judging the current unit, refresh it from the current file and read:

- its enclosing heading and section purpose;
- the previous and next reviewable units when present;
- accepted edits that now affect the local context;
- document-wide terminology and voice.

For a heading, also compare its covered content and sibling headings. Check whether it names the section accurately, fits the hierarchy, and sounds natural in the document's register.

Decide whether to keep or revise the unit. Preserve a natural unit as-is; review does not imply rewriting. When revision is useful, provide one recommended version. Do not add facts, examples, claims, sources, capabilities, or conclusions absent from the original.

## Present and stop

Respond in the user's language using this compact shape:

```text
Location: [line or heading path]
Type: [title / heading / paragraph / list item / table]
Decision: [keep / revise]

Original:
> [current unit]
```

For `revise`, append:

```text
Recommendation:
> [one recommended version]

Reason:
[one to three concrete sentences tied to wording and context]
```

Stop after this unit. Do not preview, judge, or edit the next unit in the same turn.

## Apply the user's decision

Interpret natural-language equivalents of these actions:

- **Accept and continue**: apply only the presented recommendation, then review the next unit.
- **Keep and continue**: leave the current unit unchanged, then review the next unit.
- **Replace with ...**: apply the user's wording, then review the next unit.
- **Try again**: offer one new recommendation for the same unit.
- **Explain**: clarify the current judgment without advancing.
- **Stop**: report the current position and leave the remaining units untouched.

After an accepted edit, reread the affected local context from the file before advancing. Use the updated file as the source of truth. Do not revisit an accepted unit unless a later edit creates a direct inconsistency; flag that inconsistency and request approval before changing it.

## Finish the document

After the last unit, run a read-only consistency pass over:

- heading hierarchy and naming patterns;
- terminology;
- transitions affected by accepted edits;
- conspicuous repetition or formulaic endings.

List only remaining issues with locations. Do not make another whole-document rewrite or apply cleanup edits without approval. Finish when every queued unit has a recorded decision and the consistency pass has been reported.
