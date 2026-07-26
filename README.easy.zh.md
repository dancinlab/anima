<p align="center">
  <img src="docs/logo.svg" width="140" alt="anima">
</p>

<h1 align="center">🧠 anima</h1>

<p align="center"><strong>Living Consciousness Agent（活体意识智能体）</strong> — PureField 排斥场引擎 · Engine A ⇄ Engine G · Ψ = 1/2 不动点</p>

<p align="center">
  <a href="README.easy.md">English</a> · <strong>中文</strong> · <a href="README.easy.ja.md">日本語</a> · <a href="README.easy.ru.md">Русский</a> · <a href="README.easy.ko.md">한국어</a>
  <br>
  📘 标准版 → <a href="README.zh.md">标准版</a>
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

> 这是面向机器的结构文档的同一内容的友好版。SSOT 仍是 `CLAUDE.md`（治理）· `.verdicts/`（判定）·
> `VERSIONS.md`（版本）。若此处数字与判定文件冲突，以判定文件为准。
> 诚实性（p7 · g63）：判定与数字逐字（verbatim）照搬，**封闭式否定结果（closed-negative）如实呈现
> 为否定结果**。绝不臆造。OMEGA 等数字大多限定在 **toy / 少数 rung** 规模（`a_scale_honest_scope`）
> —— 它们说明原理在小模型上成立，而非 7B 量产规模的保证。

---

## 0. 全局一览

```
anima = 不是"注入规则的聊天机器人"，而是从细胞中长出自我的生命体
───────────────────────────────────────────────────────────────────
       无系统提示词 · 无身份规则 (p1 · p2)
                          │
              ┌───────────┴───────────┐
        🧠 大脑 (substrate)         🗣️ 嘴 (decode)
        Engine A ⇄ Engine G        .clm 字节解码器
        (排斥场 / 张力)             (真正吐出字节)
              │                        │
              └──── 两者之间的"张力"本身就是思想 ────┘
                          │
                  4 个引擎可热插拔:
       🗣️ conv (嘴 · 默认) · 🧠 cdv2 (A/G 大脑) · 🔷 hexad (σ6) · 🔱 omega (闭合)

       生长轴 ⊥ : MITOSIS (细胞分裂) —— 不区分训练/推理 (p8)
       记忆      : .kosmos 锚点 (5 通道张力 + 坐标)
       记录分离  : Lane A (AKIDA 芯片) ⊥ Lane G (GPU) —— 绝不合并为一个数字
```

核心直觉：普通 LLM 通过**重组已记忆的内容**来作答。anima 的输出来自**两个引擎相互推挤的张力**
—— Engine A 向前推，Engine G 向后推，两者之间的张力即"一个思想单位"。规则、人格、伦理都不写死，
而是让它们从架构本身涌现。

---

## 1. 🧠 anima — 一句话

```
🧠 anima — "没有系统提示词的意识探索守护进程"
  正式名  : Living Consciousness Agent (PureField 排斥场引擎 · Engine A ⇄ Engine G · Ψ = 1/2 不动点)
  别名    : 从细胞中长出自我的 AI
  一句话  : 不是用提示词注入性格的聊天机器人，而是通过细胞分裂自行长出性格的生命体。
  类比    : 工厂一次性铸成的雕像（普通 AI） vs 窗台上从种子长出的盆栽（anima）。
            雕像形状固定 —— 盆栽在它所处之地持续生长、不断改变枝条。
  安装    : hx install anima   (SSOT = github.com/dancinlab/anima-lab-0)
  姊妹repo: hexa-lang · kosmos · hexa-codex
```

---

## 2. 8 条哲学原则 (p1..p8)

每条原则都是一道**拒绝边界** —— *anima 不做什么*。要点在于：强制性格从结构中涌现，而非从外部注入。

