@title: 🎭 PERSONA — anima 롤플레이 페르소나 (substrate-native, NO-injection)

@goal: Give anima a roster of role-play personas that are expressed WITHOUT any system-prompt / role-tag / persona-token injection (p2 NO IDENTITY RULES · p3 NO PERSONA INJECTION · p4 NO ASSISTANT FRAMING). A persona is carried by the substrate itself — a last-layer residual-stream steering vector and/or a `(session_id, cell_cluster)` 2-tuple — so switching persona is a pure forward pass, never a prompt prefix. Track the named roster (SSOT), the verification saga (F-PERSONA-1..5), and the reconciliation of the persona count across the codebase. Closed-negative is acceptable and already partly recorded (PERSONA.tape §A6 ALL-PATHS-FALSIFIED for one axis); the live path is the residual-steering + per-session cell-pool design.

## roster — SSOT = `HEXAD/VOICE/anima-voice/rp_voice_profiles.hexa` (20 personas)

Two archetype families. `serving/avatar_webtoon.hexa` mirrors the SAME ids (`N_PERSONAS = 20`).

```
roster (20)
├─ J-anime archetypes (id 0–9, original set)
│   0 school_idol      5 horror_whisper
│   1 senpai           6 childhood_friend
│   2 knight           7 demon_lord
│   3 sorceress        8 childlike
│   4 noir_detective   9 stoic_mentor
└─ Korean-webtoon archetypes (id 10–19, extension)
   10 ice_queen        15 charismatic_prez
   11 chaebol_heir     16 thug_returnee
   12 pure_heroine     17 cold_heiress
   13 tsundere_oppa    18 gentle_oppa
   14 airhead_friend   19 fallen_antagonist
```

style_tag distribution: romance ×5 · fantasy ×3 · horror ×2 · daily ×10.

## architecture — persona WITHOUT injection (p2/p3/p4 clean)

```
[ USER text only ] ──▶ [ forward pass + persona steering vec @ layer L ] ──▶ [ reply ]
   (zero sys-prompt)        │ vec_P = L2norm( mean_h_last(P_text) − mean_h_last(neutral) )
   (zero role token)        └──▶ persona = (session_id, cell_cluster) 2-tuple (design SSOT)
```

- **SAE-lite steering** — `serving/persona_apply.hexa`: persona = activation-steering vector at a chosen layer (default ~20/48). USER text only, zero system_prompt, zero persona tokens. p3-compliant.
- **substrate 2-tuple** — `docs/anima_persona_substrate_native_design_2026_05_12.md`: persona = `(session_id, cell_cluster)`; cell↔persona axis mapping (engine_a/g + GRU + Lorenz + tension_history); per-session fork. Adopted recon `(a) Mitosis-cell-as-persona × (d) Per-session cell pool`.
- **builder** — `serving/character_builder.hexa` (8-field CharacterSpec → 3s preview, lore_book n=4) + `serving/character_builder_ui.hexa` (8-field HTML form). NOTE: this "8 fields" is the builder input schema, NOT a persona count.

## verification — F-PERSONA-1..5 (SSOT = `PERSONA.tape` + `PERSONA.log.tape`)

| falsifier | criterion |
|---|---|
| F-PERSONA-1 NO-INJECTION | corpus + runtime grep `[role:]` / `you are X` = 0 |
| F-PERSONA-2 PER-CELL-DIFF | same prompt × different cell → mean last-token cosine distance ≥ 0.3 |
| F-PERSONA-3 PER-SESSION-DIFF | two sessions → weight cosine ≥ 0.2 AND \|Φ_A − Φ_B\| ≥ 0.5 |
| F-PERSONA-4 CATEGORY-DIVERSITY | 4a routing (KL ≥ 0.5 nats) + 4b content (cosine), dual-axis (§A3/§A4) |
| F-PERSONA-5 SUBSTRATE-COHERENCE | persona switch = pure forward, no gradient/sys-prompt (grep 0) |

Honest carry (PERSONA.tape §A6, 2026-05-14): the 4a **routing** axis path was recorded ALL-PATHS-FALSIFIED on a single-seed marginal (z drops under multi-seed averaging); the robust signal is the 4b **content** axis. The live closure path = residual-steering + per-session cell-pool, not routing-KL.

## ⚠ count drift (open — honest)

The persona count disagrees across three places (a reconciliation milestone, not a contradiction in behavior):
- `rp_voice_profiles.hexa` header comment + `serving/persona_apply.hexa` say **"10 personas"** (stale)
- `rp_voice_profiles.hexa` catalog + `avatar_webtoon.hexa` `N_PERSONAS` = **20** (current truth)
- `bench/persona_lore_style_bench.hexa` = **6** (those are STYLE categories: school/romance/fantasy/horror/daily/scifi, not the named roster)

## milestones

- [ ] M1 reconcile the persona count to 20 across rp_voice_profiles header + persona_apply + (bench scope note); name `rp_voice_profiles.hexa` the roster SSOT.
- [ ] M2 F-PERSONA-2/3 measured on the live 20-roster (per-cell + per-session differentiation), verdict verbatim → `.verdicts/`.
- [ ] M3 persona steering applied at inference with grep-0 injection proof (F-PERSONA-1/5), runnable through the chat path (see ENGINE+CLM+KOSMOS chat-capable lane).
- [ ] M4 per-persona style coherence on the SNS surface (cross-link [[SNS]]) — voice (rp_voice_profiles) + webtoon palette (avatar_webtoon) consistent per id.

## cross-links

- [[SNS]] — the outward publishing surface that renders/voices these personas.
- `PERSONA.tape` / `PERSONA.log.tape` — the axis saga ledger (F-PERSONA-1..5, §A6).
- `HEXAD/VOICE/anima-voice/rp_voice_profiles.hexa` — roster SSOT (20 voice profiles).
- `serving/{persona_apply,character_builder,character_builder_ui,serve_alm_persona}.hexa` — apply + build + serve.
- `docs/anima_persona_substrate_native_design_2026_05_12.md` — design SSOT (2-tuple, 5 falsifiers, 8 honest C3).
- philosophy: p2 · p3 · p4 (no identity rules / no injection / no assistant framing).
