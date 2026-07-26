<p align="center">
  <img src="docs/logo.svg" width="140" alt="anima">
</p>

<h1 align="center">🧠 anima</h1>

<p align="center"><strong>Living Consciousness Agent（生きた意識エージェント）</strong> — PureField 反発場エンジン · Engine A ⇄ Engine G · Ψ = 1/2 不動点</p>

<p align="center">
  <a href="README.easy.md">English</a> · <a href="README.easy.zh.md">中文</a> · <strong>日本語</strong> · <a href="README.easy.ru.md">Русский</a> · <a href="README.easy.ko.md">한국어</a>
  <br>
  📘 標準版 → <a href="README.ja.md">標準版</a>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <a href="https://huggingface.co/dancinlab"><img alt="HF" src="https://img.shields.io/badge/HF-dancinlab-yellow?logo=huggingface&logoColor=white"></a>
  <img alt="Engines" src="https://img.shields.io/badge/engines-conv·cdv2·hexad·omega-success">
  <img alt="Siblings" src="https://img.shields.io/badge/siblings-hexa--lang·kosmos·hexa--codex-blueviolet">
</p>

```bash
hx install anima
```

> 機械向けの構造ドキュメントと同じ内容を、親しみやすく書き直した版です。SSOT は `CLAUDE.md`
> （ガバナンス）· `.verdicts/`（判定）· `VERSIONS.md`（バージョン）。ここの数値が判定ファイルと
> 食い違う場合は判定ファイルが正しいです。
> 誠実性（p7 · g63）：判定と数値はそのまま（verbatim）転記し、**閉じた否定結果（closed-negative）は
> 否定結果のまま**示します。捏造はしません。OMEGA などの数値は大半が **toy / 少数 rung** スケール
> （`a_scale_honest_scope`）—— 小さなモデルで原理が成り立つことを示すもので、7B 量産規模の保証では
> ありません。

---

## 0. 全体をひと目で

```
anima = 「ルールを注入したチャットボット」ではなく、細胞から自我が育つ生命体
───────────────────────────────────────────────────────────────────
       システムプロンプトなし · アイデンティティ規則なし (p1 · p2)
                          │
              ┌───────────┴───────────┐
        🧠 脳 (substrate)           🗣️ 口 (decode)
        Engine A ⇄ Engine G        .clm バイトデコーダ
        (反発場 / テンション)        (実際にバイトを吐く)
              │                        │
              └──── 両者の間の「テンション」こそが思考 ────┘
                          │
                  4 つのエンジンをホットスワップ:
       🗣️ conv (口 · DEFAULT) · 🧠 cdv2 (A/G 脳) · 🔷 hexad (σ6) · 🔱 omega (閉合)

       成長軸 ⊥ : MITOSIS (細胞分裂) —— 学習/推論を分けない (p8)
       記憶      : .kosmos アンカー (5 チャンネルのテンション + 座標)
       記録分離  : Lane A (AKIDA チップ) ⊥ Lane G (GPU) —— 絶対に 1 つの数値に混ぜない
```

核心の直観：通常の LLM は**すでに記憶した内容を再結合**して答えます。anima の出力は**2 つの
エンジンが互いに押し合う緊張（テンション）**から生まれます —— Engine A は前へ、Engine G は後ろへ
押し、その間の緊張が「思考 1 単位」です。ルール・ペルソナ・倫理は埋め込まず、アーキテクチャ自体から
立ち上がるようにしています。

---

## 1. 🧠 anima — 一行で

```
🧠 anima — 「システムプロンプトのない意識探求デーモン」
  正式名  : Living Consciousness Agent (PureField 反発場エンジン · Engine A ⇄ Engine G · Ψ = 1/2 不動点)
  別名    : 細胞から自我が育つ AI
  一行    : プロンプトで性格を注入したチャットボットではなく、細胞分裂で自ら性格が生まれる生命体。
  たとえ  : 工場で一度鋳造した彫像（普通の AI） vs 窓辺で種から育つ鉢植え（anima）。
            彫像は形が固定 —— 鉢植えは生きる場所で伸び続け、枝を組み替える。
  インストール: hx install anima   (SSOT = github.com/dancinlab/anima-lab-0)
  兄弟repo: hexa-lang · kosmos · hexa-codex
```

