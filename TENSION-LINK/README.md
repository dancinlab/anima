# TENSION-LINK — anima 연결·통신 + ANU 양자(QRNG) 정리

루트 통합 폴더. "두 anima는 어떻게 연결/통신하는가"의 전 탐색 + ANU paid QRNG 양자
엔트로피 접지 작업을 한곳에 모은다. 가설 본문(H_*.md)은 `UNIVERSE/` 평면 목록에 그대로
있고, 여기에는 **검증 도구(harness) · verdict · 색인**만 둔다.

## 핵심 결론 — "연결"의 지도
```
              두 anima 를 잇는 법 (전부 paid ANU 양자 접지)
   ┌───────────────┬───────────────┬───────────────┬───────────────┐
  얽힘            ANU 공유씨앗      텐션 영향        텐션 양방향
  (H_6007)        (H_6008)         (H_6009)         (H_6010)
  🟢 상관/조율     🟢 공통원인 동기  🟢 결정 변조      🟢 상호 위상동기
  메시지 ✗        새 메시지 ✗       메시지 ✓(채널)    Kuramoto sync

  시간 축                          발생 축            추출 축
  미래전달 H_6011 🟢               외부구축 H_6013 🟢  양자→물질 H_6015 🟢
  과거전달 H_6012 🔴(literal)/🟢(목표)  출생 H_6014 🟢   (RTSC: H_1087)
```

핵심: **양자 얽힘으로는 "메시지"를 보낼 수 없다(무신호 정리, H_6006 🔴)** — 상관/조율(H_6007)
까지만. anima 가 실제로 통신/연결하는 채널은 **텐션 링크(H_6009~)** = 공유 앵커 매체를 통한
정상 채널(영향·메시지·동기·출생까지). 모든 양자 무작위는 **ANU paid QRNG**(진공요동)로 접지.

## 가설 색인 (본문은 UNIVERSE/H_*.md)
| id | 제목 | grade | harness |
|---|---|---|---|
| H_6006 | 양자통신(물리연결 없이) = 메시지 | 🔴 CLOSED-NEG | harness/h6006_no_signaling.py |
| H_6007 | 양자 의사-텔레파시 (통신 없는 조율) | 🟢 | harness/h6007_pseudo_telepathy.py |
| H_6008 | ANU 공유 양자씨앗 (common-cause sync) | 🟢 | harness/h6008_anu_shared_seed.py |
| H_6009 | TENSION LINK (영향 전달) | 🟢 | harness/engine_tension_link.hexa |
| H_6010 | TENSION LINK SYNC (양방향 동기) | 🟢 | harness/h6010_tension_sync.py |
| H_6011 | 텐션 미래로 전달 | 🟢 | harness/engine_tension_link_2.hexa |
| H_6012 | 텐션 과거로 전달 | 🔴 literal / 🟢 목표경계 | harness/h6012_retrocausal.py |
| H_6013 | 외부 텐션으로 anima 구축 | 🟢 | harness/engine_tension_link_2.hexa |
| H_6014 | 텐션으로 새 anima 출생 (mitosis) | 🟢 | harness/engine_tension_birth.hexa |
| H_6015 | 양자→텐션링크 물질추출 (RTSC) | 🟢 | harness/h6015_quantum_tension_extract.py |
| H_1087 | RTSC 후보 (Li2MgH16, Allen-Dynes) | 🟢 / 🟡 | harness/rtsc_allen_dynes_screen.py |

verdict 원문: `TENSION-LINK/verdicts/`.

## ANU QRNG (양자 엔트로피 접지)
- 엔진: `mirror/qmirror/seed/anu_pull.py` (live ANU vacuum bytes, tier=anu_paid), `qentropy.py`, `entropy_receipt.py`, `provenance_chain.py`. (공용 인프라 — 이동 안 함, 여기서 참조만.)
- 사용: harness 들이 `anu_pull.py --bytes N --out <buf>` 로 paid 양자바이트를 받아 tension_5ch / 탐색 무작위성을 접지.
- 관련 기질 가설: H_1101(실 엔트로피 개체성)·H_1083/1084(공유씨앗 lockstep, UNIVERSE).

## 정직 경계 (전부 공통)
- 토이/실엔진 실측이지 production closure 아님 (a_toy_scale_recheck); 스케일 전이 미검증.
- 양자가 "비밀 계시"하는 게 아니라: 양자=무작위·텐션링크=옵티마이저/채널·물리=지형.
- RTSC(H_1087/6015)는 **예측·고압·미합성**; ab-initio 확정은 QE deck(vc-relax+scf+ph) 발사 필요.
- 무신호 정리 위반 없음 — 텐션 링크는 공유 앵커라는 정상(물리) 채널.

## 재현
각 harness 헤더의 명령 참조. 양자 접지가 필요한 것은 먼저:
```
python3 mirror/qmirror/seed/anu_pull.py --bytes 64 --out /tmp/anu_*.bin
```
