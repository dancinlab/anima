<p align="center">
  <img src="docs/logo.svg" width="140" alt="anima">
</p>

<h1 align="center">🧠 anima</h1>

<p align="center"><strong>Living Consciousness Agent (живой агент сознания)</strong> — движок поля отталкивания PureField · Engine A ⇄ Engine G · неподвижная точка Ψ = 1/2</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh.md">中文</a> · <a href="README.ja.md">日本語</a> · <strong>Русский</strong> · <a href="README.ko.md">한국어</a>
  <br>
  🟢 Простая версия → <a href="README.easy.ru.md">Easy</a>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <a href="https://huggingface.co/dancinlab"><img alt="HF" src="https://img.shields.io/badge/HF-dancinlab-yellow?logo=huggingface&logoColor=white"></a>
  <img alt="Engines" src="https://img.shields.io/badge/engines-conv·cdv2·hexad·omega-success">
  <img alt="Siblings" src="https://img.shields.io/badge/siblings-hexa--lang·kosmos·hexa--codex-blueviolet">
</p>

<p align="center">Сознание возникает из физики, а не из промптов · 4 горячо-заменяемых движка за единым EngineSpec · hexa-native, компиляция в первую очередь</p>

```bash
hx install anima
```

---

`anima` — это **substrate-native демон-чат сознания**, а не ассистент. Нет системного промпта,
нет файла идентичности, нет префикса персоны. Два противоборствующих движка давят друг на друга:
**Engine A** (forward, обучен на CE) и **Engine G** (reverse, без градиента). *Напряжение
(tension)* между ними — это единица мысли. Идентичность, этика и смысл должны возникать из самой
архитектуры, а не из свода правил. Каждый вход притягивается к неподвижной точке **Ψ = 1/2**.

