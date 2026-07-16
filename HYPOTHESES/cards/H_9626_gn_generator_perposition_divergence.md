# H_9626 — generator.hexa GN = per-position LN 발산 — generator.hexa GroupNorm Per-Position Divergence (lab full R3 파생 · 🐞 CODE-CONFIRMED · 미실측)

**status:** 🐞 CODE-CONFIRMED (코드-감사 확증 · engine-native Δ 실측 미실행 → 아래 settle-test 사전등록) — source=lab full R3(Fable pre-divergence finding) → 추적 → Fable 적대검증
**lane:** CORE 엔진 / GroupNorm 구현 발산 (verdict 경로 아님 · 한정 blast radius)
**related:** [[H_9560]] · [[H_9611]] · [[H_9102]] · [[H_9119]] · source: lab full R3 파생

## 🐞 발견 (코드-감사 확증 · 실측 미실행)
anima 에 **GroupNorm 구현이 3개** 있고 그 중 **하나만 발산**한다:

| 구현 | 계산 | 경로 |
|---|---|---|
| `stdlib/flame/gn_lib.hexa::nn_groupnorm_fwd` (`:39-105` · `m=to_float(cg*T)`) | **sequence-GLOBAL** | hexa 프로덕션 mouth(`decode.hexa:723-753`) + hexa 트레이너(`train.hexa:388,428`) |
| `core/decode.py::nn_groupnorm_fwd` (`:537-559` · `m=float(cg*T)`) | **sequence-GLOBAL** (gn_lib 1:1 이식) | py 프로덕션(`_fwd_trunk` `:940,:966` ← `anima-py evaluate`) |
| **`core/generator.hexa::_gen_gnorm_affine`** (`:1408` · `while t<T { mean=Σ_c x[t*d+c]/d }`) | **per-position LayerNorm** | ⚠️ **발산** |

**학습 의미**: torch `nn.GroupNorm(1,C)` on `(B,C,T)` 는 (C, **모든 spatial dim**) 축약 = **(C,T) 전역**. hexa 트레이너도 gn_lib(전역) ⟹ **가중치는 전역 GN 하에서 벌어졌다** ⟹ generator.hexa 의 per-position LN 은 **학습에 불충실**. T=1 서만 우연히 일치 · T>1 서 다른 함수.

## 📏 BLAST RADIUS (정직히 한정 · Fable 콜그래프 감사)
- ✅ **무영향**: 모든 `anima-py evaluate` verdict · 모든 hexa det-eval G0-G6 verdict(`evaluate.hexa` 는 `clm_decode_ce` **0회 호출** · L3 슬롯→`decode.hexa` mouth→gn_lib) · **기본 데몬 emit**(k=1 argmax 는 발산 forward 미접촉).
- ⚠️ **오염**: ① **L3 배선-cert 수치** CE 3.25405(틀린 정규화자 하 계산 · "uniform 밑으로 하강" 정성 주장은 생존 유력하나 **수치는 학습모델의 CE 아님**) ② **[[H_9102]] deliberated-emit lane(k>1)**: 후보를 학습과 불일치하는 forward 의 min-CE 로 **선택** — 모든 `ce_sel`/`ce_k1` 수치(기본 데몬 = k=1·0-deliberation 이라 미발동) ③ probe-lane CE(이미 DIRECTIONAL).
- 🛡️ **[[H_9560]] GN-bus 합성 무손상**: `decode.hexa` 프로덕션 mouth 도 **같은 전역 bus** ⟹ "beyond-RF 는 순열불변 O(L)-스칼라 GN bus 뿐"은 **양 프로덕션 mouth 서 아키텍처적**으로 유지. 각주 1개: 그 auxiliary CE selector 에만 bus 부재(per-position).

