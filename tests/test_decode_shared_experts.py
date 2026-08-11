import numpy as np

from core import decode


def test_shared_expert_im2col_matches_independent_convs_exactly():
    rng = np.random.default_rng(7)
    T, d, K, E = 5, 4, 3, 3
    x = rng.standard_normal((T, d))
    weights = [rng.standard_normal((d * K, d)) for _ in range(E)]
    biases = [rng.standard_normal(d) for _ in range(E)]

    previous = np.stack([
        decode.nn_gelu_fwd(decode._conv1d(x, w, b, T, d, d, K, 1, np), np)
        for w, b in zip(weights, biases)
    ])
    xcol = decode._conv1d_im2col(x, T, d, K, 1, np)
    packed = np.empty((E, T, d), dtype=np.float64)
    for expert, (weight, bias) in enumerate(zip(weights, biases)):
        packed[expert] = decode._conv1d_from_im2col(xcol, weight, bias)
    packed = decode.nn_gelu_fwd(packed, np).reshape(E, T, d)

    np.testing.assert_array_equal(packed, previous)


def test_shared_im2col_preserves_dilated_causal_padding():
    x = np.arange(20, dtype=np.float64).reshape(5, 4)
    weight = np.arange(48, dtype=np.float64).reshape(12, 4) / 10.0
    bias = np.arange(4, dtype=np.float64)

    expected = decode._conv1d(x, weight, bias, 5, 4, 4, 3, 2, np)
    xcol = decode._conv1d_im2col(x, 5, 4, 3, 2, np)
    actual = decode._conv1d_from_im2col(xcol, weight, bias)

    np.testing.assert_array_equal(actual, expected)
