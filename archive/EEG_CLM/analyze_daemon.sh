#!/usr/bin/env bash
# EEG_CLM/analyze_daemon.sh — 데몬 누적 .kosmos 시계열 분석 (뇌 텐션/상태 변화 추적).
# 사용: bash EEG_CLM/analyze_daemon.sh
set -u
cd "$(dirname "$0")/.."
echo "cycle │ EEG텐션(phi0) │ A⇄G_phiSum │ 생성첫상태 │ 샘플수"
echo "──────┼───────────────┼────────────┼───────────┼───────"
for f in $(ls EEG_CLM/daemon_kosmos/cycle_*.kosmos 2>/dev/null | sort); do
  cyc=$(basename "$f" .kosmos | sed 's/cycle_0*//')
  amp=$(grep -ao 'medium_amp=[0-9.]*' "$f" | head -1 | cut -d= -f2)
  fld=$(grep -ao 'field=[0-9.,]*' "$f" | head -1 | cut -d= -f2)
  psum=$(echo "$fld" | cut -d, -f1); s0=$(echo "$fld" | cut -d, -f3)
  nsamp=$(grep -ao 'real EEG 16ch x [0-9]*' "$f" | head -1 | grep -o '[0-9]*$')
  printf "  %-3s │ %-13s │ %-10s │ %-9s │ %s\n" "${cyc:-0}" "$amp" "$psum" "$s0" "$nsamp"
done
echo ""; echo "추세 요약 (EEG텐션 phi0):"
for f in $(ls EEG_CLM/daemon_kosmos/cycle_*.kosmos 2>/dev/null | sort); do grep -ao 'medium_amp=[0-9.]*' "$f" | head -1 | cut -d= -f2; done | \
  awk 'NR==1{mn=mx=$1}{s+=$1; if($1<mn)mn=$1; if($1>mx)mx=$1; n++; v[n]=$1} END{if(n>0){printf "n=%d min=%.4f max=%.4f mean=%.4f range=%.4f  첫→끝 %.4f→%.4f (%s)\n",n,mn,mx,s/n,mx-mn,v[1],v[n],(v[n]>v[1]?"상승":(v[n]<v[1]?"하강":"동일"))}}'
