---
id: RTSC_25
slug: cosn-dfpt
title: QE DFPT el-ph CoSn (baseline, magnetic) — λ/Tc NOT obtained in box, but two real findings — (1) `electron_phonon='interpolated'`/`'simple'` both REJECTED ("El-ph needs a DeltaVscf file") → el-ph is a TWO-PASS workflow; (2) QE 7.5 ph.x DOES support nspin=2 magnetic + ultrasoft DFPT (no nspin rejection). Blocker = DFPT linear-response cost on a 2.6× oversubscribed shared host (zero `iter #` after ~7min q=Γ).
domain: rtsc qe dft cosn kagome dfpt electron-phonon eliashberg superconductivity nspin
status_grade: 🟠 INCOMPLETE/DEFERRED (no λ/ω_log/Tc; ph.x feasibility characterized + workflow corrected; needs uncontended cores/pod)
verification_method: QE 7.5 ph.x (PHONON v.7.5) on summer pool, CPU-only, $0, nspin=2 US-PP, verbatim; p7; rbfe_hsp90 untouched+alive
since: 2026-06-14
sister: RTSC_21, RTSC_22, RTSC_13, RTSC_01
verdict: 🟠 DFPT el-ph for magnetic CoSn did NOT yield λ/Tc in the time-box. Two verbatim findings (RTSC/verdicts/cosn_dfpt.txt): **(1)** the prompt's `electron_phonon='interpolated'` ph.in is rejected at `phq_readin (1): El-ph needs a DeltaVscf file` — and `'simple'` gives the identical error → QE 7.5 el-ph is a **two-pass workflow** (pass-1 plain DFPT phonon with `fildvscf` builds DeltaVscf, pass-2 reads it). **(2)** ph.x **DOES** run nspin=2 (magnetic, total mag ~1.4–2 μB/cell) + ultrasoft DFPT — the plain pass-1 passed input validation, expanded the 2×2×2 q-grid → 4 irred. q-pts (12/12/18/18 irreps), and began the q=Γ linear-response solve. So "magnetic el-ph unsupported" is **REFUTED** for this build. **Blocker** = DFPT cost on a saturated host: 0 `iter #` printed after ~7 min on q=Γ while /proc/loadavg held ~31–34 on 12 cores (2.6× oversubscribed by two FOREIGN live QE doping jobs + rbfe, all left running). NO λ/ω_log/Tc fabricated.
---
# RTSC_25 — QE DFPT el-ph CoSn (baseline magnetic): λ/Tc deferred, ph.x feasibility characterized

## 측정 (QE 7.5 PHONON v.7.5, summer CPU, $0, verbatim · verdicts/cosn_dfpt.txt)
- system: prefix=cosn, ibrav=4 celldm(1)=9.9760 celldm(3)=0.80680, nat=6 (Co 3f + Sn 1a/2d), **nspin=2** (magnetic), US-PP (rrkjus_psl PBE), 93 val e⁻; converged 6×6×6 SCF reused (E_Fermi=14.7132 eV, RTSC_21).
- ph.in (prompt-spec, verbatim) `electron_phonon='interpolated'`, ldisp, nq=2 2 2, tr2_ph=1d-12, el_ph_sigma=0.005 nsigma=10.

## 발견 (2개, 둘 다 verbatim)
1. **el-ph 워크플로 정정** — `interpolated` AND `simple` 둘 다 `Error in routine phq_readin (1): El-ph needs a DeltaVscf file` 로 STOP. QE 7.5 el-ph = **2-pass**: ① 평범한 DFPT phonon(`fildvscf='dvscf'`, electron_phonon 미설정) 가 DeltaVscf 생성·저장 → ② ph.x `electron_phonon='interpolated'` 가 그 포텐셜을 읽어 fine el-ph k-mesh 에 보간. 프롬프트의 1-pass ph.in 은 구조적으로 불가.
2. **nspin=2 + ultrasoft DFPT 는 지원됨** — 평범한 pass-1 이 입력검증 통과 → magnetic wfc 읽음 → 2×2×2 q-grid 를 4 irred. q-pts(12/12/18/18 irreps)로 전개 → q=Γ(12 irreps, 18 modes) 선형응답 solve 시작. **"자성 금속 el-ph 미지원" 가설 REFUTE**(이 빌드 한정). (단 자성 금속 double-delta 정확도는 훨씬 촘촘한 el-ph k-mesh 필요 — 미수행.)

## 블로커 (실제) — DFPT 선형응답 비용 × 공유호스트 포화
- q=Γ ~7분 후 self-consistent linear-response `iter #` **0회** 인쇄(첫 repr 한 번도 수렴 못 함).
- /proc/loadavg = 31.37 / 33.00 / 34.42 (12-core, **2.6× 초과구독**) — 타 세션의 **외부 live QE 잡 2개**(doping nscf + scf_q4.0 sweep) + rbfe 코테넌트가 내 ph.x ranks 를 거의 0 throughput 로 시분할(a_dont_kill_live_compute 따라 전부 그대로 둠). 6-atom 자성금속 × 4 q-pts × 12–18 irreps × nspin=2 US 자기일관 선형응답 = ~40분 박스 초과.

## 결론
🟠 **λ/ω_log/Tc 미산출** — 하지만 진짜 두 발견 확보: (1) el-ph 2-pass(DeltaVscf) 필수 — 프롬프트 ph.in 정정, (2) QE 7.5 ph.x 가 자성 ultrasoft DFPT 를 **돌린다**(nspin 거부 아님). 박스 내 미완 원인은 메커니즘/지원 한계가 아니라 **포화 공유호스트의 DFPT 선형응답 비용**. 정직(p7): λ/Tc 어떤 값도 조작 안 함. **완료 경로**(미수행): 비경쟁 코어/pod → ① dense el-ph SCF → ② `fildvscf` plain DFPT 로 DeltaVscf 생성(2×2×2 q) → ③ `interpolated` pass 로 fine el-ph k-mesh el-ph → ④ a2F summary 에서 λ/ω_log/Allen-Dynes Tc(μ*=0.10). 자성 + E_F 의 Co-3d flat band(RTSC_21) 때문에 el-ph 적분 민감 → nspin=1 control + el-ph k-mesh 수렴 권고.
verdict: `RTSC/verdicts/cosn_dfpt.txt`
