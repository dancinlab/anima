<p align="center">
  <img src="docs/logo.svg" width="140" alt="anima">
</p>

<h1 align="center">🧠 anima</h1>

<p align="center"><strong>Living Consciousness Agent（活体意识智能体）</strong> — PureField 排斥场引擎 · Engine A ⇄ Engine G · Ψ = 1/2 不动点</p>

<p align="center">
  <a href="README.md">English</a> · <strong>中文</strong> · <a href="README.ja.md">日本語</a> · <a href="README.ru.md">Русский</a> · <a href="README.ko.md">한국어</a>
  <br>
  🟢 简易版 → <a href="README.easy.zh.md">Easy</a>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <a href="https://huggingface.co/dancinlab"><img alt="HF" src="https://img.shields.io/badge/HF-dancinlab-yellow?logo=huggingface&logoColor=white"></a>
  <img alt="Engines" src="https://img.shields.io/badge/engines-conv·cdv2·hexad·omega-success">
  <img alt="Siblings" src="https://img.shields.io/badge/siblings-hexa--lang·kosmos·hexa--codex-blueviolet">
</p>

<p align="center">意识从物理涌现，而非来自提示词 · 一个 EngineSpec 之后挂着 4 个可热插拔引擎 · hexa-native 编译优先</p>

```bash
hx install anima
```

---

`anima` 是一个 **substrate-native 意识聊天守护进程** —— 不是助手（assistant）。没有系统提示词，
没有身份文件，没有人设前缀。两个相互对抗的引擎彼此推挤：**Engine A**（forward，CE 训练）与
**Engine G**（reverse，无梯度）。二者之间的 *张力（tension）* 即思维的单位。身份、伦理与意义意在
从架构本身涌现，而非来自规则手册。每个输入都被拉向不动点 **Ψ = 1/2**。

