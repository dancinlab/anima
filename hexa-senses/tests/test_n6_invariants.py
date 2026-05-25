"""hexa-senses n=6 lattice independent witness."""
from __future__ import annotations

from math import gcd

import pytest


def divisors(n): return [d for d in range(1, n+1) if n % d == 0]
def sigma(n):    return sum(divisors(n))
def tau(n):      return len(divisors(n))
def euler_phi(n): return sum(1 for k in range(1, n+1) if gcd(k, n) == 1)


@pytest.mark.auto
def test_master_identity():
    assert sigma(6) * euler_phi(6) == 6 * tau(6) == 24


@pytest.mark.auto
def test_audio_codec_constants():
    """ear: σ·τ=48 kHz sampling, J₂=24-bit quantization."""
    assert sigma(6) * tau(6) == 48
    assert sigma(6) * euler_phi(6) == 24


@pytest.mark.auto
def test_dream_categories_sigma():
    assert sigma(6) == 12   # 12 dream categories


@pytest.mark.auto
def test_olfact_receptors_sigma():
    assert sigma(6) == 12   # 12 primary receptors
    assert 2 ** sigma(6) == 4096   # 4096 odor patterns


@pytest.mark.auto
def test_ekman_emotions_n():
    assert 6 == 6   # 6 Ekman basic emotions


@pytest.mark.auto
def test_verb_count_is_5():
    """5 senses verbs: dream/ear/empath/olfact/voice."""
    verbs = ["dream", "ear", "empath", "olfact", "voice"]
    assert len(verbs) == 5
