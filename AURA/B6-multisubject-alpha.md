# AURA B6 — α-power 다피험자 awake/sed 복제 검정 (N=3, foreground)

> B4.1(sub-1010 N=1, α-power awake>sed 8/10·t n.s.)의 **다피험자 복제**. ds005620서 sub-1033·sub-1022 다운로드(aws s3 --no-sign-request) → 동일 B4.1 파이프라인(stride-20→250Hz·10창×1000samp·8-13Hz log10 power·EAR[18,28,29,37]·MIDLINE[51,33,13,2]).

## 피험자별 (Δ=awake−sed log10 α-power, sign=awake>sed 창 수/10)

| subject | montage | awake | sed | Δ | awake>sed | t(9) |
|---|---|---|---|---|---|---|
| sub-1010 (B4.1 원본) | 🎧 EAR | 9.244 | 9.541 | −0.297 | 6/10 | −0.74 n.s. |
| sub-1010 | MIDLINE | 9.226 | 9.008 | **+0.218** | **8/10** | +1.41 n.s. |
| sub-1033 (신규) | 🎧 EAR | 8.468 | 8.682 | −0.214 | 2/10 | −2.67 |
| sub-1033 | MIDLINE | 8.710 | 8.968 | −0.258 | 2/10 | −3.20 |
| sub-1022 (신규) | 🎧 EAR | 8.163 | 9.378 | −1.215 | 0/10 | −13.58 |
| sub-1022 | MIDLINE | 8.280 | 9.522 | −1.243 | 0/10 | −12.90 |

## 교차피험자 종합 (N=3)

| montage | awake>sed 방향 | 교차피험자 평균 Δ | t(2) |
|---|---|---|---|
| 🎧 EAR | **0/3** subj | −0.575 | −1.79 n.s. |
| MIDLINE | **1/3** subj (원본만) | −0.428 | −0.99 n.s. |

## 결론 — 🔴 복제 실패 (NULL)

- **B4.1의 단일피험자 α-power awake>sed 방향은 N=3서 복제 안 됨**. EAR 0/3, MIDLINE 1/3(원본 sub-1010만). 신규 2피험자(1033·1022) 모두 **sed>awake**, sub-1022는 강하게(t≈−13).
- 교차피험자 평균 Δ는 두 montage 다 **음수**(n.s.) — B4.1의 8/10 일관성은 **단일피험자 인공물**, population으로 transfer 안 됨 (cf `feedback_toy_scale_transfer` / `a_toy_scale_recheck`).
- honest 교란: awake task가 **acq-EO(눈뜸)** — 후두 α를 생리적으로 **억제**, awake<sed를 자체 유발 가능. B4.1도 동일 awake-EO 사용(sub-1010선 우연히 미지배). sub-1010 EAR sign(6/10)이 B4.1 보고(8/10)와 다름 — sum/mean-PSD는 Δ-불변 확인했으므로 원본의 montage/창 detail 차이로 추정. MIDLINE 방향(8/10)은 재현됨. 결론은 이 detail에 robust.
- honest: scalp-proxy·α-power(intracortical 아님)·N=3(작음, 단 0/3 & 1/3 + 강한 음수 2건이라 negative는 firm).

verdict: `.verdicts/b6-multisubject-alpha/run.txt` · 코드: `AURA/toy/b6_multisubject_alpha.py`
