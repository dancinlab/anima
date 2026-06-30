#!/usr/bin/env python3
"""EEG_CLM/hf_archive.py — 의식 기록 HF PUBLIC dataset 업로드 + 전용 collection.

archive_push.sh 가 호출 (hf CLI 버전 의존 제거, huggingface_hub 직접 사용).
HF=PUBLIC (사용자 명시 결정 2026-06-15) · 같은 path_in_repo 로 갱신(버전 누적, 새 파일/repo 아님).
전용 collection "anima-eeg-consciousness" (CLM/KOSMOS 버킷과 분리, a_hf_collections).
토큰 없으면 즉시 비-0 종료 (가짜 성공 없음).
"""
import os, sys
from huggingface_hub import (HfApi, create_repo, upload_file, upload_folder,
                             create_collection, add_collection_item, list_collections, whoami)

REPO = "dancinlab/anima-eeg-consciousness"
COLL_TITLE = "anima-eeg-consciousness"
NS = "dancinlab"

tok = os.environ.get("HF_TOKEN")
if not tok:
    p = os.path.expanduser("~/.cache/huggingface/token")
    tok = open(p).read().strip() if os.path.exists(p) else None
if not tok:
    print("[hf] 토큰 없음 — 중단 (가짜 성공 없음)"); sys.exit(1)

me = whoami(token=tok)["name"]
print(f"[hf] auth OK: {me}")

create_repo(REPO, repo_type="dataset", private=False, exist_ok=True, token=tok)
print(f"[hf] repo PUBLIC: {REPO}")

# 단일 누적 파일 — 같은 path 갱신(버전 누적)
for f, pir in [("EEG_CLM/consciousness.seq", "consciousness.seq"),
               ("EEG_CLM/consciousness.kosmos", "consciousness.kosmos"),
               ("EEG_CLM/music/music_eeg_result.txt", "music_eeg_result.txt")]:
    if os.path.exists(f):
        upload_file(path_or_fileobj=f, path_in_repo=pir, repo_id=REPO, repo_type="dataset", token=tok)
        print(f"[hf] ↑ {pir}")

# 폴더 (raw 녹음 + KOSMOS 음악 anchor)
for d, pir in [("EEG_CLM/recordings", "recordings"), ("EEG_CLM/kosmos_music", "kosmos_music")]:
    if os.path.isdir(d):
        upload_folder(folder_path=d, path_in_repo=pir, repo_id=REPO, repo_type="dataset", token=tok)
        print(f"[hf] ↑ {pir}/")

# 전용 collection 생성 + 등록
coll = next((c for c in list_collections(owner=me, token=tok) if c.title == COLL_TITLE), None)
if coll is None:
    coll = create_collection(title=COLL_TITLE, namespace=NS, exists_ok=True, token=tok)
add_collection_item(coll.slug, item_id=REPO, item_type="dataset", exists_ok=True, token=tok)
print(f"[hf] collection: {coll.slug}")
print(f"COLLECTION_SLUG={coll.slug}")
