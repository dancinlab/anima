# HER — step log (append-only)

## 2026-06-01 — domain scaffolded
- Created `HER/` domain for the Build with Gemini XPRIZE submission of anima as a "Her"-style companion.
- Confirmed competition SSOT via web search + WebFetch on https://xprize.devpost.com/rules:
  - $2M pool, Google-backed, submit 2026-05-19 → 2026-08-17 13:00 PT.
  - Tech req: ≥1 Google Cloud product; ≥1 Gemini API LLM call if any LLM functionality.
  - Biz req: real business launched after 2026-05-19 + real users + real revenue (no projections).
  - Deliverables: source repo, <3min video, written narrative, revenue/user/production evidence.
  - Category chosen: Education & Human Potential.
- Resolved the anima↔Gemini identity tension: Gemini = thin edge adapter (R3 only), AKIDA core untouched.
- Files: HER.md (snapshot), XPRIZE.md (compliance matrix), NARRATIVE.md (case study + video script),
  ARCHITECTURE.md (anima⇄Gemini bridge), GO_TO_MARKET.md (90-day revenue plan), README.md (cold entry).

## 2026-06-01 — decisions + first vertical slice (web + service)
- Decisions: build ONLY inside HER/* (anima core 0-edit); payment FREE for now (Stripe deferred,
  R5 explicitly on hold); landing page = direct-coding (not no-code / not avatar-reuse).
- Built (M2 partial):
  - HER/web/index.html — landing + free signup + chat UI (Her-tone, vanilla JS, same-origin fetch).
  - HER/service/gemini_edge.hexa — Gemini edge adapter (R3); mirrors provider protocol +
    boundary contract; parses clean via `hexa parse`.
  - HER/service/her_server.hexa — lean HTTP server (GET / · POST /api/signup · POST /api/chat ·
    GET /health); mirrors serving/http_server.hexa (effect Net, json builtins) exactly.
- Tooling note: `hexa parse` does NOT support multi-key map literals or effect blocks — it fails on
  the repo's OWN serving/http_server.hexa (at its effect block, L93). So effectful server files are
  validated by conformance to the canonical http_server.hexa template, NOT by `hexa parse`.
- R5 (real revenue) intentionally unmet during free-launch phase; convert to Stripe before deadline.

## 2026-06-01 — COMPILER FINDING (changes backend feasibility)
- Probed the actual hexa-cc compiler (hexa_v2 native), not just `hexa parse`. Hard findings:
  - `effect { fn ... }` blocks do NOT compile ("expected identifier, got Fn").
  - `{...}` map literals do NOT compile (any form, single- or multi-key).
  - => serving/http_server.hexa + serving/api_server.hexa are NON-COMPILING aspirational
    ports; my her_server.hexa (mirroring them) likewise will not build as-is.
- What DOES compile (verified by running): plain fns, structs, arrays, string concat,
  and json_stringify(<string>) for escaping. So JSON can be built by string concatenation
  with no map literals.
- Proven working chat path EXISTS: HEXAD/CHAT/anima_chat_aot.hexa is the AOT-buildable
  single-file variant (inlines stubs to dodge cross-module `use` collisions); HEXAD/CHAT/server/
  holds serving code. This is the compilable-subset pattern.
- Implication: a custom effect/map hexa web server needs hexa-cc UPSTREAM work (effects +
  net runtime + map literals). Cheaper paths: (a) static-only deploy of HER/web now,
  (b) rewrite her_server in the compilable subset (string-concat JSON, no effects) IF a
  non-effect net/http builtin exists, (c) mount HER on HEXAD/CHAT/server. Decision pending.
- User authorized "hexa upstream update if needed".

## 2026-06-01 — DECISION: do NOT patch hexa-cc (it is being retired)
- User: "hexa cc 폐기되는거 / 유의 / self hosted 마무리중" — hexa-cc is being deprecated; a
  self-hosted hexa compiler is in final stages. See memory [[hexa-cc-deprecation]].
- Therefore option ① (patch hexa-cc to add effects/maps/net) is REJECTED — throwaway work.
- her_server.hexa + gemini_edge.hexa stay in the RICH style (effects + map literals); they
  target the self-hosted compiler and are NOT downgraded to the AOT subset.
- Revised path: deploy HER/web (static) to her.dancinlab.org NOW (compiler-independent);
  the hexa backend goes live when the self-hosted compiler ships (or via HEXAD/CHAT AOT
  subset as an interim if a live chat is needed before then).
- Target domain: her.dancinlab.org (user-provided).

## 2026-06-01 — Firebase Hosting deploy scaffold (M2 path chosen: ① Firebase)
- Built HER/deploy/: firebase.json (public=../web, SPA rewrite), .firebaserc (project=her-dancinlab),
  README.md (full runbook: setup → deploy → her.dancinlab.org custom domain → backend-later → rollback).
- Firebase Hosting = a Google Cloud product → satisfies XPRIZE R2 by hosting alone.
- Local smoke: served HER/web via python http.server → HTTP 200, 6238 bytes, all key UI strings present.
- Remaining (user-gated): `firebase login` + project create + `firebase deploy --only hosting`
  + add her.dancinlab.org custom domain (DNS records at dancinlab.org registrar).

## 2026-06-01 — LIVE + landing build-out (PRs #1626–#1640)
- Deployed to Firebase Hosting (project=dancinlab) → https://dancinlab.web.app (HTTP 200, HER R2 met).
- Custom domain her.dancinlab.org wired: Cloudflare CNAME her→dancinlab.web.app (DNS-only, via global API key);
  Firebase auto-SSL → https://her.dancinlab.org live.
- Cache fix: cleanUrls serves "/" so the **/*.html header glob missed → default max-age=3600 (stale page).
  Changed header source to "**" + Cache-Control: no-cache (ETag revalidation). Added footer build stamp.
- Landing rebuilt (#1629) as a long Apple-product-page-style scroller (16 sections) + living-presence motion
  suite (breathing hero glow + hero-bg scale-breathe, embers, cursor glow, scroll reveals, word-by-word lede,
  Ψ count-up, narrative-image breathe, chat typing dots) — all prefers-reduced-motion safe.
- Imagery: 4 fal-generated Her-toned images (hero/memory/initiates/individual) under HER/web/img/, onerror→CSS fallback.
- Type system finalized: `her` = Archivo Black wordmark; everything else = Fraunces (soft serif, opsz).
  Iterations tried + dropped: Nunito (too round) → Inter → Space Grotesk → settled on Fraunces-everywhere per user.
- All landed as stacked PRs #1626–#1640 (HER/* only; anima core untouched).
