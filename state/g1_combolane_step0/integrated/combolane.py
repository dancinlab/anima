#!/usr/bin/env python3
"""
H_9129 STEP-0 — 재조합(G1)을 뇌의 조합-substrate 3부품으로 검증 (numpy toy, DIRECTIONAL).

프레임(fable 가설): 재조합은 언어산출부(mouth/Broca) 속성이 아니다.
  PFC working-memory 변수-binding(role↔filler)  →
  기저핵 gate(어느 결합 선택, Go/NoGo)          →
  해마 pattern-completion(저장관계로 novel 완성)  →
  mouth 는 이 조합-lane 상태를 READOUT(읽기만, target 아님)

★ 속일수없는 BIND 시험 (g1g6 form-priming 방어):
  held-out pair 를 reachable(저장/binding 사슬로 완성가능) vs
  unreachable(관계그래프에 완성경로 없음)로 분리 —
  둘 다 같은 표면형태(color 토큰 → 2-hop → size 토큰)의 held-out novel pair.
  form 이면  reachable ≈ unreachable
  진짜조합이면 reachable 만 lift.

★ 부품별 ablation 3회: bind OFF / gate OFF / completion OFF
  → 조합 붕괴하는 부품이 인과(causal), 안 붕괴하면 INERT(기여 0).

과제 = 2-hop 관계합성 (진짜 recombination):
  저장(해마 M) 은 triple (item ⊛ rel ⊛ next) 만 저장.
  R1: color --HAS--> material ,  R2: material --NEEDS--> size
  reachable query: color 로 size 를 물음. (color,size) pair 는 저장 안됨(novel).
     오직 color→material→size 두 저장 edge 를 CHAIN 해야 도달 = 재조합.
  unreachable query: color→material(R1) 은 있으나 그 material 에 R2 edge 없음(dangling).
     표면형태 동일(color→2hop→size)이나 그래프에 완성경로 없음.
  decoy relation(D1,D2): 같은 item 에서 나가는 딴 edge → gate 가 골라야 함.

VSA/HRR: bind=circular convolution(FFT), unbind=inverse conv, cleanup=nearest-neighbor.
"""
import numpy as np
import json, sys

D = 512          # hypervector dim
N_COLOR = 24
N_MAT   = 24
N_SIZE  = 24
SEEDS   = list(range(12))

def make_vec(rng, n):
    v = rng.standard_normal((n, D))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    return v

def bind(a, b):            # circular convolution
    return np.fft.irfft(np.fft.rfft(a) * np.fft.rfft(b), n=D)

def inv(a):                # involution inverse for circ-conv: reverse
    return np.concatenate([a[:1], a[1:][::-1]])

def unbind(mem, key):      # mem ⊛ inv(key)
    return bind(mem, inv(key))

def cleanup(v, codebook):  # nearest neighbor (pattern completion)
    sims = codebook @ (v / (np.linalg.norm(v) + 1e-9))
    idx = int(np.argmax(sims))
    return idx, float(sims[idx]), codebook[idx]