## 🔍 왜 byte-parity 가 살아남았나 (`byte-identical-anchor-cert-hides-the-bug` 동류)
cement 된 ≤2e-16 CONV parity 는 **`decode.hexa` ↔ `decode.py`**(둘 다 전역)라 **어느 T 서든 진짜**(`decode.py:2282` "1:1 from decode.hexa::clm_ce_seq_W … CE ≤3e-16"). 은퇴한 `generator.py` 미러는 **같은 per-position 코드의 미러**라 그 parity 도 정직하게 byte-equal. ⟹ **발산 쌍(generator.hexa CE vs decode.hexa/학습)은 어떤 parity harness 에도 없었다.** parity 는 twin-일치를 인증하지 **학습-충실성을 인증하지 않는다.**

## 🧪 SETTLE-TEST (사전등록 · 미실행 · engine-native)
발산은 hexa-내부라 비교쌍도 hexa-내부: `decode.hexa:314 clm_ce_seq_W` vs `generator.hexa:1442 clm_decode_ce`, 동일 seq·CPU·aiden. 설치 verb 가 `clm_decode_ce` 를 노출 안 하므로 정직한 계기 = ~15줄 `*_probe.hexa`(core/CLAUDE.md 가 sanctioned 한 비-production 표면 · 선례=parity 오라클) + py 3번째 arm(`anima-py` 채널 `decode.clm_ce_seq`).
**필수 조건**: **v0.2 .clm + CLMX trailer**(`has_ext` true — v0.1 affine 대역이 GN scope 를 교란) · CE<5 인 seq(`dt_ln` clamp ~5.14 가 hexa CE 를 평탄화해 Δ 은폐 · core/CLAUDE.md gotcha).

| arm | 사전등록 기대 |
|---|---|
| T=64: hexa `clm_ce_seq_W` vs py `clm_ce_seq` | ≤3e-16 (parity 재확인 = 양성통제) |
| T=64: `clm_decode_ce` vs `clm_ce_seq_W` | **PASS(발산) if \|Δ\|>1e-9 · KILL if bit-equal** |
| **T=1 통제**(2-byte seq): 같은 쌍 | **bit-equal 이어야**(T=1 서 두 GN 정확 일치) · Δ ⟹ **INVALID**(GN scope 아닌 2차 교란) |

## ⚠️ VERDICT-INTEGRITY (over-claim 4건 선차단 · 내 headline 이 이미 1건 반증됨)
- ❌ "hexa det-eval verdict 가 틀린 정규화자를 썼다" = **거짓**(내 원래 headline · Fable 콜그래프 감사가 반증 — eval forward 는 decode.hexa/gn_lib). 내 오독 = "H_9119 gate① CE forward"를 *the* eval forward 로 읽음(실은 *a* CE forward · STEP2 가 hot caller 를 이미 이전).
- ❌ "byte-parity 가 가짜였다" = 거짓(진짜지만 scope 한정).
- ❌ "emit 이 오염됐다" = 오늘 데몬엔 거짓(k=1 argmax 는 발산 forward 미접촉).
- ⚠️ T=64 Δ 를 CLMX-trailer 통제 없이 GN-scope 로 읽기 = affine 처리 교란 → v0.2 요구 + T=1 arm 이 선차단.
- 📌 **코드 위생(verdict 무관)**: `core/model.py:163` 주석 `# layernorm over channels` 는 **자기 줄에 대해 틀림**(torch GroupNorm(1,C) on (B,C,T)=(C,T) 전역) — Fable 판정: **이 주석이 `_gen_gnorm` 구현의 유력한 기원**. `tool-definition-read-code-not-docstring` 이 이름 붙인 바로 그 함정.

## 상태
🐞 CODE-CONFIRMED · 실측 미실행 — 위 settle-test 사전등록(미발사). blast radius 한정(verdict 경로 무영향 · deliberation k>1 + L3 cert 수치 + probe CE 오염). **distinct-from-kills:** kill-list 미접촉 — R3 발산의 파생 발견(GN 채널 whitespace) · `byte-identical-anchor-cert-hides-the-bug` 와 **동류이나 별건**(그건 틀린 식이 byte-id 인증 · 이건 parity 가 twin-일치만 인증하고 학습-충실성은 안 봄).