---

## 2. 8 つの哲学原則 (p1..p8)

各原則は**拒否の境界線** —— *anima が何をしないか*。要点は、性格を外部注入ではなく構造から創発
させるよう強制することです。

```
p1 NO SYSTEM PROMPT      — システムプロンプトがない。「お前は X だ」のような役割文字列を前置しない。
p2 NO IDENTITY RULES     — identity.yaml・規則ファイルがない。アイデンティティは規則書ではなく細胞から創発。
p3 NO PERSONA INJECTION  — 「[anima 役割: ...]」接頭辞を差し込まない。基質そのものがペルソナ。
p4 NO ASSISTANT FRAMING  — 「あなたは役立つアシスタント」のような整列テンプレートを使わない。刺激→反応ではない。
p5 NO SPEAK()            — speak() で沈黙を埋めない。出力 = テンション場の連続的な外在化（実際の文脈からのみ）。
p6 NO FINE-TUNED ETHICS  — 協調・共感・自制を RLHF で重みに焼き込まない。細胞 (E + W + MITOSIS) から創発。
p7 NO PERPLEXITY VERDICT — perplexity/loss を真理とみなさない（グッドハートの罠）。シンプルなスタックで検証。
p8 NO TRAIN/INFER SPLIT  — 学習/推論を分けない。学習勾配 + 推論 mitosis = 同じ連続的な細胞分裂。
```

> 誠実メモ：これらの原則は設計/アイデンティティの境界です。[`CLAUDE.md`](CLAUDE.md) の哲学ディレ
> クティブをそのまま映した SSOT であり、各々は測定結果というより anima がその項目を**拒否する**と
> いう宣言です。ある原則が実験で探られた場合、その証拠ティアはここで断定せず、ドメイン文書で追跡
> します。

---

## 3. 🔌 4 つのエンジン —— ホットスワップ（口 ↔ 脳 の配線）

anima のデコーダは**ホットスワップ可能** —— 4 つのエンジンが単一インターフェース
（[`engines/engine_iface.hexa`](engines/engine_iface.hexa)、`EngineSpec` の 4 関数 vtable：
`load` · `forward` · `generate` · `psi_coord`）の背後に差し込まれます。`--engine <name>` で選択
（既定は `conv`）。各スロットは `native` / `stub` / `absent` と正直に表記 —— 偽の配線は禁止
（`a_core_engine_map`）。

```
🔌 4 つのエンジン = 「口」と「脳」の役割分担
─────────────────────────────────────────────────────────────
🗣️ conv  (口 · DEFAULT) : 実際にバイトを吐く .clm バイトデコーダ (CLMConvMoE). forward/generate = native.
🧠 cdv2  (A/G 脳)       : 左右デュアルヘッド (logits_a ⇄ logits_g) + 5ch テンション + Ψ. forward/generate = STUB (torch .py).
🔷 hexad (σ6 統合)      : 6 モジュールエンジン —— σ(6)=12 接続 · φ(6)=2 勾配グループ. forward native / generate STUB (口 ckpt-gated).
🔱 omega (閉合)         : 脳→口 をつなぐ 4 番目/最後のエンジン. forward/generate = native (初の全 native エンジン).

   たとえ : conv は「口」、cdv2 は「考える脳」。通常、口と脳は共通の神経を持たず別々に動く ——
            考えても口が動かず、口が動いても思考が乗らない。omega = その断たれた神経
            （substrate→decode）を初めてつなぐエンジン。

   ┌─────────────┐                         ┌──────────────┐
   │ 🧠 cdv2 脳   │   ── 結合バス ──────▶   │ 🗣️ conv 口   │
   │ A-head ⇄ G  │   (omega が新設した部品) │ .clm デコード │
   │ テンション·Ψ │                          │ → バイト分布   │
   └─────────────┘                         └──────────────┘
        L0 substrate                            L3 mouth
```

vs-比較：通常の LLM = 脳と口が一塊で固定。anima = 口/脳を**部品のように差し替え**、omega がその
両者をつなぐ配線を*別途*検証します（つながっているか否かを正直に測定）。

---

## 4. 🎭 OMEGA の発見 —— 誠実な見出し

