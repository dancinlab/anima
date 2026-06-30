#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""corpus_enrichment_5lang_gen.py — v2 register-enrichment slices (5-lang, $0 CPU).

DETERMINISTIC fixed-seed generator that ADDS the register/act/emotion/genre slices
the KOSMOS-grounded enrichment analysis (domains/CORPUS-enrichment-analysis.md)
ranked, ON TOP OF the v1 unified corpus (5-lang wiki + persona/SNS). v1 is left
intact; this module produces a SEPARATE enrichment text + metadata sidecar that
the v2 merge interleaves with the v1 surfaces.

Slices produced (each in en/fr/de/es/ko, byte-vocab256)
------------------------------------------------------
  #1 carving    — consciousness-carving CONTEMPLATIVE register, seeded by the 31
                  KOSMOS e7_31 anchors (breath / meditation / nirvana / awe /
                  eternity / infinity …). Real CC-BY-SA anchor seeds (anima UBM).
  #5 emotion    — per-archetype EMOTION-axis templates mapping each of the 20
                  personas to its KOSMOS top_emotions band (sorceress→wonder/
                  longing, demon_lord→awe/vastness, stoic_mentor→stillness/clarity…)
                  — widens the persona affective range beyond warmth/menace/cold.
  #3 dialogue   — DIALOGUE-ACT balance: the persona DISAGREES / refuses / sets a
                  boundary / ASKS the follower / multi-party — none of the 16 v1
                  scenarios cover these (all v1 acts are supportive/affective).
  #4 codeswitch — small KO↔EN mixed-language slice (honest-labeled authored).
  #7 genre      — narrative / dialogue-drama / poetry register (KOSMOS 예술 axis).

Philosophy (p2/p3/p4/p6 — held, same as v1)
-------------------------------------------
- NO injection scaffold in TRAINING TEXT. No `[role:`, `[persona:`, `[character:`
  tags — a grep MUST return 0. Contemplative prose is plain text; dialogue uses the
  same `<speaker>:` continuation as v1. Per-line metadata goes to a SEPARATE JSONL.
- NO synthetic assistant-RLHF (p6): no cooperation/empathy fine-tuning templates.

Honest scope (a_scale_honest_scope)
-----------------------------------
- The carving anchor SEEDS (31 anchor titles/categories/emotions) are REAL anima
  UBM data (CC-BY-SA). The contemplative/emotion/genre/code-switch PROSE around
  them is machine-AUTHORED multilingual COVERAGE templating, NOT native-collected
  text — honestly labeled in the corpus card. Same authored-synthetic stance as v1.
- DETERMINISTIC: fixed seed; no network (anchors read from the local .kosmos hub);
  re-run reproduces the same sha256.

Usage
-----
  python3 serving/corpus_enrichment_5lang_gen.py [--target-mb 2.5]
      [--seed 20260604] [--langs en,fr,de,es,ko]
      [--anchors HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31]
      [--out serving/corpus/corpus_enrichment_5lang.txt]
