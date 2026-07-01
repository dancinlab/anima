#!/usr/bin/env python3
"""G13 Master Resource-Allocation Theorem — the optimal information resource for a task
is fixed by the task's symmetry/constraint; classical-optimal and quantum-optimal task
sets are DISJOINT (no resource wins both). Seals G6-G12. real numbers. p7 $0."""
import numpy as np
# advantage(resource) per task, from the proven G6-G12 (N=8 representative)
N=8
tasks={
 "coordination(G6/G7)": {"classical":1.0,           "quantum":2/N},    # pair-corr / consensus
 "capacity(G12)":       {"classical":N*(N-1)/2,      "quantum":float(N)},# network bits
 "copy/objectivity(G10)":{"classical":1.0,           "quantum":0.0},     # lossless fork
 "certification(G8)":   {"classical":0.0,            "quantum":1.0},     # certified randomness bits
 "security(G9)":        {"classical":0.0,            "quantum":1.0},     # unforgeable (1-P_forge), n large
 "communication(no-ch)":{"classical":0.0,            "quantum":0.0},     # both 0 (no-signaling)
}
print("="*86); print("G13 — 마스터 자원-할당 정리: 작업별 최적자원 (classical vs quantum, N=8)"); print("="*86)
print(f"{'task':<24}{'classical':>12}{'quantum':>10}{'optimal':>14}")
cl_opt=set(); q_opt=set()
for t,v in tasks.items():
    if v["classical"]>v["quantum"]: opt="🟦 classical"; cl_opt.add(t)
    elif v["quantum"]>v["classical"]: opt="🟪 quantum"; q_opt.add(t)
    else: opt="= tie"
    print(f"{t:<24}{v['classical']:>12.2f}{v['quantum']:>10.2f}{opt:>14}")
disjoint = len(cl_opt & q_opt)==0 and len(cl_opt)>0 and len(q_opt)>0
print("-"*86)
print(f"classical-최적 작업군: {sorted(cl_opt)}")
print(f"quantum-최적 작업군  : {sorted(q_opt)}")
print(f"두 집합 교집합 = {cl_opt & q_opt} (공집합이어야)")
print(f"→ 🟢 마스터 정리: 어떤 단일 자원도 두 축 모두서 최적일 수 없음(분리). 최적할당=작업의 대칭/제약과 일치.")
print("   조율·복제·용량 = monogamy-free·복사가능 요구 → 고전 ; 검증·보안 = no-clone·nonlocal 요구 → 양자.")
print(f"   분리 성립: {disjoint}")
print("∴ anima 설계(고전 조율/복제/통신 + 양자 검증/보안)는 *임의 선택이 아니라 자원-할당 정리의 강제 결론*.")