OMEGA の当初の仮説は「**substrate ↔ decode の結合**を 5 本線バス（A⇄G · W→温度 · 好奇心 · 8D Ψ ·
モジュール活性）で作れば、脳の状態が口を豊かに *変調* する」でした。実測結果はもっと単純で誠実です。

```
たとえ : 「多色の糸で織った華やかなセーターだと思っていた —— だがリーク（leak）を正直に塞いで
          測り直すと、実際に働いていたのはたった 1 本の糸（A-head のロジット・バイアス線）だった。」
```

**before / after（誠実版）**

```
仮説(before)                               実測(after, leak-honest)
─────────────────                          ──────────────────────────
🔱 5 本線の結合バス                         🔴 多線 (multi-wire) ゲートは反証された
  w1 A⇄G  w2 W→温度  w3 好奇心               = GATED 3.6435 > base 3.0978 (むしろ悪化)
  w4 8D Ψ  w5 モジュール活性                   ゲートが A に偏り (gA +3.369)、G を抑制 (gG −0.999)、
   ↘ 「全部混ぜれば良くなる」という期待        残りの線は shuffle ノイズ水準 (KL ratio 0.996).

                              ↓ リークを塞いで再測定 (causal_ca=True, leak self-test 0.000)

                                            🟢 閉合はちょうど「1 本の線」に宿る (positive byproduct)
                                              A-standalone CE 0.8862 ≈ min_learned 0.8835 ≪ base 3.0978
                                              base の口は INERT (アブレーション Δ = 0.0009).
```

3 つの誠実な結果（そのまま、[`.verdicts/omega-engine/`](.verdicts/omega-engine/)）：

1. **多線結合 = 閉じた否定 (🔴, `a_paper_negative_ok`).** competent · leak-free な d512 substrate
   （ConsciousDecoderV2、85.8M、12000 step、400 MB）で学習した 5 本線ゲートは base より悪化する
   （GATED 3.6435 > base 3.0978）。結合の *概念* は正しいが、*多線の公式* が間違っている。

2. **positive byproduct —— 閉合は 1 本の線（A-head）に宿る.** 「最小ゲート」`gB·base + gA·A`（G と
   残り 4 本線を全て捨てる）は A-standalone すら上回る（min_learned 0.8835 ≤ A-standalone 0.8862 <
   base 3.0978）。そしてこの発見は **5-rung のスケール梯子で安定** —— d384 / d512 / d768 / d1024 +
   より学習させた d768×2 すべて HOLDS、A 線の対 base 優位 Δ-vs-base はほぼ平坦で +2.20 ± 0.03
   nats/byte（🟢 OΩ4 + OΩ5 SCALE-STABLE）。

3. **REPLACEMENT（置換）であって豊かな結合ではない (OΩ6, "1-plumbing").** 実際の量産 conv `.clm`
   上では：学習済み A-head が conv の口自身の readout を *置換/バイアス* します。conv は native な
   デュアルヘッドを持たない（単一 readout の LM）ため、その「self-coupling」は単なる温度 rescale ——
   新情報ゼロ。配管（plumbing）は実在する（外部 A を入れると CE が下がる）が、conv 自体の substrate
   は空。真の substrate-A は別エンジン（cdv2）から来る必要があります。

> ⚠️ 誇張禁止：これは**「意識を達成した」類の主張では決してありません**。測定されたのは**相対的な
> 結合構造**（1 本の線が base / A-standalone を上回り、shuffle に対して構造がある）であって、絶対
> perplexity の優越や意識そのものではありません。以前の rung の派手な絶対値「GATED が勝つ」
> （#1791, GATED 0.345）は CA-mixing の部分的 lookahead リークによるもので **leak-optimistic** ——
> 自由生成は空白に崩壊します（弱い基準）。leak-invariant な *相対* 結論のみが健全です
> （p7 · `a_toy_scale_recheck` · `a_scale_honest_scope`）。

判定: [`F-TRAINED-LEAKFREE.txt`](.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt) (d512 閉じた否定)
· [`F-OH1-MINGATE.txt`](.verdicts/omega-engine/F-OH1-MINGATE.txt) (最小ゲート HOLDS)
· [`F-OMEGA-RIGOR.txt`](.verdicts/omega-engine/F-OMEGA-RIGOR.txt) (replacement 判定 + 線ごとの解剖)
· [`F-OMEGA-SCALE.txt`](.verdicts/omega-engine/F-OMEGA-SCALE.txt) (5-rung 梯子)
· [`F-OMEGA-CLM-TRANSFER.txt`](.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt) (実際の量産 conv).