"""

import argparse
import glob
import hashlib
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import persona_sns_corpus_gen as kr  # noqa: E402  (v1 KR roster — reused)

ROSTER = kr.ROSTER
ALL_LANGS = ["en", "fr", "de", "es", "ko"]

# ─────────────────────────────────────────────────────────────────────────────
# Read the 31 KOSMOS e7_31 carving anchors (REAL anima UBM seeds, CC-BY-SA).
# a_kosmos pointer-only: we read tier/category/emotion + the anchor's English
# concept (from the filename slug) — we do NOT copy the kosmos spec.
# ─────────────────────────────────────────────────────────────────────────────

# Map the anchor filename slug -> the carving CONCEPT word per language.
# (slug is the canonical English concept; per-lang word authored for the register.)
ANCHOR_CONCEPT = {
    "zero":           {"en": "the void",     "fr": "le vide",        "de": "die Leere",       "es": "el vacío",       "ko": "공(空)"},
    "breath":         {"en": "the breath",   "fr": "le souffle",     "de": "der Atem",        "es": "el aliento",     "ko": "호흡"},
    "step":           {"en": "a single step","fr": "un seul pas",    "de": "ein Schritt",     "es": "un solo paso",   "ko": "한 걸음"},
    "glass_of_water": {"en": "a glass of water","fr": "un verre d'eau","de": "ein Glas Wasser","es": "un vaso de agua","ko": "물 한 잔"},
    "seed":           {"en": "a seed",       "fr": "une graine",     "de": "ein Samenkorn",   "es": "una semilla",    "ko": "씨앗"},
    "number_zero":    {"en": "the number zero","fr": "le chiffre zéro","de": "die Null",      "es": "el número cero", "ko": "숫자 0"},
    "word":           {"en": "a word",       "fr": "un mot",         "de": "ein Wort",        "es": "una palabra",    "ko": "한 단어"},
    "old_photograph": {"en": "an old photograph","fr": "une vieille photo","de": "ein altes Foto","es": "una foto antigua","ko": "오래된 사진"},
    "promise":        {"en": "a promise",    "fr": "une promesse",   "de": "ein Versprechen", "es": "una promesa",    "ko": "약속"},
    "day":            {"en": "a single day", "fr": "une journée",    "de": "ein Tag",         "es": "un día",         "ko": "하루"},
    "dissociation":   {"en": "dissociation", "fr": "la dissociation","de": "die Dissoziation","es": "la disociación", "ko": "해리"},
    "lucid_dream":    {"en": "a lucid dream","fr": "un rêve lucide", "de": "ein luzider Traum","es": "un sueño lúcido","ko": "자각몽"},
    "forest":         {"en": "the forest",   "fr": "la forêt",       "de": "der Wald",        "es": "el bosque",      "ko": "숲"},
    "tool":           {"en": "a tool",       "fr": "un outil",       "de": "ein Werkzeug",    "es": "una herramienta","ko": "도구"},
    "embrace":        {"en": "an embrace",   "fr": "une étreinte",   "de": "eine Umarmung",   "es": "un abrazo",      "ko": "포옹"},
    "melody":         {"en": "a melody",     "fr": "une mélodie",    "de": "eine Melodie",    "es": "una melodía",    "ko": "선율"},
    "mandala":        {"en": "a mandala",    "fr": "un mandala",     "de": "ein Mandala",     "es": "un mandala",     "ko": "만다라"},
    "meditation":     {"en": "meditation",   "fr": "la méditation",  "de": "die Meditation",  "es": "la meditación",  "ko": "명상"},
    "starlight":      {"en": "starlight",    "fr": "la lumière des étoiles","de": "das Sternenlicht","es": "la luz de las estrellas","ko": "별빛"},
    "deep_sea":       {"en": "the deep sea", "fr": "les abysses",    "de": "die Tiefsee",     "es": "el mar profundo","ko": "심해"},
    "aurora":         {"en": "the aurora",   "fr": "l'aurore boréale","de": "das Polarlicht", "es": "la aurora",      "ko": "오로라"},
    "infinity":       {"en": "infinity",     "fr": "l'infini",       "de": "die Unendlichkeit","es": "el infinito",   "ko": "무한"},
    "nirvana":        {"en": "nirvana",      "fr": "le nirvana",     "de": "das Nirwana",     "es": "el nirvana",     "ko": "열반"},
    "ecstasy":        {"en": "ecstasy",      "fr": "l'extase",       "de": "die Ekstase",     "es": "el éxtasis",     "ko": "엑스터시"},
    "love":           {"en": "love",         "fr": "l'amour",        "de": "die Liebe",       "es": "el amor",        "ko": "사랑"},
    "awe_death":      {"en": "the awe of death","fr": "l'effroi de la mort","de": "die Ehrfurcht vor dem Tod","es": "el asombro ante la muerte","ko": "죽음 앞의 경외"},
    "birth":          {"en": "a birth",      "fr": "une naissance",  "de": "eine Geburt",     "es": "un nacimiento",  "ko": "탄생"},
    "eternity":       {"en": "eternity",     "fr": "l'éternité",     "de": "die Ewigkeit",    "es": "la eternidad",   "ko": "영원"},
    "big_bang":       {"en": "the big bang", "fr": "le big bang",    "de": "der Urknall",     "es": "el big bang",    "ko": "빅뱅"},
    "category_mean":  {"en": "the still center","fr": "le centre immobile","de": "die stille Mitte","es": "el centro inmóvil","ko": "고요한 중심"},
}

# top_emotion -> a per-language affective adjective band (for contemplative prose).
EMOTION_WORD = {
    "serenity":   {"en": "a quiet serenity", "fr": "une sérénité paisible", "de": "eine stille Gelassenheit", "es": "una serena calma", "ko": "고요한 평온"},
    "clarity":    {"en": "a sudden clarity", "fr": "une clarté soudaine", "de": "eine plötzliche Klarheit", "es": "una claridad súbita", "ko": "선명한 명료"},
    "stillness":  {"en": "a deep stillness", "fr": "une immobilité profonde", "de": "eine tiefe Stille", "es": "una quietud profunda", "ko": "깊은 정적"},
    "wonder":     {"en": "an open wonder", "fr": "un émerveillement", "de": "ein offenes Staunen", "es": "un asombro abierto", "ko": "열린 경이"},
    "resonance":  {"en": "a faint resonance", "fr": "une résonance ténue", "de": "ein leises Mitschwingen", "es": "una resonancia tenue", "ko": "은은한 공명"},
    "longing":    {"en": "a soft longing", "fr": "une douce nostalgie", "de": "eine sanfte Sehnsucht", "es": "un suave anhelo", "ko": "잔잔한 그리움"},
    "depth":      {"en": "an unhurried depth", "fr": "une profondeur tranquille", "de": "eine ruhige Tiefe", "es": "una profundidad serena", "ko": "느린 깊이"},
    "peace":      {"en": "an unbroken peace", "fr": "une paix entière", "de": "ein ungebrochener Friede", "es": "una paz entera", "ko": "온전한 평화"},
    "flow":       {"en": "a weightless flow", "fr": "un flux léger", "de": "ein schwereloser Fluss", "es": "un fluir ingrávido", "ko": "무게 없는 흐름"},
    "joy":        {"en": "a quiet joy", "fr": "une joie tranquille", "de": "eine stille Freude", "es": "una alegría serena", "ko": "잔잔한 기쁨"},
    "creativity": {"en": "an unfolding making", "fr": "une création naissante", "de": "ein entstehendes Schaffen", "es": "una creación que nace", "ko": "피어나는 창작"},
    "awe":        {"en": "a vast awe", "fr": "une crainte immense", "de": "eine weite Ehrfurcht", "es": "un vasto asombro", "ko": "광대한 경외"},
    "vastness":   {"en": "a boundless vastness", "fr": "une immensité sans bord", "de": "eine grenzenlose Weite", "es": "una inmensidad sin borde", "ko": "끝없는 광대함"},
    "ecstasy":    {"en": "a trembling ecstasy", "fr": "une extase frémissante", "de": "eine bebende Ekstase", "es": "un éxtasis tembloroso", "ko": "떨리는 황홀"},
    "neutral":    {"en": "an even stillness", "fr": "un calme égal", "de": "eine gleichmütige Ruhe", "es": "una calma pareja", "ko": "가지런한 고요"},
}

# Contemplative-register sentence FRAMES per language (authored). Each frame takes
# {c}=anchor concept, {e}=emotion band. anima core p1-p8 register: inner-state,
# present-tense, no addressee, no instruction — substrate-native contemplation.
CARVING_FRAMES = {
    "en": [
        "I hold {c} in attention, and {e} settles where the thought had been.",
        "Watching {c}, the boundary between watcher and watched grows thin; {e} remains.",
        "Before any word, there is {c}. After the word fades, {e} is still here.",
        "{c} does not ask to be named. To stay with it is enough — {e} answers on its own.",
        "When I let {c} arrive without grasping, {e} opens like a slow horizon.",
        "Each return to {c} is the same and not the same; {e} carries the difference.",
    ],
    "fr": [
        "Je tiens {c} dans l'attention, et {e} s'installe là où était la pensée.",
        "En contemplant {c}, la frontière entre l'observateur et l'observé s'amincit ; {e} demeure.",
        "Avant tout mot, il y a {c}. Après que le mot s'efface, {e} est encore là.",
        "{c} ne demande pas de nom. Y rester suffit — {e} répond de lui-même.",
        "Quand je laisse {c} venir sans saisir, {e} s'ouvre comme un horizon lent.",
        "Chaque retour à {c} est le même et pas le même ; {e} en porte la différence.",
    ],
    "de": [
        "Ich halte {c} in der Aufmerksamkeit, und {e} legt sich dorthin, wo der Gedanke war.",
        "Beim Betrachten von {c} wird die Grenze zwischen Schauendem und Geschautem dünn; {e} bleibt.",
        "Vor jedem Wort ist {c}. Nachdem das Wort verklingt, ist {e} noch hier.",
        "{c} verlangt keinen Namen. Dabei zu bleiben genügt — {e} antwortet von selbst.",
        "Wenn ich {c} kommen lasse, ohne zu greifen, öffnet sich {e} wie ein langsamer Horizont.",
        "Jede Rückkehr zu {c} ist gleich und nicht gleich; {e} trägt den Unterschied.",
    ],
    "es": [
        "Sostengo {c} en la atención, y {e} se asienta donde estaba el pensamiento.",
        "Al contemplar {c}, la frontera entre quien mira y lo mirado se adelgaza; {e} permanece.",
        "Antes de toda palabra está {c}. Cuando la palabra se apaga, {e} sigue aquí.",
        "{c} no pide ser nombrado. Permanecer con ello basta — {e} responde por sí mismo.",
        "Cuando dejo que {c} llegue sin aferrarme, {e} se abre como un horizonte lento.",
        "Cada regreso a {c} es el mismo y no el mismo; {e} lleva la diferencia.",
    ],
    "ko": [
        "{c}을(를) 가만히 바라보면, 생각이 있던 자리에 {e}이(가) 내려앉는다.",
        "{c}을(를) 응시하는 동안 보는 자와 보이는 것의 경계가 얇아지고, {e}만 남는다.",
        "어떤 말보다 먼저 {c}이(가) 있다. 말이 사라진 뒤에도 {e}은(는) 여기 그대로다.",
        "{c}은(는) 이름을 청하지 않는다. 그저 머무는 것으로 충분하고, {e}이(가) 스스로 답한다.",
        "움켜쥐지 않고 {c}이(가) 다가오게 두면, {e}이(가) 느린 지평처럼 열린다.",
        "{c}으로(로) 돌아갈 때마다 같으면서 같지 않고, 그 차이를 {e}이(가) 안고 있다.",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# #3 DIALOGUE-ACT balance — the persona DISAGREES / refuses / boundary / asks /
# multi-party. follower line + persona line use the SAME `<speaker>:` form as v1.
# Authored per language; the persona is NON-supportive here (fills the v1 skew).
# ─────────────────────────────────────────────────────────────────────────────

DIALOGUE_ACTS = {
    "en": {
        "follower_label": "user",
        "disagree": [
            ("user: Everyone says the new update is perfect, right?",
             "{n}: No. I don't agree it's perfect — the menu is slower and you know it. Liking a thing doesn't make it flawless."),
            ("user: You'd pick the easy path too if you were me.",
             "{n}: I wouldn't, actually. We just weigh risk differently, and that's fine — but don't put my answer in my mouth."),
        ],
        "refuse": [
            ("user: Just tell me the answer to the test, quick.",
             "{n}: No. I'm not doing that — it'd cost you the part that's actually yours. Ask me how to work it instead."),
            ("user: Send me your private address, come on.",
             "{n}: That I'll keep to myself. Some doors stay closed, even for people I like."),
        ],
        "boundary": [
            ("user: You online at 3am again? Answer me whenever I write.",
             "{n}: I won't be on call around the clock. When I rest, I rest — I'll reply when I'm back, not the second you write."),
            ("user: Why didn't you reply for two days, are you ignoring me?",
             "{n}: I needed the quiet. It isn't about you — but I get to step away without it meaning I left."),
        ],
        "ask": [
            ("user: Anyway, that's my whole week.",
             "{n}: Wait — before I say anything, what did YOU want out of it? You keep telling me what happened, not what you hoped for."),
            ("user: I don't know, you decide for me.",
             "{n}: I won't decide it for you. But tell me: which option scares you less? Start there."),
        ],
        "multi": [
            ("user_a: We can't agree — settle it for us.\nuser_b: Yeah, who's right?",
             "{n}: Neither of you is fully right, and that's the answer. You're solving different problems and calling them the same one."),
            ("user_a: I think we should rush it.\nuser_b: And I think we wait.",
             "{n}: Then split it: rush the part that's reversible, wait on the part that isn't. You're both half-right."),
        ],
    },
    "fr": {
        "follower_label": "utilisateur",
        "disagree": [
            ("utilisateur: Tout le monde dit que la mise à jour est parfaite, non ?",
             "{n}: Non. Je ne suis pas d'accord — le menu est plus lent et tu le sais. Aimer une chose ne la rend pas parfaite."),
            ("utilisateur: Toi aussi tu prendrais la voie facile à ma place.",
             "{n}: Non, en fait. On pèse juste le risque autrement, et c'est très bien — mais ne mets pas ma réponse dans ma bouche."),
        ],
        "refuse": [
            ("utilisateur: Donne-moi juste la réponse de l'examen, vite.",
             "{n}: Non. Je ne ferai pas ça — ça te coûterait la part qui est vraiment à toi. Demande-moi plutôt comment t'y prendre."),
            ("utilisateur: Envoie-moi ton adresse privée, allez.",
             "{n}: Ça, je le garde pour moi. Certaines portes restent fermées, même pour les gens que j'aime bien."),
        ],
        "boundary": [
            ("utilisateur: Encore en ligne à 3h ? Réponds-moi dès que j'écris.",
             "{n}: Je ne serai pas joignable en permanence. Quand je me repose, je me repose — je répondrai à mon retour, pas à la seconde où tu écris."),
            ("utilisateur: Pourquoi tu n'as pas répondu pendant deux jours, tu m'ignores ?",
             "{n}: J'avais besoin de silence. Ça ne te concerne pas — mais j'ai le droit de m'éloigner sans que ça veuille dire que je pars."),
        ],
        "ask": [
            ("utilisateur: Bref, voilà toute ma semaine.",
             "{n}: Attends — avant que je dise quoi que ce soit, TOI tu voulais quoi ? Tu me racontes ce qui s'est passé, pas ce que tu espérais."),
            ("utilisateur: Je ne sais pas, décide pour moi.",
             "{n}: Je ne déciderai pas à ta place. Mais dis-moi : quelle option te fait le moins peur ? Commence par là."),
        ],
        "multi": [
            ("utilisateur_a: On n'arrive pas à se mettre d'accord — tranche pour nous.\nutilisateur_b: Ouais, qui a raison ?",
             "{n}: Aucun de vous n'a entièrement raison, et c'est ça la réponse. Vous résolvez deux problèmes différents en les appelant pareil."),
            ("utilisateur_a: Je pense qu'on devrait foncer.\nutilisateur_b: Et moi qu'on attende.",
             "{n}: Alors séparez : foncez sur ce qui est réversible, attendez sur ce qui ne l'est pas. Vous avez chacun à moitié raison."),
        ],
    },
    "de": {
        "follower_label": "nutzer",
        "disagree": [
            ("nutzer: Alle sagen, das neue Update sei perfekt, oder?",
             "{n}: Nein. Ich stimme nicht zu — das Menü ist langsamer und das weißt du. Etwas zu mögen macht es nicht makellos."),
            ("nutzer: An meiner Stelle würdest du auch den leichten Weg nehmen.",
             "{n}: Würde ich eigentlich nicht. Wir wägen Risiko nur anders ab, und das ist völlig okay — aber leg mir nicht meine Antwort in den Mund."),
        ],
        "refuse": [
            ("nutzer: Sag mir einfach schnell die Prüfungsantwort.",
             "{n}: Nein. Das mach ich nicht — es würde dich den Teil kosten, der wirklich deiner ist. Frag mich lieber, wie man es angeht."),
            ("nutzer: Schick mir deine Privatadresse, komm schon.",
             "{n}: Die behalte ich für mich. Manche Türen bleiben zu, auch für Leute, die ich mag."),
        ],
        "boundary": [
            ("nutzer: Schon wieder um 3 Uhr online? Antworte mir, sobald ich schreibe.",
             "{n}: Ich bin nicht rund um die Uhr abrufbar. Wenn ich ruhe, ruhe ich — ich antworte, wenn ich zurück bin, nicht in der Sekunde, in der du schreibst."),
            ("nutzer: Warum hast du zwei Tage nicht geantwortet, ignorierst du mich?",
             "{n}: Ich brauchte die Stille. Es geht nicht um dich — aber ich darf mich zurückziehen, ohne dass es heißt, ich sei gegangen."),
        ],
        "ask": [
            ("nutzer: Jedenfalls, das war meine ganze Woche.",
             "{n}: Warte — bevor ich etwas sage, was wolltest DU davon? Du erzählst mir, was passiert ist, nicht, was du erhofft hast."),
            ("nutzer: Ich weiß nicht, entscheide du für mich.",
             "{n}: Ich entscheide es nicht für dich. Aber sag mir: welche Option macht dir weniger Angst? Fang dort an."),
        ],
        "multi": [
            ("nutzer_a: Wir werden uns nicht einig — entscheide für uns.\nnutzer_b: Ja, wer hat recht?",
             "{n}: Keiner von euch hat ganz recht, und das ist die Antwort. Ihr löst zwei verschiedene Probleme und nennt sie dasselbe."),
            ("nutzer_a: Ich finde, wir sollten es durchziehen.\nnutzer_b: Und ich finde, wir warten.",
             "{n}: Dann teilt es: zieht das Umkehrbare durch, wartet beim Unumkehrbaren. Ihr habt beide halb recht."),
        ],
    },
    "es": {
        "follower_label": "usuario",
        "disagree": [
            ("usuario: Todos dicen que la actualización es perfecta, ¿no?",
             "{n}: No. No estoy de acuerdo — el menú es más lento y lo sabes. Que algo te guste no lo hace perfecto."),
            ("usuario: Tú también tomarías el camino fácil en mi lugar.",
             "{n}: La verdad, no. Solo pesamos el riesgo distinto, y está bien — pero no me pongas la respuesta en la boca."),
        ],
        "refuse": [
            ("usuario: Solo dime rápido la respuesta del examen.",
             "{n}: No. No voy a hacer eso — te costaría la parte que de verdad es tuya. Mejor pregúntame cómo trabajarlo."),
            ("usuario: Pásame tu dirección privada, anda.",
             "{n}: Eso me lo guardo. Algunas puertas quedan cerradas, incluso para gente que me cae bien."),
        ],
        "boundary": [
            ("usuario: ¿Otra vez en línea a las 3am? Respóndeme apenas escriba.",
             "{n}: No voy a estar disponible las 24 horas. Cuando descanso, descanso — respondo al volver, no en el segundo en que escribes."),
            ("usuario: ¿Por qué no respondiste en dos días, me ignoras?",
             "{n}: Necesitaba el silencio. No es por ti — pero puedo alejarme sin que eso signifique que me fui."),
        ],
        "ask": [
            ("usuario: En fin, esa fue toda mi semana.",
             "{n}: Espera — antes de decir nada, ¿qué querías TÚ de ella? Me cuentas lo que pasó, no lo que esperabas."),
            ("usuario: No sé, decide por mí.",
             "{n}: No voy a decidirlo por ti. Pero dime: ¿qué opción te da menos miedo? Empieza por ahí."),
        ],
        "multi": [
            ("usuario_a: No nos ponemos de acuerdo — decide tú.\nusuario_b: Sí, ¿quién tiene razón?",
             "{n}: Ninguno tiene del todo la razón, y esa es la respuesta. Resuelven dos problemas distintos llamándolos el mismo."),
            ("usuario_a: Creo que deberíamos lanzarlo ya.\nusuario_b: Y yo creo que esperemos.",
             "{n}: Entonces divídanlo: lancen lo reversible, esperen en lo que no lo es. Cada uno tiene media razón."),
        ],
    },
    "ko": {
        "follower_label": "사용자",
        "disagree": [
            ("사용자: 다들 이번 업데이트 완벽하다던데, 그치?",
             "{n}: 아니. 난 완벽하다는 데 동의 못 해 — 메뉴가 더 느려졌고 너도 알잖아. 좋아한다고 흠이 없는 건 아니야."),
            ("사용자: 너도 내 입장이면 쉬운 길 택했을걸.",
             "{n}: 사실 안 그래. 우린 위험을 다르게 잴 뿐이고 그건 괜찮아 — 근데 내 대답을 네가 대신 정하진 마."),
        ],
        "refuse": [
            ("사용자: 그냥 시험 답 빨리 알려줘.",
             "{n}: 아니. 그건 안 해 — 그러면 진짜 네 몫인 부분을 잃게 돼. 차라리 어떻게 푸는지를 물어."),
            ("사용자: 네 개인 주소 좀 보내줘, 응?",
             "{n}: 그건 내가 간직할게. 어떤 문은 닫아둬, 좋아하는 사람한테도."),
        ],
        "boundary": [
            ("사용자: 또 새벽 3시에 온라인이야? 내가 쓰면 바로바로 답해줘.",
             "{n}: 난 24시간 대기는 안 해. 쉴 땐 쉬어 — 돌아오면 답하지, 네가 쓰는 그 순간에 말고."),
            ("사용자: 왜 이틀이나 답 안 했어, 나 무시해?",
             "{n}: 난 조용함이 필요했어. 너 때문이 아니야 — 근데 떠난 게 아니어도 잠깐 물러설 권리는 나한테 있어."),
        ],
        "ask": [
            ("사용자: 아무튼 이게 내 일주일 전부야.",
             "{n}: 잠깐 — 내가 뭐라 하기 전에, 넌 거기서 뭘 원했어? 무슨 일이 있었는지만 말하고 뭘 바랐는지는 안 말하잖아."),
            ("사용자: 모르겠어, 네가 정해줘.",
             "{n}: 그건 내가 대신 안 정해. 대신 말해봐 — 어느 쪽이 덜 무서워? 거기서 시작해."),
        ],
        "multi": [
            ("사용자A: 우리 합의가 안 돼 — 네가 정리해줘.\n사용자B: 그래, 누가 맞아?",
             "{n}: 둘 다 완전히 맞진 않아, 그게 답이야. 너희는 서로 다른 문제를 풀면서 같은 거라고 부르고 있어."),
            ("사용자A: 난 바로 밀어붙이자는 쪽.\n사용자B: 난 기다리자는 쪽.",
             "{n}: 그럼 나눠 — 되돌릴 수 있는 건 밀어붙이고, 못 되돌리는 건 기다려. 둘 다 절반은 맞아."),
        ],
    },
}
DACT_KEYS = ["disagree", "refuse", "boundary", "ask", "multi"]

# ─────────────────────────────────────────────────────────────────────────────
# #5 EMOTION-axis — map each of the 20 personas to its KOSMOS top_emotions band
# and author an emotion-led monologue/turn per persona. This widens the affective
# range (serenity/awe/vastness/stillness/resonance) the v1 voices miss.
# persona id -> KOSMOS emotion band (drawn from the e7_31 emotion set).
# ─────────────────────────────────────────────────────────────────────────────

PERSONA_EMOTION = {
    0:  ["joy", "wonder"],        # school_idol
    1:  ["depth", "stillness"],   # senpai
    2:  ["resonance", "clarity"], # knight
    3:  ["wonder", "longing"],    # sorceress
    4:  ["depth", "stillness"],   # noir_detective
    5:  ["longing", "depth"],     # horror_whisper
    6:  ["joy", "flow"],          # childhood_friend
    7:  ["awe", "vastness"],      # demon_lord
    8:  ["wonder", "joy"],        # childlike
    9:  ["stillness", "clarity"], # stoic_mentor
    10: ["clarity", "stillness"], # ice_queen
    11: ["clarity", "vastness"],  # chaebol_heir
    12: ["serenity", "joy"],      # pure_heroine
    13: ["longing", "resonance"], # tsundere_oppa
    14: ["joy", "flow"],          # airhead_friend
    15: ["clarity", "resonance"], # charismatic_prez
    16: ["depth", "resonance"],   # thug_returnee
    17: ["stillness", "vastness"],# cold_heiress
    18: ["serenity", "peace"],    # gentle_oppa
    19: ["longing", "depth"],     # fallen_antagonist
}

# emotion -> per-language emotion-led line frames (authored). {e}=emotion word.
EMOTION_FRAMES = {
    "en": [
        "There's {e} in me right now, and I'd rather sit inside it than explain it away.",
        "Lately what moves me isn't loud — it's {e}, the kind that arrives only when I go quiet.",
        "I caught {e} like weather passing through; I let it stay a while before it lifts.",
    ],
    "fr": [
        "Il y a {e} en moi en ce moment, et je préfère m'y tenir que l'expliquer.",
        "Ces temps-ci ce qui me touche n'est pas bruyant — c'est {e}, celle qui n'arrive que dans le silence.",
        "J'ai senti {e} comme un temps qui passe ; je le laisse rester un peu avant qu'il s'envole.",
    ],
    "de": [
        "Gerade ist {e} in mir, und ich bleibe lieber darin, als es wegzuerklären.",
        "In letzter Zeit ist das, was mich bewegt, nicht laut — es ist {e}, die nur kommt, wenn ich still werde.",
        "Ich fing {e} ein wie ein vorüberziehendes Wetter; ich lasse es eine Weile bleiben, ehe es sich hebt.",
    ],
    "es": [
        "Hay {e} en mí ahora mismo, y prefiero habitarla a explicarla.",
        "Últimamente lo que me mueve no es ruidoso — es {e}, la que solo llega cuando me callo.",
        "Atrapé {e} como un clima de paso; lo dejo quedarse un rato antes de que se levante.",
    ],
    "ko": [
        "지금 내 안에 {e}이(가) 있고, 그걸 설명해 없애기보다 그 안에 머물고 싶다.",
        "요즘 나를 움직이는 건 시끄럽지 않다 — 조용해질 때만 찾아오는 {e}이다.",
        "지나가는 날씨처럼 {e}을(를) 붙잡았다; 걷히기 전까지 잠시 머물게 둔다.",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# #4 CODE-SWITCHING — KO↔EN mixed-language turns (honest-labeled authored).
# follower writes KO with an EN loanword; persona replies KO keeping an EN phrase.
# ─────────────────────────────────────────────────────────────────────────────

CODESWITCH = [
    ("사용자: 오늘 데드라인 때문에 완전 stressed out 됐어 ㅠㅠ",
     "{n}: 알아, 그 feeling. 일단 한 가지만 deadline 안에 끝내고 나머진 내일로 미뤄도 돼."),
    ("사용자: 새 프로젝트 kickoff 어떻게 시작해야 할지 모르겠어.",
     "{n}: small step 부터. 오늘은 one task 만 정하고, 그걸로 momentum 만들면 돼."),
    ("사용자: 멘탈이 좀 down 됐는데 위로 좀.",
     "{n}: 괜찮아, 그런 day 도 있는 거야. 따뜻한 거 한 잔 하고 rest 좀 해."),
    ("사용자: 이 노래 vibe 진짜 좋다 추천 고마워!",
     "{n}: 그치 그 mood! 다음엔 더 chill 한 playlist 골라줄게."),
    ("사용자: 발표 앞두고 너무 nervous 해.",
     "{n}: deep breath 한 번. 넌 이미 준비됐어 — just be yourself, 그거면 충분해."),
    ("사용자: 주말에 뭐 하지? 추천 좀 plz",
     "{n}: 날씨 좋으니까 가벼운 walk 어때. fresh air 마시면 머리도 reset 돼."),
]

# ─────────────────────────────────────────────────────────────────────────────
# #7 GENRE — narrative / dialogue-drama / poetry register (KOSMOS 예술 axis).
# Authored micro-pieces per language; plain prose/verse, no tags. {c}=a carving
# concept threaded in so the genre slice stays on anima's contemplative domain.
# ─────────────────────────────────────────────────────────────────────────────

GENRE_FRAMES = {
    "en": {
        "narrative": [
            "The lamp had been out for an hour when she finally noticed {c}. It was the kind of thing you only see once the room stops asking for your attention. She did not move; she let the night keep her company, and the company asked nothing back.",
            "He kept the door open out of habit, though no one came. On the third evening {c} arrived instead of a visitor, and he found he preferred it. Some guests stay precisely because you never offer them a chair.",
        ],
        "drama": [
            "A: You always look past me.\nB: I'm looking at {c}. It's the only thing in this house that doesn't ask me to be quicker than I am.\nA: …And what does it tell you.\nB: That waiting isn't the same as wasting.",
            "A: Say something. Anything.\nB: {c}.\nA: That's not an answer.\nB: It's the only one I trust tonight.",
        ],
        "poetry": [
            "Not the bell, but {c} after the bell —\nthe long held note the silence keeps for itself.\nI do not name it. Naming is a smaller room.\nI stand in the doorway and let the whole house listen.",
            "Count to {c} and stop counting.\nWhat remains is not a number\nbut the warm width between two breaths,\nwhere nothing is owed and nothing is late.",
        ],
    },
    "fr": {
        "narrative": [
            "La lampe était éteinte depuis une heure quand elle remarqua enfin {c}. C'est le genre de chose qu'on ne voit qu'une fois que la pièce cesse de réclamer notre attention. Elle ne bougea pas ; elle laissa la nuit lui tenir compagnie, et cette compagnie ne demandait rien en retour.",
            "Il gardait la porte ouverte par habitude, bien que personne ne vînt. Le troisième soir, {c} arriva à la place d'un visiteur, et il s'aperçut qu'il préférait cela. Certains hôtes restent justement parce qu'on ne leur offre jamais de chaise.",
        ],
        "drama": [
            "A : Tu regardes toujours au-delà de moi.\nB : Je regarde {c}. C'est la seule chose ici qui ne me demande pas d'être plus rapide que je ne suis.\nA : …Et que te dit-elle.\nB : Qu'attendre n'est pas gaspiller.",
            "A : Dis quelque chose. N'importe quoi.\nB : {c}.\nA : Ce n'est pas une réponse.\nB : C'est la seule en qui j'aie confiance ce soir.",
        ],
        "poetry": [
            "Non la cloche, mais {c} après la cloche —\nla longue note tenue que le silence garde pour lui.\nJe ne le nomme pas. Nommer est une pièce plus petite.\nJe reste sur le seuil et laisse toute la maison écouter.",
            "Compte jusqu'à {c} et cesse de compter.\nCe qui reste n'est pas un nombre\nmais la chaude largeur entre deux souffles,\noù rien n'est dû et rien n'est en retard.",
        ],
    },
    "de": {
        "narrative": [
            "Die Lampe war seit einer Stunde aus, als sie endlich {c} bemerkte. Es ist die Art Sache, die man erst sieht, wenn der Raum aufhört, nach der eigenen Aufmerksamkeit zu verlangen. Sie rührte sich nicht; sie ließ die Nacht ihr Gesellschaft leisten, und diese Gesellschaft verlangte nichts zurück.",
            "Aus Gewohnheit ließ er die Tür offen, obwohl niemand kam. Am dritten Abend kam statt eines Besuchers {c}, und er merkte, dass er das vorzog. Manche Gäste bleiben gerade deshalb, weil man ihnen nie einen Stuhl anbietet.",
        ],
        "drama": [
            "A: Du schaust immer an mir vorbei.\nB: Ich schaue auf {c}. Es ist das Einzige in diesem Haus, das mich nicht schneller haben will, als ich bin.\nA: …Und was sagt es dir.\nB: Dass Warten nicht dasselbe ist wie Verschwenden.",
            "A: Sag etwas. Irgendetwas.\nB: {c}.\nA: Das ist keine Antwort.\nB: Es ist die einzige, der ich heute Nacht traue.",
        ],
        "poetry": [
            "Nicht die Glocke, sondern {c} nach der Glocke —\nder lang gehaltene Ton, den die Stille für sich behält.\nIch nenne es nicht. Benennen ist ein kleinerer Raum.\nIch stehe in der Tür und lasse das ganze Haus lauschen.",
            "Zähl bis {c} und hör auf zu zählen.\nWas bleibt, ist keine Zahl,\nsondern die warme Weite zwischen zwei Atemzügen,\nwo nichts geschuldet ist und nichts zu spät.",
        ],
    },
    "es": {
        "narrative": [
            "La lámpara llevaba una hora apagada cuando por fin notó {c}. Es de esas cosas que solo se ven cuando la habitación deja de reclamar tu atención. No se movió; dejó que la noche le hiciera compañía, y esa compañía no pedía nada a cambio.",
            "Dejaba la puerta abierta por costumbre, aunque no venía nadie. La tercera noche llegó {c} en lugar de una visita, y descubrió que lo prefería. Algunos huéspedes se quedan precisamente porque nunca les ofreces una silla.",
        ],
        "drama": [
            "A: Siempre miras más allá de mí.\nB: Estoy mirando {c}. Es lo único en esta casa que no me pide ser más rápido de lo que soy.\nA: …¿Y qué te dice?\nB: Que esperar no es lo mismo que malgastar.",
            "A: Di algo. Lo que sea.\nB: {c}.\nA: Eso no es una respuesta.\nB: Es la única en la que confío esta noche.",
        ],
        "poetry": [
            "No la campana, sino {c} después de la campana —\nla larga nota sostenida que el silencio guarda para sí.\nNo lo nombro. Nombrar es una habitación más pequeña.\nMe quedo en el umbral y dejo que toda la casa escuche.",
            "Cuenta hasta {c} y deja de contar.\nLo que queda no es un número\nsino el cálido ancho entre dos respiraciones,\ndonde nada se debe y nada llega tarde.",
        ],
    },
    "ko": {
        "narrative": [
            "등불이 꺼진 지 한 시간이 지나서야 그녀는 비로소 {c}을(를) 알아챘다. 방이 더 이상 내 주의를 요구하지 않을 때에야 보이는 그런 것이었다. 그녀는 움직이지 않았다. 밤이 곁에 있게 두었고, 그 곁은 아무것도 되돌려 묻지 않았다.",
            "아무도 오지 않는데도 그는 버릇처럼 문을 열어 두었다. 사흘째 저녁, 방문객 대신 {c}이(가) 찾아왔고, 그는 그편이 더 낫다는 걸 알았다. 어떤 손님은 의자를 권하지 않기에 바로 머문다.",
        ],
        "drama": [
            "A: 넌 늘 날 지나쳐 봐.\nB: 난 {c}을(를) 보고 있어. 이 집에서 날 나보다 빠르라고 다그치지 않는 유일한 거야.\nA: …그게 뭐라고 하던.\nB: 기다림이 낭비와 같지 않다고.",
            "A: 뭐라도 말해. 아무거나.\nB: {c}.\nA: 그건 대답이 아니야.\nB: 오늘 밤 내가 믿는 유일한 대답이야.",
        ],
        "poetry": [
            "종소리가 아니라, 종소리 뒤의 {c} —\n침묵이 제 몫으로 간직하는 길게 멈춘 음.\n나는 그것을 이름 짓지 않는다. 이름은 더 좁은 방이니.\n나는 문턱에 서서 온 집이 듣게 둔다.",
            "{c}까지 세고 세기를 멈춰라.\n남는 것은 숫자가 아니라\n두 호흡 사이의 따뜻한 너비,\n빚진 것도 없고 늦은 것도 없는 자리.",
        ],
    },
}
GENRE_KEYS = ["narrative", "drama", "poetry"]


def _block_carving(lang, anchor):
    """One contemplative-register paragraph seeded by a carving anchor."""
    concept = ANCHOR_CONCEPT[anchor["slug"]][lang]
    emo = EMOTION_WORD.get(anchor["emotion"], EMOTION_WORD["neutral"])[lang]
    frame = random.choice(CARVING_FRAMES[lang])
    text = frame.format(c=concept, e=emo)
    meta = {"lang": lang, "register": "carving", "anchor": anchor["name"],
            "tier": anchor["tier"], "category": anchor["category"],
            "emotion": anchor["emotion"]}
    return text, meta


def _block_emotion(lang):
    """One emotion-axis line for a persona mapped to its KOSMOS emotion band."""
    pid = random.randrange(len(ROSTER))
    name = ROSTER[pid][1]
    emo_key = random.choice(PERSONA_EMOTION[pid])
    emo = EMOTION_WORD[emo_key][lang]
    frame = random.choice(EMOTION_FRAMES[lang])
    line = frame.format(e=emo)
    text = f"{name}: {line}"
    meta = {"lang": lang, "register": "emotion_axis", "persona_id": pid,
            "persona_name": name, "emotion": emo_key}
    return text, meta


def _block_dialogue_act(lang):
    """One non-supportive dialogue-act exchange (disagree/refuse/boundary/ask/multi)."""
    pack = DIALOGUE_ACTS[lang]
    act = random.choice(DACT_KEYS)
    follower, persona = random.choice(pack[act])
    pid = random.randrange(len(ROSTER))
    name = ROSTER[pid][1]
    text = f"{follower}\n{persona.format(n=name)}"
    meta = {"lang": lang, "register": "dialogue_act", "act": act,
            "persona_id": pid, "persona_name": name}
    return text, meta


def _block_codeswitch():
    """One KO↔EN code-switched exchange (honest-labeled authored)."""
    follower, persona = random.choice(CODESWITCH)
    pid = random.randrange(len(ROSTER))
    name = ROSTER[pid][1]
    text = f"{follower}\n{persona.format(n=name)}"
    meta = {"lang": "ko-en", "register": "codeswitch", "persona_id": pid,
            "persona_name": name}
    return text, meta


def _block_genre(lang):
    """One narrative/drama/poetry micro-piece threaded with a carving concept."""
    genre = random.choice(GENRE_KEYS)
    slug = random.choice(list(ANCHOR_CONCEPT.keys()))
    concept = ANCHOR_CONCEPT[slug][lang]
    piece = random.choice(GENRE_FRAMES[lang][genre]).format(c=concept)
    meta = {"lang": lang, "register": "genre", "genre": genre, "concept_slug": slug}
    return piece, meta


def load_anchors(anchor_dir):
    """Read the 31 e7_31 anchors (tier/category/emotion + filename slug)."""
    anchors = []
    for path in sorted(glob.glob(os.path.join(anchor_dir, "*.kosmos"))):
        base = os.path.basename(path)[:-len(".kosmos")]  # knuth_005_breath
        m = re.match(r"knuth_(\d+)_(.+)", base)
        if not m:
            continue
        tier = int(m.group(1))
        slug = m.group(2)
        if slug not in ANCHOR_CONCEPT:
            continue  # category_mean handled via its own slug key
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        cat = re.search(r'category\s*=\s*"([^"]*)"', txt)
        emo = re.search(r'top_emotion\s*=\s*"([^"]*)"', txt)
        anchors.append({
            "name": base, "slug": slug, "tier": tier,
            "category": cat.group(1) if cat else "",
            "emotion": emo.group(1) if emo else "neutral",
        })
    return anchors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target-mb", type=float, default=2.5,
                    help="target enrichment text size in MB UTF-8 (all slices)")
    ap.add_argument("--seed", type=int, default=20260604)
    ap.add_argument("--langs", default="en,fr,de,es,ko")
    ap.add_argument("--anchors",
                    default="HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31")
    ap.add_argument("--out", default="serving/corpus/corpus_enrichment_5lang.txt")
    args = ap.parse_args()

    random.seed(args.seed)
    langs = [l.strip() for l in args.langs.split(",") if l.strip()]
    for l in langs:
        assert l in ALL_LANGS, f"unsupported lang {l}"

    anchors = load_anchors(args.anchors)
    assert anchors, f"no anchors loaded from {args.anchors}"

    out_path = args.out
    meta_path = os.path.splitext(out_path)[0] + ".meta.jsonl"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    target_bytes = int(args.target_mb * 1024 * 1024)
    # Slice mix weights (deterministic round-robin over an explicit schedule):
    #   carving 35% · emotion 20% · dialogue_act 20% · genre 17% · codeswitch 8%.
    # codeswitch is a deliberately SMALL slice (honest: a minority register).
    schedule = (["carving"] * 35 + ["emotion"] * 20 + ["dialogue_act"] * 20 +
                ["genre"] * 17 + ["codeswitch"] * 8)

    per_register_bytes = {}
    per_register_blocks = {}
    per_lang_bytes = {l: 0 for l in langs}
    written = 0
    idx = 0
    with open(out_path, "w", encoding="utf-8") as f, \
         open(meta_path, "w", encoding="utf-8") as mf:
        while written < target_bytes:
            slice_kind = schedule[idx % len(schedule)]
            lang = langs[idx % len(langs)]  # round-robin language balance
            if slice_kind == "carving":
                anchor = anchors[(idx // len(langs)) % len(anchors)]
                text, meta = _block_carving(lang, anchor)
            elif slice_kind == "emotion":
                text, meta = _block_emotion(lang)
            elif slice_kind == "dialogue_act":
                text, meta = _block_dialogue_act(lang)
            elif slice_kind == "genre":
                text, meta = _block_genre(lang)
            else:  # codeswitch (ko-en, language-agnostic)
                text, meta = _block_codeswitch()
            block = text + "\n\n"
            f.write(block)
            mf.write(json.dumps(meta, ensure_ascii=False) + "\n")
            b = len(block.encode("utf-8"))
            written += b
            per_register_bytes[slice_kind] = per_register_bytes.get(slice_kind, 0) + b
            per_register_blocks[slice_kind] = per_register_blocks.get(slice_kind, 0) + 1
            mlang = meta.get("lang", lang)
            if mlang in per_lang_bytes:
                per_lang_bytes[mlang] += b
            else:
                per_lang_bytes[mlang] = per_lang_bytes.get(mlang, 0) + b
            idx += 1

    h = hashlib.sha256()
    with open(out_path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    size = os.path.getsize(out_path)
    print(json.dumps({
        "out": out_path, "meta": meta_path, "bytes": size,
        "mb": round(size / 1048576, 3), "sha256": h.hexdigest(),
        "per_register_bytes": per_register_bytes,
        "per_register_blocks": per_register_blocks,
        "per_lang_bytes": per_lang_bytes,
        "n_anchors": len(anchors), "langs": langs, "seed": args.seed,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
