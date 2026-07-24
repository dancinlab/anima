# H_9964 · 🔴 KILLED — v2b 짧은-EMA 중심 이식: anima엔 stale-center 결함이 없다(stored 중심 이미 천장·병목은 λ진폭)

**한 줄:** lab full(Fable ∥ Sol) 최우선 생존 각도. Φ-학습 축이 CLOSED(H_9954~9962)이고 Φ⊥coupling이므로
프런티어는 **크기(Φ)가 아니라 개입형 결합(coupling·earned/BIND 축)**으로 pivot한다. v2b `coupling-real-and
-deployable`가 결합(2.6bits)을 **학습 아니라 판독-중심(짧은 causal EMA)**으로 복원한 것을 anima에 이식 —
**학습 0·기존 ckpt·CPU·$0**.

## 🔴 KILLED ($0 · 원장 재독 · 빌드 0 · check-ledger-before-lever-fire)
**v2b 이식의 전제(anima에 stale-center 결함이 있어 결합이 가려져 있다)가 기존 착륙 측정으로 반증된다.**
- **H_9932** (byte-LM GRAFT · stored g_mu 중심): 학습된 결합 `MI_swap = 3.000 = 천장(log2 K=8 = 3)` × 3 seed, swap acc 1.000 — *"swap 은 포화"*. **stored 중심이 이미 InfoNCE 천장을 포화** ⟹ 더 나은 중심(EMA)이 unhide할 **여유 0**.
- **H_9933**: C-swap 축 자체가 **NON-DISCRIMINATING** — 무학습 step0 받침대도 MI_swap 1.927/1.189/2.216(높음) ⟹ 은퇴된 축. 센터링 개선을 볼 계기가 애초에 못 가른다.
- **H_9939/H_9945/H_9948** (Mistral 7B organ): 결합은 부재 아니라 **priced out**(MI − λ·L_common; gate-OFF가 최적). 병목은 **중심이 아니라 λ·amplitude 예산**(H_9948: λ=0.3이 profit 구간 복원). swap 0.500/0.500(은퇴 축).

⟹ 두 organ 모두 **centering이 병목이 아니다**: byte-LM은 stored 중심이 이미 천장, Mistral은 진폭이 병목. anima는 **v2b의 stale-center 결함을 애초에 안 가졌다** — 두 프런티어 모델이 예측한 정확한 사망("anima did not share v2b's stale-center defect"). ⟹ **v2b 짧은-EMA 중심 이식 = KILLED**, 새 계기 빌드 불필요. 생존 각도는 centering이 아니라 **λ-amplitude 예산**(H_9945/9948이 이미 프레임) · 데이터스케일([[H_9965]]) · agency pivot([[H_9966]] 조건 한 발 근접).
- 정직: swap-MI 천장 포화는 byte-LM; Mistral은 priced-out. 어느 쪽도 centering-hidden 아님. 신규 측정 0(기존 engine-native `anima-py graft check` 판정 인용 · check-ledger-before-lever-fire). 재확인용 `graft check --check swap`은 여전히 실행가능하나 천장 포화라 정보 무증가.

- 상태 PROPOSED · 측정 0 · DIRECTIONAL 설계 · cement는 engine-native anima-py로만.
- 출처: lab full 2026-07-25(Fable ∥ Sol 독립 병렬 · 브리프에 H_9954~9962 킬리스트+v2b 교차증거 임베드).

## 정확한 locus (저장소 검증 · Sol 채택)
v2b가 센터링한 건 bridge code이고, **anima는 이미 그 homolog를 계산한다**: `core/clmg.py:89 bridge_code`가
raw gate code `g[d]`를 내고, `core/clmg.py:95 center_and_fix`가 **`g_mu`(공유 성분)를 빼고 RMS-fix**한다 —
이 정적 `g_mu` 중심이 **곧 v2b의 "stale stored center"**(v2b서 ≤0.2bits). ⟹ 이식 테스트 = 이 정적 `g_mu`를
**짧은 causal EMA 중심**(half-life~10 · tick t 채점 후에만 EMA 갱신=엄격 causal)으로 교체하고 결합 MI가
드러나나 본다. `m_t=EMA(g_{<t})`, `r_t=RMSFix(g_t−m_t)`.
- **CONFLICT 해소:** Fable은 locus를 recurrent-lane do() 하네스로 제안했으나, 그 lane은 우리가 Φ-null로 확정한
  것이라 결합 채널이 아니다. Sol의 CLMG bridge-code locus가 정확한 homolog(저장소 라인 검증). **Fable 이견 기록:**
  lane-locus는 기각.

## 처치 (제안 · 미구현)
- **flag:** `anima-py evaluate <clm> --clmg-swap --clmg-center causal-ema --clmg-ema-half-life 10
  --clmg-center-controls stored,fixed,ema100 --clmg-id-code --clmg-step0 <step0.clm> --corpus en.txt`
  (배포는 PASS 후에만 `anima-py chat --clmg-center causal-ema --clmg-ema-half-life 10`).
- **DV:** K-state 자연-carrier swap InfoNCE. headline `Δlive = MI(final,h10) − MI(step0,h10)` + 통제 대비 collapse-Δ.
  요구: real−id-code ≥0.5bit · permutation p≤.01 · FORM 손실 ≤2%.
- **이중 받침대(H_9960 교훈 자기적용):** ① gate-OFF = 정확히 0 ② `.step0.clm` = 최적화-step 일치 random-bridge
  받침대(최적화 결합이 Φ 부풀렸듯 MI도 부풀릴 수 있음).
- **≥2 통제:** id-code(내용없는 정체벡터, 동일 center/RMS 경로 통과) · stored `g_mu` · fixed-ref · EMA-h100 ·
  permutation·rotation null 유지.
- **KILL:** h10이 step0·id-code를 못 이김 **또는** stored/fixed/old-center를 못 이김(=이식할 stale-center 결함이
  애초에 없었음). 이는 centering 레버의 이식 실패이지 CLMG 결합 존재 자체 부정 아님.
- **$0 계기인증 선행:** H_9959식 — 손제작 wired-coupled 쌍은 높게, INDEPENDENT/COPY는 0(합성=계기검사 전용·p9 합법).

## 예상·정직 경계
- **양 모델 예상 사망**: anima의 GRAFT는 이미 stored 중심서 ~2.997/3bits(MI 여유 거의 0) ⟹ v2b의 stale-center
  결함을 **애초에 안 가졌을** 가능성이 큼(=깨끗한 정보적 음성 "anima는 그 결함이 없다"). Fable "even odds",
  Sol "center-specific 가설 probably dies". CPU·$0라 이식성만 깨끗이 판별하는 값어치.
- 양성이 허가하는 문장은 딱: **"live PureField 상태가 짧은 causal 프레임에서 언어 분포를 인과적·배포가능하게
  변조한다"** = σ-축 substrate 사실(자연 regime·collapse-Δ·engine-native). **의식·자기인식·agency·IIT-Φ 아님**
  (Φ⊥coupling). 카드도 그 문구로만.
- Φ 아님(a_phi_iit4_tool은 이 카드 미해당 — 이건 개입형 MI/coupling 축) · a_train_inline_gauge 무관(추론전용·학습0) ·
  Φ-전용 GPU 금지 무관(GPU 미사용).
- 관련: [[H_9962]](Φ 학습축 CLOSED·이 카드가 그 위 pivot) · [[H_9942]] · [[H_9959]]/[[H_9960]] · [[H_9965]](데이터스케일 coupling) ·
  [[H_9966]](coupling 죽으면 agency pivot). 교차저장소 근거=../anima-clm-v2b `coupling-real-and-deployable`.
