# Diagnostic: across R2's emitted fragments, how often does the mouth emit a frozen
# COMPARATOR token, a frozen MEASURABLE token, and BOTH (the weld precondition)?
import re, json
COMP={'if','when','whenever','than','more','less','greater','fewer','higher','lower','increases','decreases','correlates','predicts','causes','depends','unless','whereas','versus','compared','proportional','faster','slower','stronger','weaker'}
MEAS={'measure','measured','rate','number','count','amount','level','degree','threshold','ratio','frequency','probability','magnitude','score','value','quantity','percent','times','fraction','distance','duration','speed','size','strength','density'}
def words(s): return re.findall(r"[0-9A-Za-z가-힣]+", s.lower())
# parse rel/meas fragment pairs from the R2 log
txt=open('.verdicts/1431_bind_compose/result_R2.txt').read()
pairs=[]
lines=txt.splitlines()
cur_rel=None
for ln in lines:
    m=re.search(r"rel : '(.*)'$|rel : \"(.*)\"$", ln)
    if m: cur_rel=(m.group(1) or m.group(2)); continue
    m=re.search(r"meas: '(.*)'$|meas: \"(.*)\"$", ln)
    if m and cur_rel is not None:
        pairs.append((cur_rel, m.group(1) or m.group(2))); cur_rel=None
n=len(pairs); has_c=has_m=has_both=0
for rel,meas in pairs:
    u=set(words(rel+" "+meas))
    c=bool(u&COMP); mm=bool(u&MEAS)
    has_c+=c; has_m+=mm; has_both+=(c and mm)
print(f"pairs parsed (COMPOSE ideas across 3 seeds) = {n}")
print(f"  emitted a frozen COMPARATOR token : {has_c}/{n}")
print(f"  emitted a frozen MEASURABLE token : {has_m}/{n}")
print(f"  emitted BOTH (weld precondition)  : {has_both}/{n}")
