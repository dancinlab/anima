# CORPUS — log

Append-only history sister of `CORPUS.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-06-04 — domain created

- [x] CORPUS domain seeded (snapshot `CORPUS.md` + this log + DOMAINS.tape row).
- [x] inventory recorded: `anima-chat-corpus-mix-70wiki-30dialogue` (5-lang wiki + dialogue), `anima-persona-sns-corpus` (KR-only, 20-roster IG/YT, 4.19MB/13,322 dlg), `clm-backbone-5lang-sample`, `anima-clm-p1-corpus`.
- [x] coverage GAP identified: SNS + persona are Korean-only; 5-lang lives only in wiki/chat. → unified 5-lang corpus is the target.
- [ ] M1 5-lang persona-voice templates (en/fr/de/es) added to `serving/persona_sns_corpus_gen.py`.
- [ ] M2 unified 5-lang corpus (wiki+SNS+persona) + CORPUS_CARD + HF.
- [ ] M3 KOSMOS survey → what-to-add ranked list.
- [ ] M4 HF.jsonl + KOSMOS/CLM collections + feed 5-lang 7B retrain.
- [ ] M5 honest per-lang byte-balance report.
