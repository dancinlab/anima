# bench 결과 종합 (2026-03-29)

## 256c 결과

```
Strategy      Φ(IIT)   Φ(proxy)  CE end
──────────────────────────────────────
frozen         14.70     0.00     6.37   ← Φ(IIT) 🏆
alternating    14.44     0.00     4.50
baseline       10.98     3.47     5.33
v7             10.79     4.57     4.29   ← CE 🏆
```

## 512c 결과

```
Strategy      Φ(IIT)   Φ(proxy)  CE end
──────────────────────────────────────
baseline       14.04     0.05     5.63   ← Φ(IIT) 🏆 + CE 🏆
frozen         13.67     0.00     9.71
v7             13.06     0.64     5.79
alternating    12.80     0.00     8.21
```

## Φ(IIT) 스케일링 (phi-only)

```
Φ(IIT)
 |
31 ┤         ★ 32c (peak!)
   |
19 ┤       ★ 16c
   |
15 ┤                 ★ 512c
13 ┤             ★ ★ 256c
12 ┤           ★ 64c  128c
   |
 8 ┤     ★ 8c
   |
 3 ┤ ★ 4c
   └──────────────────→ cells
     4  8  16 32 64 128 256 512

Peak: 32c (Φ=30.89)
→ Φ(IIT)는 32c에서 최대, 이후 감소!
→ cells 늘려도 IIT Φ가 안 오름
```

## 핵심 발견

<!-- [Hc_059 bench-v2-law-55-56-scale — moved to hypotheses_candidates/Hc_059_bench_v2_law_55_56_scale.md on 2026-05-11] -->
