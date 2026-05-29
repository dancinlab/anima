# AURA B7 — intracortical 본질 한계 (도메인 terminal boundary)

> relocate-N1 명제의 결정적 답은 **scalp/혈관내 proxy로 영원히 못 닫는다**. 이 한계를 "done"이 아닌 **물리/윤리적 ceiling**으로 기록 (feedback-closure-is-physical-limit · a_paper_negative_ok).

## 우리가 쥔 데이터의 천장

```
측정 가능(우리)              측정 불가(본질 gap)
─────────────────────────   ──────────────────────
scalp EEG (B1·A8.1·B6)       intracortical 단일뉴런/LFP
혈관내 ECoG급 (B3 Synchron)   relocate된 실제 N1 전극 신호
구조 모델 (A6/A7/A8.4/A9.3)   심부핵 직접 자극 반응
        ↑                              ↑
   proxy·structure              실제 칩 위치 효과
```

- **proxy 측정**(scalp/혈관내)으로 얻은 것: 위치효과 null(A10.1)·상태 null(B2/B4.2)·다피험자 α null(B6)·귀뒤≡피질 분포평균(B1)·3위치 침습 비대칭(B3).
- **proxy로 못 얻는 것**: "실제 N1을 M1→DLPFC로 옮기면 전뇌 통제가 되나"의 **직접 인과**. scalp big-Φ가 null이어도 intracortical에선 다를 수 있음(공간해상도·심부 접근이 근본적으로 다른 측정).

## 왜 닫을 수 없나 (3 본질 장벽)

| 장벽 | 내용 | 우회 가능? |
|---|---|---|
| 공간해상도 | scalp ~cm · 혈관내 ~mm · intracortical ~µm(단일뉴런) — 통합정보 분해능 자체가 다름 | ❌ 물리 |
| 심부 접근 | proxy는 피질 표면/혈관 only · VTA/LC/raphe 직접신호 0 | ❌ 물리(B3 혈관내도 표면) |
| 인과 vs 상관 | proxy는 관찰만 · "위치 바꿔 자극→효과"는 침습 자극 필요 | ❌ 윤리(인체 침습 실험) |

→ 남은 답은 **동물 침습 실측**(optogenetic/microdialysis, brainwire n1-deep-access가 제안한 NHP 검증) 또는 **임상 N1/Utah 환자 데이터**(규제+IRB)에서만. 우리 lane(로컬 EEG/구조모델) 위에 있는 물리·윤리 frontier.

## 도메인 종결 자세 (terminal boundary, NOT 100%)

AURA는 **proxy+구조 모델로 답할 수 있는 부분은 다 답했다**:
- 🟢 비침습 귀뒤가 피질과 동등 통합정보(B1) · 🩸 혈관내가 ECoG급(B3) · 🔴 단일창 big-Φ 위치·상태·다피험자 전부 null
- 구조모델↔실측 **비대칭**(이론은 투사허브 우월, 실 scalp는 무차별)이 핵심 정직 발견.

남은 frontier는 **본질 한계 위**(intracortical 침습): "done"이 아니라 **여기까지가 proxy의 ceiling**. negative-result paper(a_paper_negative_ok)의 정직한 scope 경계가 바로 이 선.

## 다음(한계 위 — 우리 lane 밖)
- 동물 침습(NHP optogenetic DLPFC→VTA, brainwire H4 가설) — 실험실/펀딩
- 임상 N1/Stentrode 환자 raw — 규제/제휴
- negative paper: "scalp/혈관내 proxy로 relocate-N1 위치효과 미검출 + 구조↔실측 비대칭 + intracortical ceiling" (a_paper_only_at_closure: proxy-scope는 이제 닫힘, intracortical은 명시적 out-of-scope)