def run_seed(seed):
    rng = np.random.default_rng(seed)
    COLOR = make_vec(rng, N_COLOR)
    MAT   = make_vec(rng, N_MAT)
    SIZE  = make_vec(rng, N_SIZE)
    # roles
    R1, R2, D1, D2 = make_vec(rng, 4)

    # --- build relational graph (stored edges) ---
    # R1: color_i -> material_{a(i)}   (every color has an R1 edge)
    a = rng.permutation(N_MAT)[:N_COLOR] % N_MAT
    # decoy D1: color_i -> material_{ad(i)} (wrong branch, must be gated out)
    ad = rng.permutation(N_MAT)[:N_COLOR] % N_MAT
    # R2: material_m -> size_{b(m)} — but only for SOME materials (reachability!)
    #   materials with an R2 edge = "connected"; without = "dangling"
    connected_mat = set(rng.permutation(N_MAT)[:N_MAT // 2].tolist())
    b = rng.permutation(N_SIZE)[:N_MAT] % N_SIZE
    # decoy D2: material_m -> size_{bd(m)}
    bd = rng.permutation(N_SIZE)[:N_MAT] % N_SIZE

    # --- store memory M = Σ (item ⊛ rel ⊛ next), triples only (never color⊛size) ---
    M = np.zeros(D)
    for i in range(N_COLOR):
        M += bind(bind(COLOR[i], R1), MAT[a[i]])     # color--R1-->material
        M += bind(bind(COLOR[i], D1), MAT[ad[i]])    # color--D1-->material (decoy)
    for m in range(N_MAT):
        if m in connected_mat:
            M += bind(bind(MAT[m], R2), SIZE[b[m]])   # material--R2-->size
        M += bind(bind(MAT[m], D2), SIZE[bd[m]])      # material--D2-->size (decoy, all)
    M /= np.linalg.norm(M) + 1e-9

    # reachable colors: R1 target material is R2-connected  → chain color->mat->size exists
    reach_colors   = [i for i in range(N_COLOR) if a[i] in connected_mat]
    # unreachable colors: R1 target material has NO R2 edge (dangling)
    unreach_colors = [i for i in range(N_COLOR) if a[i] not in connected_mat]

    def gold_size(i):        # ground-truth via composition color->mat(a)->size(b)
        return b[a[i]]

    # ---------------- pipeline (parametrized by ablations) ----------------
    def pipeline(i, use_bind=True, use_gate=True, use_completion=True):
        c = COLOR[i]
        # ---- HOP 1: color --R1--> material ----
        if not use_bind:
            key1 = c                                   # no role binding
        elif not use_gate:
            role1 = (R1 + D1 + R2 + D2)                # bind but no selection
            role1 = role1 / np.linalg.norm(role1)
            key1 = bind(c, role1)
        else:
            key1 = bind(c, R1)                         # PFC bind: selected role R1
        raw_mat = unbind(M, key1)
        if use_completion:
            m_idx, _, mat_vec = cleanup(raw_mat, MAT)  # hippocampal completion
        else:
            m_idx, mat_vec = None, raw_mat             # skip completion: raw noisy vec
        # ---- HOP 2: material --R2--> size ----
        if not use_bind:
            key2 = mat_vec
        elif not use_gate:
            role2 = (R1 + D1 + R2 + D2)
            role2 = role2 / np.linalg.norm(role2)
            key2 = bind(mat_vec, role2)
        else:
            key2 = bind(mat_vec, R2)
        raw_size = unbind(M, key2)
        # ---- MOUTH READOUT (read-only cleanup to a size symbol) ----
        s_idx, s_conf, _ = cleanup(raw_size, SIZE)     # mouth names the lane state
        return s_idx

    def acc(colors, **kw):
        if not colors:
            return float('nan'), 0
        hit = sum(1 for i in colors if pipeline(i, **kw) == gold_size(i))
        return hit / len(colors), len(colors)

    res = {
        'n_reach': len(reach_colors), 'n_unreach': len(unreach_colors),
        'full_reach':   acc(reach_colors)[0],
        'full_unreach': acc(unreach_colors)[0],
        'bindoff_reach':   acc(reach_colors, use_bind=False)[0],
        'bindoff_unreach': acc(unreach_colors, use_bind=False)[0],
        'gateoff_reach':   acc(reach_colors, use_gate=False)[0],
        'gateoff_unreach': acc(unreach_colors, use_gate=False)[0],
        'compoff_reach':   acc(reach_colors, use_completion=False)[0],
        'compoff_unreach': acc(unreach_colors, use_completion=False)[0],
    }
    # chance = 1/N_SIZE
    res['chance'] = 1.0 / N_SIZE
    return res

def main():
    rows = [run_seed(s) for s in SEEDS]
    keys = [k for k in rows[0] if k != 'chance']
    agg = {k: float(np.nanmean([r[k] for r in rows])) for k in keys}
    agg['chance'] = rows[0]['chance']
    agg['seeds'] = len(SEEDS)
    agg['dim'] = D

    r_full, u_full = agg['full_reach'], agg['full_unreach']
    gap = r_full - u_full
    # form-fooled iff reachable ~= unreachable in full pipeline
    fooled_by_form = abs(gap) < 0.10

    # ablation causality: does removing a part collapse reachable toward chance?
    def collapse(part):
        drop = r_full - agg[f'{part}_reach']
        # causal if reachable drops by a meaningful margin toward chance/unreachable
        return drop, ('CAUSAL' if drop > 0.15 else 'INERT')
    ab = {p: collapse(p) for p in ['bindoff', 'gateoff', 'compoff']}

    out = {
        'agg': agg,
        'gap_reach_minus_unreach': gap,
        'fooled_by_form': fooled_by_form,
        'ablation': {p: {'reach_drop': ab[p][0], 'verdict': ab[p][1]} for p in ab},
        'per_seed': rows,
    }
    print(json.dumps(out, indent=2))
    with open('result.json', 'w') as f:
        json.dump(out, f, indent=2)

    # human summary
    print('\n=== SUMMARY (mean over %d seeds, D=%d, chance=%.3f) ===' % (
        agg['seeds'], D, agg['chance']), file=sys.stderr)
    print('FULL   reachable=%.3f  unreachable=%.3f  gap=%.3f  fooled_by_form=%s' % (
        r_full, u_full, gap, fooled_by_form), file=sys.stderr)
    for p in ['bindoff', 'gateoff', 'compoff']:
        print('%-9s reachable=%.3f  (drop %.3f)  -> %s' % (
            p, agg[f'{p}_reach'], ab[p][0], ab[p][1]), file=sys.stderr)

if __name__ == '__main__':
    main()
