"""
H_9129 STEP-0 / L2 basal-ganglia content-gate (numpy toy, DIRECTIONAL — 303M 아님).

Frame: recombination(G1) 은 mouth-readout 속성이 아니라 별도 lane 시스템 속성.
L2 = 기저핵 content-gate: 여러 후보결합(role-filler binding) 중 하나를 Go/NoGo 로 선택.
훈련 = disjoint value/consistency 신호(RPE-analog δ = reward - Q). mouth 는 읽기만.

관계 R = 임의 순열 π (type a 의 role ↔ type π(a) 의 filler). 순열이 '임의'이므로
surface 유사도(form)로는 못 풀린다 → form-priming 방어 내장.

BIND 시험(속일수없는): held-out novel (role,filler) pair 를 두 종류로 —
  reachable   = a ∈ TRAINED types  → π(a) 학습됨 → gate 가 f* 선택 가능(연결됨)
  unreachable = a ∈ NOVEL types    → π(a) 미학습 → gate 무근거(연결안됨)
둘 다 동일 표면형태(role + K candidates, 하나가 f*).
  form 이면      reachable ≈ unreachable (둘 다 표면만 봄)
  진짜 BIND 이면 reachable >> unreachable (학습한 관계로만 lift)

Ablation:
  gate OFF (전 결합 uniform 평균 = 선택 없음) → 조합정확도 = 1/K chance.
  gate 붕괴하면 = 인과, INERT(OFF 해도 유지)면 = 기여 0.
  + learned-W vs random-W (RPE 로 학습한 value 가 인과인지).

form-decoy: candidate 하나를 role 방향과 surface-유사(cosine 높음)하지만 type 오답으로 심음.
  form 모델은 decoy 를 고름, BIND(W) 모델은 안 속음 → fooled_by_form 직접 측정.
"""
import numpy as np, json, os

RNG = np.random.default_rng(20260705)
D          = 32          # prototype dim
T          = 40          # total types
N_TRAIN    = 30          # trained types (reachable)
N_NOVEL    = T - N_TRAIN # held-out types (unreachable)
K          = 5           # candidate bindings per trial (Go picks 1, NoGo 4)
BETA_DECOY = 0.8         # role-direction injected into a wrong-type decoy filler
PROTO_S    = 1.0/np.sqrt(D)
NOISE_S    = 1.0/np.sqrt(D)   # identity/noise scale (SNR ~1 → generalize, non-trivial)
ETA        = 0.05
STEPS      = 20000
BATCH      = 64
N_EVAL     = 3000

# ---- fixed world ----
P = RNG.standard_normal((T, D)) * PROTO_S           # type prototypes
# arbitrary bijection π that keeps trained->trained, novel->novel (train never needs novel protos)
perm_tr = RNG.permutation(N_TRAIN)
perm_nv = RNG.permutation(N_NOVEL)
PI = np.zeros(T, dtype=int)
PI[:N_TRAIN] = perm_tr
PI[N_TRAIN:] = N_TRAIN + perm_nv
trained_types = np.arange(N_TRAIN)
novel_types   = np.arange(N_TRAIN, T)

def role_feat(a, n):
    return np.atleast_2d(P[a]) + RNG.standard_normal((n, D)) * NOISE_S   # type + novel identity/noise
def filler_feat(b, n):
    return np.atleast_2d(P[b]) + RNG.standard_normal((n, D)) * NOISE_S

# ---- L2 gate: bilinear value Q(role,filler)=role^T W filler, RPE-trained ----
W = np.zeros((D, D))
def Qval(role, fill):   # rows paired
    return np.einsum('id,de,ie->i', role, W, fill)

for step in range(STEPS):
    a = RNG.choice(trained_types, BATCH)
    # half compatible (b=π(a), reward 1), half random incompatible (reward 0)
    b = np.empty(BATCH, dtype=int); reward = np.zeros(BATCH)
    comp = RNG.random(BATCH) < 0.5
    b[comp] = PI[a[comp]]; reward[comp] = 1.0
    ninc = (~comp).sum()
    # random incompatible types (trained-space filler; ensure != π(a))
    rb = RNG.choice(trained_types, ninc)
    pia = PI[a[~comp]]
    bad = rb == pia
    while bad.any():
        rb[bad] = RNG.choice(trained_types, bad.sum()); bad = rb == PI[a[~comp]]
    b[~comp] = rb
    rf = role_feat(a, BATCH); ff = filler_feat(b, BATCH)
    q  = Qval(rf, ff)
    delta = reward - q                      # RPE
    W += ETA * (rf * delta[:,None]).T @ ff / BATCH   # ΔW = η <δ role⊗filler>

