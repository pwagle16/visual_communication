# Gender Bias in LLM Hiring — 2-min visual deck

A near-wordless, self-contained slide deck summarizing *Gender Bias in LLM
Hiring Decisions: Evidence from a Japanese Context and Evaluation of
Mitigation Strategies* (arXiv:2606.18649).

## Files

- **`gender_bias_llm_hiring.pptx`** — the editable **PowerPoint** (10 slides), built to track the spoken script beat-by-beat. Title slide cites the full study name and flanks it with two cartoon résumés (pink ♀ / blue ♂). Relatable, near-wordless visuals: a you (caramel) → laptop-screening → recruiter (walnut) pipeline, a friendly robot for the LLM, résumés with applicant photos (rirekisho-style), a scales-of-fairness motif (level question → tilted answer), a raised/highlighted résumé for the result, the five models as pills, and a redacted-name résumé for the fix. Big headings. Warm **brown** palette (cream + espresso + terracotta) with **rose = female / denim = male** gender accents, Georgia + Calibri (swap in PowerPoint if unavailable).
- **`index.html`** — a self-contained animated web version of the deck.
- **`summary.html`** — the written reading handout.
- **`SCRIPT.md`** — timed narration.

## Open it

Open `index.html` in any browser. No build step, no dependencies — one file.

- **Navigate:** `→` / `←` / `space`, or click the right/left edge of the screen, or the dots.
- 10 slides, designed for **1:30–2:00**. Narration in [`SCRIPT.md`](./SCRIPT.md).

## The arc (setup → conflict → resolution)

1–4 · **Setup** — AI screens résumés; Western studies ignore Japan; the experiment's scale.
5–6 · **Conflict** — identical résumés, only the name changes → every model favors the female name.
7–10 · **Resolution** — "ignore gender" fails; hiding the name works; but GPT-4o refuses 42% of redacted résumés.

## Design

Soft pastel world — a pink-to-blue gradient ground, rounded type, floating
white cards. Color encodes the narrative: **pink** carries the problem
(female-name bias), **blue** carries the fix (name redacted → bias gone), and a
soft **coral** flags the deployment catch. Numbers and symbols do the talking —
no paragraphs on the slides.
