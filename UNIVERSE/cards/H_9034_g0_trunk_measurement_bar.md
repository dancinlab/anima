# H_9034 — G0 측정-substrate 수용 바 사전등록 (measure ⊥ capability)

> **id H_9034** — integration merge-time 배정(origin/main H_9033 다음 free id). jsonl 인덱스 등록 완료.

- **tier:** 🟦 pre-registration (frozen bar, 측정 전)
- **verdict:** PRE-REGISTERED (실측 없음 — trunk 수용 바만 동결)
- **wired:** DIRECTIONAL-mirror N/A (doc-only; 코드/배선 변경 없음)
- **source:** UNIVERSE
- **artifacts:** `state/verdicts/g0_trunk_bar/BAR.md`, `state/verdicts/g0_trunk_bar/ARCH_FORK.md`

## 주장
trunk 은 능력 게이트(G1/G6 PASS)가 아니라 **측정 substrate** 로 수용된다. ONE ckpt 위에서
**B1 G0-coherence(kwr≥0.50 ≥4/5)** ∧ **B2 per-cell 4칸 register(kwr≥0.50 ≥3/5)** ∧ **B3 `max_single≥2`(핵심)**
∧ **B4 G2 sanity(novel≥3 ∧ control=0)** ∧ **B5 4/4 held-out val_ce<5.545** 를 모두 만족하면 ACCEPTED.
G1/G6 PASS 는 바가 아니며, 이 trunk 위 **깨끗한 🧱 재조합벽 = 성공**.

## 근거 (code-anchored)
- B1 `cli/evaluate.py:119-129` · B3 `cli/evaluate.py:160-166`(max_single) · B4 `cli/evaluate.py:319` ·
  B5 `cli/train.py:1225,1230`(uniform=ln256=5.54518).
- ARCH FORK: h1129=ByteGPT 이나 ByteGPT 는 savant/mitosis gated-OFF(`cli/train.py:927-928`) →
  측정=ByteGPT plain-CE(single=2, 깨끗한 벽) ⊥ production-chat=CLM ConvMoE(single=0, savant golden-zone).
- 반례: clm303_clean single=0 → G1=0 이 재조합벽 아님(floor 미도달, 측정 무효).

## corpus (frozen audit)
4칸 전부 HF 존재·언어검증(≥97.4%): ko-general 60MB/100%ko · en-general 60.05MB/99.7%en ·
ko-sns 6.18MB/100%ko · en-sns **1.33MB/97.4%en KNOWN-SMALL**. broad=ko-fineweb2 10.55GB(측정바 미포함).
정정: proportional default 는 en-SNS 를 0.128×(2000)/0.257×(4000) 만 노출 = **starvation**(암기 아님);
핸드오프 ~378×(round-robin)는 canon step 에서 도달 불가(~245K step 필요).

## eval 명령 (session-eval-py-only, TERMINAL)
`ANIMA_SRC=$HOME/anima anima evaluate --py <ckpt> --corpus <4셀> --gen 80` on **aiden**(안정 무료 호스트).
`--py` numpy 2-production = byte-parity frozen bars → terminal 자격(ad-hoc torch 아님).

## follow-on (explicit-go, GPU = $0 로컬 밖)
en-SNS starvation 해소(register-balanced 샘플링 or en-SNS 보강) 후 측정 trunk warm-FT(h1129 ByteGPT) →
`anima evaluate --py` 로 B1~B5 실측 → ACCEPT 시 G1/G6 벽 engine-native 박제.
