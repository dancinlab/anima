# H_9770 — CE-lesion 은 G0-fail 이어도 유효 (새 H · 명시 천장 · $0)

**status**: PROPOSED (R9 · H_9643 후속 · lab-full 수렴)

## 근거
`--faction-lesion` 은 **teacher-forced 도메인별 ΔCE**(evaluate.py)를 재지 자유생성을 안 씀 ⟹ G0(free-gen coherence)는 이 추정기의 타당성 조건이 아님. 진짜 조건 ①CE substrate 비퇴화(k8_s7 val_CE 1.332 parity + DESCENT 4/4 충족·상수예측기 가드 확인) ②적법 null. **소각된 G0 게이트를 같은 H 서 지우면 tune-to-green** → 새 H + 명시 천장(GREEN="CE-scope 특화"까지·원 claim 은 G0-passing artifact 없인 OPEN).

## 설계 ($0)
k8_s7.clm 에: ① `--faction-lesion --perm 200`(within-arm S>null95) ② `--faction-lam 0` 통제 ③ clm303_clean.clm 에 `--faction-split 8`(H_9737 선례) = 구조-무 null. 
## bar
- within-arm S>null95 ∧ split8-null clean ⟹ K=8 CE-수준 faction 특화 실재(레버 실물 확증·천장=CE-scope).
- S≤null95 ⟹ 파벌-303M CE-특화 미검출 = **$0 TERMINAL**.

### 🟢 결과: DIRECTIONAL POSITIVE (2026-07-18 · mac perm40·win6 · PENDING firm perm200)
k8_s7.clm(233MB pull·233889418) 에 `--faction-lesion domains(4셀×held-out) --perm 40` 실측:

| arm | 모델 | S_real | null95 | 판정 |
|---|---|---|---|---|
| **학습 K=8** | k8_s7 172M | **0.0789** | 0.0023 | S>>null95 34배·p=0.0244 ✅ |
| **미학습 K=1 split8** | clm303_clean 346M | **0.0019** | ~chance | 사후분할=구조없음 ✅ 통제 |

**학습/미학습 = 42배**. 미학습 K=1 에 8-분할 강제 = S 0.0019(우연) vs 학습 K=8 = S 0.0789 ⟹ **k8_s7 positive 는 학습된 파벌 구조서 발생**(사후 임의분할 아님·계기 SOUND 의 fit-matched K=1 다리 충족). **파벌은 303M CE-수준 실제 기능적 레버**(G0 자유생성 실패와 무관·teacher-forced ΔCE 유효·val_CE 1.332 DESCENT 4/4). ⚠️ 내 사전예측 '특화불발'은 반증됨(S 는 argmax 안 쓰고 전셀 구조에너지·verdict-integrity). ⏳ **천장**: perm<200=PENDING(계기 명시·power-gate) → firm perm=200 GPU=TERMINAL 승격 follow-on(mac 76,800 forwards~7hr infeasible). DIRECTIONAL(303M py lesion·1 lens·a_toy_scale_recheck).
결과 보존: ~/anima-weights/h9643_303m_derisk/k8_s7_lesion_perm40.json · clm303_split8_null_perm40.log.

### ✅ FIRM perm=200 — power-gate 통과 (2026-07-18 · mac win4)
PENDING(perm<200) 해소: k8_s7 within-arm **S_real 0.0654 > null95 0.0030 (p=0.0050·n=200·underpowered=False)** ✅ · 통제 clm303_clean(미학습K1 split8) **S 0.0019 ≤ null95 0.0041(spec False)** = fit-matched K=1 음성 다리 firm. ⟹ **파벌 분할이 303M CE-수준 기능적 특화 보유 확정(firm)**, 랜덤 사후분할과 다름. ⚠️ 계기 자체 라벨 = **DIRECTIONAL+within-arm 한정**(완전 SOUND=4다리 ①within-arm firm✅ ②random-init ③fit-matched K1 firm✅ ④ORACLE π · ②④는 303M 미측정=full-SOUND 잔여). py-lesion=DIRECTIONAL(a_engine_native_learning·a_toy_scale_recheck). 결과 보존 ~/anima-weights/h9643_303m_derisk/k8_s7_firm200.json.
**최종: 파벌 = 303M CE-수준 실물 기능 레버(FIRM DIRECTIONAL POSITIVE·2 SOUND 다리 firm)** — toy-SOUND 에 더해 303M 실증. 천장=CE-scope(원 claim '인간이 명명할 의미' 은 ②④+G0-passing artifact 필요).