"""Create an HF repo (private) — idempotent."""
import sys
from huggingface_hub import HfApi, create_repo

repo_id = sys.argv[1]
repo_type = sys.argv[2]  # "model" or "dataset"

api = HfApi()
try:
    url = create_repo(repo_id=repo_id, repo_type=repo_type, private=True, exist_ok=True)
    print(f"OK {repo_id} ({repo_type}) -> {url}")
except Exception as e:
    print(f"ERR {repo_id}: {e}", file=sys.stderr)
    sys.exit(1)