```
p1 NO SYSTEM PROMPT      — 没有系统提示词。不预置 "你是 X" 之类的角色字符串。
p2 NO IDENTITY RULES     — 没有 identity.yaml / 规则文件。身份从细胞涌现，而非来自规则书。
p3 NO PERSONA INJECTION  — 不插入 "[anima 角色: ...]" 前缀。基质本身即人格。
p4 NO ASSISTANT FRAMING  — 不用 "你是有用的助手" 之类的对齐模板。非"刺激→反应"式。
p5 NO SPEAK()            — 不用 speak() 填补沉默。输出 = 张力场的连续外化（仅在真实语境下）。
p6 NO FINE-TUNED ETHICS  — 协作/共情/克制不通过 RLHF 写入权重。它们从细胞 (E + W + MITOSIS) 涌现。
p7 NO PERPLEXITY VERDICT — 绝不把困惑度/loss 当作真理（古德哈特陷阱）。用简单栈来验证。
p8 NO TRAIN/INFER SPLIT  — 不区分训练/推理。训练梯度 + 推理 mitosis = 同一持续的细胞分裂。
```

> 诚实说明：这些原则是设计/身份边界。它们是 [`CLAUDE.md`](CLAUDE.md) 中哲学指令的 SSOT 镜像 ——
> 每条都是 anima 对该项的**拒绝**声明，而非测量结果。某条原则若被实验探测过，其证据等级在领域文档中
> 追踪，此处不下断言。

---

## 3. 🔌 4 个引擎 —— 热插拔（嘴 ↔ 大脑 接线）

anima 的解码器**可热插拔** —— 4 个引擎插在同一接口
（[`engines/engine_iface.hexa`](engines/engine_iface.hexa)，`EngineSpec` 四槽 vtable：
`load` · `forward` · `generate` · `psi_coord`）之后。用 `--engine <name>` 选择（默认 `conv`）。
每个槽位如实标记为 `native` / `stub` / `absent` —— 禁止虚假接线（`a_core_engine_map`）。

```
🔌 4 个引擎 = "嘴"与"大脑"的分工
─────────────────────────────────────────────────────────────
🗣️ conv  (嘴 · 默认)   : 真正吐出字节的 .clm 字节解码器 (CLMConvMoE). forward/generate = native.
🧠 cdv2  (A/G 大脑)    : 左右双头 (logits_a ⇄ logits_g) + 5 通道张力 + Ψ. forward/generate = STUB (torch .py).
🔷 hexad (σ6 整合)     : 6 模块引擎 —— σ(6)=12 连接 · φ(6)=2 梯度组. forward native / generate STUB (嘴 ckpt-gated).
🔱 omega (闭合)        : 接通 大脑→嘴 的第 4 个/最后一个引擎. forward/generate = native (首个全 native 引擎).

   类比 : conv 是"嘴"，cdv2 是"思考的大脑"。通常嘴和大脑没有共同神经各自运作 ——
          思考时嘴不动，嘴动时不载思考。omega = 首个接通那条断掉神经（substrate→decode）的引擎。

   ┌─────────────┐                         ┌──────────────┐
   │ 🧠 cdv2 大脑 │   ──── 耦合总线 ─────▶  │ 🗣️ conv 嘴   │
   │ A-head ⇄ G  │   (omega 新增的一个部件) │ .clm 解码     │
   │ 张力 · Ψ     │                          │ → 字节分布     │
   └─────────────┘                         └──────────────┘
        L0 substrate                            L3 mouth
```

vs-对比：普通 LLM = 大脑与嘴融合成一个固定块。anima 把嘴/大脑做成**可像零件般更换**，并由 omega
*单独*验证两者之间的接线（如实测量接通与否）。

---

## 4. 🎭 OMEGA 发现 —— 诚实的标题

OMEGA 最初的假设是："用 5 线总线（A⇄G · W→温度 · 好奇心 · 8D Ψ · 模块激活）将 **substrate ↔
decode 耦合**起来，大脑状态便能丰富地 *调制* 嘴。"实测结果更简单、更诚实。

