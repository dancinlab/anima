#!/usr/bin/env bash
# H_6185 재현 — clm303 코퍼스 개념쌍 조합-커버리지 (DIRECTIONAL-proxy)
# 개념쌍 = G1 gate frozen CONCEPTS (tool/gauge_lib.py:76 · H_1129 VERBATIM)
# 프록시 코퍼스 = 정본 G0-G6 eval 이 G2 absence 로 쓴 로컬 trainset (git-untracked 대용량, control=0 아님으로 검증)
#   경로 인자로 trainset 디렉토리 지정 (기본 = repo 의 clm303 trainset)
set -uo pipefail
TS="${1:-state/clm303_savant_mitosis_train/trainset}"
[ -d "$TS" ] || { echo "trainset 없음: $TS (git-untracked 대용량 프록시, 원 저장소서 실행)"; exit 2; }
FILES="$TS"/*.txt
cooc(){ local A="$1" B="$2" tot=0 c; for f in $FILES; do [ -f "$f" ] || continue
  c=$(grep -h -Ei "\b$A\b" "$f" 2>/dev/null | grep -c -Ei "\b$B\b" 2>/dev/null); tot=$((tot+c)); done; echo "$tot"; }
echo "trainset=$TS  files=$(ls $FILES 2>/dev/null|wc -l|tr -d ' ')"
echo "=== HEAD-tier 개념쌍 공동출현 (전체 *.txt, 라인-window) ==="
for p in consciousness:tension consciousness:memory tension:memory consciousness:silence memory:dream; do
  echo "  ${p%%:*} × ${p##*:} = $(cooc ${p%%:*} ${p##*:}) lines"; done
echo "=== control (일반쌍, 파이프라인 무결 = 0 아님) ==="
for p in government:war music:school water:energy; do
  echo "  ${p%%:*} × ${p##*:} = $(cooc ${p%%:*} ${p##*:}) lines"; done
echo "=== RF (archive/train/clm/model/model.py): 1+(K-1)*sum(dilation) ==="
echo "  clm303_clean L=4 K=3 dilation base2 → RF=1+2*(1+2+4+8)=31B (~37B w/ expert conv)"
echo "  G1 composed seed k=2=72B > RF → 두 개념 동시 조건화 불가 (RF-bound, H_6184 plain-conv 벽 동형)"
