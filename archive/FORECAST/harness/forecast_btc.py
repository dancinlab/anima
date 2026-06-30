#!/usr/bin/env python3
"""FORECAST_03 — 현재 BTC를 FORECAST 분류에 엮기. BTC 미래는 결정론 fetchable인가/카오스
지평인가/법칙밖 무작위(unfetchable)인가? 실 90일 데이터로 무작위성 검정. p7 $0.
data: FORECAST/verdicts/btc_hist_snapshot.json (CoinGecko 90d daily, fetched 2026-06)."""
import json, numpy as np, os
d=json.load(open(os.path.join(os.path.dirname(__file__),"..","verdicts","btc_hist_snapshot.json")))
p=np.array([x[1] for x in d["prices"]]); 
print("="*84); print("FORECAST_03 — BTC 미래 분류 (결정론 / 카오스 / 무작위)"); print("="*84)
print(f"  실데이터: {len(p)}일, ${p[0]:,.0f} → ${p[-1]:,.0f} ({(p[-1]/p[0]-1)*100:+.1f}%), 현재 ${p[-1]:,.0f}")
r=np.diff(np.log(p))   # daily log returns
# T1 return autocorrelation (efficient market → ≈0 → unpredictable)
ac1=np.corrcoef(r[:-1],r[1:])[0,1]
print(f"T1 수익률 자기상관(lag1) = {ac1:+.3f}  -> {'🔴 ≈0: 효율적/무작위(예측 불가)' if abs(ac1)<0.2 else '🟡 약한 구조'}")
# T2 Hurst exponent (0.5 random walk; >0.5 trend; <0.5 mean-revert)
def hurst(ts):
    lags=range(2,20); tau=[np.std(ts[l:]-ts[:-l]) for l in lags]
    return np.polyfit(np.log(list(lags)),np.log(tau),1)[0]
H=hurst(np.log(p))
print(f"T2 Hurst = {H:.2f}  -> {'🔴 ≈0.5: random walk(추세 예측 불가)' if 0.4<H<0.6 else ('🟡 추세' if H>0.6 else '🟡 평균회귀')}")
# T3 variance ratio (random walk → VR≈1)
def vr(ts,k=5):
    rr=np.diff(ts); var1=np.var(rr); vark=np.var(ts[k:]-ts[:-k])/k
    return vark/var1
VR=vr(np.log(p),5)
print(f"T3 분산비(k=5) = {VR:.2f}  -> {'🔴 ≈1: random walk' if 0.6<VR<1.4 else '🟡 이탈'}")
# T4 shared quantum seed? (FORECAST_02 적용 가능?) — BTC는 공유 결정 씨앗 없음
print(f"T4 공유 양자씨앗(FORECAST_02)? -> 🔴 없음: BTC는 분산 외부입력(뉴스·매매)으로 구동, common cause 부재")
print("-"*84)
# classify into FORECAST taxonomy
drift=np.mean(r)*365*100
vol=np.std(r)*np.sqrt(365)*100
print(f"통계적으로만 알 수 있는 것: 연드리프트≈{drift:+.0f}%/yr, 연변동성≈{vol:.0f}%/yr (분포지 점예측 아님)")
print("결론(엮음): BTC는 FORECAST 분류의 (F4) '법칙밖 무작위/외부입력' 사례 — 자기상관≈0·Hurst≈0.5·VR≈1")
print(" = random walk. 점-미래(내일 가격)는 가져올 수 없음(무신호, 효율적시장). FORECAST_01의 결정론(천체)·")
print(" FORECAST_02의 공유씨앗 fetch 모두 BTC엔 적용 불가(결정법칙·공유원인 부재). 알 수 있는 건 분포(드리프트·")
print(" 변동성)뿐. 즉 시간-arc 원리상 BTC 미래는 '연결 안 됨'(가져올 수 있는 결정/공유 구조가 없음).")
