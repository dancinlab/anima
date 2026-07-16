# H_9557 — 문맥-다리 RF 인구조사 — In-Context Bridge · RF Census (fable A-F1 · R2-measure · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R2-measure lane · 사전등록) — source=fable A-F1
**lane:** BINDING / two-lane · 추론시 문맥-다리 (쓰기 0)
**related:** [[H_9359]] · [[H_9358]] · [[H_9346]] · [[H_9327]] · source: lab full R2-measure (fable A-F1)

## 제안 (Fable Lane-A 수렴안 · R2)
**아이디어**: 두-lane 벽 = 연산자↔선언 저장소 **런타임 다리 부재**(H_9359 확정). C3/C5 는 전부 *저장소*에 CPT 로 **썼다**. 미탐 = CONV byte-LM 이 확실히 소비하는 **유일 런타임 입력 = 자기 문맥 바이트**를 다리로 쓰기 — **쓰기 0**. 선언 사실을 연산자 질의의 *추론 문맥*에 넣고, 연산자 답이 문맥 극성을 따라가나 본다.
**메커니즘 (신규 플래그 불요)**: 기존 terminal 경로 `anima-py evaluate <clm> --xbind m.json`. nbind-eval-v1 매니페스트의 free-text `seed` 필드에 `seed = <문맥 문장> + 구분자 + not{stem} 질의`. arm/stem: (a) 참 선언 문맥 · (b) 극성-FLIP 선언 · (c) 무관-stem 선언(복사편향 통제) · (d) 연산자 템플릿-클래스로 쓴 선언(주소모형 arm). 각 byte offset D ∈ {RF 내부 · ≈RF · ≫RF}. 판독 = flip-tracking.
**$0 pre-screen**: (i) RF 산술 — evaluate scorer `win`(기존 매니페스트 64)이 RF 또는 최소 packing 밑이면 **INSTRUMENT-DEAD** at 구성(win 수정 or KILL). (ii) C3 잔차 재분석 → [[H_9560]].
**사전등록 판정표(요지)**: C0 양성통제(선언-표면 질의 flip-track ≥0.75) 미달⟹**INVALID**(연산자 셀 읽지 말 것 · anima-v2 V2_1 교훈). PASS = 연산자 flip-track(a vs b) ≥0.75·p<.01·D≤RF ∧ D≫RF 서 우연 CI 로 감쇠 ∧ (c) 우연. KILL = C0 통과인데 전 D 우연 = read-path-general 음성(정직 등록). ANOMALY = D≫RF 서도 추적 ⟹ CONV-RF 모형 자체 오류.
**통제 ≥2**: (c) 무관-stem + D≫RF arm + C0 양성통제. EN ⟹ SCREENER/DIRECTIONAL.
**p7/p8**: 진리점수 없음(flip-track 이진). 재조합 여전 🧱 가정 안 함.
**verdict-integrity**: 함정 = flip-track 을 '다리'로 오독(실은 byte-copy/recency) → (c) 무관-문맥이 답 움직이면 복사편향 INVALID + D-감쇠 서명 요구로 선차단.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. monitor-only/게이트-벽 회피. 측정 주장 0(설계). **distinct-from-kills:** 가장 가까운 kill = H_9327 flip1·C5 담체-쓰기 — 둘 다 *쓰기 후* weight-store 경로. 이건 쓰기 0, CONV 가 확실히 소비하는 문맥바이트를 시험(어떤 arm 도 안 건드린 소스).
