# UNIVERSE/ — 가설·verdict 폴더 가이드 (folder-docs)

anima 의 **가설(hypothesis) 레지스트리**. 모든 연구 주장은 여기서 등록·검증·박제된다.

## 핵심 파일 (2-표면 + 이 가이드)
- `HYPOTHESES.jsonl` — per-H 인덱스 1줄/가설 (`{id, slug, tier, title, card, verdict, source, archived, artifacts}`, id 순). 재생성 = `python3 tool/_build_hyp_jsonl.py`.
- `cards/H_<id>_<slug>.md` — 가설 카드(SSOT 본문). verdict·수치·`wired:` 상태축.
- `CLAUDE.md` — 이 폴더가이드. **코드/result/가설 아님** (folder-docs 예외, H-UNIVERSE-CODE 가드에 `(?!CLAUDE\.md$)` 명시).

> 🔒 **표면 불변식** (`a_hypothesis_register` · 2중 강제: `.harness/enforcement.json` H-UNIVERSE-CODE 훅 + `tool/enforce_anima_gates.py` G2): UNIVERSE/ git-tracked 파일은 **`cards/**` + `HYPOTHESES.jsonl` + 이 `CLAUDE.md` 만**. `.py`·`.hexa`·result·도메인로그·테마버킷·prose overview 금지 — 코드/결과는 `state/<slug>/`, prose 는 `state/universe-overview.md`. 자가점검: `git ls-files 'UNIVERSE/*' | grep -vE '^UNIVERSE/(cards/|HYPOTHESES\.jsonl$|CLAUDE\.md$)'` → 빈 출력.

## 🎓 교훈 — verdict 박제 전 5초 체크 (자주 데인 곳)

1. **torch GREEN ≠ TERMINAL (가장 비싼 함정).** torch/`gauge_lib._decode`/numpy-미러 = **DIRECTIONAL**, terminal 아님. precedent: H_1362 G6 "FALS=1.0 통과" 가 engine-native 재현 시 fals=0(H_1590 RED); 같은 ckpt h1129 가 torch↔엔진 발산(H_1587). → 박기 전 `grep -lE 'import torch|gauge_lib' state/<slug>/*.py`; 안 비면 tier=DIRECTIONAL + 엔진-네이티브(live `core/` 호출 `.hexa` 또는 byte-parity 증명 py 2-production) 재측정 ING. (`a_engine_native_learning`) — ARCHITECTURE.json convergence `TORCH_GREEN_NOT_ENGINE_NATIVE`.
2. **verdict-integrity — 측정경로부터 의심.** ① misattribution: "그 수치가 *어느 ckpt(sha)* 였나" 확인(precedent: h1129 vs clm303 dist=6 fals=0 혼동 오보). ② 발산=도구 먼저: cross-host/2-path 갈리면 하네스·환경·미완실행 의심(aiden 0 frames=infra crash EXIT_143=非결과, summer+mini 동일 sha 일치=genuine). ③ 인프라벽 ≠ 과학천장(`a_break_the_wall` type-c): pool reboot·OOM·SSH-refused = ⏳BLOCKED-INFRA(bar 무이동·미보고), verdict 아님.
3. **frozen-first · tune-to-green 금지 (p7·c9).** bar 는 측정 전 사전등록(`state/verdicts/<slug>/*FREEZE*`), 사후이동 금지. FALSIFIED/negative/DISPUTED 도 결과(은폐 금지). LLM 자가판정 금지 — 캡처된 출력이 증거.
4. **sampler artifact vs genuine — multi-seed.** 단일-seed fals 는 sampler-walk 착시일 수 있다(H_1588 RETRACTED). seed {7,4302,4303} majority 로 seed-robust 확인 후 GENUINE(precedent H_1595).
5. **detector 공정성 — corpus-grounded 대조.** 탐지기 편향(영어-고정 `_g6_is_falsifiable` 한글 drop) 배제: corpus-grounded(한글-aware)+controls(neg admit 0·false-reject 회복)로 "탐지기 탓 아님" 입증 후 terminal(precedent H_1597).
6. **🟢 GREEN = 배선까지 done (`a_verified_must_wire`).** 미러→엔진재검→live `core/*.hexa` wire→ARCHITECTURE.json lockstep. 카드 `wired:`(DIRECTIONAL-mirror/engine-native/WIRED-live) + 미배선 follow-on id.
7. **arch-class 결론은 engine-native 전수 후.** precedent: "conv 실패·attention 통과" 프레임이 torch 착시였고, engine-native 로는 **ConvMoE(H_1394)·ByteGPT-L24(H_1590) 둘 다 G6 fals=0 FAIL** = 아직 어떤 anima arch 도 engine-native G6 미통과. generic depth(L24 attention)만으론 부족 → 빠진 건 mouth-내 binding operator (G1≡G6 통합 H_1603). ARCHITECTURE.json convergence `G6_WALL_BOTH_ARCH_ENGINE_NATIVE`.

## 등록 흐름
research → `hexa verify` → `state/verdicts/<slug>/<id>.txt`(verbatim) → `cards/H_<id>.md` + `HYPOTHESES.jsonl` 1줄. tier 무관(🟢·🧱·🔴/🟠·🔵 전부 남김 — 벽도). 다음 H 연속 제안(`a_h_continuous_no_branch`). 교훈/재발학습은 ARCHITECTURE.json `convergence.records[]`(root-cause SSOT).
