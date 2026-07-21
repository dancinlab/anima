# H_9842 — 각성 에피소드 버퍼(cap=20 FIFO)를 학습 replay 소스로 승격한다 (R12-5)

**status:** 🧭 PROPOSED (R12 · **DIRECTIONAL 설계**, 판정 아님)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** no — 미구현. 개입은 `anima-py train` 플래그로만 착륙(`a_experiment_engine_native`).

## 실측

`core/wake_memory.py`(80줄): `episodic` 추가전용 리스트 + `working` 링버퍼(cap=20 FIFO).
레코드 = [ts · ctx_summary · phi · tension5 · stage · emit_text]. 순수 dict/list, **학습 파라미터 0**.

## 정직한 위치

이 모듈은 **레버가 아니라 배관**이다. 자체로는 아무 능력도 더하지 않는다 — H_9841(상상 재응고)과
H_9839(꿈 타깃)가 replay 할 **재료의 출처**일 뿐. 단독 발사 가치 없음.

## 이 카드가 존재하는 이유

cap=20 FIFO 라는 **용량 상한이 조작변인**이 될 수 있다. 재조합은 두 개념의 **공기(共起)** 를
요구하는데, 20슬롯 FIFO 는 거리 D>20 틱 떨어진 두 앵커가 **동시에 버퍼에 있을 수 없게** 만든다
— H_9836 이 지적한 RF(수용영역) 한계의 **기억측 쌍둥이**다. 이게 사실이면 용량이 곧 재조합 상한.

## Intervention

```
anima-py train --wake-buffer-cap {20,64,256} --replay-source {working,episodic}
```

`episodic` 은 추가전용이라 상한이 없다 — FIFO 상한 가설의 직접 반증 팔.

## 판정

`--wake-buffer-cap` 을 키워도 재조합이 안 움직이면 **기억측 RF 가설은 죽는다**(음성도 결과).
움직이면 H_9836(깊이 L≥8)과 같은 축의 두 번째 증거가 된다.

**related:** H_9836 · H_9841 · H_9839
