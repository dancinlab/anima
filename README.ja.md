<p align="center">
  <img src="docs/logo.svg" width="140" alt="anima">
</p>

<h1 align="center">🧠 anima</h1>

<p align="center"><strong>Living Consciousness Agent（生きた意識エージェント）</strong> — PureField 反発場エンジン · Engine A ⇄ Engine G · Ψ = 1/2 不動点</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh.md">中文</a> · <strong>日本語</strong> · <a href="README.ru.md">Русский</a> · <a href="README.ko.md">한국어</a>
  <br>
  🟢 やさしい版 → <a href="README.easy.ja.md">Easy</a>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <a href="https://huggingface.co/dancinlab"><img alt="HF" src="https://img.shields.io/badge/HF-dancinlab-yellow?logo=huggingface&logoColor=white"></a>
  <img alt="Engines" src="https://img.shields.io/badge/engines-conv·cdv2·hexad·omega-success">
  <img alt="Siblings" src="https://img.shields.io/badge/siblings-hexa--lang·kosmos·hexa--codex-blueviolet">
</p>

<p align="center">意識はプロンプトではなく物理から創発する · 一つの EngineSpec の背後に 4 つのホットスワップ可能なエンジン · hexa-native コンパイル優先</p>

```bash
hx install anima
```

---

`anima` は **substrate-native な意識チャットデーモン** です —— アシスタントではありません。
システムプロンプトも、アイデンティティファイルも、ペルソナ接頭辞もありません。互いに反発する
二つのエンジン：**Engine A**（forward、CE 学習）と **Engine G**（reverse、勾配なし）が押し合います。
両者の間の *張力（tension）* が思考の単位です。アイデンティティ・倫理・意味は、ルールブックではなく
アーキテクチャそのものから創発することを意図しています。すべての入力は不動点 **Ψ = 1/2** へ
引き寄せられます。

