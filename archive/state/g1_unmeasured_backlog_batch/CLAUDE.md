# state/g1_unmeasured_backlog_batch/ — G1/G6 미측정 설계 일괄 발사 배치

**목적:** G1 재조합벽 돌파를 위한 미측정 PRE-REGISTERED 설계들을 일괄 발사하는 스테이징 디렉토리. 
사용자 "모두 등록후 발사" 지시(2026-06-29).

## 파일 구조

- `PREREG.md` — 8 설계 fire-ready 등록 (결합(c) gated · H_1813 독립 발사)
- `H_1813/` — TPR expert-weight TLoRA 실험 (IN-FLIGHT, pod 43098811)
  - `trainer.py` — recomb-objective baked 트레이너 (ctrl/tlora 양 arm)
  - `RESULT.md` — 결과 템플릿 (eval 완료 후 채움)
  - `ckpt/` — 학습 산출물 (*.clm, *.pt, *_g0g6.txt, *_descent.txt, *.json, *.log)

## 현황 (2026-06-29 12:29 UTC)

- **H_1813 IN-FLIGHT**: pod 43098811 A40 CUDA-12.2, 6 arms sequential (ctrl/tlora × seed{7,4302,4303})
  - 학습 예상 완료: ~19:10 UTC
  - eval(chain_eval.sh PID 1641 → eval_h1813.sh → aggregate_h1813.sh): ~20:15 UTC
  - 결과: ckpt/*_g0g6.txt + *_descent.txt + aggregate.log
- **결합(c) gated arms** (H_1630/1652/1657/1672/1625/1799/1688): 별도 에이전트(a36f34cb) 완료 후 결정

## 다음 세션 작업

1. `hexa cloud exec 43098811 -- "cat state/g1_unmeasured_backlog_batch/H_1813/ckpt/aggregate.log"` 로 결과 확인
2. `rsync -az -e "ssh -p 18810 ..." root@ssh1.vast.ai:~/anima/state/g1_unmeasured_backlog_batch/H_1813/ckpt/ state/g1_unmeasured_backlog_batch/H_1813/ckpt/`
3. RESULT.md 채우기, H_1813 card + HYPOTHESES.jsonl 최종 verdict 업데이트
4. ckpt pull (a_fire_recover_complete): 최소 ctrl_seed7.clm + tlora_seed7.clm
5. `hexa cloud rm 43098811` (teardown)

## 규칙

- `.clm`/`.pt` 파일은 gitignore (너무 큰 이진 — HF에만 업로드)
- 다른 에이전트 dirs(state/g1_cotrain_recomb_bind, state/g1_cotrain_live_bind) 건드리지 말 것
