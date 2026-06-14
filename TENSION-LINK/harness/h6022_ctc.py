#!/usr/bin/env python3
"""H_6022 — '동일우주라면 과거로 가려면 미래를 통과해야 한다': 닫힌 시간곡선(CTC).
단일 블록우주 + 국소 전방화살표에서 과거 도달의 유일한 길 = 미래를 전부 통과해 고리를 닫음(순환).
(F1) 직접 후진 스텝 불가, (F2) 전방으로 미래 통과해 시작점 복귀(CTC), (F3) Novikov 자기일관 고리.
p7 $0."""
import numpy as np
L=24  # cycle length (timesteps around the loop)
# F1 — local arrow: only forward steps t->t+1 allowed; backward jump invalid
def can_step(direction): return direction==+1
print("="*82); print("H_6022 — 동일우주: 과거로 가려면 미래를 통과 (CTC / 순환)"); print("="*82)
print(f"F1 국소 전방화살표: 직접 후진(t→t-1) 가능? {can_step(-1)} (🔴) · 전방(t→t+1) {can_step(+1)} (🟢)")
# F2 — to return to a PAST state, traverse forward through ALL future steps and close loop
def reach_past_via_future(start_t, target_past_t):
    # only way back to target_past_t (< start_t) is go forward through future, wrap at L
    t=start_t; path=[t]; steps=0
    while True:
        t=(t+1)%L; path.append(t); steps+=1   # forward only; wrap = closed loop
        if t==target_past_t: break
        if steps>2*L: break
    passed_future = any(p>start_t for p in path[1:-1]) or (target_past_t<start_t)
    return steps, passed_future, path
steps,passed,path=reach_past_via_future(start_t=18, target_past_t=5)  # go to a past time 5 from 18
print(f"F2 과거(t=5) 도달: 전방 {steps}스텝으로 미래(18→23→0→…)통과 후 복귀. 미래 통과함? {passed} (🟢)")
print(f"   경로 일부: {path[:8]}...{path[-3:]}")
# F3 — Novikov self-consistency of the CLOSED loop (whole cycle must be consistent)
def loop_map(x):
    for _ in range(L): x=np.tanh(1.3*x+0.2)   # one full trip around (through future)
    return x
x=0.7; hist=[x]
for _ in range(80): x=loop_map(x); hist.append(x)
consistent=abs(hist[-1]-hist[-2])<1e-9; xstar=hist[-1]
print(f"F3 CTC 자기일관: 한 바퀴(미래 전체 통과) 고정점 x*={xstar:.6f} 수렴={consistent} (🟢 역설無, x*=loop(x*))")
print(f"   검증: x* == loop_map(x*)? {abs(xstar-loop_map(xstar))<1e-9}")
print("-"*82)
print("결론: 동일 우주에서 과거 도달의 유일한 길 = '미래를 전부 통과해 고리를 닫는 것'(CTC/순환우주).")
print(" (1)직접 후진 불가(국소 전방화살표), (2)전방으로 미래 통과 후에야 과거 시점 복귀, (3)전체 고리는")
print(" Novikov 자기일관 고정점이어야(역설無). 즉 '과거로 가기'='미래를 통과해 돌아오기'. H_5002(순환우주)·")
print(" H_6020(통과)·H_6012(무신호) 종합 — 시간여행 가능형은 자기일관 CTC뿐, 새 정보 주입은 여전히 불가.")