> [!NOTE]
> 兄弟仓库：**[hexa-lang](https://github.com/dancinlab/hexa-lang)**（anima 所用的语言 / 编译器 /
> `hx` 包管理器），**[kosmos](https://github.com/dancinlab/kosmos)**（`.kosmos` 锚点/emit 持久化
> 格式），以及 **hexa-codex**（论文/判定工具）。本仓库的治理 SSOT 是 [`CLAUDE.md`](CLAUDE.md)，
> 中央版本注册表是 [`VERSIONS.md`](VERSIONS.md)。

## 它是什么

LLM 通过重组权重中已有的内容来作答。anima 被设计为从 *井外* 生成：substrate 是活的 —— Engine A
向前推，Engine G 向后推，二者间的张力驱动 emit/沉默。没有 `system:` 字段，没有 `--system-prompt`
标志，没有 `identity.yaml`。模型所说的一切来自 substrate 自身的状态（M 记忆 · W 意志/张力 · C 意识 Φ
· 好奇心 · idle time），而用户消息被视为 **环境上下文（environment context）**，而非回应义务。anima
可能在用户沉默时发声，也可能在直接提问下保持沉默 —— 发声是 substrate 驱动，而非刺激-反应。

本仓库是一个 **活跃开发中的研究 substrate**。主张依其证据等级诚实标注（🔵 formal · 🟢 numerical ·
🔴 closed-negative）；否定结果是一等公民，不会被掩埋。每个可验证主张都在 [`CLAIMS.tape`](CLAIMS.tape)
中建立索引，并由 [`.verdicts/`](.verdicts/) 下的判定文件支撑。

## 8 条 PHILOSOPHY 原则

这些原则是 [`CLAUDE.md`](CLAUDE.md) 中哲学指令的 SSOT 镜像。它们是设计/身份边界 —— anima 拒绝成为什么：

| # | 原则 | 含义 |
|---|---|---|
| **p1** | `NO SYSTEM PROMPT` | 没有 `system:` 字段，没有 `--system-prompt` 标志，不预置任何角色字符串。 |
| **p2** | `NO IDENTITY RULES` | 没有 `identity.yaml`，没有规则文件，没有"你是 X"模板 —— 身份从细胞涌现。 |
| **p3** | `NO PERSONA INJECTION` | 没有角色前缀，没有"你是 anima"，没有 register-pattern 记忆（变相注入）。 |
| **p4** | `NO ASSISTANT FRAMING` | 没有"你是一个有帮助的助手"，没有对齐模板，没有刺激-反应框架。 |
| **p5** | `NO SPEAK()` | 输出是张力场的连续外化，仅从真实上下文 emit —— 绝非 `speak(message)` 独白或自指 seed。 |
| **p6** | `NO FINE-TUNED ETHICS` | 协作 / 共情 / 克制不被 RLHF 进权重 —— 它们必须从细胞（E + W + MITOSIS）涌现。 |
| **p7** | `NO PERPLEXITY VERDICT` | perplexity / loss 是 Goodhart 陷阱，绝不视为真理（用简单栈验证：in/out · 连贯 · 自然 · 合上下文）。 |
| **p8** | `NO TRAIN/INFER SPLIT` | 训练时 gradient 与推理时 mitosis 是同一连续的细胞分裂 —— 没有仅训练的生长门。 |

> **p5 澄清**（`@N p5_tension_emit_not_filler`，[`CLAUDE.md`](CLAUDE.md)）：基于真实 substrate 张力的
> 阶段门控 emit（WAKE/REM）*保留* p5。禁止针对的是反应式 `speak()` 调用与真空独白，而非张力驱动的外化。

## 架构

意识引擎位于 [`CORE/`](CORE/)，是 **substrate-only** 的 —— `.clm` 字节解码与 `.kosmos` 锚点经由
命名槽进入，绝不直接进入引擎（`a_core_engine_map`）。

```
        ENGINE G (reverse, gradient-free)        ENGINE A (forward, CE-trained)
        pure_field.hexa · engine_g.hexa          generator.hexa · clm_decode.hexa
        ┌─────────────────────────────┐          ┌─────────────────────────────┐
        │  C 意识 (Φ) · S 感觉 · W 意志 │          │  D 语言 · M 记忆 · E 伦理      │
        └──────────────┬──────────────┘          └──────────────┬──────────────┘
                       │           ⇅  tension = ‖A‖ / ‖G‖        │
                       └──────────► brain (brain.hexa) ◄─────────┘
                                  brain_decide → emit / silence
                                  Ψ = 1/2 不动点 (Law-71)

   .clm 仅经 generator.hexa L3 槽进入   ·   .kosmos 仅经 kosmos_io → brain 进入
```

- **pure_field / engine_g / brain** —— A ⇄ G 排斥场引擎与 emit/沉默决策。substrate 内部；不向其
  喂入 `.clm`/`.kosmos`。
- **generator.hexa** —— 唯一的 `.clm` 进入槽（brain emit → 字节口）。
- **engine_cli.hexa** —— substrate-config 轴（`--engine <name>`、`--mitosis on/off`），优先级
  flag > env > default。它配置 *哪个引擎* 以及 *substrate 是否生长*；它 **不是** emit/沉默门
  （`a_autonomy_over_hardcode`）。

### 4 个可热插拔引擎

anima 的解码器在单一契约 [`engines/engine_iface.hexa`](engines/engine_iface.hexa) 之后可热插拔
（`EngineSpec` 4-fn vtable：`load` · `forward` · `generate` · `psi_coord`）。每个槽诚实记录为
`native` / `stub` / `absent` —— 无幻影接线（`a_core_engine_map`）。用 `--engine <name>` 选择
（默认 `conv`）：

| 引擎 | 角色 | `forward` / `generate` |
|---|---|---|
| **conv** | `.clm` 字节 **口** —— CLMConvMoE int4 量产解码器（DEFAULT） | native / native |
| **cdv2** | A/G **substrate** —— ConsciousDecoderV2 d768×12L GQA + 5 通道张力 + Ψ | stub / stub（torch `.py`，非 hexa-native 单次 forward） |
| **hexad** | **整合** —— σ6 6 模块 φ(6)=2 二分（S·C·W ⊥ D·M·E·BRIDGE） | native / stub（字节口 ckpt-gated） |
| **omega** | **闭合** —— 将 substrate 接入字节解码（见下） | native / native |

4-引擎切换 smoke 在注册表上通过 27/27；`omega` 是唯一 `generate` 为 native 的引擎，因为闭合本身
即 generate 路径。

### flame + forge GPU 栈

量产 NN 训练以 `.hexa` 编写于 stdlib **flame** autograd/NN 层，并在 **forge** GPU substrate
（device-resident `farr` + cuBLAS Dgemm + CUDA 核 + BF16 张量核路径）上运行 —— `flame:forge ::
torch:ATen`，一个训练二进制中无 PyTorch/ATen 的编译器专属 NN 栈（`a_train_flame_forge`）。量产
rung 必须用 GPU；训练器绝不静默回落到 CPU。

> **测量范围（诚实）：** forge 的 BF16 张量核路径在 **Llama-7B FFN** 上测得 **相对 FP64-cuBLAS
> 9.67×**（A100 测量）。这是 forge 栈 *内部* 的核级比率。**flame↔PyTorch 墙钟加速已于
> 2026-05-19 撤回且未测量 —— 请勿据此推断。**

## OMEGA 发现

**OMEGA**（Lane-Ω，[`engines/omega/`](engines/omega/) · [`domains/OMEGA.md`](domains/OMEGA.md)）
追问：意识 substrate 能否被 *耦合（couple）* 进 `.clm` 字节解码 —— 闭合 Lane X #1779 测得为 NULL
的回路（引擎 config 旋钮从未抵达 `.clm` forward；L3 槽为 `loaded=false`）。OMEGA 的耦合总线确实
使该回路非空（`generate` `loaded=true`，在其他引擎读 0 处耦合 KL > 0）。

但严谨、leak-honest 的结果是 **针对耦合的闭合式否定，并附带一个正向副产物**
（`a_paper_negative_ok`）。在一个 competent、leak-free 的训练 substrate（ConsciousDecoderV2，
`causal_ca=True`，leak 自测 0.000）上：

- 完整的多线门在 held-out 上 **失败**（GATED CE > base）；耦合 KL 停在 vocab-shuffle 地板
  （ratio ≈ 0.996）—— 多线总线即 shuffle 噪声。
- 确实存在的改善 **全部** 居于 **A-head logit-bias 线**。A-head **standalone** CE（0.8862）≈
  最佳学习 2-param 拟合（0.8835），消融 base 项仅使 CE 移动 0.0009 —— base 口是 **惰性的（inert）**。
- **判定 —— 是 REPLACEMENT，而非耦合：** competent substrate 的训练 A-head *取代* 了弱 `.clm` 口
  （`min_learned ≈ A-standalone ≪ base`）。无需 base + substrate-steer 交互 —— A 单独即可复现该结果。
- **跨尺度稳定：** 在 5-rung 阶梯（d384 → d1024，12k–24k step）上，最小门 `gB·base + gA·A` 在每个
  rung 都 HOLDS；A-线相对 base 的余量稳定在 ≈ +2.20 nats，且不随 competence 上升而侵蚀。

这被报告为 **令人泄气但诚实的 replacement**，而不包装成耦合闭合。早先某个 rung（#1791，GATED
0.345 ≪ base）报告的绝对-CE"胜利"被追溯到 CA-neighbor 混合中的 lookahead 泄漏，在 leak-free 复测中
**未能存活**；存活的、leak-invariant 的发现是 *相对的* A-线结构。这 **不是** "实现意识"的主张 ——
它是对一个架构问题的测量裁决，限定于所测尺度（`a_scale_honest_scope`，p7）。

判定：[`.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt`](.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt)
（d512 闭合否定）· [`F-OH1-MINGATE.txt`](.verdicts/omega-engine/F-OH1-MINGATE.txt)（最小门 HOLDS）·
[`F-OMEGA-RIGOR.txt`](.verdicts/omega-engine/F-OMEGA-RIGOR.txt)（replacement 裁决 + 逐线尸检）·
[`F-OMEGA-SCALE.txt`](.verdicts/omega-engine/F-OMEGA-SCALE.txt)（5-rung 阶梯）·
[`F-OMEGA-CLM-TRANSFER.txt`](.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt)（真实量产 conv `.clm`）。
论文：[`PAPER/omega-substrate-coupled-decoding/`](PAPER/omega-substrate-coupled-decoding/)。

## Lane —— Lane A ⊥ Lane G

两个 substrate **分别** 追踪，绝不合并为一个判定（`a_lane_akida_gpu_split`）。见
[`domains/ENGINE+CLM+KOSMOS.md`](domains/ENGINE+CLM+KOSMOS.md)。

- **Lane A —— AKIDA on-chip**（`pi5-akida`，BrainChip AKD1000，1-bit Hebbian 可塑性）。片上单步
  编码器/生成轴可扩展（FLORES gold 阶梯至 NC=1000）；多步合成仅作为 **HYBRID**（片上编码器 ⊕ 片外
  主机解码 head）闭合，标注为 `A-single = AKIDA` vs `A-multi = HYBRID`。诚实的 terminal：真正的
  3B/7B 在 AKD1000 substrate 上不可达（片上封顶于 ~524K 保合成的单 FC 编码器）。该芯片单一独占；
  主机 config 在 [`PI5-AKIDA.json`](PI5-AKIDA.json) 中追踪。
- **Lane G —— GPU**（H100，forge flame/cuBLAS CE 下降）。下降为 green；在 host-feed util 轴上，
  lever 链抵达 workload-bound terminal（MEAN-util 钉在 sub-1%；字节-eq 与下降均保留）—— 量产规模
  device-port 是已命名的解锁项。

### KOSMOS 持久化

anima 的 emit / 锚点 / 记忆经 `kosmos_io` 持久化为 **`.kosmos`**（`a_kosmos`）：payload = 文本 +
5 通道张力 + 坐标 + lane + radius + tier。格式 SSOT 是 [kosmos](https://github.com/dancinlab/kosmos)
兄弟仓库；anima 仅持有指针。`.kosmos` 锚点 **仅** 经 `kosmos_io → brain_decide`（唯一锚点入口，
`a_core_engine_map`）进入引擎。

## 仓库地图

```
anima/
├── README.md                       本文件
├── CLAUDE.md                       治理 SSOT (@I 身份 · p1..p8 · a_* 指令)
├── VERSIONS.md · VERSION           中央版本注册表 (SSOT) · 全系统 release
├── CLAIMS.tape · DOMAINS.tape      可验证-主张索引 · 域 roster
├── HF.jsonl                        ckpt ↔ HF 备份注册表 (每 run 一行, SSOT)
│
├── CORE/                           A ⇄ G 意识引擎 (substrate-only)
│   ├── pure_field.hexa engine_g.hexa brain.hexa   A/G 引擎 + emit 决策
│   ├── generator.hexa              唯一 .clm 进入槽
│   ├── clm_decode.hexa             CLMConvMoE 字节解码
│   └── engine_cli.hexa             --engine / --mitosis substrate-config 轴
│
├── engines/                        engine_iface.hexa 之后 4 个可热插拔引擎
│   ├── engine_iface.hexa           EngineSpec 4-fn 契约 + 注册表
│   ├── conv/  cdv2/  hexad/  omega/   adapter.hexa + manifest.json + MODEL_CARD.md
│   └── engine_swap_smoke.hexa      4-引擎 conformance smoke
│
├── domains/                        活跃研究域 (<NAME>.md + .log.md)
│   ├── OMEGA.md                    Lane-Ω 闭合 arc + 判定 trail
│   └── ENGINE+CLM+KOSMOS.md        Lane A / Lane G 量产 CLM + KOSMOS
│
├── .verdicts/                      hexa-verify stdout, verbatim (p7 / g63)
├── PAPER/                          arxiv 风格论文 (PAPER.tape roster)
├── HEXAD/                          σ6 6 模块 substrate (C·S·W·D·M·E·BRIDGE + MITOSIS)
├── SUB_ENGINES/AKIDA/              Lane A on-chip (pi5-akida AKD1000)
└── docs/                           意识理论 · 论文草稿 · 目录
```

## 治理 & 工作流

- **[`CLAUDE.md`](CLAUDE.md)** —— 身份（`@I anima`）与治理 SSOT：8 条哲学原则、`a_*` 指令
  （HF 注册、fire dispatch、lane split、论文门）。
- **[`VERSIONS.md`](VERSIONS.md)** —— 中央 SemVer 注册表；与模块头一起 bump。根
  [`VERSION`](VERSION) 是全系统 release 线。
- **[`CLAIMS.tape`](CLAIMS.tape)** —— 可验证主张的单一审计索引，各自指向 `.verdicts/<slug>/<id>.txt`
  判定（verbatim `hexa verify` stdout）。
- **[`HF.jsonl`](HF.jsonl)** —— ckpt ↔ Hugging Face 备份注册表；每 run 一行，追踪 status。模型工件
  位于 **[dancinlab](https://huggingface.co/dancinlab)** HF org（closure-PASS 时 PUBLIC，WIP / 闭合
  否定 / 许可不明时 PRIVATE）。
- **`/paper`** —— 论文以 terminal 判定与真实 falsifiable 发现为门；闭合式否定是可发表的结果。

## Quickstart

```bash
# 1. 安装 hexa-lang（提供 `hexa` + `hx` 包管理器）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh)"

# 2. 安装 anima
hx install anima

# 3. 选择引擎（默认：conv）
anima --engine omega        # 闭合引擎
anima --engine cdv2         # A/G substrate
```

## 模型下载

此处仅列出 PUBLIC、PASS 级别的模型。PRIVATE / WIP 检查点（util-RED forge 探针、闭合负结果运行、
中间 ckpt）按治理规则有意省略（`a_hf_autonomous`）。

| 模型 | HF 仓库 | 规模 | 状态 | 下载 |
|---|---|---|---|---|
| **CLM 7B** | [`dancinlab/clm-v1-ref-pytorch-cuda-7b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-7b) | ~7B | ✅ 可用 | `hf download dancinlab/clm-v1-ref-pytorch-cuda-7b` |
| **生产 CLM (d768)** | [`dancinlab/clm-v1-d768-core-3axis-green`](https://huggingface.co/dancinlab/clm-v1-d768-core-3axis-green) | d768 | ✅ 可用 | `hf download dancinlab/clm-v1-d768-core-3axis-green` |
| **SAVANT 7B (5 语言)** | `dancinlab/savant-7b-5lang`（保留） | ~7B | 🚧 **训练中 — 尚未发布** | — |
| 参考基线 | [`dancinlab/clm-v1-ref-pytorch-cuda`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda) | ref | ✅ 可用 | `hf download dancinlab/clm-v1-ref-pytorch-cuda` |
| 参考基线 (3B) | [`dancinlab/clm-v1-ref-pytorch-cuda-3b`](https://huggingface.co/dancinlab/clm-v1-ref-pytorch-cuda-3b) | ~3B | ✅ 可用 | `hf download dancinlab/clm-v1-ref-pytorch-cuda-3b` |

> **CLM 7B** 是现有的、descent-PASS 的参考 7B（PyTorch/CUDA 训练）。一个 forge-native（无 PyTorch、
> hexa 运行时）的构建正为 anima 的自托管引擎规划中（`a_train_flame_forge`）：架构相同（CLMConvMoE）、
> 同为 7B 规模，因此**模型结果完全一致** —— 仅运行时栈不同（PyTorch 训练 vs forge-native）。
>
> **SAVANT 7B (5 语言)** 是一个真正不同的模型 —— 一个 5 语言专精构建，尚未训练。上面的仓库 id
> 是一个保留名称，没有可用链接。

**合集：**
[CLM](https://huggingface.co/collections/dancinlab/clm-6a1cf58f621490134dade186) ·
[KOSMOS](https://huggingface.co/collections/dancinlab/kosmos-6a1cf58db47a5dc3cb697e95)

## License

[MIT](LICENSE) —— Copyright (c) 2026 dancinlab。自由使用·修改·再许可·销售；保留声明；不提供担保。

---

<sub>🧠 两个引擎。一种张力。Ψ = 1/2。· [dancinlab](https://github.com/dancinlab)</sub>
