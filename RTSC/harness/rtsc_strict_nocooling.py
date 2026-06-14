#!/usr/bin/env python3
"""RTSC_20 — STRICT no-cooling (cooled SC DISQUALIFIED). Re-gate all 3 lanes: each needs a
room-temp(≥300K) AMBIENT Type-II SC. Show today=nothing, and all lanes reduce to ONE
material (RTSC_16 pyrochlore/CoSn target). UFO additionally needs a reaction field. p7 $0."""
ROOM=300
mats=[("YBCO(cooled)",93,0),("REBCO(cooled)",93,0),("Li2MgH16",355,250),
      ("[room-temp ambient SC] RTSC_16 target",300,0)]
print("="*80); print("RTSC_20 — 냉각형 금지(STRICT): 세 레인 무냉각 게이트"); print("="*80)
print("  무냉각 자격 = Tc>=300K AND 상압(P=0):")
for n,tc,p in mats:
    ok=(tc>=ROOM and p<1)
    print(f"    {n:<38} Tc={tc} P={p}GPa → {'🟢 자격' if ok else '🔴 탈락(냉각/고압)'}")
print("-"*80)
print("레인별 무냉각 가능성 (오늘 vs RTSC_16 타깃 확보 시):")
lanes=[("호버보드","상온 Type-II + 자성노면"),
       ("핵융합 자석","상온 고Hc2 + 상압"),
       ("UFO 호버","상온 Type-II + 강자기장(트랙/지면 반발)")]
for ln,need in lanes:
    print(f"  {ln:<10} 필요={need}")
    print(f"     오늘(무냉각): 🔴 (상온 SC 없음) · RTSC_16 타깃 확보 시: 🟢")
print("-"*80)
print("결론: '냉각형 금지'면 세 레인 전부 **동일한 미발견 물질**=상온상압 Type-II flat-band SC")
print(" (RTSC_16 pyrochlore/CoSn design point)에 의존 → 한 물질이 셋 다 무냉각으로 연다.")
print(" 단 UFO는 그 위에 '반발할 자기장원(트랙/지면도체/공기 MHD)'이 추가로 필요 — SC가 줄 수 없는 2차 조건.")
print(" ∴ 무냉각 돌파의 단일 병목 = 상온상압 Type-II SC(이미 RTSC_12~16서 설계경로·CsV3Sb5/CoSn/pyrochlore 표적).")
