"""Regression guards for memory-bounded CLM int4 block loading."""
from __future__ import annotations

import struct

import numpy as np

import decode


def _serialized_block(codes: np.ndarray, scales: np.ndarray) -> bytes:
    cout, rest = codes.shape
    flat = (codes.reshape(-1).astype(np.int16) + 8).astype(np.uint8)
    if len(flat) % 2:
        flat = np.concatenate((flat, np.array([8], dtype=np.uint8)))
    packed = flat[0::2] | (flat[1::2] << 4)
    return (
        struct.pack("<II", cout, rest)
        + packed.tobytes()
        + np.asarray(scales, dtype="<f4").tobytes()
    )


def test_load_block_matches_legacy_values_and_orientation():
    codes = np.array([
        [-8, -7, -1, 0, 1],
        [2, 3, 4, 6, 7],
        [7, 0, -8, 5, -3],
    ], dtype=np.int8)
    scales = np.array([0.25, -1.5, 0.03125], dtype=np.float32)
    payload = _serialized_block(codes, scales)

    wt, off = decode._load_block(payload, 0)
    legacy = (codes.astype(np.float64) * scales.astype(np.float64)[:, None]).T.copy()

    assert off == len(payload)
    assert wt.flags.c_contiguous
    assert wt.shape == (codes.shape[1], codes.shape[0])
    assert np.array_equal(wt, legacy)


def test_load_block_ignores_padding_nibble_for_odd_element_count():
    codes = np.array([[-8, 0, 7]], dtype=np.int8)
    scales = np.array([2.0], dtype=np.float32)
    payload = _serialized_block(codes, scales)
    wt, off = decode._load_block(payload, 0)

    assert off == len(payload)
    assert np.array_equal(wt[:, 0], np.array([-16.0, 0.0, 14.0]))
