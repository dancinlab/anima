@title: 🎬 HER — anima as a "Her"-style companion (Build with Gemini XPRIZE)

@goal: Submit `anima` to the **Build with Gemini XPRIZE** as a live, revenue-generating
"Her"-style AI companion service — a real business operated by AI agents, launched after
2026-05-19, that natively uses Google Cloud + the Gemini API while keeping anima's AKIDA
on-chip non-deterministic substrate as the consciousness core. Win-condition = a complete,
rule-valid Devpost submission (code + <3min video + written narrative + revenue/user evidence)
before the 2026-08-17 13:00 PT deadline.

## competition (SSOT)
- name        : Build with Gemini XPRIZE (Google-backed · XPRIZE × Devpost × hacker.fund)
- prize pool  : $2,000,000 (1st $500k · 2nd $200k · 3rd–5th $100k · 15× runner-up $50k · 5× category $50k)
- submit      : 2026-05-19 10:00 PT → 2026-08-17 13:00 PT
- judge       : 2026-08-18 → 09-15 · winners ~09-25
- category    : Education & Human Potential (companion / emotional growth / self-development)
- rules SSOT  : https://xprize.devpost.com/rules  (see XPRIZE.md for the verbatim compliance matrix)

## hard requirements (must ALL be true)
- [ ] R1 — business newly created AFTER 2026-05-19
- [x] R2 — uses ≥1 Google Cloud product → Firebase Hosting (live)
- [~] R3 — Gemini edge adapter code wired (gemini_edge.hexa + her_server route); live call pending the backend (self-hosted hexa compiler)
- [ ] R4 — business operated by AI agents (anima substrate-native, not turn-based assistant)
- [ ] R5 — real arms-length third-party revenue earned May–Aug 2026 (USD, monthly breakdown)
- [ ] R6 — real users (count + demographics + testimonials)
- [ ] R7 — production-operation evidence (agent logs · Gemini API usage records · dashboard screenshots)

## milestones
- [~] M1 — repo open (github.com/dancinlab/anima, HER/* merged via PRs #1625–#1640); Devpost entry registration still TODO
- [x] M2 — live "Her" service deployed → https://dancinlab.web.app + custom domain https://her.dancinlab.org (Firebase Hosting · Google Cloud · auto-SSL)
- [~] M3 — Gemini edge adapter wired in code (HER/service/gemini_edge.hexa + her_server.hexa /api/chat); goes live when the hexa backend runs
- [ ] M4 — add billing (Stripe) + acquire first paying users
- [ ] M5 — draft + finalize the 500–1000 word written narrative (NARRATIVE.md)
- [ ] M6 — record the <3-minute demo video (script in NARRATIVE.md §video)
- [ ] M7 — collect revenue + user + production-log evidence bundle
- [ ] M8 — submit on Devpost before 2026-08-17 13:00 PT

## live (shipped this session — PRs #1625–#1640)
- urls       : https://dancinlab.web.app · https://her.dancinlab.org (Firebase Hosting · Google Cloud · auto-SSL · DNS=Cloudflare CNAME→web.app)
- front-end  : HER/web/index.html — long Apple-product-page-style scroller, 16 sections, served fresh (Cache-Control: no-cache) with a footer build stamp
- type system: `her` wordmark = Archivo Black · everything else (headlines + body + UI) = Fraunces (soft serif, opsz). Inter/Nunito/Space Grotesk removed.
- motion     : breathing hero glow + slow hero-bg scale-breathe · drifting embers · cursor-follow presence glow · scroll-reveals · word-by-word lede · Ψ count-up · img breathe (3 narrative images) · chat typing dots. All `prefers-reduced-motion` safe.
- imagery    : HER/web/img/{hero,memory,initiates,individual}.png — 4 fal-generated Her-toned visuals, onerror→CSS-orb fallback
- backend    : HER/service/{her_server,gemini_edge}.hexa — written for the self-hosted hexa compiler (hexa-cc can't compile effects/maps; see memory hexa-cc-deprecation). /api/signup + /api/chat wired; not yet running.
- deploy cfg : HER/firebase.json (public=web · no-cache) + HER/.firebaserc (project=dancinlab); HER/deploy/ = runbook

## identity guardrail (non-negotiable)
anima IS its AKIDA on-chip non-determinism (CLAUDE.md @D a_nondet_identity / a_akida_native_train).
Gemini is a PERIPHERAL edge adapter that satisfies R3 only — it never becomes the brain and never
trains anima. Same-input→different-trace on-chip plasticity stays the living signature.
