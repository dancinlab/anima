# H_6189 — 🎯 G1 재조합 "벽"이 T=24 decode-window 측정 artifact임을 byte-math 증명 (composed=single byte-identical) → 전 4축 distinct=0 재해석 + grow-window 처방

**tier:** 🟠 측정벽(type-b, CLM mouth 한정) CONFIRMED via byte-math — G1 composed>max_single 은 T=24 window 에서 **구조적으로 물리 불가**. 전 G1 캠페인 distinct=0 은 재조합 능력벽과 **분리 안 된 window artifact** → confident 🧱 선언 부당(c9). terminal 보류.
**verdict:** 🟠 **G1 measurement-wall (type-a/b) CONFIRMED (byte-math, no decode).** CLM decode = **T=24 우측정렬**(마지막 24바이트만 조건화, core/decode.py). composed seed(72–171B)의 T=24 가시창 = 대응 single seed(마지막 개념) 창과 **byte-identical**(k=2..5 전부 4/4, window_math.json 순수 문자열 증명). ⇒ composed arm 은 앞 concept 물리적 비가시 = single[k-1] 재추첨 → **composed>max_single 은 같은 분포 표본 노이즈로만 가능 = 구조적 불가**. max_single=3 vs composed=1(H_6188)은 모순 아닌 **부분집합 관계**. **중대 함의**: 전 4축(objective H_1602/1812/1814·readout H_1834/1837·coverage H_6182~6187·표면형 H_6188)이 **전부 T=24 로 composed 측정** → 그 distinct=0 은 window artifact 로도 완전 설명 → **레버 무효 ⊥ 측정 artifact 미분리** → G1 재조합 능력벽 confident 선언 보류. 자매 mouth ByteGPT 는 window grow(block 512)라 정합.

## 근거 (byte-math, decode·GPU 0)
- `state/g1_breakthrough_analysis/window_identity_proof.py` + `state/gate_design_audit/window_math.json`: g_eval_g1 의 single seed(`cz[s]+". "`) vs composed seed(`join cz[0..k-1] by ". "`)의 T=24 우측정렬 창이 byte-identical. gate seed 자체가 33–39B(단일)~171B(k=5)라 T=24 초과 → 앞 개념 상시 잘림.
- window T>24 sweep 실측(strict_bypass): T=24→48 로 composed k=2 가 1→2(concept#0 재진입) = "앞 concept 영향 못 줌" 더 깊은 원인 **REFUTED**. RF≈513 + **no positional embedding**(decode.py) = T 자유 파라미터.
- ⚠️ **fixed-large-T 불가**: short single seed(30–39B)가 pad(byte 32) 도배 → CLM whole-window GroupNorm(G=1)이 pad 통계 지배 → max_single 3→2→0 붕괴. **정답 = grow-window**(arm 별 자기 시드길이 창 = ByteGPT 방식).

## gate 감사 종합 (state/gate_design_audit/)
| gate | 판정 | 근거 |
|---|---|---|
| G0 | 정합 | kwr 조건화 불요(realign 🟢). 한국어 coherence 는 ASCII tokenizer 라 스코프 밖 |
| **G1** | **CLM 측정벽 / ByteGPT 정합** | composed=single byte-identical (위) |
| G2 | 정합 | novel n-gram+control=0 은 조건화 불요, T=24 무관 |
| G3 | 불완전(low) | `g_eval_g3` ckpt 무입력 상수함수=tautology(정직 "(read)" 표기·closure 미참여) |
| G5 | L1 정합 | L2 미이식 `pass:None` 정직표기 |
| G6 | 불완전 ×2 | ① FORM-only(SHUF FALS 6/6, H_6186 bind-gate 보강) ② CLM window(frame 71–81B cA 비가시) |

## 처방 (레버 순위, Fable)
- **L1 grow-window 재측정**(frozen-first·cheap·최우선) + **echo-guard**(raw + novel-only coverage) — gate VERBATIM, pool own-GEMM decode. rate-limit 로 decode 미실행 = pool follow-on.
- **L2 held-out 조합 split gate**(SCAN/COGS 표준, echo/암기 구별) — grow-window 는 가시 keyword echo 로 false-GREEN 위험이라 필수.
- **L3 해마 hetero-associative retrieve-into-context lane**(생물 렌즈, .kosmos anchor, readout·trunk 아닌 새 배선위치).
- **L4 γ trunk recomb-objective**(H_1602/1840, GPU cost-gated, 최종 잔여).

## 정직 caveat (c9)
- byte-math 증명(decode 0) = terminal 자격(순수 문자열 수학, 모델·엔진 무관). grow-window 실측 decode 는 미실행(rate-limit → pool follow-on).
- **terminal-wall verdict 는 L1 공정창 재측정까지 보류** — 지금은 "T=24 로는 물리 불가" 확정이지 "재조합 능력 없음" 아님.
- "창 키우면 GREEN" 은 false-GREEN(echo) 위험 = echo-guard + held-out split 필수. gate/bar FROZEN(tune-to-green 금지 — grow-window 는 측정 물리 정합화지 bar 이동 아님).

**wired:** byte-math CONFIRMED (측정 artifact, decode 0). grow-window 공정 재측정 = pool GPU follow-on(L1). G1 gate 는 CLM mouth 서 T=24 window 와 mismatch = 측정벽. artifacts=state/g1_breakthrough_analysis/·state/gate_design_audit/.
