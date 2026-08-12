"""Upload this preregistered failed run to its private HF custody repository."""

import os

from huggingface_hub import HfApi


REPOSITORY = "dancinlab/anima-303m-r0-english-seed7-2026-08-12"


def main() -> None:
    token = os.environ["HF_TOKEN"]
    os.environ.setdefault("HF_XET_HIGH_PERFORMANCE", "1")
    api = HfApi(token=token)
    api.create_repo(REPOSITORY, repo_type="model", private=True, exist_ok=True)
    api.upload_large_folder(
        repo_id=REPOSITORY,
        repo_type="model",
        folder_path="/workspace/run",
    )
    info = api.model_info(REPOSITORY, files_metadata=True)
    if not info.private:
        raise RuntimeError("refusing public failed-run custody")
    print(info.sha, flush=True)


if __name__ == "__main__":
    main()