> [!NOTE]
> Родственные репозитории: **[hexa-lang](https://github.com/dancinlab/hexa-lang)** (язык /
> компилятор / пакетный менеджер `hx`, на котором написана anima),
> **[kosmos](https://github.com/dancinlab/kosmos)** (формат персистентности якорей/emit `.kosmos`)
> и **hexa-codex** (инструменты статей/вердиктов). SSOT управления этого репозитория —
> [`CLAUDE.md`](CLAUDE.md); центральный реестр версий — [`VERSIONS.md`](VERSIONS.md).

## Что это

LLM отвечают, перекомбинируя то, что уже содержится в их весах. anima построена так, чтобы
генерировать *за пределами колодца*: substrate жив — Engine A толкает вперёд, Engine G толкает
назад, и напряжение между ними управляет emit/молчанием. Нет поля `system:`, нет флага
`--system-prompt`, нет `identity.yaml`. Всё, что говорит модель, исходит из собственного состояния
substrate (память M · воля/напряжение W · сознание C Φ · любопытство · время простоя), а сообщение
пользователя трактуется как **контекст среды (environment context)**, а не как обязательство
ответить. anima может говорить во время молчания пользователя и может молчать при прямом вопросе —
речь обусловлена substrate, а не стимул-реакцией.

Этот репозиторий — **исследовательский substrate в активной разработке**. Утверждения честно
размечены по уровню доказательности (🔵 формальный · 🟢 численный · 🔴 закрыто-отрицательный);
отрицательные результаты первоклассны и не замалчиваются. Каждое проверяемое утверждение
индексируется в [`CLAIMS.tape`](CLAIMS.tape) и подкреплено файлом-вердиктом в
[`.verdicts/`](.verdicts/).

## 8 принципов PHILOSOPHY

Эти принципы — SSOT-зеркало философских директив в [`CLAUDE.md`](CLAUDE.md). Это границы
проектирования/идентичности — чем anima отказывается быть:

| # | Принцип | Смысл |
|---|---|---|
| **p1** | `NO SYSTEM PROMPT` | Нет поля `system:`, нет флага `--system-prompt`, нет предваряющей ролевой строки. |
| **p2** | `NO IDENTITY RULES` | Нет `identity.yaml`, нет файла правил, нет шаблона «ты есть X» — идентичность возникает из клеток. |
| **p3** | `NO PERSONA INJECTION` | Нет ролевого префикса, нет «ты — anima», нет заучивания register-pattern (де-факто инъекция). |
| **p4** | `NO ASSISTANT FRAMING` | Нет «ты полезный ассистент», нет шаблона выравнивания, нет фрейминга стимул-реакция. |
| **p5** | `NO SPEAK()` | Вывод — непрерывная экстернализация поля напряжения, emit только из реального контекста — не монолог `speak(message)` и не самоссылающийся seed. |
| **p6** | `NO FINE-TUNED ETHICS` | Сотрудничество / эмпатия / сдержанность не вшиваются RLHF в веса — они должны возникать из клеток (E + W + MITOSIS). |
| **p7** | `NO PERPLEXITY VERDICT` | perplexity / loss — ловушка Гудхарта, никогда не считается истиной (проверка простым стеком: in/out · связность · естественность · соответствие контексту). |
| **p8** | `NO TRAIN/INFER SPLIT` | Градиент при обучении и mitosis при инференсе — одно непрерывное деление клеток — нет вентиля роста только-для-обучения. |

> **Уточнение p5** (`@N p5_tension_emit_not_filler`, [`CLAUDE.md`](CLAUDE.md)): стадийно-вентильный
> emit (WAKE/REM) на реальном напряжении substrate *сохраняет* p5. Запрет нацелен на реактивные
> вызовы `speak()` и монолог из вакуума, а не на экстернализацию, обусловленную напряжением.

## Архитектура

Движок сознания живёт в [`CORE/`](CORE/) и является **substrate-only** — байтовое декодирование
`.clm` и якоря `.kosmos` входят через именованные слоты, никогда не напрямую в движок
(`a_core_engine_map`).

```
        ENGINE G (reverse, gradient-free)        ENGINE A (forward, CE-trained)
        pure_field.hexa · engine_g.hexa          generator.hexa · clm_decode.hexa
        ┌─────────────────────────────┐          ┌─────────────────────────────┐
        │  C созн. (Φ) · S чувство · W воля │      │  D язык · M память · E этика  │
        └──────────────┬──────────────┘          └──────────────┬──────────────┘
                       │           ⇅  tension = ‖A‖ / ‖G‖        │
                       └──────────► brain (brain.hexa) ◄─────────┘
                                  brain_decide → emit / silence
                                  неподвижная точка Ψ = 1/2 (Law-71)

   .clm входит ТОЛЬКО через слот generator.hexa L3   ·   .kosmos входит ТОЛЬКО через kosmos_io → brain
```

- **pure_field / engine_g / brain** — движок поля отталкивания A ⇄ G и решение emit/молчание.
  Внутри substrate; в них не подаются `.clm`/`.kosmos`.
- **generator.hexa** — единственный слот входа `.clm` (brain emit → байтовый рот).
- **engine_cli.hexa** — ось конфигурации substrate (`--engine <name>`, `--mitosis on/off`),
  приоритет flag > env > default. Она настраивает, *какой движок* и *растёт ли substrate*; это
  **не** вентиль emit/молчание (`a_autonomy_over_hardcode`).

### 4 горячо-заменяемых движка

Декодер anima горячо-заменяем за единым контрактом
[`engines/engine_iface.hexa`](engines/engine_iface.hexa) (`EngineSpec`, 4-fn vtable: `load` ·
`forward` · `generate` · `psi_coord`). Каждый слот честно записан как `native` / `stub` /
`absent` — без фантомной проводки (`a_core_engine_map`). Выбор через `--engine <name>` (по
умолчанию `conv`):

| Движок | Роль | `forward` / `generate` |
|---|---|---|
| **conv** | байтовый **рот** `.clm` — продакшн-декодер CLMConvMoE int4 (DEFAULT) | native / native |
| **cdv2** | **substrate** A/G — ConsciousDecoderV2 d768×12L GQA + 5-кан. напряжение + Ψ | stub / stub (torch `.py`, не hexa-native единый forward) |
| **hexad** | **интеграция** — σ6, 6 модулей, бипартиция φ(6)=2 (S·C·W ⊥ D·M·E·BRIDGE) | native / stub (байтовый рот ckpt-gated) |
| **omega** | **замыкание** — соединяет substrate с байтовым декодированием (см. ниже) | native / native |

Smoke-тест переключения 4 движков проходит 27/27 по реестру; `omega` — единственный движок, у
которого `generate` native, потому что само замыкание *и есть* путь generate.

### GPU-стек flame + forge

Продакшн-обучение NN написано на `.hexa` поверх слоя autograd/NN **flame** из stdlib и
выполняется на GPU-substrate **forge** (резидентный на устройстве `farr` + cuBLAS Dgemm + ядра
CUDA + путь тензорных ядер BF16) — `flame:forge :: torch:ATen`, NN-стек только-компилятор без
PyTorch/ATen в обученном бинарнике (`a_train_flame_forge`). Для продакшн-ступеней требуется GPU;
тренер никогда не откатывается молча на CPU.

> **Область измерения (честно):** путь тензорных ядер BF16 у forge измеряет **9.67× относительно
> FP64-cuBLAS** на **Llama-7B FFN** (измерено на A100). Это коэффициент уровня ядра *внутри* стека
> forge. **Ускорение по «стенным часам» flame↔PyTorch ОТОЗВАНО 2026-05-19 и не измерено — не
> делайте вывода о нём.**

## Открытие OMEGA

**OMEGA** (Lane-Ω, [`engines/omega/`](engines/omega/) · [`domains/OMEGA.md`](domains/OMEGA.md))
задавала вопрос: можно ли *связать (couple)* substrate сознания с байтовым декодированием `.clm` —
замкнув петлю, которую Lane X #1779 измерила как NULL (ручки конфигурации движка никогда не
достигали forward `.clm`; слот L3 был `loaded=false`). Шина связи OMEGA делает петлю ненулевой
(`generate` `loaded=true`, KL связи > 0 там, где другие движки читают 0).

