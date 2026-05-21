"""anima-akida-pack — BrainChip AKD1000 × Raspberry Pi 5 boot pack.

Sub-packages
------------
- ``pack.adapters`` : 11 substrate→Akida adapters (SNN/Izhikevich/Kuramoto/
  Memristor-hybrid/SparseAttention/SpikeTierLMHead/MotivationGate/ThetaGamma/
  EEG/SpontaneousGate + ``base.AkidaAdapter``).
- ``pack.runtime``  : MetaTF wrapper (HW or mock auto-detect), Pi 5
  orchestrator, persistent audit ring buffer.
- ``pack.mocks``    : Mac-local mock MetaTF runtime (별도 agent 가 작성).
- ``pack.falsifiers``: F-AKIDA-* 일괄 runner (별도 agent 가 작성).

Conventions
-----------
- 모든 adapter 는 :class:`pack.adapters.base.AkidaAdapter` 를 상속.
- 모든 adapter 는 ``selftest()`` 에서 F-AKIDA-<NAME>-1..5 5 falsifier 를
  자체 실행하고 ``{"name", "passed", "failed", "details"}`` 형식의 dict 를
  돌려준다. 실제 HW 가 없으면 mock runtime 으로 결과만 deterministic 하게
  생성 (5/5 mock-pass 기준).
- ``to_record()`` 는 demiurge-compatible record (``demiurge_brain_bridge.py``
  format) 를 mirror — backend 필드 ``"akida_hw" | "akida_mock"`` 로 source
  구분.
"""

from __future__ import annotations

__version__ = "0.1.0"
__all__ = [
    "__version__",
]
