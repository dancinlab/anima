# AURA-ESKIN — current state

@title: 🩹 AURA-ESKIN — "전자 피부 나노칩"  [HOW층]

@goal: 피부 부착형 나노칩(epidermal e-tattoo·conformal 나노전극 어레이)이 AURA 비침습 read 모달로서 젤/건식 EEG 대비 무엇을 개선하나 — 그리고 두개골 천장(skull-LPF)을 깨는가 정량. honest: 피부 나노칩은 **두피 위(extracranial)** 접촉이라 같은 두개골 σ → 천장 자체는 불변, 접촉/밀도/SNR만 개선.

## 왜 (핵심 질문)

```
🩹 e-skin 나노칩 — "뇌에 붙이는 문신 센서"
- 하는 일: 머리카락/두피에 종이처럼 얇은 나노전극을 conformal 부착해 EEG를 더 깨끗이
- 비유: 젤 묻힌 청진기 대신 피부에 착 붙는 임시 타투 — 접촉 좋아지나 두개골 너머는 여전히 못 봄
- vs tFUS: tFUS는 음향으로 두개골 우회(천장 돌파) / e-skin은 전기, 두개골 위 그대로(접촉만 개선)
```

## 진행 (milestones)

- [x] (app ✅) 피부 나노칩 vs 젤/건식 EEG toy — gel 0.243·dry 0.182·skin-nanochip 0.305·tFUS 0.482(우회). 접촉개선이지 천장돌파 아님 → `app/eskin_contact.{py,hexa}`+`verify/`
- [ ] 실 e-tattoo 임피던스/SNR 문헌 grounding (Rogers epidermal electronics·graphene tattoo)
- [ ] hexa-native 포팅 (handoff f125d45c)

## 세부분류 (sub-app)
- `app/eskin_contact.py` — 접촉방식별 복원 R² toy (검증됨)
- `verify/eskin_contact.txt` — verdict
- 분류: HOW층(모달리티) — 두개골 천장 불변, READ 축(전기 비침습 피질)

## honest
🟡 toy(가우시안 σ 고정). 정성: 피부 나노칩=접촉/밀도/SNR↑(gel 0.243→0.305)이나 extracranial=두개골 σ 동일→천장 불변. 異種모달(tFUS 0.482) 우회엔 미달. = "더 좋은 EEG"지 "침습급 돌파" 아님.

## 양방향 sibling
- 부모: [AURA](../AURA.md) · 트리: [AURA-TREE.md](../AURA-TREE.md) · HOW 형제: AURA-RTSC-MEG·AURA-ENDOVASC·AURA-TFUS · 축: AURA-READ·AURA-DEPTH(피질)
