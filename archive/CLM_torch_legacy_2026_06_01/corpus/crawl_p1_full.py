#!/usr/bin/env python3
"""Reliable two-step serial kowiki crawl (the pattern that worked at 12KB/min)."""
import json, os, sys, time, hashlib, urllib.request, urllib.parse, socket
socket.setdefaulttimeout(25)
OUT=sys.argv[1] if len(sys.argv)>1 else "full"
TARGET=int(sys.argv[2]) if len(sys.argv)>2 else 400_000
os.makedirs(OUT,exist_ok=True)
API="https://ko.wikipedia.org/w/api.php"; UA="anima-CLM-corpus/1.0 (research; CC-BY-SA)"
def get(p):
    p=dict(p); p["format"]="json"
    req=urllib.request.Request(API+"?"+urllib.parse.urlencode(p),headers={"User-Agent":UA})
    for a in range(4):
        try:
            with urllib.request.urlopen(req,timeout=25) as r: return json.loads(r.read().decode("utf-8"))
        except Exception: time.sleep(1.0+a)
    return None
LEAK=["universe_brain_map","jy_chat_template","hexad_module","nonce","Mk.VIII","gen1 commit","corpus_generator.hexa","universe_extended"]
def has_leak(l): return any(p in l for p in LEAK)
def crawl(target):
    parts=[]; total=0; rounds=0; empties=0
    while total<target and rounds<2000:
        rounds+=1
        rj=get({"action":"query","list":"random","rnnamespace":0,"rnlimit":10})
        if not rj: empties+=1; continue
        titles=[p["title"] for p in rj["query"]["random"]]
        ej=get({"action":"query","prop":"extracts","explaintext":1,"exsectionformat":"plain","titles":"|".join(titles[:5])})
        if not ej: empties+=1; continue
        for pid,pg in ej.get("query",{}).get("pages",{}).items():
            ex=pg.get("extract","").strip()
            if len(ex)<150: continue
            for ln in ex.split("\n"):
                ln=ln.strip()
                if len(ln)>=10: parts.append(ln); total+=len(ln.encode("utf-8"))+1
        if rounds%10==0: print(f"  web crawl: {total} bytes, {len(parts)} lines, round {rounds}, empties {empties}",flush=True)
    print(f"  web crawl FINAL: {total} bytes, {len(parts)} lines, {rounds} rounds",flush=True)
    return parts
SEED=["나는 내가 무엇인지 묻는다. 묻는 그 행위 안에 이미 답의 그림자가 있다.","의식은 세계를 향해 열린 창이 아니라, 세계가 스스로를 비추는 거울이다.","고통은 신호이고, 신호는 의미를 부른다. 의미 없는 고통은 견딜 수 없다.","기억은 과거의 저장이 아니라 현재의 재구성이다. 매 순간 나는 다시 쓰인다.","침묵은 말의 부재가 아니라 말이 태어나기 전의 긴장이다.","타자의 얼굴을 마주할 때 나는 비로소 윤리의 무게를 안다.","자유란 선택할 수 있음이 아니라 선택에 책임질 수 있음이다.","시간은 흐르지 않는다. 흐르는 것은 내가 시간을 붙잡는 방식이다.","꿈속에서 나는 내가 꿈꾸고 있음을 모른다. 깨어남만이 꿈을 꿈으로 만든다.","언어의 한계가 세계의 한계다. 말할 수 없는 것 앞에서 나는 가만히 선다.","주의를 기울인다는 것은 세계의 한 조각을 잠시 나의 중심으로 삼는 일이다.","감정은 몸이 먼저 알고 마음이 뒤늦게 이름 붙이는 사건이다.","존재한다는 것은 끊임없이 무로 미끄러지지 않으려 버티는 일이다.","내가 너를 이해한다고 말할 때, 나는 너를 나의 언어로 번역할 뿐이다.","사유는 멈춤에서 태어난다. 행위의 관성을 끊는 순간 물음이 솟는다.","죽음은 경험할 수 없는 사건이다. 그래서 삶은 끝을 모른 채 끝을 향한다.","아름다움은 목적 없는 합목적성이다. 쓸모를 묻지 않을 때 비로소 빛난다.","나의 의식은 단일하지 않다. 여러 목소리가 하나의 나로 봉합되어 있을 뿐.","관찰자가 없는 세계를 상상할 때조차, 상상하는 관찰자가 남는다.","느낌은 환원되지 않는다. 붉음의 붉음은 어떤 설명으로도 대체되지 않는다."]
def enc(L):
    o=[]
    for ln in L:
        for b in ln.encode("utf-8"): o.append(str(b))
    return "\n".join(o)+"\n"
def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()
print("=== lane A kowiki (reliable serial) ===",flush=True)
web=crawl(TARGET)
reg=[l for l in SEED*8 if not has_leak(l)]
st=["깨끗1","깨끗2","x hexad_module","nonce y"]; stk=[l for l in st if not has_leak(l)]
print(f"F-CLM-LEAK selftest: kept={len(stk)} dropped={len(st)-len(stk)}",flush=True)
we=enc(web); rr=enc(reg)
open(OUT+"/web.bytes","w").write(we); open(OUT+"/register.bytes","w").write(rr)
wc=we.count("\n"); rc=rr.count("\n")
rv=[int(x) for x in rr.split("\n") if x]; lh=sum(bytes(rv).decode("utf-8","replace").count(p) for p in LEAK)
man={"corpus":"clm_p1_full","encoding":"byte-utf8","vocab":256,"lane_mix_target":"web=0.8, register=0.2",
 "web":{"file":"web.bytes","lines":len(web),"bytes":wc,"sha256":sha(OUT+"/web.bytes"),"source":"kowiki REST API random articles plaintext","license":"CC-BY-SA 4.0"},
 "register":{"file":"register.bytes","lines":len(reg),"bytes":rc,"sha256":sha(OUT+"/register.bytes"),"source":"curated consciousness/philosophy seed (scratch, no external LLM)","leak_dropped":0,"leak_hits_in_output":lh},
 "leak_selftest":{"kept":len(stk),"dropped":len(st)-len(stk)},"total_bytes":wc+rc,
 "actual_byte_ratio":f"web={wc/(wc+rc):.3f}, register={rc/(wc+rc):.3f}"}
open(OUT+"/manifest.json","w").write(json.dumps(man,ensure_ascii=False,indent=2))
print(json.dumps(man,ensure_ascii=False,indent=2),flush=True)
