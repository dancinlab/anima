#!/usr/bin/env python3
# SAVANT 5-lang starter corpus — Wikipedia REST summary pull (CC-BY-SA-4.0, genuine native text).
# Real provenance (g63), NOT synthetic. Per-language seed topics expanded via "related" + random.
import json, sys, time, urllib.request, urllib.parse

LANGS = ["en", "fr", "de", "es", "ru"]
# Seed topics per language (native-language article titles). We also pull /random/summary in bulk.
SEEDS = {
 "en": ["Consciousness","Mathematics","Physics","Music","Philosophy","History","Universe","Time","Memory","Language","Science","Art","Mind","Brain","Logic","Number","Light","Energy","Life","Earth"],
 "fr": ["Conscience","Mathématiques","Physique","Musique","Philosophie","Histoire","Univers","Temps","Mémoire","Langage","Science","Art","Esprit","Cerveau","Logique","Nombre","Lumière","Énergie","Vie","Terre"],
 "de": ["Bewusstsein","Mathematik","Physik","Musik","Philosophie","Geschichte","Universum","Zeit","Gedächtnis","Sprache","Wissenschaft","Kunst","Geist","Gehirn","Logik","Zahl","Licht","Energie","Leben","Erde"],
 "es": ["Conciencia","Matemáticas","Física","Música","Filosofía","Historia","Universo","Tiempo","Memoria","Lenguaje","Ciencia","Arte","Mente","Cerebro","Lógica","Número","Luz","Energía","Vida","Tierra"],
 "ru": ["Сознание","Математика","Физика","Музыка","Философия","История","Вселенная","Время","Память","Язык","Наука","Искусство","Разум","Мозг","Логика","Число","Свет","Энергия","Жизнь","Земля"],
}
UA = {"User-Agent":"dancinlab-savant-corpus/1.0 (research; mk55911@proton.me)"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception as e:
        return None

def summary(lang, title):
    u = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(title)
    d = get(u)
    if d and d.get("extract"):
        return d["extract"].strip(), d.get("title", title)
    return None, None

def related(lang, title):
    u = f"https://{lang}.wikipedia.org/api/rest_v1/page/related/" + urllib.parse.quote(title)
    d = get(u)
    if not d: return []
    return [p.get("title") for p in d.get("pages", []) if p.get("title")]

TARGET_PER_LANG = int(sys.argv[1]) if len(sys.argv) > 1 else 1500  # articles per lang

for lang in LANGS:
    seen = set()
    out = []
    queue = list(SEEDS[lang])
    qi = 0
    fails = 0
    while len(out) < TARGET_PER_LANG and fails < 80:
        if qi < len(queue):
            title = queue[qi]; qi += 1
        else:
            # expand via related of already-collected, else random
            d = get(f"https://{lang}.wikipedia.org/api/rest_v1/page/random/summary")
            if d and d.get("extract") and d.get("title") not in seen:
                seen.add(d["title"]); txt = d["extract"].strip()
                if len(txt) > 40: out.append(txt)
                else: fails += 1
                continue
            else:
                fails += 1; continue
        if title in seen: continue
        seen.add(title)
        txt, canon = summary(lang, title)
        if txt and len(txt) > 40:
            out.append(txt); fails = 0
            if qi >= len(queue) and len(queue) < TARGET_PER_LANG*2:
                for rt in related(lang, title)[:6]:
                    if rt not in seen: queue.append(rt)
        else:
            fails += 1
    with open(f"wiki_{lang}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    nb = sum(len(t.encode()) for t in out)
    print(f"{lang}: {len(out)} articles, {nb} bytes")
