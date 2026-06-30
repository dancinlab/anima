# AURA C6 — 🎯 hexa-loop 돌파: 두개골 LPF 천장은 "다른 transfer 모달"로 깬다

> /hexa-loop discover→verify→absorb 1회전. C5가 EEG-단독 천장(~28%)을 정량했고, C6은 **그 천장을 무엇이 깨나**를 in-silico로 발굴. honest: toy(ubu-1 numpy seed42).

## DISCOVER (돌파 후보 랭킹)

| 후보 | 가설 | 검증성 |
|---|---|---|
| ⭐ 다중모달 융합 | 두개골 LPF 우회 = 다른 transfer 모달 추가 | in-silico ✅ |
| prior-injection inverse | 개인 MRI fwd model로 ill-posed→well-posed | toy 미구현(C7) |
| temporal super-res | 공간 막혀도 시간(ms)으로 보완 | toy 미구현(C7) |
| 능동 deconvolution | 두개골 transfer fn 측정→역필터 | LPF는 정보소실이라 역필터 한계 |

## VERIFY (다중모달 융합 in-silico) 🟡

C5 EEG-단독(blur σ0.5) baseline에 모달 추가, 복원 R²:

| 융합 | R² | Δ |
|---|---|---|
| EEG-only (C5) | 0.243 | — |
| +fNIRS (σ0.7, 같은 두개골 blur) | 0.245 | **+0.002** |
| +tFUS (σ0.22, 초음파 sharp) | **0.482** | **+0.239** |

```
복원율 R²
0.48┤              ███ +tFUS (두개골 전기-LPF 우회)
0.24┤ ███ ███          ← EEG·EEG+fNIRS (같은 blur=중복, 천장)
    └─EEG─+fNIRS─+tFUS─▶
      같은 모달 더 쌓기 ✗   ·   다른 transfer 모달 ✓
```

## 돌파 명제 (verified)

🎯 **두개골 전기-LPF 천장(28%)은 EEG 강화로 못 깬다 — "다른 물리 transfer를 가진 비침습 모달"로 깬다.**

- **fNIRS 추가 = 무의미**(Δ+0.002): fNIRS도 두개골 통과 시 공간 blur(σ0.7) → EEG와 **같은 LPF 한계** → 중복 정보. C2의 "센서 융합(법3)"이 순진하면 효과 없음을 정량.
- **tFUS 추가 = 천장 돌파**(Δ+0.239, 28→48%): 집속초음파는 **음향**(전기 아님)이라 두개골을 **mm 해상도로 통과** → EEG가 못 받는 고공간주파 회수. 두개골 *전기*-LPF를 물리적으로 우회.
- → **"비침습으로 침습급"의 진짜 지렛대 = EEG 더 좋게가 아니라, 두개골 전기-LPF를 우회하는 sharp 비침습 모달(tFUS/fUS) 융합.** C2/C3의 5법(전부 전기 EEG계)이 천장에 막힌 이유 = 모두 같은 전기-두개골 채널.

## C-축 재정렬 (C6 돌파 반영)

```
기존 5법(전기 EEG계) ──천장 28%(C5)── 같은 LPF
              +
다른 transfer 모달(tFUS 음향) ──돌파 48%(C6)── LPF 우회
              ↓
NOVEL goal 갱신: 비침습 침습급 = "전기+음향(+혈류) 이종모달 융합"
```

## honest
- 🟡 toy(1D-ring·synthetic·ridge): 절대 48%는 toy-specific. **정성 발견 robust**: 같은-blur 모달=중복, 다른-transfer 모달=천장돌파(정보이론 일반).
- ⚠ 실제 tFUS: 주로 *자극* 모달이고 성인 두개골은 초음파도 감쇠 — fUS *영상*은 신생아/동물/개두창 주력. "비침습 tFUS read"는 낙관적; 성인 비침습 음향-imaging은 미성숙(돌파 후보지 기성품 아님).
- C7(잔여): prior-injection + temporal super-res in-silico · real head-model(MNE) 다중모달 fwd · 성인 fUS 가능성 문헌.

## 양방향 sibling
- [C(NOVEL 축)](C-postaural-invasive-NOVEL.md) · [C5](C5-source-recon-ceiling.md)(EEG-단독 천장) · [C3](C3-noninvasive-methods-sota.md)(5법=전기계) · brainwire `beyond-electrical-stimulation.md`(tFUS 모달)
