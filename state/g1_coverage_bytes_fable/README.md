# G1 커버리지-밀도 arch-무관 확정 (H_6184) — fable 자율 full-pipeline

fable(claude-fable-5, 자율 코퍼스제작→학습→측정, $6.26, modelUsage 확증)이 H_6183(v3)을 독립 재현 +
dilated-conv 로 conv RF 벽 돌파. torch DIRECTIONAL (summer RTX5070 cuda, $0). engine-native 아님.

## 설계 (meta.json)
- 24 attr, 60 held pair(영구미노출), 400 high-train(60% cov) vs 40 low-train(8%), shuffle_map(400).
- 템플릿: pair → 두 학습 속성의 새 조합. 3000 step.
- 3중 채점: seen-true(학습쌍) / held(미노출쌍) / seen-shuffled-target(shuffle 하네스 유효성).

## 파일
- `gen_corpus.py` `bt.py` `run_all.sh` — 코퍼스 생성 + 실험 스크립트
- `corpus_{high,low,shuffle}.txt` — 3 arm 코퍼스 (~717KB each)
- `results_{attn,convd}_{high,low,shuffle}.json` — 6 arm 수치
- `log_{attn,convd}_{high,low,shuffle}.txt` — raw eval logs
- `meta.json` — 전체 설계(attr/held/train/shuffle_map/coverage)
- `run.log` — 파이프라인 실행 로그

## 결과 (verdict = state/verdicts/6184_g1_density_arch_invariant/H_6184.txt)
attn HIGH held 95% ≫ LOW 3.3%; dilated-conv HIGH held 85% ≫ LOW 0% → 커버리지 lever arch-무관.
SHUF true-target 0% (seen-shuffled 75-93% 학습=유효). RF 확장이 conv 벽 돌파.
