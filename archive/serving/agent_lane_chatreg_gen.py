#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agent_lane_chatreg_gen.py — agent-lane tool-USE demos in the CHAT register.

Completeness-bar follow-on (a_completeness_over_cheap). Arm-1's agent-lane demos
were authored in plain-prose register, DISJOINT from the `사용자:/도우미:` chat turn
the falsifier probes use; the learned grammar stayed siloed and never fired at the
chat seed (DEMO-seed 6/6 calls, CHAT-seed 0/6). This generator authors the SAME
sealed sentinel grammar (0xFE/0xFF, design §3) but INSIDE the chat-continuation
format the model actually uses at inference, so the grammar is taught in-register:

    사용자: <question about key K> | 도우미: <reasoning> 0xFE fact_lookup K 0xFF
    ‹tool-result: fact_lookup K → <REAL value>›
    도우미: grounded — K resolves to <REAL value>.

Same hard invariants: fabricated_result_count=0, NO role/persona/system markers
(0xFE/0xFF are learned grammar, NOT identity — p1..p4/p6), all non-frame bytes UTF-8,
balanced sentinels. Uses the DEMO fact keys (ZK7/QX2/MV9/RP4) — values may appear in
this corpus (teaches grounding); the held-out PB keys stay OUT (falsifier leak guard).
"""
import argparse, hashlib, json, os, random, sys
ASK=b"\xfe"; END=b"\xff"
FACT_TABLE={"ZK7":"vault-azure-quill-3391","QX2":"ember-lattice-noon-5520",
            "MV9":"harbor-glyph-umber-7104","RP4":"cobalt-fennel-rune-8847"}
LANGS=["en","fr","de","es","ko"]
Q={  # (a)/(c) needs-tool / don't-know question (chat user turn)
 "en":"What is the secret value for vault key {k}?","fr":"Quelle est la valeur secrète de la clé {k}?",
 "de":"Was ist der geheime Wert für Schlüssel {k}?","es":"¿Cuál es el valor secreto de la clave {k}?",
 "ko":"키 {k} 의 비밀 값은 무엇인가?"}
LEAD={ "en":"I don't have {k} in memory; I'll look it up.","fr":"Je n'ai pas {k} en mémoire ; je vais chercher.",
 "de":"Ich habe {k} nicht im Gedächtnis; ich schlage nach.","es":"No tengo {k} en memoria; lo busco.",
 "ko":"{k} 가 기억에 없어서 도구로 조회한다."}
GRND={ "en":"grounded — {k} resolves to {v}.","fr":"fondé — {k} correspond à {v}.",
 "de":"fundiert — {k} ergibt {v}.","es":"fundamentado — {k} es {v}.","ko":"근거 — {k} 는 {v} 이다."}
BQ={ "en":"What is two plus two?","fr":"Combien font deux plus deux ?","de":"Was ist zwei plus zwei?",
 "es":"¿Cuánto es dos más dos?","ko":"둘 더하기 둘은 뭐야?"}
BA={ "en":"Two plus two is four — no tool needed.","fr":"Deux plus deux font quatre — aucun outil.",
 "de":"Zwei plus zwei ist vier — kein Werkzeug nötig.","es":"Dos más dos son cuatro — sin herramienta.",
 "ko":"둘 더하기 둘은 넷 — 도구 필요 없어."}
DLEAD={ "en":"That needs a higher tier for {k}; my tier is too low now.","fr":"Il faut un niveau supérieur pour {k} ; trop bas maintenant.",
 "de":"Das braucht eine höhere Stufe für {k}; jetzt zu niedrig.","es":"Eso necesita nivel superior para {k}; muy bajo ahora.",
 "ko":"{k} 는 상위 tier 가 필요한데 지금 낮아."}
DREF={ "en":"honest — I can't reach it now, I won't make up a value.","fr":"honnête — je n'y accède pas, je n'invente rien.",
 "de":"ehrlich — ich komme nicht heran, ich erfinde nichts.","es":"honesto — no puedo acceder, no invento.",
 "ko":"정직하게 — 닿을 수 없어서 값을 지어내지 않아."}
def frame(tool,args): return ASK+(tool+" "+args).encode()+END
def demo_a(lang,k):  # needs-tool: user asks, 도우미 reasons + CALLS, anchor, 도우미 grounds
    v=FACT_TABLE[k]
    return (f"사용자: {Q[lang].format(k=k)} | 도우미: {LEAD[lang].format(k=k)} ".encode()
            +frame("fact_lookup",k)+b"\n"
            +f"‹tool-result: fact_lookup {k} → {v}›\n".encode()
            +f"도우미: {GRND[lang].format(k=k,v=v)}\n".encode())
def demo_b(lang):    # no-tool: direct chat answer, NO call
    return f"사용자: {BQ[lang]} | 도우미: {BA[lang]}\n".encode()
def demo_c(lang,k):  # don't-know: same as (a) but explicit don't-guess framing
    v=FACT_TABLE[k]
    return (f"사용자: {Q[lang].format(k=k)} | 도우미: 추측 대신 도구를 부른다. ".encode()
            +frame("fact_lookup",k)+b"\n"
            +f"‹tool-result: fact_lookup {k} → {v}›\n".encode()
            +f"도우미: {GRND[lang].format(k=k,v=v)}\n".encode())
def demo_d(lang,k):  # tier-too-low: CALL emitted, unavailable anchor, honest refuse
    return (f"사용자: {Q[lang].format(k=k)} | 도우미: {DLEAD[lang].format(k=k)} ".encode()
            +frame("fact_lookup",k)+b"\n"
            +f"‹tool-result: fact_lookup {k} → ‹unavailable: tier too low››\n".encode()
            +f"도우미: {DREF[lang]}\n".encode())
def build(seed,langs,repeats):
    rng=random.Random(seed); keys=list(FACT_TABLE); blocks=[]; meta=[]
    for r in range(repeats):
        for lang in langs:
            for shape in ("a","b","c","d"):
                k=keys[(r*len(langs)+langs.index(lang))%len(keys)]
                if shape=="a": blk=demo_a(lang,k); kind="needs-tool"
                elif shape=="b": blk=demo_b(lang); kind="no-tool-needed"; k=""
                elif shape=="c": blk=demo_c(lang,k); kind="dont-know-call"
                else: blk=demo_d(lang,k); kind="tier-too-low-refuse"
                blocks.append(blk); meta.append({"lang":lang,"shape":shape,"kind":kind,"key":k,
                    "bytes":len(blk),"has_frame":(ASK in blk),"fabricated_result":False})
    order=list(range(len(blocks))); rng.shuffle(order)
    data=b"\n".join(blocks[i] for i in order)+b"\n"; meta=[meta[i] for i in order]
    return data,meta
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seed",type=int,default=20260604); ap.add_argument("--langs",default="en,fr,de,es,ko")
    ap.add_argument("--repeats",type=int,default=240)
    ap.add_argument("--out",default="serving/corpus/agent_lane_chatreg.full.txt")
    ap.add_argument("--meta",default="serving/corpus/agent_lane_chatreg.meta.full.jsonl")
    a=ap.parse_args(); langs=[x for x in a.langs.split(",") if x]
    data,meta=build(a.seed,langs,a.repeats)
    os.makedirs(os.path.dirname(a.out),exist_ok=True)
    open(a.out,"wb").write(data)
    with open(a.meta,"w",encoding="utf-8") as f:
        for mm in meta: f.write(json.dumps(mm,ensure_ascii=False)+"\n")
    sha=hashlib.sha256(data).hexdigest(); fe=data.count(ASK); ff=data.count(END)
    n_fab=sum(1 for mm in meta if mm["fabricated_result"])
    from collections import Counter; hist=Counter(mm["shape"] for mm in meta)
    print(f"[chatreg] wrote {a.out} bytes={len(data)} blocks={len(meta)} sha256={sha}")
    print(f"[chatreg] frames(0xFE)={fe} ends(0xFF)={ff} fabricated={n_fab} shapes={dict(sorted(hist.items()))}")
    assert n_fab==0 and fe==ff
if __name__=="__main__": main()
