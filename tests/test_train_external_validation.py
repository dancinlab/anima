import importlib.util
import os
import sys
import tempfile
import unittest


TORCH_AVAILABLE = importlib.util.find_spec("torch") is not None


def _import_train():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for part in (os.path.join(root, "core"), os.path.join(root, "cli")):
        if part in sys.path:
            sys.path.remove(part)
        sys.path.insert(0, part)
    sys.modules.pop("train", None)
    import train
    return train


@unittest.skipUnless(TORCH_AVAILABLE, "PyTorch training extra is not installed")
class ExternalValidationCellTest(unittest.TestCase):
    def test_explicit_validation_file_is_disjoint_and_train_file_is_not_truncated(self):
        import torch

        train = _import_train()
        with tempfile.TemporaryDirectory() as directory:
            train_path = os.path.join(directory, "train.bytes")
            validation_path = os.path.join(directory, "validation.bytes")
            with open(train_path, "wb") as fh:
                fh.write(b"T" * 128)
            with open(validation_path, "wb") as fh:
                fh.write(b"V" * 96)

            cell = train.ByteCell(train_path, val_frac=0.5,
                                  validation_path=validation_path)
            self.assertEqual(cell.train_end, 128)
            self.assertEqual(cell.val_size, 96)
            x_train, y_train = cell.window(16, torch.Generator().manual_seed(1))
            x_val, y_val = cell.val_window(16, torch.Generator().manual_seed(2))
            self.assertEqual(set(x_train.tolist() + y_train.tolist()), {ord("T")})
            self.assertEqual(set(x_val.tolist() + y_val.tolist()), {ord("V")})
            cell.close()
            self.assertTrue(cell._f.closed)
            self.assertTrue(cell._val_f.closed)

    def test_legacy_tail_validation_keeps_existing_split_behavior(self):
        import torch

        train = _import_train()
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "combined.bytes")
            with open(path, "wb") as fh:
                fh.write(b"T" * 64 + b"V" * 64)

            cell = train.ByteCell(path, val_frac=0.5)
            self.assertEqual(cell.train_end, 64)
            self.assertEqual(cell.val_size, 64)
            x_val, _ = cell.val_window(16, torch.Generator().manual_seed(3))
            self.assertEqual(set(x_val.tolist()), {ord("V")})
            cell.close()


if __name__ == "__main__":
    unittest.main()