W_learned = W.copy()
W_random  = RNG.standard_normal((D, D)) * (np.abs(W_learned).mean() + 1e-9)  # matched-scale control

def build_trial(a):
    """role of type a + K candidates: [f*, form-decoy, 3 random-incompat]. returns role, cand_feats, star_idx, decoy_idx."""
    pia = PI[a]
    r = role_feat(a, 1)[0]
    # f*  (compatible)
    fstar = filler_feat(pia, 1)[0]
    # form-decoy: wrong type c, but surface-similar to role (inject role direction) → fools cosine
    others = [t for t in range(T) if t != pia]
    c = int(RNG.choice(others))
    decoy = (P[c] + BETA_DECOY * P[a] + RNG.standard_normal(D) * NOISE_S)
    # 3 random incompatible
    rest = []
    for _ in range(K - 2):
        t = int(RNG.choice([x for x in range(T) if x != pia]))
        rest.append(filler_feat(t, 1)[0])
    cands = [fstar, decoy] + rest
    order = RNG.permutation(K)
    cands = [cands[i] for i in order]
    star_idx  = int(np.where(order == 0)[0][0])
    decoy_idx = int(np.where(order == 1)[0][0])
    return r, np.array(cands), star_idx, decoy_idx

def evaluate(pool, W_use, n=N_EVAL):
    gated_hit = decoy_pick = form_hit = form_decoy = 0
    for _ in range(n):
        a = int(RNG.choice(pool))
        r, cands, star, decoy = build_trial(a)
        q = np.einsum('d,de,ke->k', r, W_use, cands)      # gate value per candidate
        sel = int(np.argmax(q))
        gated_hit += (sel == star); decoy_pick += (sel == decoy)
        # form baseline = cosine(role, filler)
        cos = cands @ r / (np.linalg.norm(cands,axis=1)*np.linalg.norm(r) + 1e-9)
        fsel = int(np.argmax(cos))
        form_hit += (fsel == star); form_decoy += (fsel == decoy)
    return dict(gated_acc=gated_hit/n, gated_decoy_rate=decoy_pick/n,
                form_acc=form_hit/n, form_decoy_rate=form_decoy/n)

chance = 1.0 / K
res = {
    "config": dict(D=D,T=T,N_TRAIN=N_TRAIN,N_NOVEL=N_NOVEL,K=K,STEPS=STEPS,
                   BETA_DECOY=BETA_DECOY,NOISE_S=float(NOISE_S),chance=chance),
    "reachable_trainedW":   evaluate(trained_types, W_learned),
    "unreachable_trainedW": evaluate(novel_types,   W_learned),
    # ablation: learned-W removed -> random-W (matched scale) = gate value destroyed
    "reachable_randomW":    evaluate(trained_types, W_random),
    "unreachable_randomW":  evaluate(novel_types,   W_random),
    # ablation: gate OFF entirely (uniform average / no selection) = chance
    "ungated_chance": chance,
}

os.makedirs(os.path.dirname(__file__) or ".", exist_ok=True)
with open(os.path.join(os.path.dirname(__file__), "result.json"), "w") as f:
    json.dump(res, f, indent=2)

def pct(x): return f"{x*100:5.1f}%"
r_on, u_on = res["reachable_trainedW"], res["unreachable_trainedW"]
r_ab, u_ab = res["reachable_randomW"],  res["unreachable_randomW"]
print("="*64)
print(f"chance (ungated / gate-OFF)          = {pct(chance)}")
print("-- gate ON (learned W, RPE-trained) --")
print(f"  reachable   gated_acc = {pct(r_on['gated_acc'])}  decoy={pct(r_on['gated_decoy_rate'])}")
print(f"  unreachable gated_acc = {pct(u_on['gated_acc'])}  decoy={pct(u_on['gated_decoy_rate'])}")
print("-- ABLATION: learned-W -> random-W (value destroyed) --")
print(f"  reachable   gated_acc = {pct(r_ab['gated_acc'])}")
print(f"  unreachable gated_acc = {pct(u_ab['gated_acc'])}")
print("-- form-priming baseline (cosine, no W) --")
print(f"  reachable   form_acc  = {pct(r_on['form_acc'])}  form_decoy={pct(r_on['form_decoy_rate'])}")
print(f"  unreachable form_acc  = {pct(u_on['form_acc'])}  form_decoy={pct(u_on['form_decoy_rate'])}")
print("="*64)
print(f"BIND lift (reachable-unreachable, gate ON) = {(r_on['gated_acc']-u_on['gated_acc'])*100:5.1f} pts")
print(f"gate causal (ON reachable - ablated random-W) = {(r_on['gated_acc']-r_ab['gated_acc'])*100:5.1f} pts")