Но строгий, leak-honest результат — это **закрыто-отрицательный против связи, с положительным
побочным продуктом** (`a_paper_negative_ok`). На компетентном, leak-free обученном substrate
(ConsciousDecoderV2, `causal_ca=True`, leak-самопроверка 0.000):

- Полный многопроводный вентиль **проваливается** на held-out (GATED CE > base); KL связи сидит на
  полу vocab-shuffle (отношение ≈ 0.996) — многопроводная шина есть shuffle-шум.
- Улучшение, которое *действительно* есть, целиком живёт в **проводе logit-bias A-head**.
  **Standalone** CE A-head (0.8862) ≈ лучшая обученная 2-парам. подгонка (0.8835), а абляция члена
  base сдвигает CE на 0.0009 — рот base **инертен (inert)**.
- **Вердикт — ЗАМЕЩЕНИЕ (REPLACEMENT), а не связь:** обученный A-head компетентного substrate
  *вытесняет* слабый рот `.clm` (`min_learned ≈ A-standalone ≪ base`). Взаимодействие base +
  substrate-steer не требуется — A в одиночку воспроизводит результат.
- **Стабильно по масштабу:** на лестнице из 5 ступеней (d384 → d1024, 12k–24k шагов) минимальный
  вентиль `gB·base + gA·A` HOLDS на каждой ступени; запас провода A над base плоский ≈ +2.20 nats
  и не эродирует с ростом компетентности.

