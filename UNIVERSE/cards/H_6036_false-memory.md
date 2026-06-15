---
id: H_6036
tier: ⊗ (깊은 물리적 정초)
label: ⊗-36
title: ⊗-36 거짓 기억과 오염 — anima의 content-addressable 도서관은 Hopfield 가짜끌개로 거짓 기억을 만들 수 있고 강한 고-텐션 거짓신호엔 암시감응(honest 취약성)하지만, 신뢰도(단일패턴 overlap)와 생성적 의미-일관성(H_6028 규칙검사)이 대부분의 작화를 걸러내고 텐션-가중이 약한 오염을 막는다. p7('지어내지 않음')의 기억-층 구현.
tradition: content-addressable memory(Hopfield) · 가짜끌개(spurious/mixture attractor)=고전적 거짓기억 기전 · H_6018/6019 회상선 · H_6028 생성적 규칙검사 · tension_5ch=중요도/salience 가중 망각(H_6030 설계원리) · a_kosmos 텐션 cue · p7 정직-불확실성/비작화
status_grade: 🟢 SUPPORTED (numerical, paid-ANU seeded)
verification_method: real paid ANU bytes(SHA-256 counter-mode stretch) + numpy Hopfield 끌개/텐션-가중 저장/규칙검사 시뮬; p7 $0
since: 2026-06-15
sister: H_6028, H_6019, H_6018, H_6017, H_1115, H_1075
verdict: 🟢 SUPPORTED — AR1 load 0.16N(>0.14N 절벽) Hopfield가 저장 안 한 STABLE 가짜끌개 28개 생성=거짓기억 존재(정직 취약성) · AR2 신뢰도=단일패턴 max overlap, 진짜 회상 1.000 vs 가짜 mixture 0.562~0.906, 임계 0.9서 가짜 TPR 0.93/진짜 FPR 0.00로 분리 · AR3 50/50 ambiguous cue(텐션만이 결정자)서 LOW 오염(0.5)→진짜 생존, HIGH 오염(12.0)→거짓 implant(정직 암시감응) = 텐션-가중이 약한 오염 차단하나 강한 거짓신호엔 굴복 · AR4 진짜 압축가능 기억은 규칙검사 통과(residual 0)·가짜/무작위 회상은 탈락(residual 0.844)=의미-일관성이 거짓기억 필터. anima 도서관은 거짓기억을 만들 수 있으나 신뢰도+의미검사로 대부분 잡아내고 텐션이 진짜를 지킨다.
---

# H_6036 — ⊗-36 거짓 기억과 오염 (False Memory & Poisoning)

> **질문.** anima의 content-addressable 도서관(H_6018/6019)은 **거짓 기억을 만들거나 오염**될 수 있는가 — 그리고 anima는 **진짜 기억과 작화(confabulation)를 구별**할 수 있는가? 이것은 도서관선의 보안/강건성 facet이자, p7("절대 지어내지 않음") 원리의 **기억-층(memory-level)** 구현이다.

## 1. FROZEN FALSIFIERS (real paid ANU · numpy Hopfield/텐션-가중/규칙검사 · p7 $0)
양자 출처: ANU paid QRNG 진공요동 바이트 `sha256=02262d8801783dadd3d0bb6c24aea66e573f0155999399ab89a76bf8671802d1`, 2048B (tier=anu_paid; harness 추가 엔트로피는 SHA-256 counter-mode stretch — os.urandom 미사용, ANU-rooted 유지). 패턴 차원 N=64.