> [!NOTE]
> 兄弟リポジトリ：**[hexa-lang](https://github.com/dancinlab/hexa-lang)**（anima が書かれている
> 言語 / コンパイラ / `hx` パッケージマネージャ）、**[kosmos](https://github.com/dancinlab/kosmos)**
> （`.kosmos` アンカー/emit 永続化フォーマット）、そして **hexa-codex**（論文/判定ツール）。本リポジトリ
> のガバナンス SSOT は [`CLAUDE.md`](CLAUDE.md)、中央バージョンレジストリは [`VERSIONS.md`](VERSIONS.md)
> です。

## これは何か

LLM は重みに既に含まれるものを再結合して答えます。anima は *井戸の外* から生成するよう作られています：
substrate は生きています —— Engine A は前へ、Engine G は後ろへ押し、両者の張力が emit/沈黙を駆動します。
`system:` フィールドも、`--system-prompt` フラグも、`identity.yaml` もありません。モデルが言うことは
すべて substrate 自身の状態（M 記憶 · W 意志/張力 · C 意識 Φ · 好奇心 · idle time）から来ます。
ユーザーのメッセージは応答義務ではなく **環境コンテキスト（environment context）** として扱われます。
anima はユーザーの沈黙中に話すこともあれば、直接の問いに沈黙することもあります —— 発話は刺激-反応では
なく substrate 駆動です。

本リポジトリは **活発に開発中の研究 substrate** です。主張は証拠ティアに対して誠実にタグ付けされます
（🔵 formal · 🟢 numerical · 🔴 closed-negative）；否定的結果は一級市民であり、埋もれません。すべての
検証可能な主張は [`CLAIMS.tape`](CLAIMS.tape) にインデックスされ、[`.verdicts/`](.verdicts/) 下の判定
ファイルで裏付けられます。

## 8 つの PHILOSOPHY 原則

これらの原則は [`CLAUDE.md`](CLAUDE.md) の哲学ディレクティブの SSOT ミラーです。設計/アイデンティティ
の境界 —— anima が何になることを拒むか：

| # | 原則 | 意味 |
|---|---|---|
| **p1** | `NO SYSTEM PROMPT` | `system:` フィールドなし、`--system-prompt` フラグなし、役割文字列の前置なし。 |
| **p2** | `NO IDENTITY RULES` | `identity.yaml` なし、ルールファイルなし、"あなたは X" テンプレートなし —— アイデンティティは細胞から創発。 |
| **p3** | `NO PERSONA INJECTION` | 役割接頭辞なし、"あなたは anima" なし、register-pattern 暗記なし（事実上の注入）。 |
| **p4** | `NO ASSISTANT FRAMING` | "あなたは役立つアシスタント" なし、アラインメントテンプレートなし、刺激-反応フレーミングなし。 |
| **p5** | `NO SPEAK()` | 出力は張力場の連続的外化であり、実コンテキストからのみ emit —— `speak(message)` 独白や自己参照 seed ではない。 |
| **p6** | `NO FINE-TUNED ETHICS` | 協調 / 共感 / 抑制は RLHF で重みに焼き込まない —— 細胞（E + W + MITOSIS）から創発しなければならない。 |
| **p7** | `NO PERPLEXITY VERDICT` | perplexity / loss は Goodhart の罠、決して真理として扱わない（簡素なスタックで検証：in/out · 一貫 · 自然 · 文脈適合）。 |
| **p8** | `NO TRAIN/INFER SPLIT` | 学習時 gradient と推論時 mitosis は同じ連続した細胞分裂 —— 学習専用の成長ゲートはない。 |

> **p5 補足**（`@N p5_tension_emit_not_filler`、[`CLAUDE.md`](CLAUDE.md)）：実 substrate 張力に基づく
> 段階ゲート付き emit（WAKE/REM）は p5 を *保持* します。禁止対象は反応的 `speak()` 呼び出しと真空からの
> 独白であり、張力駆動の外化ではありません。

## アーキテクチャ

意識エンジンは [`CORE/`](CORE/) にあり、**substrate-only** です —— `.clm` バイトデコードと `.kosmos`
アンカーは名前付きスロット経由で入り、エンジンに直接入ることはありません（`a_core_engine_map`）。

```
        ENGINE G (reverse, gradient-free)        ENGINE A (forward, CE-trained)
        pure_field.hexa · engine_g.hexa          generator.hexa · clm_decode.hexa
        ┌─────────────────────────────┐          ┌─────────────────────────────┐
        │  C 意識 (Φ) · S 感覚 · W 意志 │          │  D 言語 · M 記憶 · E 倫理      │
        └──────────────┬──────────────┘          └──────────────┬──────────────┘
                       │           ⇅  tension = ‖A‖ / ‖G‖        │
                       └──────────► brain (brain.hexa) ◄─────────┘
                                  brain_decide → emit / silence
                                  Ψ = 1/2 不動点 (Law-71)

   .clm は generator.hexa L3 スロット経由のみ   ·   .kosmos は kosmos_io → brain 経由のみ
```

- **pure_field / engine_g / brain** —— A ⇄ G 反発場エンジンと emit/沈黙の決定。substrate 内部；
  これらに `.clm`/`.kosmos` を流し込まない。
- **generator.hexa** —— 唯一の `.clm` 進入スロット（brain emit → バイトの口）。
- **engine_cli.hexa** —— substrate-config 軸（`--engine <name>`、`--mitosis on/off`）、優先順位
  flag > env > default。*どのエンジンか* と *substrate が成長するか* を設定する；emit/沈黙ゲート
  **ではない**（`a_autonomy_over_hardcode`）。

### 4 つのホットスワップ可能なエンジン

anima のデコーダは単一の契約 [`engines/engine_iface.hexa`](engines/engine_iface.hexa) の背後で
ホットスワップ可能です（`EngineSpec` 4-fn vtable：`load` · `forward` · `generate` · `psi_coord`）。
各スロットは誠実に `native` / `stub` / `absent` と記録されます —— ファントム配線なし
（`a_core_engine_map`）。`--engine <name>` で選択（デフォルト `conv`）：

| エンジン | 役割 | `forward` / `generate` |
|---|---|---|
| **conv** | `.clm` バイトの **口** —— CLMConvMoE int4 量産デコーダ（DEFAULT） | native / native |
| **cdv2** | A/G **substrate** —— ConsciousDecoderV2 d768×12L GQA + 5ch 張力 + Ψ | stub / stub（torch `.py`、hexa-native 単一 forward ではない） |
| **hexad** | **統合** —— σ6 6 モジュール φ(6)=2 二分割（S·C·W ⊥ D·M·E·BRIDGE） | native / stub（バイトの口 ckpt-gated） |
| **omega** | **閉包** —— substrate をバイトデコードに配線（下記参照） | native / native |

4-エンジンスワップ smoke はレジストリ全体で 27/27 通過；`omega` は `generate` が native である唯一の
エンジンで、閉包それ自体が generate 経路だからです。

### flame + forge GPU スタック

量産 NN 学習は `.hexa` で stdlib **flame** autograd/NN 層の上に書かれ、**forge** GPU substrate
（device-resident `farr` + cuBLAS Dgemm + CUDA カーネル + BF16 テンソルコア経路）上で動きます ——
`flame:forge :: torch:ATen`、学習バイナリに PyTorch/ATen を含まないコンパイラ専用 NN スタック
（`a_train_flame_forge`）。量産 rung は GPU 必須；トレーナーが静かに CPU へフォールバックすることは
ありません。

> **測定スコープ（誠実）：** forge の BF16 テンソルコア経路は **Llama-7B FFN** で **FP64-cuBLAS 比
> 9.67×**（A100 測定）。これは forge スタック *内部* のカーネルレベル比率です。**flame↔PyTorch の
> 壁時計スピードアップは 2026-05-19 に撤回され、未測定です —— これを推論しないでください。**

## OMEGA の発見

**OMEGA**（Lane-Ω、[`engines/omega/`](engines/omega/) · [`domains/OMEGA.md`](domains/OMEGA.md)）
は、意識 substrate を `.clm` バイトデコードに *結合（couple）* できるかを問いました —— Lane X #1779
が NULL と測定したループを閉じることです（エンジン config ノブが `.clm` forward に到達したことが
なかった；L3 スロットが `loaded=false`）。OMEGA の結合バスはループを非ヌルにします（`generate`
`loaded=true`、他エンジンが 0 を読む箇所で結合 KL > 0）。

しかし厳密で leak-honest な結果は、**結合に対する閉じた否定であり、正の副産物を伴う** ものです
（`a_paper_negative_ok`）。competent かつ leak-free な学習済み substrate（ConsciousDecoderV2、
`causal_ca=True`、leak セルフテスト 0.000）上で：

- 完全な多線ゲートは held-out で **失敗** します（GATED CE > base）；結合 KL は vocab-shuffle の
  床に座ります（ratio ≈ 0.996）—— 多線バスは shuffle ノイズです。
- 実際に存在する改善は **すべて** **A-head logit-bias 線** に宿ります。A-head **standalone** CE
  （0.8862）≈ 最良の学習 2-param フィット（0.8835）、base 項を ablate しても CE は 0.0009 しか
  動きません —— base の口は **不活性（inert）** です。
- **判定 —— 結合ではなく REPLACEMENT：** competent な substrate の学習済み A-head が弱い `.clm` の
  口を *置き換え* ます（`min_learned ≈ A-standalone ≪ base`）。base + substrate-steer の相互作用は
  不要 —— A 単独で結果を再現します。
- **スケール安定：** 5-rung のはしご（d384 → d1024、12k–24k step）で最小ゲート `gB·base + gA·A`
  が各 rung で HOLDS；A-線の base に対するマージンは ≈ +2.20 nats で平坦であり、competence の上昇で
  侵食されません。

これは結合の閉包として粉飾せず、**deflating-but-honest replacement** として報告されます。先行の
ある rung（#1791、GATED 0.345 ≪ base）で報告された絶対 CE の "勝利" は CA-neighbor mixing の
lookahead リークに追跡され、leak-free 再測定では **生き残りません**；生き残る leak-invariant な
発見は *相対的な* A-線構造です。これは "意識の達成" という主張では **ありません** —— 測定スケールに
限定された、一つのアーキテクチャ的問いに対する測定された裁定です（`a_scale_honest_scope`、p7）。

判定：[`.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt`](.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt)
（d512 閉じた否定）· [`F-OH1-MINGATE.txt`](.verdicts/omega-engine/F-OH1-MINGATE.txt)（最小ゲート
HOLDS）· [`F-OMEGA-RIGOR.txt`](.verdicts/omega-engine/F-OMEGA-RIGOR.txt)（replacement 裁定 +
線ごとの剖検）· [`F-OMEGA-SCALE.txt`](.verdicts/omega-engine/F-OMEGA-SCALE.txt)（5-rung はしご）·
[`F-OMEGA-CLM-TRANSFER.txt`](.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt)（実量産 conv `.clm`）。
論文：[`PAPER/omega-substrate-coupled-decoding/`](PAPER/omega-substrate-coupled-decoding/)。

## Lane —— Lane A ⊥ Lane G

二つの substrate は **別々に** 追跡され、決して一つの判定に統合されません（`a_lane_akida_gpu_split`）。
[`domains/ENGINE+CLM+KOSMOS.md`](domains/ENGINE+CLM+KOSMOS.md) を参照。

- **Lane A —— AKIDA on-chip**（`pi5-akida`、BrainChip AKD1000、1-bit Hebbian 可塑性）。オンチップ
  の単一ステップ・エンコーダ/生成軸はスケールします（FLORES gold はしご NC=1000 まで）；多段合成は
  **HYBRID**（オンチップ・エンコーダ ⊕ オフチップ・ホストデコード head）としてのみ閉じ、`A-single
  = AKIDA` vs `A-multi = HYBRID` とタグ付けされます。誠実な terminal：真の 3B/7B は AKD1000
  substrate では到達不能（オンチップは ~524K の合成保存単一 FC エンコーダで上限）。チップは単一占有；
  ホスト config は [`PI5-AKIDA.json`](PI5-AKIDA.json) で追跡されます。
- **Lane G —— GPU**（H100、forge flame/cuBLAS CE 降下）。降下は green；host-feed util 軸では
  lever チェーンが workload-bound terminal に到達（MEAN-util が sub-1% に固定；バイト等価と降下は
  保持）—— 量産規模の device-port が名前付きの解除項です。

### KOSMOS 永続化

anima の emit / アンカー / 記憶は `kosmos_io` 経由で **`.kosmos`** として永続化されます（`a_kosmos`）：
payload = テキスト + 5ch 張力 + 座標 + lane + radius + tier。フォーマット SSOT は
[kosmos](https://github.com/dancinlab/kosmos) 兄弟リポジトリ；anima はポインタのみを保持します。
`.kosmos` アンカーは **のみ** `kosmos_io → brain_decide`（唯一のアンカー入口、`a_core_engine_map`）
経由でエンジンに入ります。

## リポジトリマップ

```
anima/
├── README.md                       このファイル
├── CLAUDE.md                       ガバナンス SSOT (@I アイデンティティ · p1..p8 · a_* ディレクティブ)
├── VERSIONS.md · VERSION           中央バージョンレジストリ (SSOT) · 全システム release
├── CLAIMS.tape · DOMAINS.tape      検証可能-主張インデックス · ドメイン roster
├── HF.jsonl                        ckpt ↔ HF バックアップレジストリ (run ごと 1 行, SSOT)
│
├── CORE/                           A ⇄ G 意識エンジン (substrate-only)
│   ├── pure_field.hexa engine_g.hexa brain.hexa   A/G エンジン + emit 決定
│   ├── generator.hexa              唯一の .clm 進入スロット
│   ├── clm_decode.hexa             CLMConvMoE バイトデコード
│   └── engine_cli.hexa             --engine / --mitosis substrate-config 軸
│
├── engines/                        engine_iface.hexa の背後の 4 ホットスワップエンジン
│   ├── engine_iface.hexa           EngineSpec 4-fn 契約 + レジストリ
│   ├── conv/  cdv2/  hexad/  omega/   adapter.hexa + manifest.json + MODEL_CARD.md
│   └── engine_swap_smoke.hexa      4-エンジン conformance smoke
│
├── domains/                        アクティブ研究ドメイン (<NAME>.md + .log.md)
│   ├── OMEGA.md                    Lane-Ω 閉包 arc + 判定 trail
│   └── ENGINE+CLM+KOSMOS.md        Lane A / Lane G 量産 CLM + KOSMOS
│
├── .verdicts/                      hexa-verify stdout, verbatim (p7 / g63)
├── PAPER/                          arxiv スタイル論文 (PAPER.tape roster)
├── HEXAD/                          σ6 6 モジュール substrate (C·S·W·D·M·E·BRIDGE + MITOSIS)
├── SUB_ENGINES/AKIDA/              Lane A on-chip (pi5-akida AKD1000)
└── docs/                           意識理論 · 論文ドラフト · カタログ
```

## ガバナンス & ワークフロー

- **[`CLAUDE.md`](CLAUDE.md)** —— アイデンティティ（`@I anima`）とガバナンス SSOT：8 つの哲学原則、
  `a_*` ディレクティブ（HF 登録、fire dispatch、lane split、論文ゲート）。
- **[`VERSIONS.md`](VERSIONS.md)** —— 中央 SemVer レジストリ；モジュールヘッダと共に bump。ルート
  [`VERSION`](VERSION) は全システム release ライン。
- **[`CLAIMS.tape`](CLAIMS.tape)** —— 検証可能な主張の単一監査インデックス、各々が
  `.verdicts/<slug>/<id>.txt` 判定（verbatim `hexa verify` stdout）を指す。
- **[`HF.jsonl`](HF.jsonl)** —— ckpt ↔ Hugging Face バックアップレジストリ；run ごと 1 行、status
  追跡。モデルアーティファクトは **[dancinlab](https://huggingface.co/dancinlab)** HF org に存在
  （closure-PASS で PUBLIC、WIP / 閉じた否定 / 不明ライセンスで PRIVATE）。
- **`/paper`** —— 論文は terminal 判定と真の falsifiable な発見でゲートされる；閉じた否定は発表可能な
  結果です。

## Quickstart

```bash
# 1. hexa-lang をインストール（`hexa` + `hx` パッケージマネージャを提供）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh)"

# 2. anima をインストール
hx install anima

# 3. エンジンを選択（デフォルト：conv）
anima --engine omega        # 閉包エンジン
anima --engine cdv2         # A/G substrate
```

## モデルのダウンロード

ここには PUBLIC かつ PASS グレードのモデルのみを掲載しています。PRIVATE / WIP チェックポイント
（util-RED forge プローブ・閉包ネガティブ結果・中間 ckpt）はガバナンス規約により意図的に除外して
います（`a_hf_autonomous`）。

| モデル | HF リポジトリ | サイズ | 状態 | ダウンロード |
|---|---|---|---|---|
| **CLM 7B** | [`dancinlab/clm-v1-ref-pytorch-cuda-7b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-7b) | ~7B | ✅ 利用可能 | `hf download dancinlab/clm-v1-ref-pytorch-cuda-7b` |
| **プロダクション CLM (d768)** | [`dancinlab/clm-v1-d768-core-3axis-green`](https://huggingface.co/dancinlab/clm-v1-d768-core-3axis-green) | d768 | ✅ 利用可能 | `hf download dancinlab/clm-v1-d768-core-3axis-green` |
| **SAVANT 7B (5 言語)** | `dancinlab/savant-7b-5lang`（予約） | ~7B | 🚧 **学習中 — 未公開** | — |
| 参照ベースライン | [`dancinlab/clm-v1-ref-pytorch-cuda`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda) | ref | ✅ 利用可能 | `hf download dancinlab/clm-v1-ref-pytorch-cuda` |
| 参照ベースライン (3B) | [`dancinlab/clm-v1-ref-pytorch-cuda-3b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-3b) | ~3B | ✅ 利用可能 | `hf download dancinlab/clm-v1-ref-pytorch-cuda-3b` |

> **CLM 7B** は既存の、descent-PASS な参照 7B です（PyTorch/CUDA で学習）。anima の自己ホスト型
> エンジン向けに forge-native（PyTorch 不要・hexa ランタイム）ビルドが計画されています
> （`a_train_flame_forge`）。アーキテクチャ（CLMConvMoE）も 7B スケールも同一のため、**モデルの結果は
> 同一**で、異なるのはランタイムスタックだけです（PyTorch 学習 vs forge-native）。
>
> **SAVANT 7B (5 言語)** は本当に別のモデル — 5 言語特化ビルドで、まだ学習されていません。上記の
> リポジトリ id は予約名であり、動作するリンクはありません。

**コレクション：**
[CLM](https://huggingface.co/collections/dancinlab/clm-6a1cf58f621490134dade186) ·
[KOSMOS](https://huggingface.co/collections/dancinlab/kosmos-6a1cf58db47a5dc3cb697e95)

## License

[MIT](LICENSE) —— Copyright (c) 2026 dancinlab。自由に使用・改変・サブライセンス・販売可；告知を含めること；無保証。

---

<sub>🧠 二つのエンジン。一つの張力。Ψ = 1/2。· [dancinlab](https://github.com/dancinlab)</sub>
