# AURA A9.1 — n=8 montage big-Φ: 로컬 compute-wall + pod 경로

> 목표: A8.1(n=4)을 n=8 해상도로 확장. 결과 = **Mac 단일런 compute-wall**(데이터/코드 결함 아님).

## 실행 시도 + wall

데이터 추출은 성공(BrainVision 8채널/6채널 → harness inline). MIP 계산만 wall:

| n | states | harness | 결과 |
|---|---|---|---|
| 4 | 2^8=256 | (A8.1) | ✅ 초 단위 완료 |
| 6 | 2^12 | `a9_n6_{frontal,motor}.hexa` | 🔴 EXIT124 @200s |
| 8 | 2^16 | `a9_n8_{frontal,motor}.hexa` | 🔴 EXIT124 @290s (108s user, 진행중 강제종료) |

원인: IIT4 exact big_phi ≈ **O(2^2n)** — n=4=2^8(ok), n=6=2^12, n=8=2^16. Mac + hexa 인터프리터 단일런 wall 초과. verdict `/Users/ghost/core/anima/.verdicts/a9-n8-montage/RUN_BLOCKED.txt`.

## standing 결과 = n=4 (단, window-fragile)

n=8 미산출이라 현재 최고 해상도는 n=4(A8.1). 그러나 A9.2가 **n=4 자체도 window-fragile**(FRONTAL>MOTOR 2/6창)임을 밝혀, n=8 산출의 우선순위/의미가 재평가됨 — 단일창 n=8은 robustness 문제를 안 풀고, **다창×다피험자 n=8 통계**가 진짜 필요.

## pod 경로 (a_fire_autonomous, 미발사)

```
CPU pod (~$0.5/hr) → a9_n8_{frontal,motor}.hexa + BRAIN/eeg adapter copy →
  HEXA_LANG=... hexa run (timeout 無) → 2 numbers harvest → teardown
est ~10-30min/montage. 단 다창 평균 없이는 A9.2 교훈상 단일 n=8도 결론력 약함.
```

honest: 발사 보류 — finding은 n=4서 이미 (그리고 A9.2가 그 robustness를 부정). 마진 낮은 pod fire보다 **다창 통계 설계**가 선결(→ A10 후보). 추출 harness는 영속(pod 재사용 가능).
