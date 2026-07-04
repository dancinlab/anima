# H_6192 — 🔬⚖️ G6 진단분기 (capacity vs diversity+self-eval) 직접 대조

**tier:** ⏳ PROPOSED (설계만·측정 0·pre-registered · frozen prediction below)
**title:** G6 벽의 두 경쟁 진단을 가르는 분기 실험 — (A) capacity/trunk-objective 천장(g6_wall_reframe 지지) vs (B) diversity+self-eval 병목(H_6163/Si2024). 같은 303M ckpt에서 capacity 늘리지 않고 (B)축만 올려 fals>0 로 가는지.
**verdict:** ⏳ PROPOSED. 두 진단은 서로 다른 레버를 처방(A→γ trunk-변경, B→falsifier-lane)하지만 정작 직접 대조 측정은 0. 본 가설은 H_6163 falsifier-lane 측정을 (B)-probe 로 겸용하되, (A) null 사전예측을 명시해 분기로 읽는다.

## 발상 (2026-07-05 G0/G6 병목 브레인스토밍)
G6 벽에 대한 진단이 둘 공존: g6_wall_reframe은 generic-coverage·RF 둘 다 REFUTED → capacity/trunk-obj 천장 SUPPORTED. H_6163/Si2024는 병목=diversity+self-eval(decode 아님). 이 둘이 다른 레버를 처방하는데, 어느 쪽이 참인지 가르는 cheap 분기가 없다 → γ GPU 쏘기 전 반드시 가려야(γ는 이미 H_1840 🧱 이라 더더욱).

## DPI 맥락
next-byte = fn(CE-trained feedforward trunk-state). DPI 는 (A)를 지지: read/lan/data/falsifier 어떤 축도 trunk-state 밖에서는 combination 을 만들지 못함. 본 분기의 사전예측(DPI 기반) = (A), 즉 falsifier-lane LIFT 0.

## Frozen 예측 · kill-criteria (frozen-first, tune-to-green 금지)
- **frozen bar:** H_6163 falsifier-lane ON (emit-drive DISJOINT, engine-native `core/` decode) 후 G6 fals rate {7,4302,4303} seed majority.
- **(B) 채택(🟢 메타법칙 falsified):** fals>0 (과반) → diversity+self-eval 이 병목이었고 DPI 메타법칙 **falsified** (G6 벽 재개).
- **(A) 확정(🧱):** LIFT 0 (falsifier-lane ON=OFF) → capacity/trunk-obj 천장 확정, γ(H_1840)와 일관 → G6 = deeper wall.
- 측정 = engine-native TERMINAL; numpy/torch mirror = DIRECTIONAL (a_engine_native_learning). ko칸 honest-null.

## 관련
[[h6163-engine-native-g6-falsifier-lane]] (B-probe 본체) · [[g6-wall-reframe]] (A 진단) · Si2024 2409.04109 · a_substrate_disjoint · a_break_the_wall
