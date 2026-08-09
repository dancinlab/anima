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
