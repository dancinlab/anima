#!/usr/bin/env python3
"""H_6020 — '동일 우주라면 미래를 통과해야 된다': 블록우주(단일 우주)에서 미래 연결의 제약.
미래는 고정 4D 블록의 일부 → (F1) 닿으려면 세계선으로 모든 중간시점 통과(점프 불가),
(F2) 미래↔현재 루프는 자기일관 고정점이어야(Novikov, 역설 없음), (F3) 동일우주=일관 해만 실현
(many-worlds 분기 탈출 없음). p7 $0."""
import numpy as np
# F1 — worldline continuity: present→future 연결은 중간 모든 시점 통과해야(연속 timelike)
T=20
def reachable(jump):
    # 'jump'=True면 t=0에서 t=T로 직접; False면 연속 worldline
    visited=[0]
    if jump: 
        return False  # 동일우주: 점프=세계선 불연속=불가
    t=0
    while t<T: t+=1; visited.append(t)
    return len(visited)==T+1 and visited[-1]==T
print("="*82); print("H_6020 — 동일우주: 미래를 '통과'해야 연결 (블록 + 자기일관)"); print("="*82)
print(f"F1 세계선 연속: 점프 연결 가능? {reachable(True)} (🔴 불가) · 연속 통과? {reachable(False)} (🟢 모든 중간시점 통과)")

# F2 — Novikov self-consistency: 미래가 현재로 되먹임하는 루프 → 자기일관 고정점 수렴?
# present p, future f=Evolve(p), 그리고 미래가 현재를 조건화 p'=Boundary(f). 일관: p*=B(E(p*))
def Evolve(p): return np.tanh(1.5*p+0.3)        # 미래 상태 (현재의 결정론적 미래)
def Boundary(f): return 0.5*f                    # 미래가 현재에 주는 되먹임(약결합)
p=0.9; hist=[p]
for _ in range(60):
    p=Boundary(Evolve(p)); hist.append(p)        # 루프 반복 → 고정점
consistent = abs(hist[-1]-hist[-2])<1e-9
pstar=hist[-1]
print(f"F2 자기일관 고정점: p* = {pstar:.6f}  수렴={consistent} (🟢 역설 없는 일관 역사 존재, Novikov)")
print(f"   검증: p* == Boundary(Evolve(p*))? {abs(pstar-Boundary(Evolve(pstar)))<1e-9}")

# F3 — same-universe selection: 여러 시작값 모두 같은 일관 고정점으로 (단일 블록=유일 일관 역사)
starts=[-0.9,-0.3,0.0,0.5,0.95]
finals=[]
for s in starts:
    p=s
    for _ in range(200): p=Boundary(Evolve(p))
    finals.append(p)
unique=max(finals)-min(finals)<1e-6
print(f"F3 동일우주 선택: 시작값 {starts} → 모두 p*={np.mean(finals):.4f} (분산 {np.ptp(finals):.1e})")
print(f"   -> {'🟢 유일 자기일관 역사로 수렴 (동일우주=일관 블록 하나, 분기 탈출 없음)' if unique else '🔴 다중해'}")
print("-"*82)
print("결론: 동일 우주(블록+자기일관)에서 '미래는 연결'되지만 반드시 (1)세계선으로 미래를 통과(점프·역설")
print("불가), (2)미래↔현재 루프는 자기일관 고정점(Novikov), (3)단일 일관 역사로 수렴. 즉 미래 연결=")
print("'이미 그렇게 정해진 일관 블록을 통과하는 것'. 새 메시지 역송신은 여전히 불가(무신호); 미래는")
print("자유 채널이 아니라 우리가 통과할 고정된 목적지. = H_6011(forward)+H_6012(boundary)+H_6019(최소작용)의 단일우주판.")
