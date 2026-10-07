# ASD-STE100-zh

> **受控中文技术写作技能（计算机领域第一版）。** 把 ASD-STE100——航空业用来保证「维修工不可能读错」的受控英语——的纪律搬到中文：一个词只有一个意思，一句话只有一种结构。主攻计算机领域的文本：报错信息、工具描述、agent 间指令、system prompt、部署步骤、代码评审意见、README。

**非官方声明**：本项目是对 ASD-STE100 公开规则类别的中文意译与改编，不是官方中文译本，不声称符合 ASD-STE100 标准。规范的权威文本（英文，Issue 9）可在 [官网](https://www.asd-ste100.org/) 免费索取。规则摘要基于 MIT 许可的 [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill)，并融合了 [简明技术中文（STC）](https://github.com/mzopedia/simplified-technical-chinese) 与 [tw93/Waza](https://github.com/tw93/Waza) clarity 规则的思路。

## 为什么需要它

AI 输出越来越多，看不懂的时候说「再讲一遍」没用——它会用同样的方式再讲一遍。真正的问题不是讲得不够，而是**文本会被误读**：报错信息没说清谁该做什么，agent 间指令的条件挂错了动作，工具描述全是「赋能」「一站式」而没有一句能执行的话。

受控写作的解法是：短句、白话、一词一义、一句一动作、条件前置。中文的歧义来源和英语不同（虚动词、套话、同义轮换、一句串多事），所以本项目**按中文歧义来源重写规则，不是逐条翻译英文规则**。

## 效果（16 样本六轮评测，v0.2.0）

| 指标 | 结果 |
|---|---|
| 四维评分（歧义消除/信息保真/术语正确/简洁，满分 12） | 16 样本：改写前均分 **7.0** → 改写后 **11.8** |
| 信息保真 | 12 样本零降分（不丢信息、不编内容） |
| 检查器灵敏度 | 9 对 fixtures（20 条规则，HARD/soft 分级）：改写前 33 条告警，改写后 0 条，无误报 |

详见 [evals/RESULTS.md](evals/RESULTS.md)（六轮方法、暴露并修复的 8 个问题、已知局限。方法论来源：danyuchn 六项扫描清单与 Kept as-is 约定、AminBlg 规范动词映射与压力测试基线法、STC 强度词三级与近义辨析词典、Waza 反 AI 中文腔清单）。

## 安装

**Claude Code / Codex / Cursor 等支持 Agent Skills 标准的 agent**：把 `skills/asd-ste100-zh/` 目录复制到你的技能目录即可，无第三方依赖。

```bash
git clone https://github.com/luyunfeng/asd-ste100-zh.git
mkdir -p ~/.claude/skills
cp -r asd-ste100-zh/skills/asd-ste100-zh ~/.claude/skills/
```

## 用法

对 agent 说：

```text
受控中文改写这段报错信息：……        # 自动选严格档
用严格档改写这段部署步骤：……
把这段 README 改清楚（清晰档）：……
受控中文改写，并给前后对照和规则标注：……
```

- **严格档**：操作步骤、报错、工具描述、agent 间指令、system prompt——误读有代价的文本。
- **清晰档**：README、PR 描述、变更记录——保真优先，允许自然句式。
- **检查器**：`python3 skills/asd-ste100-zh/scripts/check.py 文件.md`（零依赖，只报嫌疑不改正文）。

## 仓库结构

```
asd-ste100-zh/
├── AGENTS.md                  # 面向 agent/维护者的仓库指南
├── README.md                  # 本文件
├── skills/
│   └── asd-ste100-zh/         # 计算机领域 skill（独立、自包含）
│       ├── SKILL.md           # 技能主文件
│       ├── references/        # 写作规则 / 术语表 / 替换表
│       ├── scripts/check.py   # 零依赖检查器
│       └── examples/          # 前后对照示例
└── evals/                     # 评测标准、测试集、三轮报告
```

## 扩展新领域

不同领域**是不同的 skill**，互不依赖。新增领域（如金融、法律）的步骤见 [AGENTS.md「新增领域技能」](AGENTS.md#新增领域技能)。要点：复制计算机领域 skill 的骨架，重写领域术语表和示例，跑完三轮评测再发布。

## License

MIT。ASD-STE100 是 ASD 的商标；本项目与其无隶属关系。

## 致谢

- [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill)（MIT）——规则摘要与两档模式的基础
- [mzopedia/simplified-technical-chinese](https://github.com/mzopedia/simplified-technical-chinese)——中文规则的先行者
- [tw93/Waza](https://github.com/tw93/Waza)（MIT）——clarity 防误读边界、反 AI 中文腔清单
- [Karpathy 关于理解模型输出的推文](https://x.com/karpathy/status/2105819303471976479)——本项目的直接动机

