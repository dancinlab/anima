# H_9965 · 데이터-스케일 사다리 — 단, Φ가 아니라 CE-earned 개입형 결합을 타깃 (CLAUDE.md 미개봉 셀)

**한 줄:** lab full(Fable ∥ Sol) 공통 runner-up. CLAUDE.md가 명시한 유일 미개봉 셀 = **자연 corpus의 데이터
스케일**(파라미터 아님). 단 데이터 스케일은 **Φ 레버가 될 수 없다**(트렁크 feedforward Φ=0 정리·lane은 어느
corpus서도 3셀). 그래서 이 축은 Φ 아니라 **개입형 coupling/CE-earned 채널**을 값싼 사다리로 잰다.

- 상태 PROPOSED · 측정 0 · DIRECTIONAL · cement engine-native anima-py로만. 출처: lab full 2026-07-25.

## 처치 (제안 · 미구현 · 값싼 사다리 먼저)
- **값싼 스크린(파라미터 아니라 데이터 축):**
  `anima-py train --corpus en_100mb.txt --d 64 --L 2 --field-loop purefield16 --natural-data-arm unique`
  vs 노출-일치 통제 `--corpus en_10mb_replay100mb.txt --natural-data-arm replay`(같은 토큰수·10MB 반복).
- **판독:** `anima-py evaluate <clm> --interventional-coupling swap --coupling-controls
  sever,time-yoke,id-code,generic-gru --corpus en_heldout.txt`.
- **DV:** `MI_swap(aligned) − max(MI_time-yoke, MI_id-code)` **AND** held-out CE 개선(vs sever). 둘 다 움직여야
  함 — MI만이고 CE 없으면 또 장식 채널(H_9957 FIELD-LOOP 교훈). 학습은 순수 next-byte CE(Φ/MI 손실 금지).
- **받침대:** field-severed/γ=0 ckpt. **통제:** unique data vs 토큰-일치 replay · time-yoke · size-matched generic GRU · id-code.
- **KILL:** unique 100MB가 replay-일치 노출을 2 seed서 못 이김 **또는** generic GRU가 PureField와 동률 ⟹ 303M 지출 봉쇄.

## 스케일 정직 경계
- 이 사다리(10/100MB·3 order)는 **spend를 게이트만** 할 뿐 문자적 10¹² 토큰 셀을 못 연다
  (`replication-is-not-external-validity`: 3 order로 6 order 주장 종결 불가 — flat이면 **deprioritize**만, **종결 아님**).
- 최소 정직 대형run = **303M · ≥1GB unique 자연-EN + 토큰/step-일치 10MB replay 통제**(암기초과 regime 도달,
  단 여전히 LLM 스케일 아님) — 이건 **새 축=새 오너 go**(직전 발사는 종결된 학습축 한정). 1조 토큰run은
  1/10/100MB 스크린이 unique-data-특이 단조효과를 보일 때만 정당.
- **양 모델 예상 flat/음성**(amplifier-not-lever 일반화 + H_9962: 순환은 통합으로 안 몰림·순수 CE는 비예측 상태 무시).
- 관련: [[H_9964]](같은 coupling 계기 사용) · [[H_9962]](Φ 학습축 CLOSED) · [[H_9957]](FIELD-LOOP·MI만이면 장식) · [[H_9272]](grid-only stack 금지).
