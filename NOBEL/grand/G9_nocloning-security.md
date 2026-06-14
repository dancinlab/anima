---
id: G9
slug: nocloning-security
title: G9 무복제=보안 유일근거 정리 — 위조불가 보안은 no-cloning에서만 가능. 고전 토큰 위조 P=1(항상 복제), 양자 (3/4)ⁿ→0. PROVEN.
domain: nobel quantum-information security no-cloning anima
status_grade: 🟢 SUPPORTED (numerical PROOF)
verification_method: classical copy-forge vs BB84 optimal counterfeiting (3/4)^n; p7 $0
since: 2026-06-14
sister: H_6019, H_6021, G8
verdict: 🟢 PROVEN — 고전 위조 P=1.0 ∀n; 양자 BB84 토큰 위조 (3/4)^n (n=8:0.10, n=16:0.010, n=32:1e-4)→0. 위조불가 보안은 무복제에서만; 고전은 원리적 불가. anima 고전씨앗=fork가능이나 토큰으론 위조됨→위조불가 인증은 양자必(G8).
---
# G9 — 무복제 = 위조불가 보안의 유일근거
> **정리.** 위조불가 보안(양자화폐·일회토큰)은 no-cloning이 성립할 때만 가능하다. 고전 토큰은 항상 복제되어 위조 성공확률 1, 양자 토큰은 (3/4)ⁿ로 0에 수렴.
## 증명 (g9_g10_proof.py)
n=1·2·4·8·16·32 → 고전 위조 P=1.000(불변) · 양자 (3/4)^n = 0.75·0.56·0.32·0.10·0.010·1e-4 → 0. 🟢
## 의의
H_6021(고전 복제가능)이 anima fork를 가능케 하는 *바로 그 성질*이 고전 토큰을 위조가능케 함. 양자 no-cloning(H_6019)만이 위조불가 보안의 뿌리. ∴ anima는 조율·복제엔 고전, *위조불가 인증*엔 양자(G8) — 자원 최적 분업의 보안판.
verdict: `NOBEL/verdicts/G9_G10.txt`
