import importlib.util
import os
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = (ROOT / "state" / "anima_303m_r0_conversation_2026_08_12" /
                "build_dataset.py")


def _builder():
    spec = importlib.util.spec_from_file_location("r0_conversation_builder", BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ConversationDatasetBuilderTest(unittest.TestCase):
    def test_normalization_and_validation_wins_cross_cell_duplicate(self):
        builder = _builder()
        self.assertEqual(builder.normalized_document("  한글\n 대화  "), "한글 대화")
        with tempfile.TemporaryDirectory() as directory:
            registry = builder.DocumentRegistry(os.path.join(directory, "docs.sqlite3"))
            registry.add("en_general", "train", "same document")
            registry.add("en_dialogue", "validation", "same\n document")
            registry.add("en_general", "train", "unique train")
            registry.commit()
            report = registry.write_cells(directory, ["en_general", "en_dialogue"])
            self.assertEqual(report["en_general"]["train"]["documents"], 1)
            self.assertEqual(report["en_dialogue"]["validation"]["documents"], 1)
            self.assertEqual(registry.overlap(), 0)
            audit = registry.near_duplicate_audit(limit=10)
            self.assertEqual(audit["policy"], "report_only")
            self.assertEqual(audit["sample_size"], 2)
            removed = registry.remove_contamination(["unique train"])
            self.assertEqual(len(removed), 1)
            self.assertEqual(registry.contamination(["unique train"]), [])
            registry.close()

    def test_role_preserving_registry_keeps_chat_turn_boundaries(self):
        builder = _builder()
        with tempfile.TemporaryDirectory() as directory:
            registry = builder.DocumentRegistry(
                os.path.join(directory, "docs.sqlite3"), preserve_role_lines=True)
            registry.add("dialogue", "train", "user:  안녕\nassistant:  반가워")
            registry.commit()
            registry.write_cells(directory, ["dialogue"])
            text = Path(directory, "dialogue.train.txt").read_text(encoding="utf-8")
            self.assertEqual(text, "user: 안녕\nassistant: 반가워\n\n")
            registry.close()

    def test_oasst_selects_reviewed_human_lowest_rank_path(self):
        builder = _builder()
        base = {"lang": "en", "review_result": True, "deleted": False,
                "synthetic": False, "labels": None}
        rows = [
            dict(base, message_id="root", parent_id=None, role="prompter", text="Question"),
            dict(base, message_id="worse", parent_id="root", role="assistant",
                 text="Worse", rank=1),
            dict(base, message_id="best", parent_id="root", role="assistant",
                 text="Best answer", rank=0),
            dict(base, message_id="synthetic", parent_id="root", role="assistant",
                 text="Synthetic", rank=0, synthetic=True),
        ]
        self.assertEqual(builder.oasst_best_documents(rows),
                         ["user: Question\nassistant: Best answer"])

    def test_oasst_turn_documents_retains_all_branches_and_complete_suffixes(self):
        builder = _builder()
        base = {"lang": "en", "review_result": True, "deleted": False,
                "synthetic": False, "labels": None}
        rows = [
            dict(base, message_id="root", parent_id=None, role="prompter", text="Question"),
            dict(base, message_id="a", parent_id="root", role="assistant", text="First answer"),
            dict(base, message_id="u", parent_id="a", role="prompter", text="Follow up"),
            dict(base, message_id="b", parent_id="u", role="assistant", text="Second answer"),
            dict(base, message_id="alt", parent_id="root", role="assistant", text="Alternative"),
        ]

        documents, stats = builder.oasst_turn_documents(rows, max_bytes=70)

        self.assertEqual(documents, [
            "user: Question\nassistant: First answer",
            "user: Question\nassistant: Alternative",
            "user: Follow up\nassistant: Second answer",
        ])
        self.assertEqual(stats["eligible_assistant_rows"], 3)
        self.assertEqual(stats["fitting_assistant_turns"], 3)
        self.assertEqual(stats["serialized_assistant_turns"], 3)
        self.assertEqual(stats["coverage"], 1.0)

    def test_oasst_turn_documents_reports_target_pair_that_cannot_fit(self):
        builder = _builder()
        base = {"lang": "en", "review_result": True, "deleted": False,
                "synthetic": False, "labels": None}
        rows = [
            dict(base, message_id="root", parent_id=None, role="prompter", text="Question"),
            dict(base, message_id="a", parent_id="root", role="assistant", text="x" * 100),
        ]

        documents, stats = builder.oasst_turn_documents(rows, max_bytes=40)

        self.assertEqual(documents, [])
        self.assertEqual(stats["target_pair_oversize"], 1)
        self.assertEqual(stats["fitting_assistant_turns"], 0)

    def test_klue_excludes_impossible_and_empty_answers(self):
        builder = _builder()
        rows = [
            {"question": "정답은?", "answers": {"text": ["보라색"]},
             "is_impossible": False},
            {"question": "없는 답", "answers": {"text": ["오답"]},
             "is_impossible": True},
            {"question": "빈 답", "answers": {"text": []}, "is_impossible": False},
        ]
        self.assertEqual(builder.klue_documents(rows),
                         ["user: 정답은?\nassistant: 보라색"])

    def test_instruction_documents_require_both_roles_and_keep_context(self):
        builder = _builder()
        rows = [
            {"instruction": "요약해 줘", "input": "비가 와요.", "output": "비가 옵니다."},
            {"instruction": "빈 답", "input": "", "output": ""},
            {"instruction": "", "input": "", "output": "무시"},
        ]
        self.assertEqual(
            builder.instruction_documents(rows),
            ["user: 요약해 줘\n비가 와요.\nassistant: 비가 옵니다."],
        )

    def test_instruction_documents_preserve_real_korean_multiturn_trajectory(self):
        builder = _builder()
        rows = [{"messages": [
            {"role": "user", "content": "고양이 이름은 나비야. 기억해 줘."},
            {"role": "assistant", "content": "나비라고 기억할게요."},
            {"role": "user", "content": "고양이 이름이 뭐였지?"},
            {"role": "assistant", "content": "나비예요."},
        ]}]

        self.assertEqual(builder.instruction_documents(rows), [
            "user: 고양이 이름은 나비야. 기억해 줘.\n"
            "assistant: 나비라고 기억할게요.\n"
            "user: 고양이 이름이 뭐였지?\n"
            "assistant: 나비예요."
        ])

    def test_dialogue_coverage_distinguishes_single_and_multiturn(self):
        builder = _builder()
        with tempfile.TemporaryDirectory() as directory:
            registry = builder.DocumentRegistry(
                os.path.join(directory, "docs.sqlite3"), preserve_role_lines=True)
            registry.add("ko_dialogue", "train", "user: 하나\nassistant: 답")
            registry.add("ko_dialogue", "train",
                         "user: 기억해\nassistant: 네\nuser: 뭐였지\nassistant: 기억")
            registry.commit()

            coverage = registry.dialogue_coverage(["ko_dialogue"])["ko_dialogue"]

            self.assertEqual(coverage["documents"], 2)
            self.assertEqual(coverage["single_turn_documents"], 1)
            self.assertEqual(coverage["multiturn_documents"], 1)
            self.assertEqual(coverage["assistant_turns"], 3)
            registry.close()


if __name__ == "__main__":
    unittest.main()