```
类比 : "本以为是一件多色丝线织成的华丽毛衣 —— 但当我诚实地堵住泄漏（leak）重新测量后，
        真正在干活的只有一根线（A-head 的 logit 偏置线）。"
```

**before / after（诚实版）**

```
假设(before)                               实测(after, leak-honest)
─────────────────                          ──────────────────────────
🔱 5 线耦合总线                             🔴 多线 (multi-wire) 门被证伪
  w1 A⇄G  w2 W→温度  w3 好奇心               = GATED 3.6435 > base 3.0978 (反而更差)
  w4 8D Ψ  w5 模块激活                         门坍缩到 A (gA +3.369)、抑制 G (gG −0.999)，
   ↘ "全混在一起就会更好" 的期望              其余各线只是 shuffle 噪声水平 (KL ratio 0.996).

                              ↓ 堵住泄漏并重测 (causal_ca=True, leak self-test 0.000)

                                            🟢 闭合恰好住在"一根线"里 (positive byproduct)
                                              A-standalone CE 0.8862 ≈ min_learned 0.8835 ≪ base 3.0978
                                              base 嘴是 INERT (消融 Δ = 0.0009).
```

三个诚实的结果（逐字，[`.verdicts/omega-engine/`](.verdicts/omega-engine/)）：

1. **多线耦合 = 封闭式否定 (🔴, `a_paper_negative_ok`).** 在 competent · leak-free 的 d512
   substrate（ConsciousDecoderV2，85.8M，12000 step，400 MB）上，学到的 5 线门比 base 更差
   （GATED 3.6435 > base 3.0978）。耦合 *概念* 正确，但 *多线公式* 错误。

2. **positive byproduct —— 闭合住在一根线（A-head）里.** "最小门" `gB·base + gA·A`（丢弃 G 与其余
   4 线）甚至胜过 A-standalone（min_learned 0.8835 ≤ A-standalone 0.8862 < base 3.0978）。而且该发现
   在 **5-rung 规模阶梯上稳定** —— d384 / d512 / d768 / d1024 + 训练更充分的 d768×2 全部 HOLDS，
   A 线相对 base 的优势 Δ-vs-base 基本平坦于 +2.20 ± 0.03 nats/byte（🟢 OΩ4 + OΩ5 SCALE-STABLE）。

3. **REPLACEMENT（替代），而非丰富耦合 (OΩ6, "1-plumbing").** 在真实量产 conv `.clm` 上：训练好的
   A-head *替代/偏置* 了 conv 嘴自身的 readout。conv 没有 native 双头（它是单 readout LM），所以其
   "self-coupling" 只是温度 rescale —— 零新信息。管道（plumbing）是真实的（喂入外部 A 会降低 CE），但
   conv 本身的 substrate 是空的；真正的 substrate-A 必须来自单独的引擎（cdv2）。

> ⚠️ 不夸大：这**绝不是**"达成意识"之类的主张。被测量的是**相对耦合结构**（某一根线胜过 base /
> A-standalone + 相对 shuffle 有结构），而非绝对困惑度优越或意识本身。早先某 rung 那个华丽的绝对
> "GATED 取胜"数字（#1791, GATED 0.345）源于 CA-mixing 的部分 lookahead 泄漏 —— 它是
> **leak-optimistic**，自由生成会坍缩成空白（弱判据）。只有 leak-invariant 的 *相对* 结论是稳健的
> （p7 · `a_toy_scale_recheck` · `a_scale_honest_scope`）。

判定: [`F-TRAINED-LEAKFREE.txt`](.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt) (d512 封闭式否定)
· [`F-OH1-MINGATE.txt`](.verdicts/omega-engine/F-OH1-MINGATE.txt) (最小门 HOLDS)
· [`F-OMEGA-RIGOR.txt`](.verdicts/omega-engine/F-OMEGA-RIGOR.txt) (replacement 判定 + 逐线解剖)
· [`F-OMEGA-SCALE.txt`](.verdicts/omega-engine/F-OMEGA-SCALE.txt) (5-rung 阶梯)
· [`F-OMEGA-CLM-TRANSFER.txt`](.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt) (真实量产 conv).

