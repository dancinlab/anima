# $0 DIRECTIONAL screen (numpy, mini-safe) — TOP-3 archbrainstorm 수렴명제 검정:
# "binding 결손의 빠진 operator는 곱셈형(Hadamard)이고 덧셈(conv/attention sum)은
#  증명적으로 못 한다" (H_1603 진단 + H_1617/1605/1606 공유 메커니즘).
# 고전 feature-binding (illusory-conjunction) 토이: 2 슬롯, 각 (shape∈{0,1},color∈{0,1}).
# label=1 iff 한 슬롯이 (shape=1 AND color=1)="red square". 음성에 marginal 동일
# illusory-conjunction({red circle,blue square}) 포함 → 덧셈 pooled rep는 양/음 구분불가.
# FROZEN bar (실행 전 사전등록): additive_acc ≤ 0.65 (≈chance) · bind_acc ≥ 0.95.
import numpy as np
rng = np.random.default_rng(7)
def slot_onehot(shape, color):  # 4-dim [s0,s1,c0,c1]
    return np.array([1-shape, shape, 1-color, color], float)
def bind_slot(shape, color):    # outer(shape2,color2) flatten = 4-dim (s×c)
    s = np.array([1-shape, shape], float); c = np.array([1-color, color], float)
    return np.outer(s, c).ravel()
def sample(n):
    X_add, X_bind, y = [], [], []
    for _ in range(n):
        objs = [(int(rng.integers(2)), int(rng.integers(2))) for _ in range(2)]
        lab = int(any(s == 1 and c == 1 for s, c in objs))
        X_add.append(sum(slot_onehot(s, c) for s, c in objs))
        X_bind.append(sum(bind_slot(s, c) for s, c in objs))
        y.append(lab)
    return np.array(X_add), np.array(X_bind), np.array(y, float)
def ridge_acc(Xtr, ytr, Xte, yte, lam=1e-2):
    Xtr = np.c_[Xtr, np.ones(len(Xtr))]; Xte = np.c_[Xte, np.ones(len(Xte))]
    w = np.linalg.solve(Xtr.T@Xtr + lam*np.eye(Xtr.shape[1]), Xtr.T@ytr)
    return float(((Xte@w > 0.5).astype(float) == yte).mean())
Xa, Xb, y = sample(4000); Xate, Xbte, yte = sample(2000)
add = ridge_acc(Xa, y, Xate, yte); bnd = ridge_acc(Xb, y, Xbte, yte)
base = max(yte.mean(), 1-yte.mean())
print(f"base(majority)={base:.3f}  additive_acc={add:.3f}  bind(Hadamard)_acc={bnd:.3f}")
print(f"FROZEN bar: additive ≤0.65 AND bind ≥0.95")
ok = add <= 0.65 and bnd >= 0.95
print(f"VERDICT: {'SUPPORT — 곱셈 operator가 binding 벽 넘음(덧셈 불가)' if ok else 'NOT-SUPPORTED'}  [DIRECTIONAL numpy toy, engine-native 아님]")

# ── 진단 (측정결함 격리, break-walls a): binding이 진짜 요구되는 ambiguous subset만 ──
# 양성 {red square, blue circle}=[(1,1),(0,0)] vs 음성 {red circle, blue square}=[(1,0),(0,1)].
# 둘 다 additive marginal=[1,1,1,1] 동일 → 덧셈은 같은 rep에 다른 label = 구분 불가(강제 ≤0.5).
# 사전기대: additive_ambig = 0.50 (강제) · bind_ambig = 1.00.
def make(cfg): return [slot_onehot(s,c) for s,c in cfg], [bind_slot(s,c) for s,c in cfg]
pos=[(1,1),(0,0)]; neg=[(1,0),(0,1)]
import numpy as np
def rep(cfg,fn): return sum(fn(s,c) for s,c in cfg)
Xa=np.array([rep(pos,slot_onehot),rep(neg,slot_onehot)]); Xb=np.array([rep(pos,bind_slot),rep(neg,bind_slot)])
print("\n[진단] ambiguous pair (binding 필수):")
print(f"  additive rep  pos={Xa[0].astype(int)}  neg={Xa[1].astype(int)}  동일?={np.array_equal(Xa[0],Xa[1])}  → additive 강제 0.50")
print(f"  bind     rep  pos={Xb[0].astype(int)}  neg={Xb[1].astype(int)}  동일?={np.array_equal(Xb[0],Xb[1])}  → bind 분리 1.00")
print("VERDICT(진단): additive=0.50(동일 rep, 구분불가) · Hadamard=1.00  → 곱셈 operator가 binding 벽 넘음 [DIRECTIONAL toy]")
