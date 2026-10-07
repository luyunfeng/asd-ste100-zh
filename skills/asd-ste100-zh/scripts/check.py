#!/usr/bin/env python3
"""ASD-STE100-zh 受控中文检查器 v2（零依赖，stdlib-only）。

只报「嫌疑」，不改文本；告警按 writing-rules.md 的语义判断后再处理。
告警分级：HARD = 结构类规则，建议必改；SOFT = 方向类提示，酌情处理。
按设计不检查情态与确定度（那是内容不是文风）——「可能」必须保留。

用法：
    python3 check.py 文件.md [更多文件...]
    cat 文本 | python3 check.py -
    python3 check.py --json 文件.md

退出码：0 = 无 HARD 告警；1 = 有 HARD 告警；2 = 用法错误。
"""
import json, re, sys, unicodedata

# ---- 规则定义（id, 名称, 正则, 级别, 提示） ----
RULES = [
    ("R3", "程度词无数值", r"(很|非常|较|大量|尽快|及时|显著|大幅|明显|极大|巨大)", "HARD", "写数值或条件：「在 5 分钟内」「超过 3 次时」"),
    ("R4", "营销形容词", r"(强大|强大的|领先|业界领先|行业领先|海量的|一站式|开箱即用|卓越|极致|全方位|顶级|顶尖|革命性|颠覆性|突破性|开创性|史诗级|硬核|丝滑|王炸)", "HARD", "删掉，或换成能兑现这个说法的数字"),
    ("R11", "黑话", r"(赋能|抓手|闭环|拉通|沉淀|痛点|对标|打法|拉齐|落地|助力|深度优化|强力支撑|致力于|深耕|发力|加码|引领|抢占|拥抱变化|夯实|筑牢|破局|破圈|出圈|赛道|心智|势能|护城河|顶层设计|底层逻辑|组合拳|一盘棋|双轮驱动|全链路|全方位|强强联合|深度融合|有机融合)", "HARD", "换成具体动作：让……能做到……；写清改了哪个模块")
    ,
    ("R12", "套话", r"(需要注意的是|值得一提的是|综上所述|总的来说|在一定程度上|不难发现|由此可见|应运而生|蓬勃发展|摆在[^，。]{0,8}面前)", "HARD", "删除，直接写后面的内容"),
    ("R13", "空壳指代", r"(相关|上述|该模块|相关模块|相关配置|相关参数|相关文件)", "SOFT", "写出具体名字；确实泛指时可保留"),
    ("R10", "虚动词", r"(进行|加以|作出|予以)[^，。；！？\n]{0,8}(部署|配置|调整|处理|升级|修改|优化|检查|分析|评估|确认|说明|采集|清洗|构建|清理|重启|回滚|恢复|验证|测试|发布|合入|还原|排查|审查)", "HARD", "换成直接动词：「部署服务」，不写「对服务进行部署」"),
    ("R15", "名词化", r"(实现|完成|做到)[^，。；！？\n]{0,10}的(采集|清洗|处理|升级|分析|优化|管理|支撑|保障)", "HARD", "还原成动词句：「清洗数据」，不写「完成数据的清洗」"),
    ("R16", "被动标记", r"(被|由[^，。]{0,6}(执行|完成|处理)|受到|得以)", "SOFT", "操作文本用主动语态，写清执行者；执行者确实未知时可保留"),
    ("R17", "顺序连词堆叠", r"(首先|然后|接着|最后)", "SOFT", "改用编号列表，每步一个动作，不在正文里用「首先……然后……」"),
    ("R18", "翻案腔", r"不是[^，。；！？\n]{1,16}[，。；！？][^。]{0,6}而是|不是[^，。；！？\n]{1,16}而是", "SOFT", "直接从正面说判断；材料里真实的自我修正可以保留"),
    ("R19", "人称含糊", r"(我们|咱们|大家)", "SOFT", "写具体名称：团队名、系统名；对话语体可保留"),
    ("R20", "强度词未分级", r"(应当|务必|一定要|应该|严禁|切勿|最好|尽量)", "SOFT", "三级规范化：要求写「必须」，推荐写「宜」，禁止写「不得」"),
    ("R21", "空泛副词", r"(极其|极为|十分|愈发|日益|深深地)", "SOFT", "删掉，或写出程度差异的具体数值"),
]
SENT_SPLIT = re.compile(r"[。！？\n]")
PRONOUN = re.compile(r"[其此它]|该")
DE_CHAIN = re.compile(r"的[^，。；！？\n]{0,12}的[^，。；！？\n]{0,12}的")

def char_len(s):
    return sum(1 for ch in s if not ch.isspace())

def check(text):
    alerts = []
    lines = text.splitlines()
    in_code = False
    for ln, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code or not s:
            continue
        for rid, name, pat, level, hint in RULES:
            for m in re.compile(pat).finditer(s):
                frag = m.group(0)
                alerts.append({"line": ln, "rule": rid, "name": name, "level": level, "fragment": frag[:24], "hint": hint})
        if DE_CHAIN.search(s):
            alerts.append({"line": ln, "rule": "R7", "name": "的链过长", "level": "HARD", "fragment": "的……的……的", "hint": "名词前修饰拆句或删减，每层不超过 15 字"})
        sentences = [x for x in SENT_SPLIT.split(s) if x.strip()]
        for sent in sentences:
            if len(PRONOUN.findall(sent)) >= 3:
                alerts.append({"line": ln, "rule": "R9", "name": "指代密集", "level": "HARD", "fragment": sent[:20] + "…", "hint": "「其/该/此/它」只指代上一句对象；过多时重复名词"})
            n = char_len(sent)
            if n > 40:
                alerts.append({"line": ln, "rule": "R6", "name": "句长超限", "level": "HARD", "fragment": sent[:18] + f"…（{n} 字）", "hint": "操作句 ≤30 字、描述句 ≤40 字；检查是否一句串多事"})
        if len(sentences) > 6:
            alerts.append({"line": ln, "rule": "R14", "name": "段落过长", "level": "HARD", "fragment": f"{len(sentences)} 句", "hint": "一段一主题，不超过 6 句"})
    return alerts

def main(argv):
    args = [a for a in argv if a != "--json"]
    as_json = len(args) != len(argv)
    if not args:
        print(__doc__)
        return 2
    alerts = []
    for path in args:
        text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        for a in check(text):
            a["file"] = path
            alerts.append(a)
    if as_json:
        print(json.dumps(alerts, ensure_ascii=False, indent=2))
    else:
        for a in alerts:
            tag = "HARD" if a["level"] == "HARD" else "soft"
            print(f'{a["file"]}:{a["line"]}: [{a["rule"]} {a["name"]}|{tag}] {a["fragment"]}\n    提示: {a["hint"]}')
        hard = sum(1 for a in alerts if a["level"] == "HARD")
        soft = len(alerts) - hard
        print(f"\n共 {len(alerts)} 条告警（HARD {hard} / soft {soft}）")
    return 1 if any(a["level"] == "HARD" for a in alerts) else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