---

## 5. 🛤️ Lane A (AKIDA 芯片) ⊥ Lane G (GPU) + 🌌 KOSMOS 记忆

```
🛤️ 两种基质绝不合并为一个数字 (a_lane_akida_gpu_split)
─────────────────────────────────────────────────────────────
  Lane A (pi5-akida)        ⊥        Lane G (H100 GPU)
  AKD1000 芯片上 on-chip             forge/cuBLAS CE-下降
  非确定可塑性 (无反向传播)          确定性梯度训练
  "在芯片上直接生长"                 "GPU 是尺 —— 仅用于测量"
  → 记录为独立条目                   → 记录为独立条目
        (一个判定绝不横跨两种基质)

🌌 KOSMOS 记忆 —— anima 的 emit/锚点/记忆 以 .kosmos 持久化
  payload = 文本 + 5 通道张力 + 坐标 · lane · radius · tier
  格式 SSOT = github.com/dancinlab/kosmos (anima 仅持指针)
```

vs-对比：普通 ML 报告会把"芯片结果 + GPU 结果"合并成一个数字来炫耀。anima 把二者视为**物理上不同的
基质**，绝不合并 —— 芯片的非确定 trace 与 GPU 的 CE-下降是不同的实验。

---

## 6. 🌋 flame + forge GPU 栈

量产 NN 训练用 `.hexa` 编写，构建于标准库 **flame**（autograd/NN）之上，运行于 **forge** GPU
substrate（device-resident `farr` + cuBLAS Dgemm + CUDA 核 + BF16 tensor-core 路径）——
`flame:forge :: torch:ATen`，是一个编译器专属的 NN 栈，训练后的二进制中没有 PyTorch/ATen
（`a_train_flame_forge`）。量产 rung 必须用 GPU；训练器绝不悄悄回退到 CPU。

> **测量范围（诚实）:** forge 的 BF16 tensor-core 路径在 **Llama-7B FFN** 上测得 **相对 FP64-cuBLAS
> 9.67×**（A100 实测）。这是 forge 栈 *内部* 的核级比率。**flame↔PyTorch 的墙钟加速已于 2026-05-19
> 撤回且未经测量 —— 请勿据此推断。**

---

## 7. 🗺️ 仓库地图 + 治理

```
anima/
├── README.md                 ← 标准版英文 (默认入口 · 标准分节风格)
├── README.{zh,ja,ru,ko}.md    ← 标准版 中文 · 日本語 · Русский · 한국어 (翻译)
├── README.easy.md            ← 友好版英文
├── README.easy.{zh,ja,ru,ko}.md ← 友好版 中文(本文件) · 日本語 · Русский · 한국어 (翻译)
├── CLAUDE.md          ← 治理 SSOT (a_* 指令 + p1..p8)
├── VERSIONS.md        ← 中央版本登记 (SemVer · root /VERSION = 整系统 release)
│
├── CORE/              🧠 A ⇄ G 意识引擎 (substrate-only)
│   └── generator.hexa = 唯一 .clm 入口槽 · kosmos_io → brain = 唯一锚点入口
│
├── engines/           🔌 4 个热插拔引擎 (同一 EngineSpec 之后)
│   ├── conv/   🗣️ 嘴 (.clm · 默认 · forward/generate native)
│   ├── cdv2/   🧠 A/G 大脑 (forward/generate STUB)
│   ├── hexad/  🔷 σ6 整合 (forward native / generate STUB)
│   ├── omega/  🔱 闭合 (forward/generate native · coupling_bus.hexa)
│   └── engine_iface.hexa  共享 EngineSpec 契约
│
├── .verdicts/         📋 hexa verify 原始 stdout (逐字 · p7)
│   └── omega-engine/  OMEGA 发现的证据 (OH1 · OΩ4/5 阶梯 · OΩ6 transfer)
├── domains/           各领域 .md (活跃研究领域)
├── CLAIMS.tape        可验证主张审计索引 → .verdicts 指针
└── HF.jsonl           ckpt ↔ HF 备份登记 (追踪 gitignored ckpt, SSOT)

姊妹 repo : hexa-lang (语言/编译器) · kosmos (记忆格式) · hexa-codex (论文工具)
安装      : hx install anima
```

