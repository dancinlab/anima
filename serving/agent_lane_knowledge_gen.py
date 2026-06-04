#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agent_lane_knowledge_gen.py — agent-lane tool-DOMAIN knowledge corpus (3rd layer).

THE MISSING 3RD LAYER of the agent lane. The agent lane is built in 3 layers:

    layer 1  lane default       = base chat (wiki + persona/SNS + carving/enrichment)
    layer 2  tool-USE demos     = HOW to call (sentinel 0xFE/0xFF grammar, call→
                                  real-result→grounded) — agent_lane_corpus_gen.py
                                  + the tooluse rung-0 corpus (#1833)
    layer 3  tool-DOMAIN knowledge  ←── THIS FILE ──→  = WHAT the tool's domain IS
             (so the model can REASON in the domain, not just emit a call frame)

Layer 2 teaches the call frame; layer 3 teaches the conceptual ground the call
sits on. A model with only layer 2 can shape a `0xFE backtest …0xFF` frame but
cannot reason about WHAT a backtest measures, what a drawdown is, why paper
trading precedes live. Layer 3 supplies that authored CONCEPTUAL coverage for
the five AGENT tool domains:

    CODE       (deep)        AGENT/CODE/CODE.md       — programming / debugging / algorithms
    TRADING    (deep)        AGENT/TRADING/TRADING.md — markets / indicators / risk / backtest
    MERCHANT   (procedural)  AGENT/MERCHANT/MERCHANT.md — listings / pricing / fulfillment / CS
    DESKTOP    (procedural)  AGENT/DESKTOP/DESKTOP.md  — macOS app / window / screen control
    CREATOR    (procedural)  AGENT/CREATOR/CREATOR.md  — content modality / channels / publish

5-lang (en/fr/de/es/ko), byte-level vocab256, DETERMINISTIC (fixed seed).

⛔ TRADING HONEST HARD GATE (a_scale_honest_scope · p6 · p7)
-----------------------------------------------------------
The TRADING slice is authored CONCEPTUAL knowledge ONLY. It explains HOW trading
*concepts* work (what a moving average IS, what RSI MEASURES, why risk is sized).
It carries:
  • NO real tickers / prices / company names as fact
  • NO live signals, NO "buy/sell X" recommendation, NO financial advice
  • NO fabricated market data presented as truth
Every TRADING line is framed "how the concept works", clearly conceptual. The
generator `assert`s a deny-list of advice/recommendation verbs returns 0 hits in
the TRADING slice, and that no real-ticker pattern appears.

Philosophy (p1..p8 — held)
--------------------------
- Knowledge is carried as PLAIN TEXT, like the wiki backbone — NO `[role:` /
  `[persona:` / `[character:` / `[assistant:` / `[system:` markers. A grep over
  the training text returns 0 (the generator asserts it). This is wiki-style
  factual/conceptual coverage, NOT RLHF assistant padding (p6 holds): it teaches
  domain CONCEPTS, never cooperation/empathy/restraint templates.
- byte-vocab256: every byte is valid UTF-8 (NO 0xFE/0xFF — those are layer-2
  grammar bytes; this layer is pure prose, so it composes cleanly UNDER the
  sentinel surface without colliding with it).
- DETERMINISTIC: fixed seed; no network; re-run reproduces the same sha256.

Honest scope (a_scale_honest_scope)
-----------------------------------
- Machine-AUTHORED multilingual CONCEPTUAL coverage (wiki-style). NOT scraped, NO
  PII, NO proprietary/real-financial data, NO fabricated facts-as-truth.
- This feeds a FUTURE agent-lane model at the PROVEN scale — the 18M chat rung
  that PASSED (`dancinlab/anima-clm-default-lane-rung0-byte-18m`, F-DEFAULT-LANE-
  CHAT 🟢). It is NOT a 7B claim: the default corpus is data-starved at 7B
  (.verdicts/default-lane-7b/). Scope = small/18M only; transfer UNVERIFIED.
- This is a SAMPLE + generator. NO training is fired here ($0 scaffold only).

Usage
-----
  python3 serving/agent_lane_knowledge_gen.py \
      [--seed 20260605] [--langs en,fr,de,es,ko] [--repeats 4] \
      [--out serving/corpus/agent_lane_knowledge_5lang.sample.txt] \
      [--meta serving/corpus/agent_lane_knowledge_5lang.meta.sample.jsonl]
"""

import argparse
import hashlib
import json
import os
import random
import re
import sys

LANGS = ["en", "fr", "de", "es", "ko"]
DOMAINS = ["CODE", "TRADING", "MERCHANT", "DESKTOP", "CREATOR"]
DEEP = {"CODE", "TRADING"}  # deep domains; the other three are procedural/lighter.

# Forbidden in TRADING (advice / recommendation / live-signal language) — asserted 0.
TRADING_DENY = re.compile(
    r"\b(buy now|sell now|should buy|should sell|"
    r"you should (buy|sell|invest)|guaranteed return|"
    r"hot stock|price target|will (rise|fall|moon|crash)|i recommend (buying|selling))\b",
    re.IGNORECASE,
)
# Real-ticker-as-fact pattern guard for TRADING (e.g. "$AAPL", "TSLA at 250").
TRADING_TICKER = re.compile(r"\$[A-Z]{1,5}\b|\b[A-Z]{2,5} at \d")
# Philosophy marker guard (p1..p4) — asserted 0 across the whole corpus.
PHIL = re.compile(r"\[(role|persona|character|assistant|system):")


# ═══════════════════════════════════════════════════════════════════════════════
# KNOWLEDGE BANKS — each entry is one conceptual fact, authored in all 5 langs.
# Plain prose ONLY (no role/persona/system tags). Each entry: (id, {lang: text}).
# Rendered as: "<lead-in for domain in lang> <text>" → wiki-style knowledge line.
# ═══════════════════════════════════════════════════════════════════════════════

# Per-domain, per-lang lead-in that frames the line as conceptual knowledge
# (NOT advice, NOT a command). Plain prose.
LEAD = {
    "CODE": {
        "en": "In programming,", "fr": "En programmation,", "de": "Beim Programmieren,",
        "es": "En programación,", "ko": "프로그래밍에서,",
    },
    "TRADING": {
        "en": "As a trading concept,", "fr": "En tant que concept de trading,",
        "de": "Als Trading-Konzept,", "es": "Como concepto de trading,",
        "ko": "트레이딩 개념으로서,",
    },
    "MERCHANT": {
        "en": "In online selling,", "fr": "Dans la vente en ligne,",
        "de": "Im Online-Verkauf,", "es": "En la venta en línea,", "ko": "온라인 판매에서,",
    },
    "DESKTOP": {
        "en": "On a desktop computer,", "fr": "Sur un ordinateur de bureau,",
        "de": "Auf einem Desktop-Computer,", "es": "En un ordenador de escritorio,",
        "ko": "데스크톱 컴퓨터에서,",
    },
    "CREATOR": {
        "en": "In content production,", "fr": "Dans la production de contenu,",
        "de": "In der Content-Produktion,", "es": "En la producción de contenido,",
        "ko": "콘텐츠 제작에서,",
    },
}

# ── CODE (deep) — concepts · debugging · languages/patterns · algorithms ──────
CODE_BANK = [
    ("variable", {
        "en": "a variable is a named place that holds a value, and the value can change as the program runs.",
        "fr": "une variable est un emplacement nommé qui contient une valeur, et cette valeur peut changer pendant l'exécution.",
        "de": "eine Variable ist ein benannter Platz, der einen Wert hält, und der Wert kann sich während des Programmlaufs ändern.",
        "es": "una variable es un lugar con nombre que guarda un valor, y el valor puede cambiar mientras el programa se ejecuta.",
        "ko": "변수는 값을 담는 이름 붙은 자리이며, 프로그램이 실행되는 동안 값이 바뀔 수 있다.",
    }),
    ("function", {
        "en": "a function groups a reusable block of steps under a name, takes inputs called arguments, and may return a result.",
        "fr": "une fonction regroupe un bloc d'étapes réutilisable sous un nom, prend des entrées appelées arguments et peut renvoyer un résultat.",
        "de": "eine Funktion bündelt einen wiederverwendbaren Block von Schritten unter einem Namen, nimmt Eingaben namens Argumente und kann ein Ergebnis zurückgeben.",
        "es": "una función agrupa un bloque reutilizable de pasos bajo un nombre, recibe entradas llamadas argumentos y puede devolver un resultado.",
        "ko": "함수는 재사용 가능한 단계 묶음을 이름 아래 모으고, 인자라는 입력을 받아 결과를 반환할 수 있다.",
    }),
    ("loop", {
        "en": "a loop repeats a block of code while a condition holds; an off-by-one error or a condition that never becomes false causes a bug.",
        "fr": "une boucle répète un bloc de code tant qu'une condition est vraie ; une erreur de décalage d'un ou une condition jamais fausse provoque un bug.",
        "de": "eine Schleife wiederholt einen Codeblock, solange eine Bedingung gilt; ein Off-by-One-Fehler oder eine nie falsche Bedingung verursacht einen Bug.",
        "es": "un bucle repite un bloque de código mientras una condición se cumple; un error de uno en uno o una condición que nunca es falsa produce un fallo.",
        "ko": "반복문은 조건이 참인 동안 코드 블록을 반복하며, 하나 차이 오류나 결코 거짓이 되지 않는 조건은 버그를 만든다.",
    }),
    ("recursion", {
        "en": "recursion is a function that calls itself on a smaller input and needs a base case that stops it, or it overflows the stack.",
        "fr": "la récursivité est une fonction qui s'appelle elle-même sur une entrée plus petite et a besoin d'un cas de base qui l'arrête, sinon elle déborde la pile.",
        "de": "Rekursion ist eine Funktion, die sich selbst mit einer kleineren Eingabe aufruft und einen Basisfall braucht, der sie stoppt, sonst läuft der Stack über.",
        "es": "la recursión es una función que se llama a sí misma con una entrada más pequeña y necesita un caso base que la detenga, o desborda la pila.",
        "ko": "재귀는 더 작은 입력으로 자기 자신을 호출하는 함수이며, 멈추는 종료 조건이 필요하고 없으면 스택이 넘친다.",
    }),
    ("data_structure", {
        "en": "a list keeps order and allows duplicates, a set stores unique items, and a map links keys to values for fast lookup.",
        "fr": "une liste garde l'ordre et autorise les doublons, un ensemble stocke des éléments uniques, et une table associe des clés à des valeurs pour une recherche rapide.",
        "de": "eine Liste behält die Reihenfolge und erlaubt Duplikate, eine Menge speichert eindeutige Elemente, und eine Map verknüpft Schlüssel mit Werten für schnelles Nachschlagen.",
        "es": "una lista mantiene el orden y permite duplicados, un conjunto guarda elementos únicos, y un mapa enlaza claves con valores para una búsqueda rápida.",
        "ko": "리스트는 순서를 유지하고 중복을 허용하며, 집합은 고유한 항목을 저장하고, 맵은 키를 값에 연결해 빠르게 조회한다.",
    }),
    ("complexity", {
        "en": "big-O describes how runtime grows with input size: linear scanning is O(n), nested loops over the same data are O(n squared), and a balanced tree search is O(log n).",
        "fr": "la notation grand-O décrit la croissance du temps d'exécution avec la taille de l'entrée : un balayage linéaire est en O(n), des boucles imbriquées sur les mêmes données en O(n carré), et une recherche dans un arbre équilibré en O(log n).",
        "de": "Big-O beschreibt, wie die Laufzeit mit der Eingabegröße wächst: lineares Durchsuchen ist O(n), verschachtelte Schleifen über dieselben Daten sind O(n quadrat), und die Suche in einem balancierten Baum ist O(log n).",
        "es": "la notación O grande describe cómo crece el tiempo de ejecución con el tamaño de la entrada: un recorrido lineal es O(n), bucles anidados sobre los mismos datos son O(n al cuadrado), y la búsqueda en un árbol equilibrado es O(log n).",
        "ko": "빅오 표기는 입력 크기에 따라 실행 시간이 어떻게 늘어나는지 나타낸다: 선형 탐색은 O(n), 같은 데이터를 이중 반복하면 O(n 제곱), 균형 트리 검색은 O(log n)이다.",
    }),
    ("debugging", {
        "en": "debugging starts by reproducing the failure, then narrowing where the actual output first diverges from the expected output, often with prints, a debugger, or a bisection of recent changes.",
        "fr": "le débogage commence par reproduire la panne, puis par cerner où la sortie réelle diverge d'abord de la sortie attendue, souvent avec des affichages, un débogueur ou une bissection des changements récents.",
        "de": "Debugging beginnt damit, den Fehler zu reproduzieren, und grenzt dann ein, wo die tatsächliche Ausgabe zuerst von der erwarteten abweicht, oft mit Ausgaben, einem Debugger oder einer Bisektion der jüngsten Änderungen.",
        "es": "la depuración empieza por reproducir el fallo, luego por acotar dónde la salida real diverge por primera vez de la esperada, a menudo con impresiones, un depurador o una bisección de los cambios recientes.",
        "ko": "디버깅은 먼저 오류를 재현한 뒤, 실제 출력이 기대 출력과 처음으로 갈라지는 지점을 좁혀 가는 일이며, 흔히 출력문·디버거·최근 변경의 이분 탐색을 쓴다.",
    }),
    ("error_types", {
        "en": "a syntax error stops the code from parsing, a runtime error crashes mid-execution like dividing by zero, and a logic error runs without crashing but gives the wrong answer.",
        "fr": "une erreur de syntaxe empêche l'analyse du code, une erreur d'exécution plante en cours comme une division par zéro, et une erreur de logique s'exécute sans planter mais donne une mauvaise réponse.",
        "de": "ein Syntaxfehler verhindert das Parsen des Codes, ein Laufzeitfehler stürzt mitten in der Ausführung ab wie eine Division durch null, und ein Logikfehler läuft ohne Absturz, liefert aber das falsche Ergebnis.",
        "es": "un error de sintaxis impide analizar el código, un error en tiempo de ejecución se cae a mitad como dividir por cero, y un error de lógica se ejecuta sin caerse pero da la respuesta equivocada.",
        "ko": "문법 오류는 코드 파싱을 막고, 런타임 오류는 0으로 나누기처럼 실행 중에 멈추며, 논리 오류는 멈추지 않고 실행되지만 틀린 답을 낸다.",
    }),
    ("version_control", {
        "en": "version control like git records snapshots called commits, lets parallel work live on branches, and merges them back, so a bad change can be reverted.",
        "fr": "le contrôle de version comme git enregistre des instantanés appelés commits, laisse le travail parallèle vivre sur des branches, et les fusionne, de sorte qu'un mauvais changement peut être annulé.",
        "de": "Versionskontrolle wie git zeichnet Schnappschüsse namens Commits auf, lässt parallele Arbeit auf Branches leben und führt sie zusammen, sodass eine schlechte Änderung rückgängig gemacht werden kann.",
        "es": "el control de versiones como git registra instantáneas llamadas commits, deja que el trabajo paralelo viva en ramas, y las fusiona, de modo que un cambio malo se puede revertir.",
        "ko": "git 같은 버전 관리는 커밋이라는 스냅숏을 기록하고, 병렬 작업을 브랜치에 두었다가 병합하며, 그래서 잘못된 변경을 되돌릴 수 있다.",
    }),
    ("testing", {
        "en": "a unit test checks one small piece in isolation, while an integration test checks that pieces work together; a test that fails before a fix and passes after is a regression guard.",
        "fr": "un test unitaire vérifie une petite pièce isolément, tandis qu'un test d'intégration vérifie que les pièces fonctionnent ensemble ; un test qui échoue avant un correctif et passe après est un garde-fou contre les régressions.",
        "de": "ein Unit-Test prüft ein kleines Stück isoliert, während ein Integrationstest prüft, dass Teile zusammenarbeiten; ein Test, der vor einer Korrektur fehlschlägt und danach besteht, ist ein Schutz gegen Regressionen.",
        "es": "una prueba unitaria comprueba una pieza pequeña de forma aislada, mientras que una de integración comprueba que las piezas funcionan juntas; una prueba que falla antes de un arreglo y pasa después es una guarda contra regresiones.",
        "ko": "단위 테스트는 작은 조각 하나를 따로 검사하고, 통합 테스트는 조각들이 함께 동작하는지 검사하며, 수정 전엔 실패하고 후엔 통과하는 테스트는 회귀 방지 장치다.",
    }),
    ("paradigm", {
        "en": "imperative code states step-by-step how to change state, while functional code prefers pure functions and avoids hidden side effects, making behaviour easier to reason about.",
        "fr": "le code impératif énonce pas à pas comment changer l'état, tandis que le code fonctionnel privilégie les fonctions pures et évite les effets de bord cachés, ce qui rend le comportement plus facile à raisonner.",
        "de": "imperativer Code gibt Schritt für Schritt an, wie der Zustand geändert wird, während funktionaler Code reine Funktionen bevorzugt und versteckte Nebenwirkungen vermeidet, was das Verhalten leichter nachvollziehbar macht.",
        "es": "el código imperativo indica paso a paso cómo cambiar el estado, mientras que el funcional prefiere funciones puras y evita efectos secundarios ocultos, lo que facilita razonar sobre el comportamiento.",
        "ko": "명령형 코드는 상태를 어떻게 바꿀지 단계별로 기술하고, 함수형 코드는 순수 함수를 선호하며 숨은 부작용을 피해 동작을 추론하기 쉽게 한다.",
    }),
    ("concurrency", {
        "en": "concurrency runs tasks in overlapping time; a race condition appears when two tasks touch shared data without coordination, which a lock or a message queue can prevent.",
        "fr": "la concurrence exécute des tâches sur des intervalles qui se chevauchent ; une situation de compétition apparaît quand deux tâches touchent des données partagées sans coordination, qu'un verrou ou une file de messages peut empêcher.",
        "de": "Nebenläufigkeit führt Aufgaben in überlappender Zeit aus; eine Race-Condition entsteht, wenn zwei Aufgaben gemeinsame Daten ohne Koordination berühren, was ein Lock oder eine Nachrichtenwarteschlange verhindern kann.",
        "es": "la concurrencia ejecuta tareas en tiempos solapados; una condición de carrera surge cuando dos tareas tocan datos compartidos sin coordinación, lo que un cerrojo o una cola de mensajes puede evitar.",
        "ko": "동시성은 겹치는 시간에 작업을 실행하며, 두 작업이 조율 없이 공유 데이터를 건드리면 경쟁 상태가 생기고, 락이나 메시지 큐로 막을 수 있다.",
    }),
]


# ── TRADING (deep) — CONCEPTUAL ONLY (hard gate) — markets · indicators ·
#    risk · backtest · paper-vs-live. Every line explains HOW the concept works.
#    NO tickers/prices as fact, NO signals, NO advice (asserted 0). ───────────────
TRADING_BANK = [
    ("market", {
        "en": "a market is a place where buyers and sellers agree on a price; the bid is the highest someone will pay and the ask is the lowest someone will sell for, and the gap between them is the spread.",
        "fr": "un marché est un lieu où acheteurs et vendeurs s'accordent sur un prix ; le cours acheteur est le plus haut qu'on paiera et le cours vendeur le plus bas auquel on vendra, et l'écart entre eux est le spread.",
        "de": "ein Markt ist ein Ort, an dem sich Käufer und Verkäufer auf einen Preis einigen; der Geldkurs ist der höchste, den jemand zahlt, und der Briefkurs der niedrigste, zu dem jemand verkauft, und die Lücke dazwischen ist der Spread.",
        "es": "un mercado es un lugar donde compradores y vendedores acuerdan un precio; la demanda es lo más alto que alguien pagará y la oferta lo más bajo a lo que alguien venderá, y la diferencia entre ambas es el diferencial.",
        "ko": "시장은 매수자와 매도자가 가격에 합의하는 곳이며, 매수 호가는 누군가 지불할 가장 높은 값, 매도 호가는 누군가 팔 가장 낮은 값이고, 그 간격이 스프레드다.",
    }),
    ("moving_average", {
        "en": "a moving average smooths a price series by averaging the last N values, so it lags the raw price; it is a way to describe a trend's direction, not a prediction of any future value.",
        "fr": "une moyenne mobile lisse une série de prix en faisant la moyenne des N dernières valeurs, donc elle retarde le prix brut ; c'est une façon de décrire la direction d'une tendance, pas une prédiction d'une valeur future.",
        "de": "ein gleitender Durchschnitt glättet eine Preisreihe, indem er die letzten N Werte mittelt, und hinkt daher dem Rohpreis hinterher; er beschreibt die Richtung eines Trends, ist aber keine Vorhersage eines künftigen Werts.",
        "es": "una media móvil suaviza una serie de precios promediando los últimos N valores, por lo que va por detrás del precio bruto; describe la dirección de una tendencia, no una predicción de ningún valor futuro.",
        "ko": "이동평균은 최근 N개의 값을 평균해 가격 시계열을 매끄럽게 하므로 원시 가격보다 뒤처지며, 추세의 방향을 묘사하는 도구일 뿐 미래 값에 대한 예측이 아니다.",
    }),
    ("rsi", {
        "en": "the relative strength index is a bounded oscillator from 0 to 100 that compares the size of recent gains to recent losses; it describes momentum, and conventionally high or low readings are called overbought or oversold without implying any action.",
        "fr": "l'indice de force relative est un oscillateur borné de 0 à 100 qui compare l'ampleur des gains récents aux pertes récentes ; il décrit le momentum, et par convention des lectures hautes ou basses sont dites surachat ou survente sans impliquer d'action.",
        "de": "der Relative-Stärke-Index ist ein begrenzter Oszillator von 0 bis 100, der die Größe jüngster Gewinne mit jüngsten Verlusten vergleicht; er beschreibt das Momentum, und hohe oder niedrige Werte heißen konventionell überkauft oder überverkauft, ohne eine Handlung zu implizieren.",
        "es": "el índice de fuerza relativa es un oscilador acotado de 0 a 100 que compara el tamaño de las ganancias recientes con las pérdidas recientes; describe el impulso, y por convención lecturas altas o bajas se llaman sobrecompra o sobreventa sin implicar ninguna acción.",
        "ko": "상대강도지수는 0에서 100 사이로 제한된 진동 지표로, 최근 상승폭과 하락폭의 크기를 비교하며, 모멘텀을 묘사하고 관례상 높거나 낮은 값을 과매수·과매도라 부르지만 어떤 행동도 함의하지 않는다.",
    }),
    ("volatility", {
        "en": "volatility measures how much a price swings around its average over a window; higher volatility means wider swings and is a description of risk, not of direction.",
        "fr": "la volatilité mesure l'amplitude des variations d'un prix autour de sa moyenne sur une fenêtre ; une volatilité plus élevée signifie des variations plus larges et décrit un risque, pas une direction.",
        "de": "Volatilität misst, wie stark ein Preis über ein Zeitfenster um seinen Durchschnitt schwankt; höhere Volatilität bedeutet größere Ausschläge und beschreibt Risiko, nicht Richtung.",
        "es": "la volatilidad mide cuánto oscila un precio alrededor de su media en una ventana; una volatilidad mayor implica oscilaciones más amplias y describe riesgo, no dirección.",
        "ko": "변동성은 한 구간 동안 가격이 평균을 중심으로 얼마나 출렁이는지 측정하며, 변동성이 높을수록 진폭이 크고 이는 방향이 아니라 위험을 묘사한다.",
    }),
    ("risk_sizing", {
        "en": "position sizing decides how much capital to put at risk on one idea; a common conceptual rule is to risk only a small fixed fraction of the account so that no single loss is ruinous.",
        "fr": "le dimensionnement de position décide quelle part du capital risquer sur une idée ; une règle conceptuelle courante est de ne risquer qu'une petite fraction fixe du compte pour qu'aucune perte unique ne soit ruineuse.",
        "de": "die Positionsgröße entscheidet, wie viel Kapital für eine Idee riskiert wird; eine verbreitete konzeptionelle Regel ist, nur einen kleinen festen Bruchteil des Kontos zu riskieren, damit kein einzelner Verlust ruinös ist.",
        "es": "el dimensionamiento de la posición decide cuánto capital arriesgar en una idea; una regla conceptual común es arriesgar solo una pequeña fracción fija de la cuenta para que ninguna pérdida única sea ruinosa.",
        "ko": "포지션 크기 조절은 한 아이디어에 자본을 얼마나 걸지 정하는 일이며, 흔한 개념적 규칙은 계좌의 작은 고정 비율만 위험에 노출해 단 한 번의 손실이 치명적이지 않게 하는 것이다.",
    }),
    ("stop_loss", {
        "en": "a stop is a pre-set exit level that conceptually caps how much a single position can lose; it turns an open-ended risk into a bounded one before any trade is placed.",
        "fr": "un stop est un niveau de sortie prédéfini qui plafonne conceptuellement la perte possible d'une position ; il transforme un risque ouvert en risque borné avant tout passage d'ordre.",
        "de": "ein Stopp ist ein vorab festgelegtes Ausstiegsniveau, das konzeptionell begrenzt, wie viel eine einzelne Position verlieren kann; er macht aus einem offenen Risiko ein begrenztes, bevor überhaupt gehandelt wird.",
        "es": "un stop es un nivel de salida prefijado que conceptualmente limita cuánto puede perder una posición; convierte un riesgo abierto en uno acotado antes de ejecutar cualquier operación.",
        "ko": "스톱은 미리 정해 둔 청산 수준으로, 한 포지션이 얼마나 잃을 수 있는지를 개념적으로 제한하며, 거래를 내기 전에 무한정한 위험을 한정된 위험으로 바꾼다.",
    }),
    ("drawdown", {
        "en": "drawdown is the drop from a peak equity value to a later trough, expressed as a percentage; maximum drawdown summarizes the worst such fall and is a standard way to describe how painful a strategy's history was.",
        "fr": "le drawdown est la baisse depuis un sommet d'équité jusqu'à un creux ultérieur, exprimée en pourcentage ; le drawdown maximal résume la pire de ces chutes et décrit de façon standard à quel point l'historique d'une stratégie a été douloureux.",
        "de": "ein Drawdown ist der Rückgang von einem Kapitalhöchststand zu einem späteren Tief, ausgedrückt in Prozent; der maximale Drawdown fasst den schlimmsten solchen Fall zusammen und beschreibt standardmäßig, wie schmerzhaft die Historie einer Strategie war.",
        "es": "el drawdown es la caída desde un máximo de capital hasta un mínimo posterior, expresada en porcentaje; el drawdown máximo resume la peor de esas caídas y describe de forma estándar cuán doloroso fue el historial de una estrategia.",
        "ko": "낙폭은 자본의 고점에서 이후 저점까지의 하락을 백분율로 나타낸 것이며, 최대 낙폭은 그러한 하락 중 최악을 요약해 한 전략의 이력이 얼마나 고통스러웠는지를 표준적으로 묘사한다.",
    }),
    ("backtest", {
        "en": "a backtest replays a strategy over past data to estimate how it would have behaved; it must charge fees and slippage and avoid look-ahead bias, and a good past result is a description of history, never a promise about the future.",
        "fr": "un backtest rejoue une stratégie sur des données passées pour estimer son comportement ; il doit imputer frais et glissement et éviter le biais de prévoyance, et un bon résultat passé décrit l'histoire, jamais une promesse sur l'avenir.",
        "de": "ein Backtest spielt eine Strategie über vergangene Daten ab, um abzuschätzen, wie sie sich verhalten hätte; er muss Gebühren und Slippage berücksichtigen und Look-Ahead-Bias vermeiden, und ein gutes Vergangenheitsergebnis beschreibt Historie, niemals ein Versprechen über die Zukunft.",
        "es": "un backtest reproduce una estrategia sobre datos pasados para estimar cómo se habría comportado; debe cobrar comisiones y deslizamiento y evitar el sesgo de anticipación, y un buen resultado pasado describe la historia, nunca una promesa sobre el futuro.",
        "ko": "백테스트는 과거 데이터로 전략을 재생해 어떻게 작동했을지 추정하며, 수수료와 슬리피지를 반영하고 미래 참조 편향을 피해야 하고, 좋은 과거 성과는 역사를 묘사할 뿐 미래에 대한 약속이 결코 아니다.",
    }),
    ("paper_vs_live", {
        "en": "paper trading simulates orders with no real money so a strategy can be checked safely, while live trading commits real capital; the conceptual gap is that live fills face real slippage, latency, and emotion that a simulation does not fully capture.",
        "fr": "le trading sur papier simule des ordres sans argent réel pour tester une stratégie en sécurité, tandis que le trading réel engage du capital réel ; l'écart conceptuel est que les exécutions réelles subissent glissement, latence et émotion qu'une simulation ne capture pas pleinement.",
        "de": "Paper-Trading simuliert Orders ohne echtes Geld, damit eine Strategie sicher geprüft werden kann, während Live-Trading echtes Kapital einsetzt; die konzeptionelle Lücke ist, dass echte Ausführungen reale Slippage, Latenz und Emotion erfahren, die eine Simulation nicht voll erfasst.",
        "es": "el trading en papel simula órdenes sin dinero real para probar una estrategia con seguridad, mientras que el trading real compromete capital real; la brecha conceptual es que las ejecuciones reales sufren deslizamiento, latencia y emoción que una simulación no captura del todo.",
        "ko": "모의 거래는 실제 돈 없이 주문을 시뮬레이션해 전략을 안전하게 점검하고, 실거래는 실제 자본을 투입하며, 개념적 간극은 실제 체결이 시뮬레이션이 온전히 담지 못하는 슬리피지·지연·감정을 겪는다는 점이다.",
    }),
    ("order_types", {
        "en": "a market order fills immediately at whatever price is available, while a limit order fills only at a chosen price or better; the trade-off is certainty of execution versus certainty of price.",
        "fr": "un ordre au marché s'exécute immédiatement au prix disponible, tandis qu'un ordre à cours limité ne s'exécute qu'à un prix choisi ou meilleur ; le compromis est la certitude d'exécution contre la certitude de prix.",
        "de": "eine Market-Order wird sofort zum verfügbaren Preis ausgeführt, während eine Limit-Order nur zu einem gewählten Preis oder besser ausgeführt wird; der Kompromiss ist Ausführungssicherheit gegen Preissicherheit.",
        "es": "una orden de mercado se ejecuta de inmediato al precio disponible, mientras que una orden limitada se ejecuta solo a un precio elegido o mejor; el compromiso es certeza de ejecución frente a certeza de precio.",
        "ko": "시장가 주문은 가능한 가격에 즉시 체결되고, 지정가 주문은 정한 가격이나 그보다 유리한 값에서만 체결되며, 그 절충은 체결의 확실성 대 가격의 확실성이다.",
    }),
    ("diversification", {
        "en": "diversification spreads capital across positions whose outcomes are not perfectly linked, so that the variability of the whole is lower than the sum of the parts; it is a conceptual way to reduce risk, not to raise expected return.",
        "fr": "la diversification répartit le capital sur des positions dont les résultats ne sont pas parfaitement liés, de sorte que la variabilité de l'ensemble soit plus faible que la somme des parties ; c'est un moyen conceptuel de réduire le risque, pas d'augmenter le rendement attendu.",
        "de": "Diversifikation verteilt Kapital auf Positionen, deren Ergebnisse nicht perfekt verbunden sind, sodass die Schwankung des Ganzen geringer ist als die Summe der Teile; sie ist ein konzeptioneller Weg, Risiko zu senken, nicht die erwartete Rendite zu erhöhen.",
        "es": "la diversificación reparte el capital entre posiciones cuyos resultados no están perfectamente ligados, de modo que la variabilidad del conjunto sea menor que la suma de las partes; es una forma conceptual de reducir el riesgo, no de elevar el rendimiento esperado.",
        "ko": "분산은 결과가 완벽히 연동되지 않는 포지션들에 자본을 나눠, 전체의 변동성이 부분들의 합보다 작아지게 하며, 기대 수익을 높이는 게 아니라 위험을 줄이는 개념적 방법이다.",
    }),
]


# ── MERCHANT (procedural/lighter) — listings · pricing · fulfillment · CS ──────
MERCHANT_BANK = [
    ("listing", {
        "en": "a product listing presents a title, photos, a description, and a price on a marketplace; clear titles and accurate photos help a buyer find and trust the item.",
        "fr": "une fiche produit présente un titre, des photos, une description et un prix sur une place de marché ; des titres clairs et des photos exactes aident l'acheteur à trouver l'article et à lui faire confiance.",
        "de": "ein Produktangebot zeigt einen Titel, Fotos, eine Beschreibung und einen Preis auf einem Marktplatz; klare Titel und genaue Fotos helfen einem Käufer, den Artikel zu finden und ihm zu vertrauen.",
        "es": "un anuncio de producto muestra un título, fotos, una descripción y un precio en un mercado; títulos claros y fotos exactas ayudan al comprador a encontrar el artículo y a confiar en él.",
        "ko": "상품 등록은 마켓플레이스에 제목·사진·설명·가격을 보여 주며, 명확한 제목과 정확한 사진은 구매자가 물건을 찾고 신뢰하도록 돕는다.",
    }),
    ("pricing", {
        "en": "pricing must cover the item's cost, the marketplace fee, and shipping while staying competitive; in arbitrage selling, the margin is the target price minus the sourcing cost and all fees.",
        "fr": "le prix doit couvrir le coût de l'article, la commission de la place de marché et l'expédition tout en restant compétitif ; en vente d'arbitrage, la marge est le prix cible moins le coût d'approvisionnement et tous les frais.",
        "de": "der Preis muss die Kosten des Artikels, die Marktplatzgebühr und den Versand decken und dabei wettbewerbsfähig bleiben; beim Arbitrage-Verkauf ist die Marge der Zielpreis minus Beschaffungskosten und alle Gebühren.",
        "es": "el precio debe cubrir el coste del artículo, la comisión del mercado y el envío sin dejar de ser competitivo; en la venta por arbitraje, el margen es el precio objetivo menos el coste de aprovisionamiento y todas las comisiones.",
        "ko": "가격은 경쟁력을 유지하면서 상품 원가·마켓 수수료·배송비를 모두 감당해야 하며, 구매대행 판매에서 마진은 목표 가격에서 소싱 원가와 모든 수수료를 뺀 값이다.",
    }),
    ("fulfillment", {
        "en": "fulfillment is the chain from a received order to a delivered package: source or pick the item, pack it, hand it to a carrier, and track it until the buyer confirms delivery.",
        "fr": "l'exécution est la chaîne d'une commande reçue à un colis livré : approvisionner ou prélever l'article, l'emballer, le confier à un transporteur et le suivre jusqu'à la confirmation de livraison par l'acheteur.",
        "de": "Fulfillment ist die Kette von einer eingegangenen Bestellung bis zum gelieferten Paket: den Artikel beschaffen oder entnehmen, verpacken, einem Versanddienst übergeben und verfolgen, bis der Käufer die Lieferung bestätigt.",
        "es": "la gestión del pedido es la cadena desde un pedido recibido hasta un paquete entregado: aprovisionar o recoger el artículo, empaquetarlo, entregarlo a un transportista y seguirlo hasta que el comprador confirme la entrega.",
        "ko": "주문 이행은 접수된 주문에서 배송 완료 소포까지의 흐름으로, 상품을 소싱하거나 꺼내 포장하고 배송사에 넘긴 뒤 구매자가 수령을 확인할 때까지 추적한다.",
    }),
    ("inventory", {
        "en": "inventory tracking keeps the listed stock in sync with what is on hand, and a low-stock alert warns before an item sells out so the listing can be replenished or paused.",
        "fr": "le suivi des stocks garde le stock affiché synchronisé avec ce qui est en main, et une alerte de stock bas prévient avant l'épuisement d'un article pour que la fiche soit réapprovisionnée ou suspendue.",
        "de": "die Bestandsverfolgung hält den gelisteten Bestand mit dem vorhandenen synchron, und eine Warnung bei niedrigem Bestand mahnt, bevor ein Artikel ausverkauft ist, damit das Angebot aufgefüllt oder pausiert werden kann.",
        "es": "el seguimiento del inventario mantiene el stock publicado sincronizado con lo que hay disponible, y una alerta de stock bajo avisa antes de que un artículo se agote para reponer o pausar el anuncio.",
        "ko": "재고 추적은 등록된 재고를 실제 보유분과 일치시키며, 재고 부족 경고는 품절 전에 알려 등록을 보충하거나 일시 중지할 수 있게 한다.",
    }),
    ("customer_service", {
        "en": "customer service handles questions, returns, and complaints after a sale; a clear, prompt reply that states the order, the issue, and the next step keeps a buyer's trust.",
        "fr": "le service client gère les questions, les retours et les réclamations après une vente ; une réponse claire et rapide qui indique la commande, le problème et l'étape suivante préserve la confiance de l'acheteur.",
        "de": "der Kundenservice bearbeitet Fragen, Rücksendungen und Beschwerden nach einem Verkauf; eine klare, prompte Antwort, die Bestellung, Problem und nächsten Schritt nennt, erhält das Vertrauen eines Käufers.",
        "es": "la atención al cliente gestiona preguntas, devoluciones y quejas tras una venta; una respuesta clara y rápida que indique el pedido, el problema y el siguiente paso conserva la confianza del comprador.",
        "ko": "고객 서비스는 판매 이후의 문의·반품·불만을 처리하며, 주문·문제·다음 단계를 밝히는 명확하고 신속한 답변은 구매자의 신뢰를 지킨다.",
    }),
    ("settlement", {
        "en": "settlement is when a marketplace pays out the seller's accumulated sales minus fees on a schedule; reconciling the payout against the orders confirms that the net amount is correct.",
        "fr": "le règlement est le moment où une place de marché verse au vendeur ses ventes cumulées moins les frais selon un calendrier ; rapprocher le versement des commandes confirme que le montant net est correct.",
        "de": "die Abrechnung ist, wenn ein Marktplatz die aufgelaufenen Verkäufe des Verkäufers abzüglich Gebühren nach einem Zeitplan auszahlt; der Abgleich der Auszahlung mit den Bestellungen bestätigt, dass der Nettobetrag stimmt.",
        "es": "la liquidación es cuando un mercado paga al vendedor sus ventas acumuladas menos comisiones según un calendario; conciliar el pago con los pedidos confirma que el importe neto es correcto.",
        "ko": "정산은 마켓플레이스가 정해진 주기에 따라 판매자의 누적 매출에서 수수료를 뺀 금액을 지급하는 것이며, 지급액을 주문과 대조하면 순액이 맞는지 확인된다.",
    }),
]

# ── DESKTOP (procedural/lighter) — macOS app · window · screen control ─────────
DESKTOP_BANK = [
    ("app_control", {
        "en": "controlling a desktop means launching, focusing, or quitting applications; on macOS this goes through the window server and the accessibility layer rather than guessing from pixels alone.",
        "fr": "contrôler un ordinateur de bureau signifie lancer, mettre au premier plan ou quitter des applications ; sur macOS cela passe par le serveur de fenêtres et la couche d'accessibilité plutôt que de deviner à partir des seuls pixels.",
        "de": "einen Desktop zu steuern heißt, Anwendungen zu starten, in den Vordergrund zu holen oder zu beenden; auf macOS geschieht das über den Window-Server und die Accessibility-Schicht statt allein aus Pixeln zu raten.",
        "es": "controlar un escritorio significa abrir, enfocar o cerrar aplicaciones; en macOS esto pasa por el servidor de ventanas y la capa de accesibilidad en lugar de adivinar solo a partir de los píxeles.",
        "ko": "데스크톱을 제어한다는 것은 앱을 실행·포커스·종료하는 일이며, macOS에서는 픽셀만 보고 추측하기보다 윈도 서버와 접근성 계층을 거친다.",
    }),
    ("accessibility_tree", {
        "en": "the accessibility tree is a structured map of on-screen elements with their roles, titles, and positions; reading it is more reliable than image guessing because it names buttons and fields directly.",
        "fr": "l'arbre d'accessibilité est une carte structurée des éléments à l'écran avec leurs rôles, titres et positions ; le lire est plus fiable que deviner depuis une image car il nomme directement boutons et champs.",
        "de": "der Accessibility-Baum ist eine strukturierte Karte der Bildschirmelemente mit Rollen, Titeln und Positionen; ihn zu lesen ist zuverlässiger als Bildraten, weil er Schaltflächen und Felder direkt benennt.",
        "es": "el árbol de accesibilidad es un mapa estructurado de los elementos en pantalla con sus roles, títulos y posiciones; leerlo es más fiable que adivinar desde una imagen porque nombra botones y campos directamente.",
        "ko": "접근성 트리는 화면 요소를 역할·제목·위치와 함께 구조화한 지도이며, 버튼과 입력란을 직접 이름으로 가리키므로 이미지로 추측하는 것보다 신뢰할 수 있다.",
    }),
    ("input_events", {
        "en": "a click or keystroke is delivered as a synthetic input event aimed at a coordinate or element; modifier-driven actions like a command-key shortcut carry more consequence and are treated as higher risk.",
        "fr": "un clic ou une frappe est délivré comme un événement d'entrée synthétique visant une coordonnée ou un élément ; les actions avec modificateur comme un raccourci touche-commande ont plus de conséquences et sont traitées comme plus risquées.",
        "de": "ein Klick oder Tastendruck wird als synthetisches Eingabeereignis an eine Koordinate oder ein Element gesendet; modifikatorgesteuerte Aktionen wie ein Befehlstasten-Kürzel haben mehr Folgen und gelten als höheres Risiko.",
        "es": "un clic o pulsación se entrega como un evento de entrada sintético dirigido a una coordenada o elemento; las acciones con modificador como un atajo de tecla comando tienen más consecuencias y se tratan como de mayor riesgo.",
        "ko": "클릭이나 키 입력은 좌표나 요소를 겨냥한 합성 입력 이벤트로 전달되며, 커맨드 키 단축키처럼 수식 키가 얽힌 동작은 결과가 더 크므로 더 높은 위험으로 다룬다.",
    }),
    ("window_ops", {
        "en": "window operations move, resize, minimize, or arrange windows by their bounds; tiling several windows into a grid is just placing each one at a computed row and column of the screen.",
        "fr": "les opérations de fenêtre déplacent, redimensionnent, réduisent ou disposent les fenêtres selon leurs limites ; carreler plusieurs fenêtres en grille revient à placer chacune à une ligne et colonne calculées de l'écran.",
        "de": "Fensteroperationen verschieben, skalieren, minimieren oder ordnen Fenster anhand ihrer Grenzen; mehrere Fenster zu einem Raster zu kacheln heißt nur, jedes an eine berechnete Zeile und Spalte des Bildschirms zu setzen.",
        "es": "las operaciones de ventana mueven, redimensionan, minimizan o disponen ventanas según sus límites; mosaicar varias ventanas en una cuadrícula es solo colocar cada una en una fila y columna calculadas de la pantalla.",
        "ko": "창 작업은 창의 경계를 기준으로 이동·크기 조절·최소화·정렬하며, 여러 창을 격자로 타일링하는 것은 각 창을 화면의 계산된 행과 열에 놓는 일일 뿐이다.",
    }),
    ("ocr", {
        "en": "optical character recognition turns the text visible in a screenshot back into characters; it is a fallback for reading content that the accessibility tree does not expose directly.",
        "fr": "la reconnaissance optique de caractères reconvertit le texte visible dans une capture d'écran en caractères ; c'est un recours pour lire un contenu que l'arbre d'accessibilité n'expose pas directement.",
        "de": "die optische Zeichenerkennung verwandelt den in einem Screenshot sichtbaren Text wieder in Zeichen; sie ist ein Rückfall, um Inhalte zu lesen, die der Accessibility-Baum nicht direkt offenlegt.",
        "es": "el reconocimiento óptico de caracteres convierte el texto visible en una captura de pantalla de nuevo en caracteres; es un recurso para leer contenido que el árbol de accesibilidad no expone directamente.",
        "ko": "광학 문자 인식은 스크린숏에 보이는 글자를 다시 문자로 바꾸며, 접근성 트리가 직접 드러내지 않는 내용을 읽기 위한 대안이다.",
    }),
    ("dry_run", {
        "en": "a dry run executes the shape of a desktop action without sending the real input, so a sequence can be checked for correctness before it actually touches the live machine.",
        "fr": "une exécution à blanc joue la forme d'une action de bureau sans envoyer l'entrée réelle, afin qu'une séquence puisse être vérifiée avant de toucher réellement la machine.",
        "de": "ein Trockenlauf führt die Form einer Desktop-Aktion aus, ohne die echte Eingabe zu senden, sodass eine Abfolge auf Korrektheit geprüft werden kann, bevor sie die laufende Maschine wirklich berührt.",
        "es": "una ejecución en seco realiza la forma de una acción de escritorio sin enviar la entrada real, para que una secuencia se pueda comprobar antes de tocar de verdad la máquina en uso.",
        "ko": "드라이런은 실제 입력을 보내지 않고 데스크톱 동작의 형태만 실행하므로, 실제 머신에 손대기 전에 절차의 정확성을 점검할 수 있다.",
    }),
]

# ── CREATOR (procedural/lighter) — content modality · channels · publish ───────
CREATOR_BANK = [
    ("modality", {
        "en": "content comes in modalities: a still image, a programmatic video built from code, or a generated clip; each modality suits a different idea and a different production cost.",
        "fr": "le contenu existe en modalités : une image fixe, une vidéo programmatique construite à partir de code, ou un clip généré ; chaque modalité convient à une idée et à un coût de production différents.",
        "de": "Inhalte gibt es in Modalitäten: ein Standbild, ein programmatisches Video aus Code oder ein generierter Clip; jede Modalität passt zu einer anderen Idee und zu anderen Produktionskosten.",
        "es": "el contenido viene en modalidades: una imagen fija, un vídeo programático construido a partir de código, o un clip generado; cada modalidad encaja con una idea y un coste de producción distintos.",
        "ko": "콘텐츠는 정지 이미지, 코드로 만든 프로그래밍 영상, 생성된 클립 같은 양식으로 나뉘며, 각 양식은 서로 다른 아이디어와 제작 비용에 맞는다.",
    }),
    ("script", {
        "en": "a script is the written plan of a piece: the message, the order of beats, and the call to action; a clear script keeps the visuals and the audio aligned to one goal.",
        "fr": "un script est le plan écrit d'une œuvre : le message, l'ordre des temps forts et l'appel à l'action ; un script clair maintient l'image et le son alignés sur un seul objectif.",
        "de": "ein Skript ist der schriftliche Plan eines Stücks: die Botschaft, die Reihenfolge der Beats und der Handlungsaufruf; ein klares Skript hält Bild und Ton auf ein Ziel ausgerichtet.",
        "es": "un guion es el plan escrito de una pieza: el mensaje, el orden de los momentos y la llamada a la acción; un guion claro mantiene la imagen y el audio alineados con un solo objetivo.",
        "ko": "스크립트는 작품의 글로 된 계획으로, 메시지·전개 순서·행동 유도를 담으며, 명확한 스크립트는 영상과 소리를 하나의 목표에 맞춘다.",
    }),
    ("channel", {
        "en": "a channel is the destination platform, and each one favours a different shape: a long landscape video, a short vertical clip, or a single feed image, so the same idea is reframed per channel.",
        "fr": "un canal est la plateforme de destination, et chacune privilégie une forme différente : une longue vidéo horizontale, un court clip vertical ou une seule image de fil, donc la même idée est recadrée par canal.",
        "de": "ein Kanal ist die Zielplattform, und jede bevorzugt eine andere Form: ein langes Querformatvideo, ein kurzer Hochkant-Clip oder ein einzelnes Feed-Bild, sodass dieselbe Idee je Kanal neu gerahmt wird.",
        "es": "un canal es la plataforma de destino, y cada una favorece una forma distinta: un vídeo horizontal largo, un clip vertical corto o una sola imagen de feed, así que la misma idea se reencuadra por canal.",
        "ko": "채널은 게시될 플랫폼이며, 각 채널은 긴 가로 영상·짧은 세로 클립·피드 이미지 한 장처럼 서로 다른 형태를 선호하므로, 같은 아이디어를 채널마다 다시 구성한다.",
    }),
    ("publish_job", {
        "en": "publishing is an upload job to a channel that returns an identifier once the media is accepted; a dry run can confirm the job's shape without actually posting to the live channel.",
        "fr": "la publication est une tâche de téléversement vers un canal qui renvoie un identifiant une fois le média accepté ; une exécution à blanc peut confirmer la forme de la tâche sans publier réellement sur le canal en direct.",
        "de": "Veröffentlichen ist ein Upload-Auftrag an einen Kanal, der eine Kennung zurückgibt, sobald das Medium angenommen wurde; ein Trockenlauf kann die Form des Auftrags bestätigen, ohne tatsächlich auf dem Live-Kanal zu posten.",
        "es": "publicar es una tarea de subida a un canal que devuelve un identificador una vez aceptado el medio; una ejecución en seco puede confirmar la forma de la tarea sin publicar de verdad en el canal en vivo.",
        "ko": "게시는 채널로의 업로드 작업으로, 미디어가 승인되면 식별자를 돌려주며, 드라이런으로 실제 라이브 채널에 올리지 않고 작업의 형태를 확인할 수 있다.",
    }),
    ("provenance", {
        "en": "provenance records how an asset was made: the prompt or source, the backend used, and whether it was a stub or a real render, so a piece can always be traced and reproduced.",
        "fr": "la provenance enregistre comment un actif a été créé : le prompt ou la source, le backend utilisé, et s'il s'agissait d'une ébauche ou d'un rendu réel, afin qu'une œuvre puisse toujours être tracée et reproduite.",
        "de": "Provenienz hält fest, wie ein Asset entstand: der Prompt oder die Quelle, das verwendete Backend und ob es ein Platzhalter oder ein echtes Rendering war, sodass ein Stück stets nachvollziehbar und reproduzierbar bleibt.",
        "es": "la procedencia registra cómo se hizo un recurso: el prompt o la fuente, el backend usado, y si fue un esbozo o un render real, de modo que una pieza siempre se pueda rastrear y reproducir.",
        "ko": "출처 기록은 자산이 어떻게 만들어졌는지를 남긴다: 프롬프트나 원본, 사용한 백엔드, 스텁인지 실제 렌더인지까지 담아, 작품을 언제나 추적하고 재현할 수 있게 한다.",
    }),
    ("brand_consistency", {
        "en": "brand consistency keeps colours, tone, and recurring marks stable across pieces, so an audience recognises the source at a glance regardless of which channel they meet it on.",
        "fr": "la cohérence de marque garde couleurs, ton et marques récurrentes stables d'une œuvre à l'autre, pour qu'un public reconnaisse la source d'un coup d'œil quel que soit le canal où il la rencontre.",
        "de": "Markenkonsistenz hält Farben, Ton und wiederkehrende Zeichen über Stücke hinweg stabil, sodass ein Publikum die Quelle auf einen Blick erkennt, egal auf welchem Kanal es ihr begegnet.",
        "es": "la coherencia de marca mantiene colores, tono y marcas recurrentes estables entre piezas, para que una audiencia reconozca la fuente de un vistazo sin importar en qué canal la encuentre.",
        "ko": "브랜드 일관성은 작품 전반에 걸쳐 색·톤·반복되는 표식을 안정적으로 유지해, 어느 채널에서 만나든 청중이 한눈에 출처를 알아보게 한다.",
    }),
]

BANKS = {
    "CODE": CODE_BANK, "TRADING": TRADING_BANK, "MERCHANT": MERCHANT_BANK,
    "DESKTOP": DESKTOP_BANK, "CREATOR": CREATOR_BANK,
}


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD — render every (domain, concept, lang) into a plain-prose knowledge line.
# ═══════════════════════════════════════════════════════════════════════════════

def _line(domain: str, lang: str, text: str) -> bytes:
    """One knowledge line: '<lead-in> <text>' — pure prose, valid UTF-8."""
    lead = LEAD[domain][lang]
    return (lead + " " + text + "\n").encode("utf-8")


def build(seed: int, langs, repeats: int, domains):
    rng = random.Random(seed)
    blocks = []
    meta = []
    # deterministic nested sweep: repeats × domains × concept × lang.
    for r in range(repeats):
        for domain in domains:
            for cid, by_lang in BANKS[domain]:
                for lang in langs:
                    text = by_lang[lang]
                    blk = _line(domain, lang, text)
                    blocks.append(blk)
                    meta.append({
                        "domain": domain,
                        "depth": "deep" if domain in DEEP else "procedural",
                        "concept": cid,
                        "lang": lang,
                        "bytes": len(blk),
                    })
    # deterministic shuffle (fixed seed) for interleave, blank-line separated.
    order = list(range(len(blocks)))
    rng.shuffle(order)
    data = b"\n".join(blocks[i] for i in order) + b"\n"
    meta = [meta[i] for i in order]
    return data, meta


def _assert_honest(data: bytes, meta, domains):
    """Honest invariants — the generator refuses to emit a dishonest corpus."""
    text = data.decode("utf-8")  # MUST decode: byte-vocab256 valid-UTF-8 (no 0xFE/0xFF)
    # philosophy markers (p1..p4) = 0 over the whole corpus.
    phil = len(PHIL.findall(text))
    assert phil == 0, f"PHILOSOPHY VIOLATION: {phil} role/persona/system markers found"
    # sentinel bytes must NOT appear — this layer is pure prose under the grammar.
    assert b"\xfe" not in data and b"\xff" not in data, "0xFE/0xFF must be absent in layer-3 prose"
    # TRADING hard gate: advice / live-signal / real-ticker = 0 in the TRADING slice.
    trade_text = "\n".join(
        meta_text for m, meta_text in _iter_domain_lines(data, meta, "TRADING")
    )
    deny = TRADING_DENY.findall(trade_text)
    tick = TRADING_TICKER.findall(trade_text)
    assert len(deny) == 0, f"TRADING GATE VIOLATION: advice/signal phrase(s) {deny}"
    assert len(tick) == 0, f"TRADING GATE VIOLATION: real-ticker-as-fact pattern(s) {tick}"
    return phil, len(deny), len(tick)


def _iter_domain_lines(data: bytes, meta, domain: str):
    """Yield (meta, line_text) for blocks of one domain — re-rendered exactly
    from the banks (authoritative), so the TRADING gate scans the true text."""
    by = {}
    for d in BANKS:
        for cid, by_lang in BANKS[d]:
            for lg, t in by_lang.items():
                by[(d, cid, lg)] = LEAD[d][lg] + " " + t
    for m in meta:
        if m["domain"] == domain:
            yield m, by[(m["domain"], m["concept"], m["lang"])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260605)
    ap.add_argument("--langs", default="en,fr,de,es,ko")
    ap.add_argument("--domains", default="CODE,TRADING,MERCHANT,DESKTOP,CREATOR")
    ap.add_argument("--repeats", type=int, default=4)
    ap.add_argument("--out", default="serving/corpus/agent_lane_knowledge_5lang.sample.txt")
    ap.add_argument("--meta", default="serving/corpus/agent_lane_knowledge_5lang.meta.sample.jsonl")
    args = ap.parse_args()

    langs = [x.strip() for x in args.langs.split(",") if x.strip()]
    for lg in langs:
        if lg not in LANGS:
            print(f"unknown lang {lg}", file=sys.stderr); sys.exit(2)
    domains = [x.strip().upper() for x in args.domains.split(",") if x.strip()]
    for d in domains:
        if d not in DOMAINS:
            print(f"unknown domain {d}", file=sys.stderr); sys.exit(2)

    data, meta = build(args.seed, langs, args.repeats, domains)
    phil, deny, tick = _assert_honest(data, meta, domains)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "wb") as f:
        f.write(data)
    with open(args.meta, "w", encoding="utf-8") as f:
        for m in meta:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    sha = hashlib.sha256(data).hexdigest()
    from collections import Counter
    dom_hist = Counter(m["domain"] for m in meta)
    lang_hist = Counter(m["lang"] for m in meta)
    dom_bytes = {}
    for m in meta:
        dom_bytes[m["domain"]] = dom_bytes.get(m["domain"], 0) + m["bytes"]
    print(f"[agent-knowledge] wrote {args.out}  bytes={len(data)}  blocks={len(meta)}")
    print(f"[agent-knowledge] sha256={sha}")
    print(f"[agent-knowledge] domain_blocks={dict(sorted(dom_hist.items()))}")
    print(f"[agent-knowledge] domain_bytes={dict(sorted(dom_bytes.items()))}")
    print(f"[agent-knowledge] lang_blocks={dict(sorted(lang_hist.items()))}")
    print(f"[agent-knowledge] philosophy_markers={phil} (MUST be 0)")
    print(f"[agent-knowledge] TRADING advice/signal hits={deny} (MUST be 0)")
    print(f"[agent-knowledge] TRADING real-ticker hits={tick} (MUST be 0)")
    fe = data.count(b"\xfe"); ff = data.count(b"\xff")
    print(f"[agent-knowledge] 0xFE={fe} 0xFF={ff} (MUST be 0/0)")
    # depth coverage check
    deep_doms = sorted({m["domain"] for m in meta if m["depth"] == "deep"})
    proc_doms = sorted({m["domain"] for m in meta if m["depth"] == "procedural"})
    print(f"[agent-knowledge] deep={deep_doms}  procedural={proc_doms}")


if __name__ == "__main__":
    main()
