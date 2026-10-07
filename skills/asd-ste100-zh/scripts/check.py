#!/usr/bin/env python3
"""ASD-STE100-zh 受控中文检查器（零依赖，stdlib-only）。

只报「嫌疑」，不改文本；告警需要按 writing-rules.md 的语义判断后再处理。

用法：
    python3 check.py 文件.md [更多文件...]
    cat 文本 | python3 check.py -

退出码：0 = 无告警；1 = 有告警；2 = 用法错误。
"""
import re, sys, unicodedata

VIRTUAL_VERB = re.compile(r"(进行|加以|作出|予以)[^，。；！？\n]{0,6}(部署|配置|调整|处理|升级|修改|优化|检查|分析|评估|确认|说明|采集|清洗|构建|清理|重启|回滚|恢复|验证|测试|发布|合入|还原)")
HEDGES = re.compile(r"(很|非常|较|大量|尽快|及时|显著|大幅|明显)")
JARGON = re.compile(r"(赋能|抓手|闭环|拉通|沉淀|痛点|对标|打法|拉齐|落地)")
FILLER = re.compile(r"(需要注意的是|值得一提的是|综上所述|总的来说|在一定程度上|不难发现|由此可见|相关|上述)")
PRONOUN = re.compile(r"[其此它]|该")
SENT_SPLIT = re.compile(r"[。！？\n]")

def char_len(s: str) -> int:
    n = 0
    for ch in s:
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            n += 1
        elif not ch.isspace():
            n += 1
    return n

def check(text: str):
    alerts = []
    lines = text.splitlines()
    in_code = False
    for ln, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or stripped.startswith(("#", "|", ">", "-", "*")) and ln > 1:
            pass
        if in_code:
            continue
        body = stripped
        if not body:
            continue
        for m in VIRTUAL_VERB.finditer(body):
            alerts.append((ln, "R10 虚动词", m.group(0), "换成直接动词：写「部署服务」，不写「对服务进行部署」"))
        for m in HEDGES.finditer(body):
            alerts.append((ln, "R5 程度词无数值", m.group(0), "写数值或条件：例如「在 5 分钟内」「超过 3 次时」"))
        for m in JARGON.finditer(body):
            alerts.append((ln, "R11 黑话", m.group(0), "换成具体动作或删除"))
        for m in FILLER.finditer(body):
            alerts.append((ln, "R12 套话", m.group(0), "删除，直接写后面的内容"))
        if "；" in body:
            alerts.append((ln, "R8 分号串句", "；", "拆成两句；STE 规则 8.1 完全禁止分号"))
        if re.search(r"的[^，。；\n]{0,12}的[^，。；\n]{0,12}的", body):
            alerts.append((ln, "R7 的链过长", "的……的……的", "名词前修饰拆句或删减，每层修饰不超过 15 字"))
        for m in PRONOUN.finditer(body):
            sent = SENT_SPLIT.split(body)
            pass
        sentences = [s for s in SENT_SPLIT.split(body) if s.strip()]
        for sent in sentences:
            if PRONOUN.search(sent) and len(PRONOUN.findall(sent)) >= 3:
                alerts.append((ln, "R9 指代密集", sent[:20] + "…", "「其/该/此/它」只指代上一句对象；过多时重复名词"))
            n = char_len(sent)
            limit = 40
            if n > limit:
                alerts.append((ln, "R6 句长超限", sent[:18] + f"…（{n} 字）", "操作句 ≤30 字、描述句 ≤40 字；检查是否一句串多事"))
        if sentences and len(sentences) > 6:
            alerts.append((ln, "R13 段落过长", f"{len(sentences)} 句", "一段一主题，不超过 6 句"))
    return alerts

def main(argv):
    if not argv:
        print(__doc__)
        return 2
    alerts = []
    for path in argv:
        text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        for ln, rule, frag, hint in check(text):
            alerts.append(f"{path}:{ln}: [{rule}] {frag}\n    提示: {hint}")
    for a in alerts:
        print(a)
    print(f"\n共 {len(alerts)} 条告警")
    return 1 if alerts else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