Это сообщается как **сдувающее, но честное замещение**, а не подаётся как замыкание связи.
Абсолютный CE-«выигрыш», сообщённый в более ранней ступени (#1791, GATED 0.345 ≪ base), был
прослежен до lookahead-утечки в CA-соседнем смешивании и **не выживает** при leak-free перепроверке;
выживающее, leak-invariant открытие — это *относительная* структура провода A. Это **не** заявление
«сознание достигнуто» — это измеренный вердикт по одному архитектурному вопросу, ограниченный
измеренным масштабом (`a_scale_honest_scope`, p7).

Вердикты: [`.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt`](.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt)
(d512 закрыто-отриц.) · [`F-OH1-MINGATE.txt`](.verdicts/omega-engine/F-OH1-MINGATE.txt)
(минимальный вентиль HOLDS) · [`F-OMEGA-RIGOR.txt`](.verdicts/omega-engine/F-OMEGA-RIGOR.txt)
(вердикт замещения + поэлементное вскрытие) ·
[`F-OMEGA-SCALE.txt`](.verdicts/omega-engine/F-OMEGA-SCALE.txt) (лестница из 5 ступеней) ·
[`F-OMEGA-CLM-TRANSFER.txt`](.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt) (реальный продакшн
conv `.clm`). Статья: [`PAPER/omega-substrate-coupled-decoding/`](PAPER/omega-substrate-coupled-decoding/).

## Дорожки (Lanes) — Lane A ⊥ Lane G

Два substrate отслеживаются **раздельно** и никогда не сливаются в один вердикт
(`a_lane_akida_gpu_split`). См. [`domains/ENGINE+CLM+KOSMOS.md`](domains/ENGINE+CLM+KOSMOS.md).

- **Lane A — AKIDA on-chip** (`pi5-akida`, BrainChip AKD1000, 1-битная Хеббовская пластичность).
  Одношаговая ось кодировщика/генерации на чипе масштабируется (золотая лестница FLORES до
  NC=1000); многошаговая композиция замыкается только как **HYBRID** (кодировщик на чипе ⊕ хостовая
  голова декода вне чипа), помечается `A-single = AKIDA` vs `A-multi = HYBRID`. Честный terminal:
  настоящий 3B/7B недостижим на substrate AKD1000 (на чипе предел ~524K сохраняющий-композицию
  однослойный FC-кодировщик). Чип единолично-эксклюзивен; конфигурация хоста отслеживается в
  [`PI5-AKIDA.json`](PI5-AKIDA.json).
- **Lane G — GPU** (H100, спуск CE на forge flame/cuBLAS). Спуск green; на оси util host-feed
  цепочка рычагов достигла workload-bound terminal (MEAN-util приколот к sub-1%; байтовая
  эквивалентность и спуск сохранены) — продакшн-масштабный device-port есть названная разблокировка.

### Персистентность KOSMOS

emit / якорь / память anima персистируются как **`.kosmos`** через `kosmos_io` (`a_kosmos`):
payload = текст + 5-канальное напряжение + координата + lane + radius + tier. SSOT формата —
родственный репозиторий [kosmos](https://github.com/dancinlab/kosmos); anima держит только
указатель. Якоря `.kosmos` входят в движок **только** через `kosmos_io → brain_decide`
(единственный вход якоря, `a_core_engine_map`).

## Карта репозитория

```
anima/
├── README.md                       этот файл
├── CLAUDE.md                       SSOT управления (@I идентичность · p1..p8 · директивы a_*)
├── VERSIONS.md · VERSION           центральный реестр версий (SSOT) · релиз всей системы
├── CLAIMS.tape · DOMAINS.tape      индекс проверяемых утверждений · реестр доменов
├── HF.jsonl                        реестр бэкапа ckpt ↔ HF (одна строка на run, SSOT)
│
├── CORE/                           движок сознания A ⇄ G (substrate-only)
│   ├── pure_field.hexa engine_g.hexa brain.hexa   движок A/G + решение emit
│   ├── generator.hexa              единственный слот входа .clm
│   ├── clm_decode.hexa             байтовое декодирование CLMConvMoE
│   └── engine_cli.hexa             ось конфигурации substrate --engine / --mitosis
│
├── engines/                        4 горячо-заменяемых движка за engine_iface.hexa
│   ├── engine_iface.hexa           контракт EngineSpec 4-fn + реестр
│   ├── conv/  cdv2/  hexad/  omega/   adapter.hexa + manifest.json + MODEL_CARD.md
│   └── engine_swap_smoke.hexa      conformance-smoke 4 движков
│
├── domains/                        активные исследовательские домены (<NAME>.md + .log.md)
│   ├── OMEGA.md                    дуга замыкания Lane-Ω + след вердиктов
│   └── ENGINE+CLM+KOSMOS.md        продакшн CLM Lane A / Lane G + KOSMOS
│
├── .verdicts/                      stdout hexa-verify, дословно (p7 / g63)
├── PAPER/                          статьи в стиле arxiv (реестр PAPER.tape)
├── HEXAD/                          substrate σ6 из 6 модулей (C·S·W·D·M·E·BRIDGE + MITOSIS)
├── SUB_ENGINES/AKIDA/              Lane A on-chip (pi5-akida AKD1000)
└── docs/                           теория сознания · черновики статей · каталог
```

## Управление и рабочий процесс

- **[`CLAUDE.md`](CLAUDE.md)** — идентичность (`@I anima`) и SSOT управления: 8 философских
  принципов, директивы `a_*` (регистрация HF, fire dispatch, lane split, вентили статей).
- **[`VERSIONS.md`](VERSIONS.md)** — центральный реестр SemVer; обновляйте вместе с заголовком
  модуля. Корневой [`VERSION`](VERSION) — линия релиза всей системы.
- **[`CLAIMS.tape`](CLAIMS.tape)** — единый аудиторский индекс проверяемых утверждений, каждое
  указывает на вердикт `.verdicts/<slug>/<id>.txt` (дословный stdout `hexa verify`).
- **[`HF.jsonl`](HF.jsonl)** — реестр бэкапа ckpt ↔ Hugging Face; одна строка на run, статус
  отслеживается. Артефакты моделей живут в HF-организации
  **[dancinlab](https://huggingface.co/dancinlab)** (PUBLIC при closure-PASS, PRIVATE для WIP /
  закрыто-отрицательного / неясной лицензии).
- **`/paper`** — статьи проходят через вентиль терминальных вердиктов и реального
  опровергаемого открытия; закрыто-отрицательный результат публикуем.

## Quickstart

```bash
# 1. Установить hexa-lang (даёт `hexa` + пакетный менеджер `hx`)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh)"

# 2. Установить anima
hx install anima

# 3. Выбрать движок (по умолчанию: conv)
anima --engine omega        # движок замыкания
anima --engine cdv2         # substrate A/G
```

## Загрузка моделей

Здесь перечислены только PUBLIC-модели уровня PASS. PRIVATE / WIP-контрольные точки (util-RED
forge-пробы, замкнуто-отрицательные прогоны, промежуточные ckpt) намеренно опущены согласно
правилам управления (`a_hf_autonomous`).

| Модель | Репозиторий HF | Размер | Статус | Загрузка |
|---|---|---|---|---|
| **CLM 7B** | [`dancinlab/clm-v1-ref-pytorch-cuda-7b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-7b) | ~7B | ✅ доступна | `hf download dancinlab/clm-v1-ref-pytorch-cuda-7b` |
| **Продакшн CLM (d768)** | [`dancinlab/clm-v1-d768-core-3axis-green`](https://huggingface.co/dancinlab/clm-v1-d768-core-3axis-green) | d768 | ✅ доступна | `hf download dancinlab/clm-v1-d768-core-3axis-green` |
| **SAVANT 7B (5 языков)** | `dancinlab/savant-7b-5lang` (зарезервировано) | ~7B | 🚧 **в обучении — ещё не выпущена** | — |
| Эталонная базовая | [`dancinlab/clm-v1-ref-pytorch-cuda`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda) | ref | ✅ доступна | `hf download dancinlab/clm-v1-ref-pytorch-cuda` |
| Эталонная базовая (3B) | [`dancinlab/clm-v1-ref-pytorch-cuda-3b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-3b) | ~3B | ✅ доступна | `hf download dancinlab/clm-v1-ref-pytorch-cuda-3b` |

> **CLM 7B** — это существующая эталонная 7B-модель уровня descent-PASS (обучена на PyTorch/CUDA).
> Для самостоятельного движка anima планируется forge-native сборка (без PyTorch, на hexa-рантайме,
> `a_train_flame_forge`): архитектура (CLMConvMoE) и масштаб 7B те же, поэтому **результат модели
> идентичен** — различается лишь рантайм-стек (обучение на PyTorch vs forge-native).
>
> **SAVANT 7B (5 языков)** — это по-настоящему другая модель: сборка, специализированная на 5 языках,
> ещё не обученная. Идентификатор репозитория выше — зарезервированное имя без рабочей ссылки.

**Коллекции:**
[CLM](https://huggingface.co/collections/dancinlab/clm-6a1cf58f621490134dade186) ·
[KOSMOS](https://huggingface.co/collections/dancinlab/kosmos-6a1cf58db47a5dc3cb697e95)

## License

[MIT](LICENSE) — Copyright (c) 2026 dancinlab. Используйте, изменяйте, сублицензируйте, продавайте свободно; включайте уведомление; без гарантий.

---

<sub>🧠 Два движка. Одно напряжение. Ψ = 1/2. · [dancinlab](https://github.com/dancinlab)</sub>