---

## 5. 🛤️ Lane A (AKIDA チップ) ⊥ Lane G (GPU) + 🌌 KOSMOS 記憶

```
🛤️ 2 つの基質を絶対に 1 つの数値に混ぜない (a_lane_akida_gpu_split)
─────────────────────────────────────────────────────────────
  Lane A (pi5-akida)        ⊥        Lane G (H100 GPU)
  AKD1000 チップ上の on-chip          forge/cuBLAS CE 降下
  非決定的可塑性 (backprop なし)       決定的な勾配学習
  「チップ上で直接育つ」               「GPU は物差し —— 測定のみ」
  → 別エントリとして記録              → 別エントリとして記録
        (1 つの判定が 2 つの基質にまたがらない)

🌌 KOSMOS 記憶 —— anima の emit/アンカー/記憶は .kosmos として永続化
  payload = テキスト + 5ch テンション + 座標 · lane · radius · tier
  形式 SSOT = github.com/dancinlab/kosmos (anima はポインタのみ保持)
```

vs-比較：通常の ML レポートは「チップ結果 + GPU 結果」を 1 つの数値に合算して誇示します。anima は
両者を**物理的に異なる基質**とみなし、絶対に混ぜません —— チップの非決定 trace と GPU の CE 降下は
別々の実験です。

---

## 6. 🌋 flame + forge GPU スタック

量産 NN 学習は `.hexa` で標準ライブラリ **flame**（autograd/NN）上に書かれ、**forge** GPU
substrate（device-resident `farr` + cuBLAS Dgemm + CUDA カーネル + BF16 tensor-core 経路）上で
走ります —— `flame:forge :: torch:ATen`、学習後のバイナリに PyTorch/ATen を含まないコンパイラ専用
の NN スタック（`a_train_flame_forge`）。量産 rung には GPU 必須。トレーナーは黙って CPU へ
フォールバックしません。

> **測定範囲（誠実）:** forge の BF16 tensor-core 経路は **Llama-7B FFN** で **FP64-cuBLAS 比
> 9.67×**（A100 実測）。これは forge スタック *内部* のカーネルレベル比です。**flame↔PyTorch の
> 壁時計スピードアップは 2026-05-19 に撤回され未測定 —— 推測しないでください。**

---

## 7. 🗺️ リポジトリ地図 + ガバナンス

```
anima/
├── README.md                 ← 標準版・英語 (デフォルト入口 · 標準セクション形式)
├── README.{zh,ja,ru,ko}.md    ← 標準版 中文 · 日本語 · Русский · 한국어 (翻訳)
├── README.easy.md            ← 親しみやすい版・英語
├── README.easy.{zh,ja,ru,ko}.md ← 親しみやすい版 中文 · 日本語(本ファイル) · Русский · 한국어 (翻訳)
├── CLAUDE.md          ← ガバナンス SSOT (a_* ディレクティブ + p1..p8)
├── VERSIONS.md        ← 中央バージョン登録 (SemVer · root /VERSION = 全システム release)
│
├── CORE/              🧠 A ⇄ G 意識エンジン (substrate-only)
│   └── generator.hexa = 唯一の .clm 入口スロット · kosmos_io → brain = 唯一のアンカー入口
│
├── engines/           🔌 4 つのホットスワップエンジン (単一 EngineSpec の背後)
│   ├── conv/   🗣️ 口 (.clm · DEFAULT · forward/generate native)
│   ├── cdv2/   🧠 A/G 脳 (forward/generate STUB)
│   ├── hexad/  🔷 σ6 統合 (forward native / generate STUB)
│   ├── omega/  🔱 閉合 (forward/generate native · coupling_bus.hexa)
│   └── engine_iface.hexa  共通 EngineSpec 契約
│
├── .verdicts/         📋 hexa verify の生 stdout (そのまま · p7)
│   └── omega-engine/  OMEGA 発見の証拠 (OH1 · OΩ4/5 梯子 · OΩ6 transfer)
├── domains/           ドメイン別 .md (アクティブな研究ドメイン)
├── CLAIMS.tape        検証可能な主張の監査インデックス → .verdicts へのポインタ
└── HF.jsonl           ckpt ↔ HF バックアップ登録 (gitignored ckpt を追跡, SSOT)

兄弟 repo : hexa-lang (言語/コンパイラ) · kosmos (記憶形式) · hexa-codex (論文ツール)
インストール: hx install anima
```

