import pytest


torch = pytest.importorskip("torch")

from core import clms


def _dual_fixture():
    torch.manual_seed(9888)
    module = clms.CLMSModule(
        d=12, V=16, n_slot=4, d_k=8, d_s=6, r=10,
        val_center=True, dual=True,
    ).double()
    batch = 2
    yn_q = torch.randn(batch, 12, dtype=torch.double)
    yn_a = torch.randn(batch, 12, dtype=torch.double)
    yn_b = torch.randn(batch, 12, dtype=torch.double)
    keys = torch.randn(batch, 4, 8, dtype=torch.double)
    pols = torch.tensor([[0, 1, 0, 1], [1, 0, 1, 0]])
    target_a = torch.tensor([0, 1])
    target_b = torch.tensor([1, 2])
    yn_op = torch.randn(batch, 12, dtype=torch.double)
    return module, yn_q, yn_a, yn_b, yn_op, keys, pols, target_a, target_b


def _canonical_fixture():
    torch.manual_seed(10010)
    module = clms.CLMSModule(
        d=12, V=16, n_slot=4, d_k=8, d_s=6, r=10,
        val_center=True, dual=True, pair_canonical=True,
    ).double()
    batch = 2
    yn_q = torch.randn(batch, 12, dtype=torch.double)
    yn_a = torch.randn(batch, 12, dtype=torch.double)
    yn_b = torch.randn(batch, 12, dtype=torch.double)
    yn_op = torch.randn(batch, 12, dtype=torch.double)
    keys = torch.randn(batch, 4, 8, dtype=torch.double)
    pols = torch.tensor([[0, 1, 0, 1], [1, 0, 1, 0]])
    return module, yn_q, yn_a, yn_b, yn_op, keys, pols


def test_dual_oracle_uses_both_target_slots():
    module, yn_q, yn_a, yn_b, yn_op, keys, pols, target_a, target_b = _dual_fixture()
    out, att = module(
        yn_q, keys, pols, oracle_slot=target_a, oracle_slot_b=target_b,
        need_att=True, yn_a=yn_a, yn_b=yn_b, yn_op=yn_op,
    )
    collapsed = module(
        yn_q, keys, pols, oracle_slot=target_a, oracle_slot_b=target_a,
        yn_a=yn_a, yn_b=yn_b, yn_op=yn_op,
    )

    assert att.shape == (2, 2, 4)
    assert not torch.allclose(out, collapsed)


def test_dual_address_loss_supervises_both_live_reads():
    module, yn_q, yn_a, yn_b, yn_op, keys, pols, target_a, target_b = _dual_fixture()
    _, att = module(yn_q, keys, pols, need_att=True, yn_a=yn_a, yn_b=yn_b, yn_op=yn_op)
    targets = torch.stack((target_a, target_b), dim=1)
    loss = torch.nn.functional.cross_entropy(att.reshape(-1, 4), targets.reshape(-1))
    loss.backward()

    assert att.shape == targets.shape + (4,)
    assert module.W_q.weight.grad is not None
    assert float(module.W_q.weight.grad.abs().sum()) > 0.0


def test_dual_oracle_rejects_missing_second_target():
    module, yn_q, yn_a, yn_b, yn_op, keys, pols, target_a, _ = _dual_fixture()
    with pytest.raises(ValueError, match="oracle_slot_b"):
        module(yn_q, keys, pols, oracle_slot=target_a, yn_a=yn_a, yn_b=yn_b,
               yn_op=yn_op)


def test_canonical_pair_uses_xor_identity_for_single_clue():
    module, yn_q, yn_a, yn_b, yn_op, keys, pols = _canonical_fixture()
    slot_one = torch.tensor([1, 0])
    slot_zero = torch.tensor([0, 1])

    single = module(
        yn_q, keys, pols, oracle_slot=slot_one, oracle_slot_b=slot_zero,
        yn_a=yn_a, yn_b=yn_b, yn_op=yn_op,
        pair_active=torch.zeros(2, dtype=torch.bool),
    )
    composed = module(
        yn_q, keys, pols, oracle_slot=slot_one, oracle_slot_b=slot_zero,
        yn_a=yn_a, yn_b=yn_b, yn_op=yn_op,
        pair_active=torch.ones(2, dtype=torch.bool),
    )

    # 1 xor identity(0) and 1 xor 0 occupy exactly the same learned value endpoint.
    assert torch.equal(single, composed)
    assert module.W_h.in_features == module.d_s + module.d_g
    assert clms.clms_weights_from_torch(module)["lane_type"] == 10


def test_canonical_pair_maps_exact_oracle_parity_to_existing_value_endpoints():
    module, yn_q, yn_a, yn_b, yn_op, keys, pols = _canonical_fixture()
    slot_one_a = torch.tensor([1, 0])
    slot_one_b = torch.tensor([3, 2])
    slot_zero = torch.tensor([0, 1])
    active = torch.ones(2, dtype=torch.bool)

    xor_zero = module(
        yn_q, keys, pols, oracle_slot=slot_one_a, oracle_slot_b=slot_one_b,
        yn_a=yn_a, yn_b=yn_b, yn_op=yn_op, pair_active=active,
    )
    unary_zero = module(
        yn_q, keys, pols, oracle_slot=slot_zero, oracle_slot_b=slot_zero,
        yn_a=yn_a, yn_b=yn_b, yn_op=yn_op,
        pair_active=torch.zeros(2, dtype=torch.bool),
    )

    # 1 xor 1 = 0, so composed inference cannot activate an unseen fusion region.
    assert torch.equal(xor_zero, unary_zero)


def test_canonical_pair_codec_roundtrip_preserves_lane_and_shapes():
    module, *_ = _canonical_fixture()
    weights = clms.clms_weights_from_torch(module)
    packed = clms.pack_clms(weights)
    restored, end = clms.read_clms(packed, 0, module.d, module.V)

    assert end == len(packed)
    assert restored["lane_type"] == 10
    assert restored["W_h"].shape == (module.d_s + module.d_g, module.r)
