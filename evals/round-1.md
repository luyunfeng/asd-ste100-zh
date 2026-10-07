# 评测第一轮：翻译准确性（英 → 中）

方法：对 danyuchn 规则摘要（MIT）逐类建「触发条件 / 要求 / 例外」三要素表，核对中文版是否语义完整；关键条款做回译抽查。发现偏移即修正 writing-rules.md，本文件记录全部判定。

## 三要素核对表

| 英文规则要点 | 中文处理 | 三要素核对 | 判定 |
|---|---|---|---|
| Use approved words only in approved meaning | 一词一义 + 术语表指向 | 触发=行文选词；要求=一名一词；例外=术语表未覆盖时自选并贯穿 | 保留 |
| Prefer plainer, shorter word | 白话优先 + 替换表 | 要求保留；例外=替换表声明「方向非合规」 | 保留 |
| Verb for action, not noun derived (3.7) | 虚动词规则（进行/加以/作出→直接动词） | 触发=虚动词句式；要求=直接动词；例外=无 | 保留（中文对应物） |
| No phrasal verbs (9.3) | 中文无短语动词问题 | **不适用**，标记跳过 | 替换为中文虚动词与套话规则 |
| One instruction per sentence | 一句话只做一个操作 | 要求保留；例外=无 | 保留 |
| 20/25 words limit | 操作句≤30 字、描述句≤40 字 + 字数算法 | 触发=所有句子；要求=阈值；例外=代码/表格不计 | **修正过**（见修正 A） |
| Do not omit parts to shorten | 不省略主谓宾 | 保留，例外=祈使句省主语在中文操作句中天然成立，写明 | **修正过**（见修正 B） |
| Noun clusters ≤3 | 修饰语≤15 字、连续「的」≤2 | 中文对应物换成「的链」度量 | 保留（度量替换） |
| No semicolon (8.1) | 禁分号串句 | 触发=分号；要求=拆两句；例外=**无** | **修正过**（见修正 C） |
| One topic per paragraph, ≤6 sentences | 一段一主题 ≤6 句 | 完整保留 | 保留 |
| Safety instructions lead with command | 关键指令放开头 | 保留，中文场景扩展到删除/上线变更 | 保留（场景扩展） |
| Verb forms（-ing、时态限制） | **不适用**，替换为时态副词明确化（已经/正在/将） | 中文无时态屈折 | 替换 |
| Terminology allowance | 术语表机制（cs-terms.md） | 完整保留，词表换成计算机领域自建 | 保留 |

## 回译抽查（3 条）

1. 「动作直接用动词，不名词化」→ 回译 "express an action with a verb directly; do not nominalize it" ≈ 原义（3.7）。语义保留。
2. 「禁用分号串句：两个动作写两句」→ 回译 "semicolon chaining is banned; write two actions as two sentences" ≈ 规则 8.1。语义保留。
3. 「术语表没有覆盖的概念，选全团队最常用的那个叫法，全文保持一致」→ 回译 "for concepts outside the table, pick the team's most common name and keep it consistent" ≈ 术语许可条款的改编。语义保留。

## 本轮修正（已写回 writing-rules.md）

- **修正 A**：初稿只有「操作句 ≤30 字」，遗漏描述句阈值。英文按词计数，中文没有词边界，因此补充了字数算法（汉字/英文单词/数字串/行内代码各计 1，标点不计），并补描述句 ≤40 字。
- **修正 B**：「不省略成分」初稿未处理中文操作句天然省主语（祈使句）的情况，会造成误伤。已写明例外：操作句用祈使句不算省略。
- **修正 C**：分号规则初稿写成「尽量少用」，回查 STE 规则 8.1 为完全禁止，已改回「禁用分号串句」，与英文标准强度对齐。

## 结论

13 个规则类目：10 项直接保留，3 项修正后保留，2 项英文特有规则标记不适用并替换为中文对应物。翻译语义完整性通过；进入第二轮（领域适配）。
