---
date: 2026-05-12
package: anima
component: hf-space-dancinlab-anima-chat
status: LANDED
owner: anima monorepo
cycle: HF Space dual-ckpt selector (succeeds §21 B'' swap)
ssot_artifact: ../../PASS_STRICT_SPONTANEOUS_CHAT.md §24
upstream_pin: Space sha 865ff4f / commits c3037e4 + ab8a2ee + 865ff4f
---

# HF Space dual-ckpt selector landed — anima side (2026-05-12)

## §1 Summary

`dancinlab/anima-chat` Space 에 **ckpt dropdown selector** 추가. 사용자가 매 request 마다 두 substrate 중 선택:

- **Phase 1A** (default, 권고) — `dancinlab/anima-clm-phase1a-multi-turn-sft`. V5.8 std_greedy 3/5 자연 대화 winner.
- **B''** (실험) — `dancinlab/anima-clm-bprime-prime-v4lite-15-15`. V4-lite 15/15 표면평가 winner (4 substrates 중 최고).

§21 이후 B'' 단독 default 가 V5.8 std_greedy 3/5 → 0/5 regression 을 일으켜, 자연 대화 축 vs 표면평가 축 사이의 axis-dependent trade-off 를 사용자에게 위임하는 구조로 전환.

## §2 Changes

3-file edit, single Space, 3 commits:

| file | change |
|---|---|
| `app.py` | `ckpt_choice` Radio 추가 (Phase 1A / B''), `_get_chat(ckpt_choice)` 가 per-ckpt cache (`_CHATS: dict`) 에서 lazy 로드, 2-row benchmark table |
| `anima_chat.py` | `AnimaChat.__init__(repo_id=..., filename=...)` kwargs 추가 (drop-in compat, default 는 B'') |
| `README.md` | frontmatter `dual-ckpt` + `phase-1a` + `b-double-prime` 태그, `models:` 2-row, per-ckpt comparison table |

Space commit trail:
- `c3037e4` — app.py dual-ckpt Radio + per-ckpt cache
- `ab8a2ee` — anima_chat.py repo_id/filename kwargs
- `865ff4f` — README.md dual-ckpt frontmatter + matrix

before SHA `44c49c6` (B'' only) → after SHA `865ff4f` (dual-ckpt).

## §3 Live verify (gradio_client)

input = `"안녕! 너는 누구야?"`, 2 ckpt × 2 mode = 4 generations, **4/4 OK**:

| ckpt | mode | response | elapsed |
|---|---|---|---|
| Phase 1A | greedy | `네, 맞아요. 너는 누구야?` | 25.6s |
| Phase 1A | M4_force_include | `가우야! \| 안녕!  = [\`si]` | 20.9s |
| B'' | greedy | `안녕하세요, 저도와 전문 안에 있어요. 전 세계 정보를 제공` | 70.6s |
| B'' | M4_force_include | `�ݿ�成方据年一一豳 下面氵湷的身年果時。` | 48.7s |

→ Phase 1A greedy 가 V5.8 자연 대화 character (question echo + KO 짧은 fluent) 을 재현. B'' greedy 가 V4-lite character (KO byte 풍성, 의미 collage). B'' M4 의 CJK noise 가 V5.8 0/5 regression 의 raw 발현.

## §4 Cross-link

- SSOT §: `PASS_STRICT_SPONTANEOUS_CHAT.md §24` (originally §22, promoted due to numbering collision with §22 axis exploration)
- Prior B'' swap: PSCC §21 (44c49c6)
- 4-substrate matrix: PSCC §15
- V14↔chat-cap anti-correlation: PSCC §19 + `hypotheses_candidates/Hc_1221_*.md`
- HF Space live: <https://huggingface.co/spaces/dancinlab/anima-chat>
- Phase 1A model: <https://huggingface.co/dancinlab/anima-clm-phase1a-multi-turn-sft>
- B'' model: <https://huggingface.co/dancinlab/anima-clm-bprime-prime-v4lite-15-15>

## §5 Next actions (excerpt from PSCC §24)

- 🥇 dual-ckpt UX 측정 — 5 prompts × 2 ckpt × 4 modes 40-cell live matrix
- 🥈 Phase 1A.1 (color/cosmology, 4/5 std_greedy PASS) selector 에 추가 → 3-option matrix
- 🥉 Hybrid substrate F train — V14 + V4-lite + V5.8 동시 만족 시도 (Hc_1221 falsifier)