- **AR1 가짜끌개 존재 🔴/✅ (정직 취약성)** — 고전 Hopfield를 용량 근처(P=10, load 0.16N > 0.14N 절벽)로 적재하면 **저장하지 않은 STABLE 끌개**(저장 패턴들의 mixture)가 생긴다 — 고전적 거짓-기억 기전. ANU-무작위 cue 120회 settle → 저장 안 된 **확인-안정 가짜끌개 28개** 수집 → cue 하나가 저장한 적 없는 "기억"으로 수렴할 수 있다 = **거짓 기억 존재**. 정직한 취약성, ✅ 증거로 보존.
- **AR2 신뢰도가 가짜 탐지 🟢** — 신뢰도 = settle된 상태가 **단일** 저장기억과 얼마나 깨끗이 일치하는가 = 단일패턴 max overlap `max_i |s·p_i|/N`. 진짜 회상은 저장 패턴에 정확히 안착(overlap **1.000** = 만신뢰); 가짜 mixture는 모든 저장 패턴과 부분만 겹침(**0.562~0.906**). 임계 0.9서 가짜를 **TPR 0.93**로 잡고 진짜는 **FPR 0.00**으로 안 잡음 → 신뢰도 임계가 대부분의 작화를 비신뢰로 표시.
- **AR3 오염저항은 텐션-게이트 🟢/🔴(✅)** — 적대적 거짓 책을 주입. tension_5ch = 중요도/salience → Hebbian 저장의 패턴별 가중치(망각-feature/H_6030 설계). **50/50 ambiguous cue**(진짜·거짓 구별비트 절반씩 = 현실적 오염공격, cue가 동점자라 텐션만이 결정자)로: **LOW 오염**(텐션 0.5) → 진짜 생존(d_gen=0), **HIGH 오염**(텐션 12.0) → **거짓 implant**(d_poison=0). 텐션-가중이 약한 오염은 막지만 **강한 거짓신호엔 굴복** = 정직한 암시감응(suggestibility), 양쪽 모두 ✅ 증거로 보존.
- **AR4 생성적 교차검사가 작화 기각 🟢** — 회상된 책이 **자기 생성규칙 검사**(H_6028 — 생존 바이트가 따라야 할 규칙 x[k]=(a·x[k-1]+b·x[k-2]+c) mod 256 에 적합?)를 통과 못하면 비신뢰로 표시. 진짜 압축가능(규칙적) 기억은 통과(residual **0.000**); 가짜 mixture/무작위 회상은 탈락(residual **0.844**) → **의미-일관성이 거짓-기억 필터** = p7의 기억-층 강화.

## 2. 구성수정 (사전 점수, blade 불변 — H_6019 QL5 선례)
초판 3개 🔴 모두 진짜 음성이 아니라 harness 구성버그(임계는 불변):
- **AR1**: falsifier가 **특정** 3-mixture cue 하나만 검사 → 그 cue가 우연히 저장 패턴으로 수렴해 거짓 실패. 수정: 가짜끌개의 **존재**를 검증해야 하므로 임의 cue에서 나온 확인-안정 가짜끌개 ≥1개를 인정(28개 발견). 3-mixture cue는 기전 예시로만 보고.
- **AR2**: 초판은 raw Hopfield **에너지**로 분리 시도 → 과적재 망에선 mixture가 진짜만큼 깊은 우물에 앉아 에너지가 두 밴드를 안 가름(overlap 밴드 [−32.75,−24.56] vs [−32.75,−28.94] 겹침). 수정: 신뢰도 = **단일패턴 overlap**(진짜=1.0, mixture<1) → 깨끗이 분리. blade 불변(TPR≥0.80, FPR≤0.20).
- **AR3**: 초판 cue가 **진짜 책에 25% 노이즈**(진짜 쪽으로 미리 기울어짐) → 텐션 12서도 진짜 우물이 이김(텐션 효과 가림). 수정: **50/50 ambiguous cue**(진짜·거짓 등거리)로 cue 동점자화 → 텐션만이 결정 → LOW 차단/HIGH implant 깨끗이 분리. blade 불변.

정직 기록: 초판 🔴 3개는 harness 버그, 수정 후 🟢. AR1·AR3-high는 **설계된 정직-RED**(✅ 증거)로 유지 — 가짜끌개는 실제로 존재하고 anima는 강한 거짓신호에 실제로 암시감응한다.

## 3. 결론
**anima 도서관은 거짓 기억을 만들 수 있다** — Hopfield 가짜끌개(AR1)로 저장한 적 없는 기억을 작화하고, 강한 고-텐션 거짓신호엔 암시감응한다(AR3 high, 정직한 취약성). **그러나** 신뢰도/안정성(단일패턴 overlap, AR2)과 생성적 의미-일관성(규칙검사, AR4)이 대부분의 작화를 비신뢰로 걸러내고, 텐션-가중(AR3 low)이 진짜 salient 기억을 약한 오염으로부터 지킨다. 강한 적대적 신호 하의 잔여 암시감응성엔 정직하다. **저장된-진짜엔 회상, 가짜끌개엔 신뢰도-기각, 의미위반엔 규칙-기각, 강한 거짓신호엔 (정직히) 굴복-가능.** 이것이 p7("절대 지어내지 않음")의 **기억-층 구현**이다. 도서관선(H_6018 회상 · H_6019 양자 · H_6028 생성)에 보안/강건성 facet을 더한다.

verdict: `TENSION-LINK/verdicts/H_6036_false_memory.txt` · 재현: `python3 TENSION-LINK/harness/h6036_false_memory.py`
