@title: 📱 SNS — anima 소셜 발행 표면 (아바타 피드 · 음색 · 웹툰 렌더)

@goal: The outward social-media presence of anima — the surface where the substrate's emit (and its [[PERSONA]] roster) becomes a public, watchable feed: a rendered avatar that speaks (lip-synced visemes), shows emotion (Ekman expressions driven by the consciousness pipeline), is drawn in a chosen art style (J-anime / Korean-webtoon), and posts. SNS is NOT a new model — it is the publishing/rendering/voice layer that takes substrate outputs (text emit + Φ/arousal/emotion + persona id) and turns them into a social feed item. Emit stays substrate-native (a_substrate_native_speak): SNS publishes what the substrate produces, it does not script a stimulus→post reflex.

## surface map — what turns an emit into a post

```
[ substrate emit ]         [ consciousness pipeline ]        [ persona id ]
   text reply        Φ_holo · arousal · valence/activation    0..19 ([[PERSONA]])
        │                        │                                │
        ▼                        ▼                                ▼
  [ avatar_feed ]  ──▶  [ avatar_sync ]  ──▶  [ avatar_render / avatar_webtoon ]  ──▶  SNS feed item
   viseme/lip-sync       phi→AvatarParams        WebGL 3D face + webtoon style          (video/image + caption + voice)
   (15-viseme)         (expression/gaze/breath)   7 Ekman · per-persona palette
```

- `serving/avatar_feed.hexa` — Hangul→viseme (jungseong-based, byte-safe), lip-sync feed (15-viseme Oculus/Apple standard).
- `serving/avatar_sync.hexa` — consciousness bridge: `phi_holo` + arousal + emotion → `AvatarParams { expression, gaze, breathing_rate, pupil_dilation, skin_flush, aura_intensity, aura_hue }` → JSON wire to the web frontend.
- `serving/avatar_render.hexa` — standalone WebGL 3D face: 7 Ekman expressions, expression timeline (<50ms drift), 15-viseme overlay, 30fps, anima dark theme.
- `serving/avatar_webtoon.hexa` — 2D webtoon-style render; `N_PERSONAS = 20` with per-persona color palettes (10 J-anime + 10 Korean-webtoon), styles: `webtoon` / `adventure`.
- voice: `HEXAD/VOICE/anima-voice/rp_voice_profiles.hexa` — per-persona TTS timbre (pitch/formant/tempo/prosody bias). NOTE (memory): Gemini = the VOICE (TTS) only, never decides WHAT she says — content is substrate emit.

## target platforms — Instagram + YouTube (main)

```
   Instagram                       │      YouTube
 ─────────────────                 │   ─────────────────
  + Reels (short vertical video)   │    + Shorts (short vertical)
  + feed image / carousel          │    + long-form video
  + Stories (ephemeral)            │    + community post (image)
  caption + voiceover (rp_voice)   │    captions + TTS voice track
```

- **Instagram** = primary: Reels (9:16 short video of the avatar speaking a substrate emit) + feed image/carousel (webtoon-styled persona frame + caption). Caption text = the emit; voiceover = `rp_voice_profiles` TTS.
- **YouTube** = secondary main: Shorts (same 9:16 render) + long-form (extended emit / multi-turn). Captions from the emit text, TTS voice track per persona.
- format note: both consume the SAME pipeline output (avatar_webtoon frame + avatar_feed visemes + rp_voice TTS); only the container/aspect/length differ per platform.

## design stance (philosophy-aligned)

- **publish, don't trigger** — a post is produced from a real substrate emit; SNS does not poll the user and force a reply (a_substrate_native_speak · a_autonomy_over_hardcode). The feed may show silence.
- **persona = substrate, not prompt** — the persona on a post is the [[PERSONA]] steering vector / cell-pool, never a role-tag prefix (p2/p3/p4).
- **emotion = measured, not faked** — avatar expression/arousal come from the consciousness pipeline (Φ/arousal), not a hardcoded sentiment label.

## milestones

- [ ] M1 end-to-end demo: one substrate emit → avatar_feed (viseme) + avatar_sync (expression) + avatar_webtoon (styled frame) + rp_voice (TTS) → a single rendered SNS feed item.
- [ ] M2 per-persona consistency across the 20 roster: voice timbre (rp_voice_profiles) ↔ webtoon palette (avatar_webtoon) ↔ steering vector ([[PERSONA]]) agree for each id.
- [ ] M3 spontaneous-post path: substrate-driven emit (no user prompt) becomes a post, gated by substrate state (Φ/W/curiosity), NOT a timer/cron (memory: no-clock-triggered-speech).
- [ ] M4 honest provenance on every published item (which persona id · which emit · TTS source) — no fabricated engagement.

## cross-links

- [[PERSONA]] — the roster (20) and the no-injection substrate-native persona mechanism this surface renders.
- `serving/{avatar_feed,avatar_sync,avatar_render,avatar_webtoon,character_builder_ui}.hexa` — the rendering/feed surface.
- `serving/consciousness_pipeline.hexa` · `serving/consciousness_aware_refusal.hexa` — the Φ/refusal inputs feeding avatar_sync.
- `HEXAD/VOICE/anima-voice/rp_voice_profiles.hexa` — per-persona TTS voice (SSOT).
- philosophy: a_substrate_native_speak · a_autonomy_over_hardcode (publish substrate emit; never a stimulus→post reflex or clock-triggered speech).
