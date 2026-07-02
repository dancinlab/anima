#!/usr/bin/env python3
# H_9110 chat-user consequence loop -- TRIPLE EXTRACTOR (data plumbing ONLY).
#
# Pure Python standard library only -- zero modelling, zero ML deps (engine-native
# grep gate stays clean). This file only slices a real dialogue corpus into
# (context, assistant-emit, real-human-next-response) triples; the .hexa harness then
# measures every signal on the LIVE core engine. Analogous to a corpus-prep script.
#
# Corpus: dancinlab/anima-corpus-ko-sns (HF cache), real turn-structured Korean SNS
# dialogue: lines `사용자: <text>` (human) alternate with `<persona>: <text>` (emit).
#
# Triple rule: an assistant-emit turn E immediately followed by a human turn R, with
# the nearest preceding human turn as context C:
#     ... 사용자: C ... PERSONA: E   사용자: R ...
#   -> (C=context, E=assistant-emit, R=real human next response, PERSONA tag).
# R is a real person's reaction to E in context C => EXOGENOUS (not anima-derivable).
#
# Output: triples.tsv  columns  ctx \t emit \t human_response \t persona
# (internal tabs/newlines stripped so the .hexa split parses byte-cleanly).

import sys, glob, os

USER = "사용자:"
CAP = 400  # keep the run light (mini-friendly)

def find_corpus():
    p = os.path.expanduser(
        "~/.cache/huggingface/hub/datasets--dancinlab--anima-corpus-ko-sns/"
        "snapshots/*/anima-corpus-ko-sns.txt")
    hits = glob.glob(p)
    return hits[0] if hits else None

def clean(s):
    return s.replace("\t", " ").replace("\r", " ").strip()

def speaker(line):
    if line.startswith(USER):
        return ("user", "사용자", line[len(USER):].strip())
    i = line.find(":")
    if 0 < i < 40:
        tag = line[:i].strip()
        if tag and all(ord(c) < 128 for c in tag):
            return ("persona", tag, line[i+1:].strip())
    return (None, "", "")

def main():
    path = find_corpus()
    if not path:
        sys.stderr.write("CORPUS NOT FOUND (anima-corpus-ko-sns)\n")
        sys.exit(2)
    with open(path, encoding="utf-8") as f:
        raw = [ln.rstrip("\n") for ln in f]
    parsed = [speaker(ln) for ln in raw]

    triples = []
    last_user_ctx = None
    for i in range(len(parsed) - 1):
        s, tag, txt = parsed[i]
        s1, tag1, txt1 = parsed[i+1]
        if s == "user":
            last_user_ctx = txt
        # emit E at i immediately followed by a real human turn R at i+1
        if s == "persona" and s1 == "user" and last_user_ctx is not None:
            C, E, R = clean(last_user_ctx), clean(txt), clean(txt1)
            if len(C) >= 2 and len(E) >= 2 and len(R) >= 1:
                triples.append((C, E, R, tag))
        if len(triples) >= CAP:
            break

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "triples.tsv")
    with open(out, "w", encoding="utf-8") as f:
        for C, E, R, tag in triples:
            f.write(C + "\t" + E + "\t" + R + "\t" + tag + "\n")
    sys.stderr.write("wrote %d triples -> %s\n" % (len(triples), out))

if __name__ == "__main__":
    main()