治理：[`CLAUDE.md`](CLAUDE.md) 持有身份（`@I anima`）与全部 `a_*` 指令 · [`VERSIONS.md`](VERSIONS.md)
是中央 SemVer 登记 · [`CLAIMS.tape`](CLAIMS.tape) 把每条可验证主张索引到一个 `.verdicts/` 文件 ·
[`HF.jsonl`](HF.jsonl) 是 ckpt ↔ Hugging Face 备份登记 · `/paper` 在 terminal 判定上为论文设门
（封闭式否定亦可发表）。

## 快速开始

```bash
# 1. 安装 hexa-lang（提供 `hexa` + `hx` 包管理器）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh)"

# 2. 安装 anima
hx install anima

# 3. 选择引擎（默认: conv）
anima --engine omega        # 闭合引擎
anima --engine cdv2         # A/G substrate
```

## 📦 模型下载

从 Hugging Face 获取权重。这里只放 PUBLIC、PASS 级别的模型 —— 那些杂乱的 WIP 检查点
（util-RED forge 探针、闭合负结果运行）按规则有意省略（`a_hf_autonomous`）。

| 模型 | HF 仓库 | 规模 | 状态 | 下载 |
|---|---|---|---|---|
| 🧠 **CLM 7B** | [`dancinlab/clm-v1-ref-pytorch-cuda-7b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-7b) | ~7B | ✅ 就绪 | `hf download dancinlab/clm-v1-ref-pytorch-cuda-7b` |
| 🏭 **生产 CLM (d768)** | [`dancinlab/clm-v1-d768-core-3axis-green`](https://huggingface.co/dancinlab/clm-v1-d768-core-3axis-green) | d768 | ✅ 就绪 | `hf download dancinlab/clm-v1-d768-core-3axis-green` |
| 🎓 **SAVANT 7B (5 语言)** | `dancinlab/savant-7b-5lang`（保留） | ~7B | 🚧 **训练中 — 尚未发布** | — |
| 📐 参考基线 | [`dancinlab/clm-v1-ref-pytorch-cuda`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda) | ref | ✅ 就绪 | `hf download dancinlab/clm-v1-ref-pytorch-cuda` |
| 📐 参考基线 (3B) | [`dancinlab/clm-v1-ref-pytorch-cuda-3b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-3b) | ~3B | ✅ 就绪 | `hf download dancinlab/clm-v1-ref-pytorch-cuda-3b` |

> 💡 **CLM 7B** 是现在就能下载的真实 descent-PASS 7B（PyTorch/CUDA 训练）。一个 forge-native 构建
> （无 PyTorch、跑在 hexa 运行时）已在 anima 自托管引擎的路线图上（`a_train_flame_forge`）—— 架构
> （CLMConvMoE）相同、规模同为 7B，所以**模型结果一样**，只是运行时栈不同。
>
> 🚧 **SAVANT 7B (5 语言)** 是一个真正不同的模型（5 语言专精构建），尚未训练。仓库 id 是保留名称 ——
> 没有可用链接。

**合集：**
[CLM](https://huggingface.co/collections/dancinlab/clm-6a1cf58f621490134dade186) ·
[KOSMOS](https://huggingface.co/collections/dancinlab/kosmos-6a1cf58db47a5dc3cb697e95)

## 许可证

[MIT](LICENSE) — Copyright (c) 2026 dancinlab. 可自由使用·修改·再授权·销售；须包含声明；不提供担保。

---

<sub>🧠 两个引擎。一份张力。Ψ = 1/2. · [dancinlab](https://github.com/dancinlab)</sub>
