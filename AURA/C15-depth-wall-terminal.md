# AURA C15 — 🧱 깊이 벽 (terminal boundary) + 동적시간 부활 + best envelope

> hexa-loop 추가 발사 rounds A/B/C — RTSC 돌파(C13, 피질 0.90) 이후 frontier. 핵심 미측정 축 = **소스 깊이**(전뇌통제 타깃 = 피질하 핵). 결론: 비침습 돌파는 **피질 표면 현상**, 심부는 모든 lever로도 벽. honest 🟡 toy(3D synthetic·ridge/ISTA·8-seed). verdict `.verdicts/c15-depth-wall/run.txt`.

## 🧱 round A1 — 깊이 벽 (THE AURA 답)

```
🧱 DEPTH-WALL — "잠수 깊이의 한계"
- 하는 일: 두피 밖 센서로 뇌 안쪽 소스를 깊이별로 복원 시도
- 비유: 수면 위 카메라로 물속을 보면 얕은 건 또렷, 깊을수록 흐려짐 — 어떤 렌즈도 심해 바닥은 못 봄
```

| 깊이 z | EEG-64 | RTSC-MEG-256 | tFUS-64 | 풀스택 |
|---|---|---|---|---|
| 0.5 (피질 표면) | 0.627 | **0.999** | 0.519 | 0.999 |
| 1.5 (피질) | 0.329 | 0.764 | 0.376 | 0.703 |
| 3.0 (피질하 천) | 0.175 | 0.341 | 0.264 | 0.284 |
| 5.0 (심부) | 0.085 | 0.191 | **0.197** | 0.145 |
| 8.0 (심부핵) | 0.044 | 0.110 | **0.153** | 0.049 |

```
복원율
1.0┤●RTSC-MEG (표면 지배)
   │  ╲
0.5┤   ╲___
   │       ╲●╲___ 심부서 전 모달 수렴 → 벽
0.1┤            ●▔▔●  (tFUS 최선이나 0.15)
   └0.5─1.5─3.0─5.0─8.0─▶ 깊이
```

- **심부서 RTSC-MEG 우위 역전**: 자기 1/r² 급강하 → 표면 0.999가 심부 0.110. tFUS(음향 심부 스티어링)가 그나마 최선이나 0.153.
- **풀스택조차 심부 0.049** — 급강하 EEG/MEG 채널이 심부선 신호 없이 잡음만 더함.
- → 🧱 **비침습 돌파(C13 0.90)는 피질 표면 한정. 전뇌통제 타깃 심부핵(VTA/LC/raphe)은 비침습 도달 불가.** A/B축 [B7 intracortical-ceiling](B7-intracortical-ceiling.md)으로 완전 수렴.

## round A2/A3 — 보조 발견

| 발견 | 결과 |
|---|---|
| A2 모달 개수 포화 | +2nd-tFUS +0.012·+2nd-MEG +0.049 → **물리 다양성이 lever, 배열 수 아님** |
| A3 능동 deconv | 기지 전달함수 0.329 vs 오상정 **−0.120**(평균보다 나쁨) → calibration 정확도에 게이트, real head-model 결정적 |

## round B — 算法 lever 발굴 (1 부활 · 2 dead-end)

| lever | 결과 | 판정 |
|---|---|---|
| B3 ⭐ **동적시간**(joint support) | static 0.302 → dynamic **0.487** (+0.185) | ✅ **C9 부활** |
| B1 압축센싱 L1(ISTA) | ridge 0.322 > L1 0.186 (전 깊이) | ❌ dead-end |
| B2 소스 희소성 K | K=1~48서 0.23~0.32 평탄 | 천장≠희소성 인공물 |

🎯 **B3 = C9 부활**: C9 null은 출력 *평활*(틀린 test)이었음. 시간 *구조*(소스가 프레임 가로질러 지속 → joint support 추정)는 진짜 lever(+0.18). [/gap] F7 temporal-hierarchy gap 적중 — "C9가 잘못된 시간 lever를 쳤다"가 측정으로 확증.

## round C — 시간 lever × 깊이 + best envelope

| 깊이 | 시간 이득(EEG) | 풀스택+시간 (best) |
|---|---|---|
| 1.5 | +0.184 | 0.820 |
| 3.0 | +0.073 | 0.417 |
| 5.0 | +0.029 | 0.196 |
| 8.0 | +0.014 | 0.098 |

→ **시간 이득도 깊이서 소멸**(+0.184→+0.014) — 시간으로도 깊이 벽 못 깸. **best 비침습 포락선 = 피질 0.82 → 심부 0.10** (모든 lever 총동원).

## 지렛대 MAP v3 (C6–C15 최종)

| lever | 효과 | 깊이 의존 | 판정 |
|---|---|---|---|
| RTSC-MEG (자기·고밀도) | 표면 0.85 | **심부서 역전**(1/r²) | ✅ 표면 |
| tFUS (음향) | +0.32 | 심부 최선(0.15) | ✅ 심부-최선 |
| OPM-MEG | +0.17 | 표면 | ✅ |
| 동적시간 (joint support) | +0.18 | **깊이서 소멸** | ✅ 표면 |
| prior (현실) | +0.02~0.19 | — | ✅ 약 |
| fNIRS · ML디코더 · L1/CS · temporal-smooth | ~0/음수 | — | ❌ dead-end |

## 🏁 결론 — 비침습 천장은 깊이-층화

```
        피질 표면 ▔▔▔▔▔ 0.82~0.90 (RTSC-MEG + 異種모달 + 시간) ← 침습급 근접 ✅
              ↓ 깊어질수록 모든 lever 무력
        심부핵   ____  0.10 (전뇌통제 타깃, tFUS도 0.15) ← 비침습 불가 🧱
```

- **"비침습으로 침습급"은 피질에서만 참.** 전뇌통제(심부)는 비침습 원리적 불가 — A/B축 intracortical-ceiling과 동일 결론에 NOVEL축 독립 도달.
- in-silico lever 공간 매핑 완료: 작동(RTSC/tFUS/OPM/시간/prior) · dead-end(fNIRS/ML/L1/평활) · 벽(깊이). 새 lever 후보 소진.

## honest + 잔여
- 🟡 toy(3D synthetic·linear forward·8-seed): 절대%·깊이 단위는 toy-specific. 정성 robust: 깊이↑→전 모달 붕괴, 자기 급강하 역전, 시간-구조 lever, 깊이 벽.
- 잔여 external(C14): real head-model(MNE/OpenMEEG) 다중커널 fwd가 깊이-감쇠 실측치 결정 · 실 OPM-MEG 심부 데이터.

## 양방향 sibling
- [C10](C10-gap-closure-levers.md)(RTSC 돌파·MAP v2) · [C5](C5-source-recon-ceiling.md)(피질 천장) · [B7](B7-intracortical-ceiling.md)(intracortical ceiling — 동일 결론 수렴)