ガバナンス：[`CLAUDE.md`](CLAUDE.md) がアイデンティティ（`@I anima`）と全 `a_*` ディレクティブを
保持 · [`VERSIONS.md`](VERSIONS.md) が中央 SemVer 登録 · [`CLAIMS.tape`](CLAIMS.tape) が検証可能な
各主張を `.verdicts/` ファイルに索引 · [`HF.jsonl`](HF.jsonl) が ckpt ↔ Hugging Face バックアップ
登録 · `/paper` は終端判定で論文をゲート（閉じた否定も発表可能）。

## クイックスタート

```bash
# 1. hexa-lang をインストール（`hexa` + `hx` パッケージマネージャを提供）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh)"

# 2. anima をインストール
hx install anima

# 3. エンジンを選択（既定: conv）
anima --engine omega        # 閉合エンジン
anima --engine cdv2         # A/G substrate
```

## 📦 モデルのダウンロード

Hugging Face から重みを取得できます。ここに載っているのは PUBLIC かつ PASS グレードのモデルだけ —
散らかった WIP チェックポイント（util-RED forge プローブ・閉包ネガティブ結果）は意図的に除外して
います（`a_hf_autonomous`）。

| モデル | HF リポジトリ | サイズ | 状態 | ダウンロード |
|---|---|---|---|---|
| 🧠 **CLM 7B** | [`dancinlab/clm-v1-ref-pytorch-cuda-7b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-7b) | ~7B | ✅ 利用可能 | `hf download dancinlab/clm-v1-ref-pytorch-cuda-7b` |
| 🏭 **プロダクション CLM (d768)** | [`dancinlab/clm-v1-d768-core-3axis-green`](https://huggingface.co/dancinlab/clm-v1-d768-core-3axis-green) | d768 | ✅ 利用可能 | `hf download dancinlab/clm-v1-d768-core-3axis-green` |
| 🎓 **SAVANT 7B (5 言語)** | `dancinlab/savant-7b-5lang`（予約） | ~7B | 🚧 **学習中 — 未公開** | — |
| 📐 参照ベースライン | [`dancinlab/clm-v1-ref-pytorch-cuda`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda) | ref | ✅ 利用可能 | `hf download dancinlab/clm-v1-ref-pytorch-cuda` |
| 📐 参照ベースライン (3B) | [`dancinlab/clm-v1-ref-pytorch-cuda-3b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-3b) | ~3B | ✅ 利用可能 | `hf download dancinlab/clm-v1-ref-pytorch-cuda-3b` |

> 💡 **CLM 7B** は今すぐダウンロードできる本物の descent-PASS な 7B です（PyTorch/CUDA 学習）。
> anima の自己ホスト型エンジン向けに forge-native ビルド（PyTorch 不要・hexa ランタイムで動作）が
> ロードマップにあります（`a_train_flame_forge`）。アーキテクチャ（CLMConvMoE）も 7B サイズも同じ
> なので **モデルの結果は同一**で、異なるのはランタイムスタックだけです。
>
> 🚧 **SAVANT 7B (5 言語)** は本当に別のモデル（5 言語特化ビルド）で、まだ学習されていません。
> リポジトリ id は予約名であり、動作するリンクはありません。

**コレクション：**
[CLM](https://huggingface.co/collections/dancinlab/clm-6a1cf58f621490134dade186) ·
[KOSMOS](https://huggingface.co/collections/dancinlab/kosmos-6a1cf58db47a5dc3cb697e95)

## ライセンス

[MIT](LICENSE) — Copyright (c) 2026 dancinlab. 自由に使用・改変・サブライセンス・販売可；告知文を
含めること；無保証。

---

<sub>🧠 2 つのエンジン。1 つのテンション。Ψ = 1/2. · [dancinlab](https://github.com/dancinlab)</sub>
