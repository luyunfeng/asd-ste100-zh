# AGENTS.md — 仓库指南（面向 agent 与维护者）

本仓库产出「ASD-STE100-zh」系列技能：中文受控技术写作，按领域拆分为独立 skill。计算机领域（`skills/asd-ste100-zh/`）是第一个。Agent 在本仓库工作时遵守本文件。

## 目录结构

```
skills/asd-ste100-zh/          # 计算机领域 skill（自包含，可整目录复制安装）
  SKILL.md                     # 技能主文件：触发描述、两档模式、改写流程
  references/writing-rules.md  # 中文化规则（含来源与非官方声明）
  references/cs-terms.md       # 计算机术语一词一义表
  references/substitutions.md  # 替换表（方向建议，非合规清单）
  scripts/check.py             # 零依赖检查器（stdlib-only）
  examples/before-after.md     # 前后对照示例（带规则标注）
evals/                         # rubric、12 样本测试集、fixtures、三轮报告
```

## 硬规则

1. **非官方声明不可删**。`writing-rules.md` 与 README 中的「来源与非官方声明」必须保留：本项目意译公开规则类别，不逐字复制规范文本，不声称符合 ASD-STE100。
2. **改规则必须过评测**。修改 `writing-rules.md`、`cs-terms.md`、`check.py` 任一文件后：跑 `check.py` 对 `evals/fixtures/` 全量回归，after 样本必须保持 0 告警；规则语义变化时在 `evals/` 追加一轮报告。
3. **受控改写不虚构**。示例和测试集中的改写不得添加原文没有的数值、路径、命令；原文含糊时保留含糊并结构化。
4. **领域隔离**。每个领域是独立 skill 目录；计算机领域的规则迭代不影响其他领域 skill。

## 常用命令

```bash
# 检查一段文本
python3 skills/asd-ste100-zh/scripts/check.py 文件.md

# 全量回归（改检查器或规则后必跑）
for f in evals/fixtures/after/*.txt; do python3 skills/asd-ste100-zh/scripts/check.py "$f" | tail -1; done
```

## 新增领域技能

1. 复制骨架：`cp -r skills/asd-ste100-zh skills/asd-ste100-zh-<domain>`。
2. 重写三处领域内容：SKILL.md 的 description（领域触发词与场景）、references/cs-terms.md 换成 `<domain>-terms.md`（领域一词一义表）、examples 换成领域示例。
3. 通用规则文件（writing-rules.md、substitutions.md）以计算机领域版为底，删去领域专属条目后按新领域调整。
4. 新建该领域的测试集（≥10 样本）与 fixtures，跑完三轮评测（语义核对、领域适配评分、检查器回归）并写入 `evals/`。
5. 更新 README 的结构图与安装说明。

## 提交规范

格式：`<范围>: <中文摘要>`，范围取 `skill` / `rules` / `terms` / `checker` / `evals` / `docs`。示例：`checker: 动词清单补充构建/清理等 10 个词，修复 S3/S6 漏报`。

