#!/usr/bin/env python3
"""Generate the 40 Chinese Quarto session decks from reviewed content specs.

The specs below are the instructional source of truth.  Generation only removes
mechanical repetition in front matter, speaker-note wrappers, and navigation.
Run from any directory:

    python3 presentation/scripts/generate_sessions.py
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "presentation" / "sessions"


def clean(text: str) -> str:
    return dedent(text).strip()


def yaml_quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def slide(title: str, body: str, note: str) -> str:
    return (
        f"## {title}\n\n"
        f"{clean(body)}\n\n"
        "::: {.notes}\n"
        f"{clean(note)}\n"
        ":::"
    )


def reading_block(spec: dict) -> str:
    lines = [
        f"- Hansen {spec['chapters']}：书内 {spec['book_pages']} 页，PDF {spec['pdf_pages']} 页。",
    ]
    for label, local_path, url in spec["links"]:
        lines.append(f"- {label}：仓库 {local_path}。")
        lines.append(f"- 在线阅读：[{label}]({url})。")
    return "\n".join(lines)


def render_main(spec: dict) -> str:
    chunks: list[str] = []
    chunks.append(
        clean(
            f"""
            ---
            title: "第 {spec['number']:02d} 次：{yaml_quote(spec['title'])}"
            subtitle: "{yaml_quote(spec['subtitle'])}"
            author: "Hansen《Econometrics》中文全年课程"
            date: last-modified
            session-number: {spec['number']}
            session-type: "主课"
            semester: {spec['semester']}
            duration: 90
            chapters: "{yaml_quote(spec['chapters'])}"
            book-pages: "{yaml_quote(spec['book_pages'])}"
            pdf-pages: "{yaml_quote(spec['pdf_pages'])}"
            ---
            """
        )
    )
    chunks.append(
        slide(
            "本次课的任务",
            "\n".join(f"- {item}" for item in spec["objectives"]),
            f"用 2 分钟说明本课在全年主线中的位置：{spec['position']}。请学生把三个目标改写成“下课前我能做什么”。",
        )
    )
    chunks.append(
        slide(
            "先修检查",
            "\n".join(f"- {item}" for item in spec["prerequisites"]),
            "逐项停顿，让学生先独立判断。若有两项以上不能回答，不要直接进入公式；先打开相应补充讲义定位定义。",
        )
    )
    chunks.append(
        slide(
            "从本科语言到 Hansen 语言",
            f"::: {{.bridge}}\n{spec['bridge']}\n:::",
            f"先请学生说出本科教材通常怎样表述，再展示 Hansen 的对象。追问：{spec['bridge_prompt']}",
        )
    )
    chunks.append(
        slide(
            "路线图",
            "\n".join(f"{i + 1}. {item}" for i, item in enumerate(spec["route"])),
            "强调顺序不能互换：先定义对象和识别，再写估计量，最后才谈标准误或经验解释。",
        )
    )
    for concept in spec["concepts"]:
        chunks.append(
            slide(
                concept["title"],
                concept["body"],
                concept.get(
                    "note",
                    f"本页围绕“{concept['title']}”只推进一个概念。先遮住结论，让学生解释每个符号的随机性与维数，再显示结论。",
                ),
            )
        )
    derivation = spec["derivation"]
    chunks.append(
        slide(
            f"推导起点：{derivation['title']}",
            f"::: {{.derivation}}\n{derivation['setup']}\n:::",
            f"板书推导标题“{derivation['title']}”。先写已知与目标，不允许学生从结论倒推。",
        )
    )
    for idx, step in enumerate(derivation["steps"], start=1):
        chunks.append(
            slide(
                f"推导第 {idx} 步",
                f"::: {{.derivation}}\n{step}\n:::",
                f"本步只使用：{derivation['reasons'][idx - 1]}。完成后追问这一步若缺少哪个条件会失败。",
            )
        )
    chunks.append(
        slide(
            "推导结论与含义",
            f"::: {{.takeaway}}\n{derivation['conclusion']}\n:::",
            "让学生用一句不含公式的话解释结论，再明确它没有证明什么，防止把代数结果升级为因果结论。",
        )
    )
    chunks.append(
        slide(
            "条件与维数核对",
            f"::: {{.dimension-check}}\n"
            + "\n".join(f"- {item}" for item in spec["conditions"])
            + "\n:::",
            "逐条核对：对象维数、矩存在、可逆/秩、抽样或条件期望假设。把最容易被省略的一条圈出来。",
        )
    )
    chunks.append(
        slide(
            spec["example"]["title"],
            spec["example"]["body"],
            f"先给 60 秒让学生判断例子在说明对象、识别还是推断。随后按“{spec['example']['title']}”中的数字或符号逐项解释。",
        )
    )
    chunks.append(
        slide(
            "常见错误：错在哪里",
            f"::: {{.misconception}}\n{spec['misconception']}\n:::",
            "不要只说结论错误。要求学生指出错误推理发生在哪个箭头，并给出能使该箭头成立的额外条件。",
        )
    )
    chunks.append(
        slide(
            "课堂检查题",
            f"::: {{.checkpoint}}\n{spec['check']['question']}\n:::",
            "留出 2–3 分钟独立作答，再同桌互相解释。不要在本页提前透露答案；观察学生使用的是定义还是记忆口号。",
        )
    )
    chunks.append(
        slide(
            "检查题解答与诊断",
            f"::: {{.checkpoint}}\n{spec['check']['answer']}\n:::",
            f"按错误类型分流：{spec['check']['diagnosis']}。让答错者回到对应定义页，而不是只抄答案。",
        )
    )
    chunks.append(
        slide(
            "本课小结",
            "\n".join(f"- {item}" for item in spec["takeaways"]),
            "请学生合上讲义复述三句话：目标对象、关键条件、主要推导。若只能复述公式，说明尚未形成计量含义。",
        )
    )
    chunks.append(
        slide(
            "阅读与练习",
            reading_block(spec),
            f"指定阅读时区分 A/B/C 层级。本课建议先完成：{spec['practice']}。提醒先独立写路线，再对照逐步解答。",
        )
    )
    chunks.append(
        slide(
            "备查与延伸",
            "\n".join(f"- {item}" for item in spec["extensions"]),
            "这部分不占用主线时间。根据学生方向选择一项；其余内容明确列为课后阅读，不在 90 分钟内匆忙扫过。",
        )
    )
    chunks.append(
        "\n".join(
            [
                "<!-- GENERATED from presentation/scripts/generate_sessions.py -->",
                f"<!-- CONTENT_KEY: session-{spec['number']:02d} -->",
            ]
        )
    )
    return "\n\n".join(chunks).rstrip() + "\n"


def render_workshop(spec: dict) -> str:
    chunks: list[str] = []
    chunks.append(
        clean(
            f"""
            ---
            title: "第 {spec['number']:02d} 次工作坊：{yaml_quote(spec['title'])}"
            subtitle: "{yaml_quote(spec['subtitle'])}"
            author: "Hansen《Econometrics》中文全年课程"
            date: last-modified
            session-number: {spec['number']}
            session-type: "工作坊"
            semester: {spec['semester']}
            duration: 90
            chapters: "{yaml_quote(spec['chapters'])}"
            book-pages: "{yaml_quote(spec['book_pages'])}"
            pdf-pages: "{yaml_quote(spec['pdf_pages'])}"
            ---
            """
        )
    )
    chunks.append(
        slide(
            "本次工作坊的任务",
            "\n".join(f"- {item}" for item in spec["objectives"]),
            f"说明本工作坊承接的位置：{spec['position']}。强调今天评价的是设定理由与解释闭环，不只是代码是否运行。",
        )
    )
    chunks.append(
        slide(
            "先修检查",
            "\n".join(f"- {item}" for item in spec["prerequisites"]),
            "让学生先写出估计对象、关键假设和预期诊断。若只会说软件命令，先回到相应主课。",
        )
    )
    ordered = [
        ("研究问题", spec["research_question"], "先把问题翻译成可估计对象。要求学生说清结果变量、处理/解释变量和目标总体。"),
        ("数据状态与复现方式", spec["data_status"], "明确本页是模拟、教材数据还是预计算结果。指出数据缺失时的可观察提示，不让空表静默出现。"),
        ("样本与筛选", spec["sample"], "逐项说明保留/删除观测的理由，并追问筛选后结论适用于哪个总体。"),
        ("变量变换", spec["variables"], "把每个变换连接到经济单位或随机过程性质，避免把对数、差分、标准化当成无意义预处理。"),
        ("模型与识别", spec["identification"], "先写总体模型与识别条件，再看样本估计命令。要求学生指出最不可检验的条件。"),
        ("估计量", spec["estimator"], "逐步把估计公式与代码对象对应；检查维数、投影或矩条件。"),
        ("标准误、聚类与临界值", spec["inference"], "让学生先根据抽样结构选择推断，再显示课程选择；严禁按显著性挑标准误。"),
        ("执行流程", spec["workflow"], "按输入—变换—估计—诊断—输出走一遍，明确每一步失败时应看到什么。"),
        ("R 代码：数据与设定", spec["code_setup"], "代码默认不在 Quarto 构建中执行。逐行解释固定种子、样本量和变量生成/读取。"),
        ("R 代码：估计与输出", spec["code_estimate"], "先预测输出列和符号，再运行。提醒保存 sessionInfo 与关键样本计数。"),
        ("示例输出", spec["results"], "这是固定种子预计算输出。逐列解释点估计、SE/区间、样本或簇数；不要只读星号。"),
        ("诊断", spec["diagnostics"], "逐个诊断说明它能发现什么、不能证明什么。把最危险的失败模式写在板书右侧。"),
        ("敏感性分析", spec["sensitivity"], "只改变一个有争议设定，比较估计对象是否变化；不要把无目的规格搜索称为稳健性。"),
    ]
    for title, body, note in ordered:
        chunks.append(slide(title, body, note))
    chunks.append(
        slide(
            "常见错误：错在哪里",
            f"::: {{.misconception}}\n{spec['misconception']}\n:::",
            "让学生定位错误发生在样本、识别、估计、方差还是解释层；给出一项能真正修正错误的动作。",
        )
    )
    chunks.append(
        slide(
            "课堂检查题",
            f"::: {{.checkpoint}}\n{spec['check']['question']}\n:::",
            "留 3 分钟先独立写设定和理由，再两人互查。答案必须包含方法与原因，只有命令名不给分。",
        )
    )
    chunks.append(
        slide(
            "检查题解答与诊断",
            f"::: {{.checkpoint}}\n{spec['check']['answer']}\n:::",
            f"按错误类型回看：{spec['check']['diagnosis']}。要求学生修改原答案，而不是只听讲。",
        )
    )
    chunks.append(
        slide(
            "工作坊小结",
            "\n".join(f"- {item}" for item in spec["takeaways"]),
            "请学生用“对象—设定—估计—推断—限制”五句话口头提交结果，任何一步缺失都不算复现完成。",
        )
    )
    chunks.append(
        slide(
            "复现任务与阅读",
            reading_block(spec) + f"\n- 本次提交：{spec['practice']}",
            "明确提交物包括代码、数字表和设定说明。提醒教材数据不进入 Git，只提交可复现路径和脚本。",
        )
    )
    chunks.append(
        slide(
            "备查与延伸",
            "\n".join(f"- {item}" for item in spec["extensions"]),
            "主线结束后按班级进度选择一项。其余作为研究方向阅读，避免压缩前面的诊断和解释时间。",
        )
    )
    chunks.append(
        "\n".join(
            [
                "<!-- GENERATED from presentation/scripts/generate_sessions.py -->",
                f"<!-- CONTENT_KEY: workshop-{spec['number']:02d} -->",
            ]
        )
    )
    return "\n\n".join(chunks).rstrip() + "\n"


MAIN_SESSIONS = [
    {
        "number": 1,
        "semester": 1,
        "title": "课程导论与学习诊断",
        "subtitle": "计量研究在估计什么，概率抽样为何必要",
        "chapters": "Ch.1",
        "book_pages": "1–12",
        "pdf_pages": "21–32",
        "position": "先建立对象—识别—估计—推断的全年阅读框架",
        "objectives": [
            "区分经济问题、总体对象、样本估计量与经验结论",
            "识别横截面、时间序列、面板、聚类与空间数据结构",
            "用可复现性标准检查一份经验分析是否可审计",
        ],
        "prerequisites": [
            "能解释样本均值为什么是总体均值的估计量",
            "知道 i.i.d. 中“独立”和“同分布”分别限制什么",
            "能区分相关关系与因果效应",
        ],
        "bridge": "本科课程通常从 $Y=X\\beta+e$ 开始；Hansen 先把数据看作联合分布 $F$ 的实现，再问我们想学习 $F$ 的哪个函数。回归式是工具，不是研究问题本身。",
        "bridge_prompt": "如果只报告一个显著系数，却说不清目标总体和抽样方式，结论缺了哪一层？",
        "route": [
            "从经济问题写出总体对象",
            "用概率模型连接总体和样本",
            "识别数据结构决定的依赖",
            "把估计和推断放进可复现流程",
        ],
        "concepts": [
            {
                "title": "计量问题的四层对象",
                "body": "**问题：** 工资的教育回报是多少？\n\n- 总体对象：某个 CEF 导数、BLP 系数或因果效应\n- 识别：哪些条件把可观察分布连接到该对象\n- 估计：用样本构造 $\\hat\\theta$\n- 推断：描述 $\\hat\\theta$ 的抽样不确定性",
            },
            {
                "title": "概率总体不是通讯录",
                "body": "总体 $F(y,x)$ 是数据生成分布，不必等于一个有限名单。\n\n$$\n(Y_i,X_i)\\sim F,\n\\qquad i=1,\\ldots,n.\n$$\n\n随机抽样让样本矩可以用概率定律靠近总体矩。",
            },
            {
                "title": "五类数据结构",
                "body": "| 结构 | 主要依赖 |\n|---|---|\n| 横截面 | 个体间通常近似独立 |\n| 时间序列 | 相邻时期相关 |\n| 面板 | 个体内相关 + 时间维 |\n| 聚类 | 簇内任意相关、簇间独立 |\n| 空间 | 依赖随距离或网络变化 |\n\n标准误必须与依赖结构一致。",
            },
            {
                "title": "复现是估计的一部分",
                "body": "可复现实证应保留：原始数据来源、清洗代码、估计代码、软件版本、输出表和设定说明。\n\n::: {.data-status}\n数据不能公开时，代码、变量字典和访问说明仍应公开。\n:::",
            },
        ],
        "derivation": {
            "title": "从总体均值到样本均值",
            "setup": "总体对象为 $\\mu=E[Y_i]$。用矩条件 $E[Y_i-\\mu]=0$ 定义它，样本类比令 $n^{-1}\\sum_i(Y_i-m)=0$。",
            "steps": [
                "解样本矩方程：\n$$\n0=\\frac1n\\sum_{i=1}^n(Y_i-m)\n=\\bar Y-m\n\\quad\\Rightarrow\\quad\n\\hat\\mu=\\bar Y.\n$$",
                "若 $Y_i$ 同分布且 $E|Y_i|<\\infty$，则 WLLN 给出\n$$\n\\bar Y\\xrightarrow{p}E[Y_i]=\\mu.\n$$",
                "若还独立且 $\\operatorname{var}(Y_i)=\\sigma^2<\\infty$，CLT 给出\n$$\n\\sqrt n(\\bar Y-\\mu)\\xrightarrow{d}N(0,\\sigma^2).\n$$",
            ],
            "reasons": ["样本矩的代数求解", "弱大数定律", "中心极限定理"],
            "conclusion": "同一个简单估计量同时展示全年主线：总体矩定义目标，样本矩给估计量，LLN 给一致性，CLT 给推断。",
        },
        "conditions": [
            "$Y_i$ 是标量；样本均值也是标量",
            "一致性至少需要适用的 LLN 和 $E|Y_i|<\\infty$",
            "普通 i.i.d. CLT 需要有限方差；依赖数据要换相应 CLT",
            "若样本选择机制改变分布，$\\bar Y$ 估计的是被选择总体的均值",
        ],
        "example": {
            "title": "例：工资样本中的目标总体",
            "body": "若数据只保留“全职、正工资、非军人”，样本平均工资估计的是该子总体均值。它不能自动外推到失业者、兼职者或全体劳动年龄人口。样本筛选不是清洗细节，而是目标总体定义。",
        },
        "misconception": "“i.i.d. 意味着 $Y_i$ 与 $X_i$ 独立。”错。i.i.d. 限制的是不同观测 $i$ 与 $j$ 之间；同一观测内 $Y_i$ 与 $X_i$ 正是回归要研究的依赖。",
        "check": {
            "question": "学校按班级抽取 30 个班，再调查每班所有学生。能否把 900 名学生当作 i.i.d. 个体并使用普通稳健标准误？写出理由。",
            "answer": "不能。抽样单位是班级，同班学生共享教师和同伴冲击；合理起点是把班级视为近似独立簇，并按班聚类。有效独立信息更接近 30 个簇，而不是 900 个学生。",
            "diagnosis": "若答案只说“样本量大所以可以”，回到数据结构页；若只说“用稳健标准误”，回到聚类与异方差的区别",
        },
        "takeaways": [
            "研究问题必须先翻译成总体对象和识别条件",
            "数据结构决定可用的概率定律和标准误",
            "复现记录属于估计过程，不是论文完成后的附属品",
        ],
        "practice": "写出一个经验问题的目标总体、数据结构和最危险的选择机制",
        "extensions": [
            "Hansen §1.6–1.8：软件、复现和教材数据",
            "比较设计型推断与模型型推断对“随机性”的不同来源",
            "为自己的研究目录写一个最小复现 README",
        ],
        "links": [],
    },
    {
        "number": 2,
        "semester": 1,
        "title": "矩阵代数 I",
        "subtitle": "维数、秩、逆与线性方程",
        "chapters": "Appendix A",
        "book_pages": "945–965（选讲）",
        "pdf_pages": "965–985",
        "position": "为 OLS、IV 和 GMM 建立不会跳步的维数与秩语言",
        "objectives": [
            "对计量公式逐项标注维数并识别不合法乘法",
            "用列空间和秩解释多重共线与识别",
            "证明满列秩时 $X'X$ 正定可逆",
        ],
        "prerequisites": [
            "能做基本矩阵乘法和转置",
            "知道线性组合与线性无关",
            "能解释方程个数不等于独立方程个数",
        ],
        "bridge": "本科常把 $(X'X)^{-1}$ 当作可直接按计算器的部件；Hansen 要求先说明它为什么存在。可逆性是秩与识别问题，不是排版习惯。",
        "bridge_prompt": "为什么 $n>k$ 仍不足以保证 OLS 唯一？",
        "route": ["统一列向量约定", "从列空间定义秩", "把秩连接到正定与逆", "用维数预演 IV 识别"],
        "concepts": [
            {
                "title": "统一列向量约定",
                "body": "$X_i\\in\\mathbb R^k$ 是 $k\\times1$，设计矩阵 $X\\in\\mathbb R^{n\\times k}$ 的第 $i$ 行是 $X_i'$。\n\n$$\nX'X:k\\times k,\\quad X'Y:k\\times1,\\quad \\hat\\beta:k\\times1.\n$$",
            },
            {
                "title": "列空间就是可拟合方向",
                "body": "$\\mathcal C(X)=\\{Xb:b\\in\\mathbb R^k\\}$。所有线性拟合值都在这个子空间中。若某列能由其他列线性组合，它没有提供新方向。",
            },
            {
                "title": "秩不是列数",
                "body": "$\\operatorname{rank}(X)$ 是线性无关列的最大数目。含常数、所有类别虚拟变量且再含总和约束时，会出现“虚拟变量陷阱”：列数增加但秩不增加。",
            },
            {
                "title": "线性方程与唯一解",
                "body": "$Ab=c$ 有唯一解需要方阵 $A$ 非奇异。若 $A=X'X$ 奇异，正规方程可能有多个系数解；拟合值有时仍唯一，但单个系数不被样本区分。",
            },
        ],
        "derivation": {
            "title": "满列秩推出 $X'X$ 正定",
            "setup": "已知 $X$ 为 $n\\times k$ 且 $\\operatorname{rank}(X)=k$。目标：对任意 $a\\ne0$ 证明 $a'X'Xa>0$。",
            "steps": [
                "利用结合律改写：\n$$\na'X'Xa=(Xa)'(Xa).\n$$",
                "向量内积等于平方范数：\n$$\n(Xa)'(Xa)=\\|Xa\\|^2\\ge0.\n$$",
                "满列秩意味着零空间只有 $0$；故 $a\\ne0\\Rightarrow Xa\\ne0\\Rightarrow\\|Xa\\|^2>0$。",
            ],
            "reasons": ["矩阵乘法结合律", "欧氏范数定义", "满列秩与零空间"],
            "conclusion": "$X'X>0$，所以非奇异并存在逆。OLS 唯一性来自回归元方向可区分，而不是样本量数字本身。",
        },
        "conditions": [
            "$X:n\\times k$，必须有 $n\\ge k$ 才可能满列秩",
            "满列秩是样本条件；总体识别常要求 $E[XX']>0$",
            "近共线不使矩阵精确奇异，但会使最小特征值很小、方差变大",
            "求逆次序：$(AB)^{-1}=B^{-1}A^{-1}$",
        ],
        "example": {
            "title": "例：虚拟变量陷阱",
            "body": "若样本只有东、中、西三地区，同时放入常数和三个地区虚拟变量，则\n$$\n1=D_E+D_C+D_W.\n$$\n四列存在精确关系。删除一个地区虚拟变量后，剩余系数解释为相对基准地区差异。",
        },
        "misconception": "“软件自动删除了一列，所以共线性问题已经解决。”软件只选择了一个参数化；研究者仍要说明基准组、系数解释和是否存在近共线导致的不精确。",
        "check": {
            "question": "若 $X:n\\times k$、$Z:n\\times m$，写出 $Z'X$、$(Z'Z)^{-1}Z'X$ 与 $X'P_ZX$ 的维数，并说明识别 $k$ 个系数至少需要什么秩。",
            "answer": "$Z'X:m\\times k$；$(Z'Z)^{-1}Z'X:m\\times k$；$X'P_ZX:k\\times k$。至少要求 $\\operatorname{rank}E[ZX']=k$，因而工具维数 $m\\ge k$。",
            "diagnosis": "若把 $X_i$ 当行向量导致维数相反，回到列向量约定；若只回答 $m\\ge k$，回到“数量不等于秩”",
        },
        "takeaways": ["维数检查先于代数操作", "秩描述独立方向，决定唯一性与识别", "近奇异会放大不确定性，即使软件仍能求逆"],
        "practice": "补充讲义 1 的自检题 1–3",
        "extensions": ["Schur complement 与分块逆", "特征值、条件数与数值稳定性", "广义逆在欠识别参数化中的作用"],
        "links": [],
    },
    {
        "number": 3,
        "semester": 1,
        "title": "矩阵代数 II",
        "subtitle": "投影、零化矩阵、二次型与矩阵微分",
        "chapters": "Appendix A；Ch.3 预备",
        "book_pages": "62–84；945–965（选讲）",
        "pdf_pages": "82–104；965–985",
        "position": "把 OLS 从公式变成正交投影，为 FWL 和固定效应去均值铺路",
        "objectives": ["证明 $P_X$ 与 $M_X$ 的关键性质", "用投影视角解释残差正交和自由度", "从二次型梯度推出正规方程"],
        "prerequisites": ["会标注 $X(X'X)^{-1}X'$ 的维数", "知道对称与幂等的定义", "能展开 $(Y-Xb)'(Y-Xb)$"],
        "bridge": "本科“最小化残差平方和”与“拟合值是投影”是同一个问题的代数和几何表述。几何语言会让 FWL、固定效应和 2SLS 变成同一类投影。",
        "bridge_prompt": "为什么残差与解释变量正交，却不意味着误差与解释变量总体外生？",
        "route": ["构造投影矩阵", "证明对称与幂等", "定义零化矩阵", "从二次型梯度连接正规方程"],
        "concepts": [
            {"title": "投影矩阵", "body": "$$P_X=X(X'X)^{-1}X'.$$\n\n$P_XY$ 把任意 $Y\\in\\mathbb R^n$ 映射到 $\\mathcal C(X)$。若 $v=Xa$ 已在列空间，$P_Xv=v$。"},
            {"title": "零化矩阵", "body": "$$M_X=I_n-P_X.$$\n\n它保留与 $\\mathcal C(X)$ 正交的成分并消灭 $X$：$M_XX=0$。OLS 残差为 $\\hat e=M_XY$。"},
            {"title": "迹与自由度", "body": "对称幂等矩阵的特征值只有 0/1，故\n$$\n\\operatorname{tr}(P_X)=\\operatorname{rank}(P_X)=k,\n\\quad \\operatorname{tr}(M_X)=n-k.\n$$\n这解释了残差方差分母 $n-k$。"},
            {"title": "矩阵微分的最低工具", "body": "若 $A=A'$，则\n$$\n\\frac{\\partial(b'Ab)}{\\partial b}=2Ab.\n$$\n把残差平方和展开成二次型，可直接得到 OLS 一阶条件。"},
        ],
        "derivation": {
            "title": "$P_X$ 对称且幂等",
            "setup": "假设 $X$ 满列秩，定义 $P_X=X(X'X)^{-1}X'$。目标：证明它是正交投影。",
            "steps": [
                "转置并倒序：\n$$\nP_X'=X\\{(X'X)^{-1}\\}'X'=P_X,\n$$\n因为 $X'X$ 及其逆对称。",
                "平方并在中间配出 $X'X$：\n$$\nP_X^2=X(X'X)^{-1}(X'X)(X'X)^{-1}X'.\n$$",
                "相邻的逆抵消，得到 $P_X^2=P_X$；对称保证投影方向与残差方向正交。",
            ],
            "reasons": ["转置与对称逆", "矩阵结合律", "幂等与正交投影刻画"],
            "conclusion": "$P_X$ 将样本向量投到 $X$ 的列空间；$M_X=I-P_X$ 投到正交补。$P_XM_X=0$。",
        },
        "conditions": ["$P_X,M_X:n\\times n$", "$X'X$ 需可逆", "幂等不自动意味着对称；正交投影需要二者", "$P_X$ 是样本算子，不是总体外生假设"],
        "example": {
            "title": "例：只含常数项就是去均值",
            "body": "令 $X=1_n$，则\n$$\nP_1=\\frac1n1_n1_n',\\qquad M_1=I_n-\\frac1n1_n1_n'.\n$$\n因此 $P_1Y=\\bar Y1_n$，$M_1Y=Y-\\bar Y1_n$。固定效应 within 变换就是分组版零化。",
        },
        "misconception": "“$X'\\hat e=0$ 证明 $E[Xe]=0$。”错。前者由样本最小化机械成立，即使模型内生也成立；后者是总体矩条件，需要经济和抽样假设。",
        "check": {
            "question": "证明 $M_X$ 对称、幂等，并计算 $P_XM_X$。然后解释为什么对残差再对 $X$ 回归得到全零拟合值。",
            "answer": "$M_X'=I-P_X'=M_X$；$M_X^2=I-2P_X+P_X^2=I-P_X=M_X$；$P_XM_X=P_X-P_X^2=0$。残差位于 $X$ 列空间的正交补，投回 $\\mathcal C(X)$ 为零。",
            "diagnosis": "若只做代数但解释不出几何意义，回到投影/零化定义；若把残差与误差混淆，回到样本与总体层次",
        },
        "takeaways": ["$P_X$ 保留列空间，$M_X$ 消灭列空间", "正规方程是样本正交", "迹把投影秩连接到自由度"],
        "practice": "补充讲义 1 的 FWL 推导和 Ch.3 相关习题",
        "extensions": ["FWL 的分块正规方程证明", "杠杆值 $h_{ii}$ 与留一预测", "Kronecker 积在 SUR/VAR 中的使用"],
        "links": [
            ("Ch.3 习题解答", "docs/ch03/Hansen_Ch03_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch03/Hansen_Ch03_Exercises_Solutions.md")
        ],
    },
    {
        "number": 4,
        "semester": 1,
        "title": "概率与条件化",
        "subtitle": "条件期望、LIE、总方差与概率不等式",
        "chapters": "Ch.2 前半；Appendix B",
        "book_pages": "14–30；966–985（选讲）",
        "pdf_pages": "34–50；986–1005",
        "position": "建立后续所有外生性、投影和大样本证明使用的条件期望语言",
        "objectives": ["从条件分布定义 CEF", "熟练使用迭代期望和条件中提出函数", "推导总方差分解并理解预测含义"],
        "prerequisites": ["知道联合、边际和条件概率", "会展开方差", "理解函数 $h(X)$ 在给定 $X$ 时已知"],
        "bridge": "本科把 $E(e\\mid X)=0$ 列为回归假设；Hansen 先说明若误差定义为 $Y-E[Y\\mid X]$，零条件均值是定义推论，再比较它与线性投影正交的强弱。",
        "bridge_prompt": "$E[e]=0$ 为什么远弱于 $E[e\\mid X]=0$？",
        "route": ["从条件分布到 CEF", "定义 CEF 误差", "用 LIE 推正交", "用正交分解预测误差"],
        "concepts": [
            {"title": "条件期望是随机函数", "body": "$m(x)=E[Y\\mid X=x]$ 是 $x$ 的函数；代回随机变量得到 $m(X)=E[Y\\mid X]$。它不是一个固定数字。"},
            {"title": "条件中可提出什么", "body": "对只依赖 $X$ 的 $h$，\n$$\nE[h(X)Y\\mid X]=h(X)E[Y\\mid X].\n$$\n不能把仍有额外随机性的 $Y$ 提出去。"},
            {"title": "迭代期望", "body": "$$E\\{E[Y\\mid X]\\}=E[Y].$$\n若信息集嵌套，较小信息集“赢”：$E\\{E[Y\\mid X,Z]\\mid X\\}=E[Y\\mid X]$。"},
            {"title": "总方差分解", "body": "$$\n\\operatorname{var}(Y)=E\\{\\operatorname{var}(Y\\mid X)\\}+\\operatorname{var}\\{E[Y\\mid X]\\}.\n$$\n总波动 = 条件内不可预测波动 + 条件均值的可预测波动。"},
        ],
        "derivation": {
            "title": "零条件均值推出任意函数正交",
            "setup": "令 $e=Y-E[Y\\mid X]$，所以 $E[e\\mid X]=0$。目标：对可积 $h(X)$ 证明 $E[h(X)e]=0$。",
            "steps": [
                "先用无条件迭代期望：\n$$\nE[h(X)e]=E\\{E[h(X)e\\mid X]\\}.\n$$",
                "给定 $X$ 后 $h(X)$ 已知，可提出：\n$$\nE[h(X)e\\mid X]=h(X)E[e\\mid X].\n$$",
                "代入 $E[e\\mid X]=0$：\n$$\nE\\{h(X)E[e\\mid X]\\}=E[h(X)\\cdot0]=0.\n$$",
            ],
            "reasons": ["迭代期望", "条件期望可测函数性质", "CEF 误差定义"],
            "conclusion": "CEF 误差与 $X$ 的所有可积函数正交；只知道 $E[Xe]=0$ 不能反推出零条件均值。",
        },
        "conditions": ["$h(X)e$ 可积", "信息集必须正确嵌套才能用 LIE", "条件期望等式几乎处处成立", "正交不等于独立"],
        "example": {
            "title": "反例：不相关但完全依赖",
            "body": "令 $X$ 关于 0 对称、$Y=X^2$。则 $E[XY]=E[X^3]=0$，但 $Y$ 完全由 $X$ 决定。线性不相关没有排除非线性依赖。",
        },
        "misconception": "“若 $E[Xe]=0$，则 $E[X^2e]=0$。”一般错误。前者只给一个矩条件；后者需要更强条件，例如 $E[e\\mid X]=0$。",
        "check": {
            "question": "已知 $E[Y\\mid X]=1+2X$。用 $X$ 的矩表示 $E[XY]$，并说明每一步使用的规则。",
            "answer": "$E[XY]=E\\{E[XY\\mid X]\\}=E\\{XE[Y\\mid X]\\}=E[X(1+2X)]=E[X]+2E[X^2]$。依次使用 LIE、给定 $X$ 提出 $X$、代入 CEF。",
            "diagnosis": "若直接把 $E[XY]$ 写成 $E[X]E[Y]$，混淆了独立；若少写外层期望，混淆条件对象与标量",
        },
        "takeaways": ["CEF 是条件分布的一阶矩", "LIE 是从条件结论回到总体矩的桥", "零条件均值比线性正交强"],
        "practice": "Ch.2 习题 2.1–2.4、2.10–2.14",
        "extensions": ["Jensen、Cauchy–Schwarz 与 Chebyshev", "条件期望作为 $L^2$ 投影", "均值独立与条件异方差并存"],
        "links": [
            ("Ch.2 习题解答", "docs/ch02/Hansen_Ch02_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch02/Hansen_Ch02_Exercises_Solutions.md")
        ],
    },
    {
        "number": 5,
        "semester": 1,
        "title": "CEF 与线性投影",
        "subtitle": "最佳预测、BLP、遗漏变量与因果解释",
        "chapters": "Ch.2",
        "book_pages": "14–61",
        "pdf_pages": "34–81",
        "position": "明确 OLS 将来要估计的总体靶心，并区分预测参数与因果参数",
        "objectives": ["证明 CEF 的最佳均方预测性质", "推导 BLP 系数和投影正交", "区分线性投影、结构效应与因果效应"],
        "prerequisites": ["能使用 LIE", "知道正定矩阵与一阶条件", "能区分 $E[e\\mid X]=0$ 和 $E[Xe]=0$"],
        "bridge": "本科回归常把线性 CEF 当作默认；Hansen 允许 CEF 非线性，把 BLP 定义为最佳线性近似。OLS 一致估计 BLP，并不自动证明真实 CEF 线性。",
        "bridge_prompt": "若 CEF 是弯曲的，OLS 系数是否仍有明确总体含义？",
        "route": ["CEF 的最优预测", "限制到线性候选集", "推导 BLP", "检查遗漏变量与因果解释"],
        "concepts": [
            {"title": "CEF 的正交分解", "body": "对任意 $g(X)$，\n$$\nY-g(X)=\\{Y-m(X)\\}+\\{m(X)-g(X)\\}.\n$$\n两部分正交，所以均方误差可加。"},
            {"title": "最佳线性预测", "body": "$P(Y\\mid X)=X'\\beta$ 只在所有线性函数中最小化 $E[(Y-X'b)^2]$。若 $X$ 含非线性基函数，线性是对参数线性，不必对原变量线性。"},
            {"title": "遗漏变量系数分解", "body": "若真 BLP 含 $X_1,X_2$，只回归 $X_1$，短回归系数把 $X_2$ 对 $X_1$ 的投影效应带入。偏误方向 = 相关方向 × 遗漏变量作用方向。"},
            {"title": "预测与因果不是同义词", "body": "$E[Y\\mid X=x]$ 描述观察分布；因果效应比较潜在结果 $Y(x)$。需要可忽略性等桥梁条件才可令 $E[Y(x)]=E[Y\\mid X=x]$。"},
        ],
        "derivation": {
            "title": "BLP 系数公式",
            "setup": "定义 $\\beta=\\arg\\min_b E[(Y-X'b)^2]$，假设 $Q=E[XX']>0$。目标：求显式解。",
            "steps": [
                "展开目标：\n$$\nE[Y^2]-2b'E[XY]+b'E[XX']b.\n$$",
                "对 $b$ 求导并令零：\n$$\n-2E[XY]+2E[XX']b=0.\n$$",
                "由 $Q$ 可逆：\n$$\n\\beta=E[XX']^{-1}E[XY],\n$$\n并得到 $E[X(Y-X'\\beta)]=0$。",
            ],
            "reasons": ["二次型展开", "总体一阶条件", "正定与可逆"],
            "conclusion": "BLP 系数是总体二阶矩的函数；投影误差与 $X$ 线性正交，但未必满足零条件均值。",
        },
        "conditions": ["$X:k\\times1$ 且通常含常数", "$E[Y^2]$、$E[\\|X\\|^2]$ 有限", "$E[XX']>0$ 保证唯一", "因果解释需要超出投影的一组识别假设"],
        "example": {
            "title": "例：非线性 CEF 的线性斜率",
            "body": "若 $Y=X^2+e$、$E[e\\mid X]=0$，只用常数和 $X$ 回归时，斜率由 $X$ 的分布决定。若 $X$ 对称，$\\operatorname{cov}(X,X^2)=0$，BLP 斜率为零，但 CEF 显然强烈依赖 $X$。",
        },
        "misconception": "“OLS 斜率为零，所以 $X$ 对 $Y$ 没有预测力。”错。它只排除最佳线性预测中的斜率；非线性 CEF 仍可能变化。",
        "check": {
            "question": "若 $Y=X^2$ 且 $X\\sim U[-1,1]$，含常数的 BLP 斜率是多少？截距是多少？",
            "answer": "$\\beta_1=\\operatorname{cov}(X,X^2)/\\operatorname{var}(X)=E[X^3]/E[X^2]=0$；$\\beta_0=E[Y]-\\beta_1E[X]=E[X^2]=1/3$。BLP 是水平线 $1/3$。",
            "diagnosis": "若把 BLP 写成 $X^2$，混淆候选函数集；若截距写 0，忘记含常数正交条件",
        },
        "takeaways": ["CEF 在所有函数中最佳，BLP 在线性函数中最佳", "BLP 始终有总体含义但依赖 $X$ 分布", "因果解释必须额外陈述潜在结果识别条件"],
        "practice": "Ch.2 习题 2.15–2.24 及因果效应相关题",
        "extensions": ["随机系数与 BLP 加权平均", "reverse regression 与 regression to the mean", "最佳线性近似的分布权重"],
        "links": [
            ("Ch.2 习题解答", "docs/ch02/Hansen_Ch02_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch02/Hansen_Ch02_Exercises_Solutions.md")
        ],
    },
    {
        "number": 6,
        "semester": 1,
        "title": "最小二乘代数",
        "subtitle": "正规方程、投影矩阵、FWL 与杠杆值",
        "chapters": "Ch.3",
        "book_pages": "62–96",
        "pdf_pages": "82–116",
        "position": "把总体 BLP 转为样本估计，并掌握后续所有线性模型共享的投影代数",
        "objectives": ["从样本准则推导 OLS", "用 $P_X/M_X$ 表示拟合值和残差", "完整推导 FWL 并解释控制变量"],
        "prerequisites": ["理解 BLP 总体一阶条件", "会证明投影矩阵性质", "能对分块矩阵写正规方程"],
        "bridge": "第 2 章的 $E[XX']^{-1}E[XY]$ 是总体靶心；第 3 章把期望换成样本均值，得到 $(X'X)^{-1}X'Y$。这一章是纯样本代数，还没有外生性和抽样分布。",
        "bridge_prompt": "为什么 OLS 正规方程成立不能证明估计量无偏？",
        "route": ["最小化残差平方和", "写成投影算子", "分解回归平方和", "用 FWL 隔离目标系数"],
        "concepts": [
            {"title": "OLS 样本准则", "body": "$$S_n(b)=(Y-Xb)'(Y-Xb)=\\sum_i(Y_i-X_i'b)^2.$$\n\n它是观测数据的函数；最小化得到估计量，不需要先假设误差正态。"},
            {"title": "拟合值与残差", "body": "$$\\hat Y=P_XY,\\qquad \\hat e=M_XY.$$\n\n$Y=\\hat Y+\\hat e$ 是正交分解，故 $Y'Y=\\hat Y'\\hat Y+\\hat e'\\hat e$（含适当中心化时对应 ANOVA）。"},
            {"title": "杠杆值", "body": "$h_{ii}$ 是 $P_X$ 第 $i$ 个对角元，衡量第 $i$ 个观测的回归元位置有多异常。$0\\le h_{ii}\\le1$ 且 $\\sum_i h_{ii}=k$。"},
            {"title": "留一法的代数", "body": "留一残差满足\n$$\nY_i-X_i'\\hat\\beta_{(-i)}=\\frac{\\hat e_i}{1-h_{ii}}.\n$$\n高杠杆使样本内残差看似小，却可能有大留一预测误差。"},
        ],
        "derivation": {
            "title": "FWL 定理",
            "setup": "令 $X=[X_1\\ X_2]$，目标是在控制 $X_1$ 后求 $X_2$ 系数。正规方程为 $X'(Y-X_1\\hat\\beta_1-X_2\\hat\\beta_2)=0$。",
            "steps": [
                "由第一组正规方程解出\n$$\n\\hat\\beta_1=(X_1'X_1)^{-1}X_1'(Y-X_2\\hat\\beta_2).\n$$",
                "代入第二组正规方程，收集 $I-P_{X_1}=M_{X_1}$：\n$$\nX_2'M_{X_1}(Y-X_2\\hat\\beta_2)=0.\n$$",
                "解得\n$$\n\\hat\\beta_2=(X_2'M_{X_1}X_2)^{-1}X_2'M_{X_1}Y.\n$$",
            ],
            "reasons": ["分块正规方程", "投影/零化定义", "残差化回归的一阶条件"],
            "conclusion": "控制 $X_1$ 等于先从 $Y$ 和 $X_2$ 同时剔除 $X_1$ 的线性部分，再将两份残差回归。",
        },
        "conditions": ["$X:n\\times k$ 满列秩", "$X_1$ 与残差化后的 $X_2$ 维数匹配", "FWL 是代数恒等式，不依赖随机抽样", "系数因果解释仍需总体外生/识别条件"],
        "example": {
            "title": "例：含常数的简单回归",
            "body": "令 $X_1=1_n$、$X_2=x$。则 $M_1x=x-\\bar x1_n$、$M_1Y=Y-\\bar Y1_n$，所以\n$$\n\\hat\\beta_1=\\frac{\\sum_i(x_i-\\bar x)(Y_i-\\bar Y)}{\\sum_i(x_i-\\bar x)^2}.\n$$",
        },
        "misconception": "“加入控制变量后目标系数变化，说明原回归有偏。”系数变化是样本投影事实；要称为遗漏变量偏误，还需指定总体目标并说明新增变量应进入该目标模型。",
        "check": {
            "question": "在 $Y$ 对常数、教育和经验的回归中，如何只用三个辅助回归得到教育系数？写清每一步。",
            "answer": "先将 $Y$ 对常数和经验回归取残差 $\\tilde Y$；再将教育对常数和经验回归取残差 $\\widetilde{educ}$；最后将 $\\tilde Y$ 对 $\\widetilde{educ}$（无须再加常数）回归，斜率等于完整回归教育系数。",
            "diagnosis": "若只残差化 $Y$ 而不残差化教育，回到 FWL 对称残差化；若把辅助残差当结构误差，回到样本投影层次",
        },
        "takeaways": ["OLS 是样本二次准则的解", "$P_X/M_X$ 统一拟合、残差与自由度", "FWL 把“控制不变”变成可计算的残差化"],
        "practice": "Ch.3 的投影、FWL、杠杆和数值计算题",
        "extensions": ["加权最小二乘的投影几何", "稀疏虚拟变量的吸收算法", "留一交叉验证与影响诊断"],
        "links": [
            ("Ch.3 习题解答", "docs/ch03/Hansen_Ch03_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch03/Hansen_Ch03_Exercises_Solutions.md")
        ],
    },
]


MAIN_SESSIONS += [
    {
        "number": 8,
        "semester": 1,
        "title": "OLS 有限样本理论",
        "subtitle": "无偏性、条件方差、Gauss–Markov 与 GLS",
        "chapters": "Ch.4 前半",
        "book_pages": "97–109",
        "pdf_pages": "117–129",
        "position": "在纯代数 OLS 上加入随机抽样与外生性，第一次得到统计性质",
        "objectives": ["逐步证明 OLS 条件无偏", "推导异方差下条件方差", "准确陈述经典与现代 Gauss–Markov 比较类"],
        "prerequisites": ["能写 $\\hat\\beta-\\beta=(X'X)^{-1}X'e$", "能区分样本残差与总体误差", "知道条件期望中 $X$ 可视为已知"],
        "bridge": "第 3 章只说明 OLS 怎样计算；第 4 章开始回答它在重复抽样中怎样变化。无偏性来自外生条件，不来自正规方程。",
        "bridge_prompt": "若 $X'\\hat e=0$ 对任何数据都成立，为什么内生性仍会造成偏误？",
        "route": ["写出线性投影模型", "从误差分解求条件均值", "推导条件方差", "限定比较类后陈述 Gauss–Markov"],
        "concepts": [
            {"title": "随机设计线性模型", "body": "$$Y=X\\beta+e,\\qquad E[e\\mid X]=0.$$\n\n$X$ 可以随机；条件在整个设计矩阵上求期望。若只需要线性投影参数，一些结果可在更弱矩条件下成立。"},
            {"title": "估计误差分解", "body": "$$\\hat\\beta-\\beta=(X'X)^{-1}X'e.$$\n\n左侧是 $k\\times1$；给定 $X$ 后，随机性只来自 $e$。所有有限样本矩都从这条恒等式开始。"},
            {"title": "异方差条件方差", "body": "令 $\\Sigma=\\operatorname{var}(e\\mid X)$，则\n$$\n\\operatorname{var}(\\hat\\beta\\mid X)=(X'X)^{-1}X'\\Sigma X(X'X)^{-1}.\n$$"},
            {"title": "Gauss–Markov 比较什么", "body": "在同方差、零条件均值下，OLS 在**线性且条件无偏**估计量中方差最小。它没有说 OLS 比所有非线性、有偏或正则化估计量都好。"},
        ],
        "derivation": {
            "title": "OLS 条件无偏",
            "setup": "已知 $Y=X\\beta+e$、$E[e\\mid X]=0$ 且 $X'X$ 可逆。目标：求 $E[\\hat\\beta\\mid X]$。",
            "steps": [
                "代入模型：\n$$\n\\hat\\beta=(X'X)^{-1}X'(X\\beta+e)=\\beta+(X'X)^{-1}X'e.\n$$",
                "给定 $X$ 后矩阵项可提出：\n$$\nE[\\hat\\beta-\\beta\\mid X]=(X'X)^{-1}X'E[e\\mid X].\n$$",
                "使用零条件均值，右侧为零，所以 $E[\\hat\\beta\\mid X]=\\beta$；再用 LIE 得无条件无偏。",
            ],
            "reasons": ["OLS 代数恒等式", "条件期望可测函数性质", "零条件均值与 LIE"],
            "conclusion": "无偏性的关键箭头是 $E[e\\mid X]=0$；若该条件失败，样本正规方程不能补救。",
        },
        "conditions": ["$X:n\\times k$ 满列秩", "$E[e\\mid X]=0$ 比 $E[Xe]=0$ 强", "$\\Sigma:n\\times n$；随机抽样异方差时通常对角", "BLUE 结论必须写出估计量比较类"],
        "example": {"title": "例：异方差如何进入方差", "body": "若独立观测但 $\\operatorname{var}(e_i\\mid X_i)=\\sigma_i^2$，则 $\\Sigma=\\operatorname{diag}(\\sigma_1^2,\\ldots,\\sigma_n^2)$。高方差观测按 $X_iX_i'$ 方向更多地贡献不确定性。"},
        "misconception": "“Gauss–Markov 证明同方差 OLS 永远最优。”错。结论限定在线性、无偏估计量类；若允许小偏差换大方差下降，Ridge 等估计量可有更小均方误差。",
        "check": {
            "question": "若 $E[e\\mid X]\\ne0$，但样本 OLS 仍满足 $X'\\hat e=0$，哪一步无偏性证明失败？",
            "answer": "失败在 $E[\\hat\\beta-\\beta\\mid X]=(X'X)^{-1}X'E[e\\mid X]=0$。样本残差正交只描述最小化结果，不能令结构误差的条件均值为零。",
            "diagnosis": "若回答“正规方程失败”，混淆样本残差与总体误差；若只说“内生”，要求指出具体条件期望步骤",
        },
        "takeaways": ["统计性质从估计误差分解开始", "外生性给中心，误差方差结构给波动", "效率结论永远要注明比较类"],
        "practice": "Ch.4 无偏、方差与 Gauss–Markov 习题",
        "extensions": ["GLS 的变换模型推导", "条件与无条件方差的关系", "现代 Gauss–Markov 的线性投影表述"],
        "links": [("Ch.4 习题解答", "docs/ch04/Hansen_Ch04_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch04/Hansen_Ch04_Exercises_Solutions.md")],
    },
    {
        "number": 9,
        "semester": 1,
        "title": "稳健与聚类标准误",
        "subtitle": "夹心方差、簇得分与聚类层级",
        "chapters": "Ch.4 后半",
        "book_pages": "110–136",
        "pdf_pages": "130–156",
        "position": "把标准误从软件选项变成抽样结构的结果",
        "objectives": ["从得分和推导异方差稳健方差", "把个体得分替换为簇得分得到 cluster 方差", "根据抽样和处理分配选择聚类层级"],
        "prerequisites": ["会写 OLS 夹心方差", "理解独立观测与簇间独立的区别", "知道残差是误差的样本替代"],
        "bridge": "本科“异方差稳健”常是一个命令选项；Hansen 从 $X_ie_i$ 的方差构造夹心。聚类并非另一种异方差修正，而是重新定义独立求和单位。",
        "bridge_prompt": "为什么同班学生的观测数很多，仍不能替代班级簇数？",
        "route": ["识别随机得分", "估计异方差肉矩阵", "聚合簇得分", "用设计机制决定层级"],
        "concepts": [
            {"title": "异方差夹心", "body": "$$\\widehat V_{HC}=(X'X)^{-1}\\left(\\sum_iX_iX_i'\\hat e_i^2\\right)(X'X)^{-1}.$$\n\n两片面包来自回归元曲率，肉来自得分波动。"},
            {"title": "HC0、HC1 与杠杆修正", "body": "HC1 用 $n/(n-k)$ 修正自由度；HC2/HC3 再用 $1-h_{ii}$ 修正高杠杆残差下缩。小样本差异可能明显。"},
            {"title": "簇得分", "body": "对簇 $g$ 定义\n$$\ns_g=\\sum_{i\\in g}X_i e_i.\n$$\n若簇间独立，CLT 作用于 $\\{s_g\\}_{g=1}^G$，不是簇内每个观测。"},
            {"title": "聚类层级来自设计", "body": "处理在学校层分配、冲击在学校内共享，就按学校聚类。不能先尝试学生/班级/学校三种 SE，再挑显著的层级。"},
        ],
        "derivation": {
            "title": "从个体稳健到簇稳健",
            "setup": "OLS 估计误差近似由 $\\sum_iX_ie_i$ 驱动。把观测划为 $G$ 个互相独立的簇。",
            "steps": [
                "按簇重排总得分：\n$$\n\\sum_{i=1}^nX_ie_i=\\sum_{g=1}^G\\underbrace{\\sum_{i\\in g}X_ie_i}_{s_g}.\n$$",
                "簇内任意协方差都包含在 $E[s_gs_g']$ 中；簇间独立使交叉项为零。",
                "用残差簇得分 $\\hat s_g=\\sum_{i\\in g}X_i\\hat e_i$ 替代，得到\n$$\n\\widehat V_{cl}=(X'X)^{-1}\\left(\\sum_g\\hat s_g\\hat s_g'\\right)(X'X)^{-1}.\n$$",
            ],
            "reasons": ["求和重排", "簇间独立的方差可加", "样本类比与残差替代"],
            "conclusion": "聚类稳健的有效样本规模由独立簇数 $G$ 主导；簇内增加观测不能无限改善簇级冲击的估计。",
        },
        "conditions": ["簇间近似独立，簇内允许异方差和相关", "渐近通常要求 $G\\to\\infty$", "肉矩阵 $k\\times k$", "少簇时需小样本修正或替代推断"],
        "example": {"title": "例：班级随机试验", "body": "若 30 个班随机分配教学法，每班 30 人，处理变量在班内恒定。普通 HC 把 900 人视为独立，会忽略共享教师冲击；按班聚类承认只有 30 个独立分配单位。"},
        "misconception": "“聚类标准误一定比 HC 大。”不一定。协方差方向、簇内相关符号和小样本修正都会影响大小；选择 cluster 的理由是依赖结构，不是它更保守。",
        "check": {
            "question": "政策在省级实施，数据是省内企业年度面板。至少应在哪一级聚类？为什么按企业聚类通常不足？",
            "answer": "至少按省聚类，因为处理和共同政策冲击在省级变化；按企业聚类仍把同省企业当作跨企业独立，忽略省级共同误差与处理分配相关。",
            "diagnosis": "若按企业聚类因为观测单位是企业，回到“聚类层级由依赖/分配决定”；若说双向聚类但不说明第二维，要求写出依赖来源",
        },
        "takeaways": ["夹心肉矩阵对应随机得分的协方差", "cluster 把独立单位从观测改为簇", "标准误选择必须先于显著性结果"],
        "practice": "Ch.4 聚类抽样与聚类推断题",
        "extensions": ["少簇的 wild cluster bootstrap", "双向聚类", "设计型随机化推断"],
        "links": [("Ch.4 习题解答", "docs/ch04/Hansen_Ch04_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch04/Hansen_Ch04_Exercises_Solutions.md")],
    },
    {
        "number": 10,
        "semester": 1,
        "title": "正态回归与渐近过渡",
        "subtitle": "精确 $t/F$ 分布从哪里来，又为何需要大样本理论",
        "chapters": "Ch.5；Ch.6 导入",
        "book_pages": "137–161",
        "pdf_pages": "157–181",
        "position": "把本科熟悉的 $t/F$ 检验拆成精确假设，再引出渐近替代",
        "objectives": ["推导正态回归下 $\\hat\\beta$ 与 $s^2$ 的精确分布", "说明分子分母独立为何关键", "区分精确 $t$ 与渐近正态临界值"],
        "prerequisites": ["知道正态线性变换仍正态", "知道幂等二次型与卡方的关系", "能写同方差 OLS 方差"],
        "bridge": "本科直接使用 $t$ 表；Hansen 追问：分子为何正态、分母为何卡方、二者为何独立？撤掉正态后，有限样本 $t$ 不再精确，只能等待 Ch.7 的渐近理论。",
        "bridge_prompt": "稳健标准误对应的统计量在有限样本中为什么通常不服从精确 $t$？",
        "route": ["条件正态得到系数分布", "投影正交得到独立", "残差二次型得到卡方", "撤掉正态进入渐近语言"],
        "concepts": [
            {"title": "正态回归模型", "body": "$$e\\mid X\\sim N(0,\\sigma^2I_n).$$\n\n于是 $\\hat\\beta\\mid X$ 是 $e$ 的线性变换，精确服从 $N(\\beta,\\sigma^2(X'X)^{-1})$。"},
            {"title": "残差平方和的卡方", "body": "$\\hat e=M_Xe$，且 $M_X$ 对称幂等、秩为 $n-k$：\n$$\n\\frac{\\hat e'\\hat e}{\\sigma^2}\\sim\\chi^2_{n-k}.\n$$"},
            {"title": "联合正态下不相关推出独立", "body": "$\\hat\\beta-\\beta$ 依赖 $P_Xe$，残差依赖 $M_Xe$；$P_XM_X=0$ 使二者不相关。联合正态把不相关升级为独立。"},
            {"title": "精确与渐近的价格", "body": "正态 + 同方差购买精确 $t/F$；撤掉正态后，若矩和抽样条件成立，$t$ 统计量只在大样本下近似标准正态。"},
        ],
        "derivation": {
            "title": "单个系数的精确 $t$",
            "setup": "对第 $j$ 个系数，令 $v_j=[(X'X)^{-1}]_{jj}$，$s^2=\\hat e'\\hat e/(n-k)$。",
            "steps": [
                "标准化系数：\n$$\nZ=\\frac{\\hat\\beta_j-\\beta_j}{\\sigma\\sqrt{v_j}}\\sim N(0,1).\n$$",
                "残差方差满足\n$$\nU=\\frac{(n-k)s^2}{\\sigma^2}\\sim\\chi^2_{n-k},\n$$\n且 $Z\\perp U$。",
                "代入未知 $\\sigma$：\n$$\nt=\\frac{\\hat\\beta_j-\\beta_j}{s\\sqrt{v_j}}=\\frac{Z}{\\sqrt{U/(n-k)}}\\sim t_{n-k}.\n$$",
            ],
            "reasons": ["正态线性变换", "幂等二次型与投影独立", "$t$ 分布定义"],
            "conclusion": "精确 $t$ 的每个部件都依赖正态同方差结构；稳健 $t$ 通常依靠渐近标准正态而非这条有限样本推导。",
        },
        "conditions": ["条件正态、同方差、$X$ 满列秩", "$s^2$ 分母为 $n-k$", "联合正态下才可由零协方差推出独立", "大样本稳健推断需要另一套 LLN/CLT 条件"],
        "example": {"title": "例：厚尾误差下的小样本", "body": "若误差来自厚尾分布，OLS 仍可能无偏，但系数和残差方差不再形成精确 $t$。小样本拒绝率可明显偏离 5%；增大样本是否改善取决于有限方差和 CLT。"},
        "misconception": "“只要软件报告 t statistic，就应查 $t_{n-k}$。”统计量名称不决定参考分布；稳健、聚类、弱 IV 和单位根下都要重新说明近似依据。",
        "check": {
            "question": "在正态回归证明中，哪一步使用了“联合正态下不相关即独立”？如果只知道误差不相关但非正态，会怎样？",
            "answer": "用于证明 $\\hat\\beta$ 与 $s^2$ 独立。非正态时 $P_Xe$ 与 $M_Xe$ 零协方差不保证独立，分子/分母之比不再精确服从 $t$。",
            "diagnosis": "若说系数不再无偏，混淆正态与外生性；若只说 CLT，要求指出那是渐近替代而非有限样本结论",
        },
        "takeaways": ["精确分布来自正态投影几何", "无偏不等于有精确 $t$", "Ch.6–7 用大样本概率工具替代强分布假设"],
        "practice": "Ch.5 关于 $\\hat\\beta$、$s^2$、$t/F$ 的证明题",
        "extensions": ["似然比检验与 $F$ 的关系", "正态回归信息界", "非正态下自助法和稳健推断"],
        "links": [("Ch.5 习题解答", "docs/ch05/Hansen_Ch05_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch05/Hansen_Ch05_Exercises_Solutions.md")],
    },
    {
        "number": 11,
        "semester": 1,
        "title": "渐近工具箱",
        "subtitle": "收敛、WLLN、CLT、Slutsky 与 delta method",
        "chapters": "Ch.6",
        "book_pages": "155–161",
        "pdf_pages": "175–181",
        "position": "集中建立 Ch.7 以后每个渐近证明都会重复使用的工具链",
        "objectives": ["区分依概率与依分布收敛", "正确组合 WLLN、CLT、连续映射和 Slutsky", "从 Taylor 展开推导 delta method"],
        "prerequisites": ["会用 Chebyshev 理解样本均值收敛", "知道矩阵逆需要非奇异极限", "能做一阶 Taylor 展开"],
        "bridge": "本科常记“样本大约正态”；研究生计量必须指出哪个和满足哪条 CLT、哪个矩阵由 LLN 收敛、两者如何由 Slutsky 合并。",
        "bridge_prompt": "为什么一致性本身不能给置信区间？",
        "route": ["定义两种收敛", "用 WLLN 控制样本矩", "用 CLT 控制中心化和", "用映射与 Taylor 传递极限"],
        "concepts": [
            {"title": "依概率收敛", "body": "$X_n\\to_p c$ 意味着对每个 $\\varepsilon>0$，$P(|X_n-c|>\\varepsilon)\\to0$。它是估计量靠近目标的一致性语言。"},
            {"title": "依分布收敛", "body": "$X_n\\to_d X$ 描述分布函数收敛。CLT 给的是标准化误差的依分布收敛，不表示未标准化误差保持随机波动。"},
            {"title": "WLLN 与 CLT 分工", "body": "$$\\bar Z\\to_p E[Z],\\qquad \\sqrt n(\\bar Z-EZ)\\to_dN(0,V).$$\n\n前者定中心，后者给尺度和形状。"},
            {"title": "连续映射与 Slutsky", "body": "若 $\\hat Q\\to_pQ$ 且 $Q$ 非奇异，则 $\\hat Q^{-1}\\to_pQ^{-1}$；若再有 $S_n\\to_dS$，则 $\\hat Q^{-1}S_n\\to_dQ^{-1}S$。"},
        ],
        "derivation": {
            "title": "Delta method",
            "setup": "已知 $\\sqrt n(\\hat\\theta-\\theta_0)\\to_dN(0,V)$，目标是函数 $g(\\theta_0)$ 的推断。",
            "steps": [
                "在 $\\theta_0$ 一阶展开：\n$$\ng(\\hat\\theta)=g(\\theta_0)+G'(\\hat\\theta-\\theta_0)+r_n,\n$$\n其中 $G=\\nabla g(\\theta_0)$。",
                "若 $g$ 光滑且 $\\hat\\theta\\to_p\\theta_0$，则 $\\sqrt n r_n\\to_p0$。",
                "乘 $\\sqrt n$ 并用 Slutsky：\n$$\n\\sqrt n\\{g(\\hat\\theta)-g(\\theta_0)\\}\\to_dN(0,G'VG).\n$$",
            ],
            "reasons": ["Taylor 展开", "一致性控制余项", "线性变换正态与 Slutsky"],
            "conclusion": "非线性函数的一阶不确定性由梯度传递；若梯度为零，一阶 delta method 退化，必须升级展开。",
        },
        "conditions": ["适用的 WLLN/CLT，不是只写 i.i.d. 口号", "矩存在和固定参数维数", "映射在极限点连续", "$g$ 在真值附近可微且梯度维数正确"],
        "example": {"title": "例：对数点弹性", "body": "若 $g(\\beta)=\\exp(\\beta_j)-1$，则 $G$ 只有第 $j$ 位为 $\\exp(\\beta_j)$。渐近方差为 $\\exp(2\\beta_j)V_{jj}$，实际用 $\\hat\\beta_j$ 代入梯度。"},
        "misconception": "“$X_n\\to_dX$ 后可对任何函数取极限。”需要函数在极限随机变量取值处几乎处处连续；求逆在奇异矩阵处不连续。",
        "check": {
            "question": "已知 $\\sqrt n(\\hat\\theta-\\theta)\\to_dN(0,\\sigma^2)$。求 $g(\\theta)=\\theta^2$ 的一阶渐近方差；若 $\\theta=0$ 有何问题？",
            "answer": "梯度 $g'(\\theta)=2\\theta$，方差为 $4\\theta^2\\sigma^2$。当 $\\theta=0$ 时一阶项为零，$\\sqrt n$ 标准化退化，需二阶 delta method，通常改用 $n\\hat\\theta^2$ 的极限。",
            "diagnosis": "若在 $\\theta=0$ 仍报告普通正态，回到梯度退化；若用 $2\\hat\\theta$ 没说明一致替代，回到 Slutsky",
        },
        "takeaways": ["LLN 给一致性，CLT 给根号 $n$ 波动", "连续映射要求极限点连续", "Delta method 是 Taylor + Slutsky"],
        "practice": "补充讲义 3 的自检题与 Ch.7 预备题",
        "extensions": ["随机阶 $O_p/o_p$", "二阶 delta method", "函数型 CLT 与单位根"],
        "links": [],
    },
    {
        "number": 13,
        "semester": 1,
        "title": "OLS 渐近理论",
        "subtitle": "一致性、渐近正态、夹心方差与参数函数",
        "chapters": "Ch.7",
        "book_pages": "162–195",
        "pdf_pages": "182–215",
        "position": "把 Ch.11 的概率工具完整应用于最熟悉的 OLS，并建立后续估计量模板",
        "objectives": ["证明 OLS 一致性与渐近正态", "解释 $Q^{-1}\\Omega Q^{-1}$ 的每一部分", "构造一致的稳健方差与渐近 $t/Wald$"],
        "prerequisites": ["会写 OLS 估计误差分解", "能对样本矩使用 WLLN/CLT", "理解 Slutsky 和 delta method"],
        "bridge": "Ch.5 用误差正态得到精确分布；Ch.7 撤掉正态，只保留矩、识别和抽样条件，在大样本下重建 OLS 推断。",
        "bridge_prompt": "为什么渐近正态证明中要把 $X'X$ 除以 $n$、把 $X'e$ 除以 $\\sqrt n$？",
        "route": ["用样本矩证明一致性", "按根号 $n$ 重排估计误差", "CLT 得得分极限", "一致估计夹心方差"],
        "concepts": [
            {"title": "一致性的矩条件", "body": "$E[X_ie_i]=0$ 与 $Q=E[X_iX_i']>0$ 给\n$$\n\\hat\\beta=\\hat Q^{-1}\\frac1n\\sum X_iY_i\\to_pQ^{-1}E[X_iY_i]=\\beta.\n$$"},
            {"title": "异方差肉矩阵", "body": "$$\\Omega=E[X_iX_i'e_i^2]=\\operatorname{var}(X_ie_i)$$\n在 $E[X_ie_i]=0$ 下成立。它允许误差方差随 $X_i$ 改变。"},
            {"title": "稳健方差一致估计", "body": "$$\\hat\\Omega=\\frac1n\\sum X_iX_i'\\hat e_i^2,\n\\quad \\hat V=\\hat Q^{-1}\\hat\\Omega\\hat Q^{-1}.$$\n需要残差对误差的替代在平均意义下有效。"},
            {"title": "渐近 $t$ 与 Wald", "body": "$t=(\\hat\\beta_j-\\beta_{j0})/s(\\hat\\beta_j)\\to_dN(0,1)$；$q$ 个限制的 Wald 统计量在 $H_0$ 下趋于 $\\chi_q^2$。"},
        ],
        "derivation": {
            "title": "OLS 根号 $n$ 渐近正态",
            "setup": "从 $\\hat\\beta-\\beta=(X'X)^{-1}X'e$ 出发，目标是形成 LLN 项与 CLT 项。",
            "steps": [
                "乘 $\\sqrt n$ 并配尺度：\n$$\n\\sqrt n(\\hat\\beta-\\beta)=\\left(\\frac{X'X}{n}\\right)^{-1}\\left(\\frac{X'e}{\\sqrt n}\\right).\n$$",
                "WLLN 与连续映射给 $(X'X/n)^{-1}\\to_pQ^{-1}$；向量 CLT 给 $X'e/\\sqrt n\\to_dN(0,\\Omega)$。",
                "Slutsky 合并：\n$$\n\\sqrt n(\\hat\\beta-\\beta)\\to_dN(0,Q^{-1}\\Omega Q^{-1}).\n$$",
            ],
            "reasons": ["精确代数重排", "WLLN/CLT 分工", "Slutsky 与正态线性变换"],
            "conclusion": "OLS 的通用渐近模板是“逆曲率 × 随机得分”；GMM、M 估计和 NLS 会重复这一结构。",
        },
        "conditions": ["$E[X_ie_i]=0$ 确定中心", "$Q>0$ 保证识别", "得分 $X_ie_i$ 有足够矩并满足 CLT", "维数固定；高维情形需不同理论"],
        "example": {"title": "例：同方差是夹心的特例", "body": "若 $E[e_i^2\\mid X_i]=\\sigma^2$，则\n$$\n\\Omega=E[X_iX_i'e_i^2]=\\sigma^2Q,\n$$\n所以 $Q^{-1}\\Omega Q^{-1}=\\sigma^2Q^{-1}$。"},
        "misconception": "“样本量超过 30 就能用渐近正态。”没有统一阈值。尾部、杠杆、弱识别、簇数和参数维数都会改变近似质量。",
        "check": {
            "question": "在根号 $n$ 分解中，若 $E[X_ie_i]\\ne0$，CLT 仍可能成立。为什么估计量却不以 $\\beta$ 为中心？",
            "answer": "$n^{-1}X'e\\to_pE[X_ie_i]\\ne0$，所以 $\\hat\\beta-\\beta\\to_pQ^{-1}E[X_ie_i]\\ne0$。根号 $n$ 围绕 $\\beta$ 的中心项会发散；CLT 只能描述围绕错误概率极限的波动。",
            "diagnosis": "若只说“标准误错”，回到一致性；若认为 CLT 修复内生性，强调 CLT 不改变概率极限",
        },
        "takeaways": ["识别/正交决定概率极限", "CLT 描述围绕该极限的波动", "稳健 SE 不能修复错误的估计目标"],
        "practice": "Ch.7 一致性、渐近正态、稳健方差与 delta method 题",
        "extensions": ["HC2/HC3 高阶修正", "均匀一致残差*", "Edgeworth expansion*"],
        "links": [("Ch.7 习题解答", "docs/ch07/Hansen_Ch07_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch07/Hansen_Ch07_Exercises_Solutions.md")],
    },
]


MAIN_SESSIONS += [
    {
        "number": 14,
        "semester": 1,
        "title": "约束估计与最小距离",
        "subtitle": "把理论限制写成参数空间中的加权投影",
        "chapters": "Ch.8",
        "book_pages": "196–220",
        "pdf_pages": "216–240",
        "position": "从无约束估计进入一般限制、有效权重与 Hausman 比较",
        "objectives": ["推导线性等式约束下的最小二乘估计量", "用最小距离统一参数限制", "解释正确与错误限制的偏差—方差后果"],
        "prerequisites": ["会用 Lagrange 乘子", "能读二次型加权距离", "理解渐近协方差矩阵"],
        "bridge": "本科常通过删除变量施加限制；Hansen 把 $r(\\beta)=0$ 看成参数空间中的集合，并用加权距离把无约束估计量投到该集合。",
        "bridge_prompt": "正确限制为何能降低方差，错误限制为何即使样本很大也危险？",
        "route": ["线性限制与约束 LS", "把限制写成最小距离", "选择有效权重", "检查错设与 Hausman equality"],
        "concepts": [
            {"title": "线性等式限制", "body": "$R'\\beta=c$，其中 $R:k\\times q$、$c:q\\times1$。$q$ 是独立限制个数；必须有 $\\operatorname{rank}(R)=q$。"},
            {"title": "最小距离", "body": "若无约束估计量 $\\hat\\theta$ 估计 $h(\\beta)$，最小化\n$$\n(\\hat\\theta-h(b))'W(\\hat\\theta-h(b)).\n$$\n权重定义哪些方向的偏离代价更大。"},
            {"title": "有效权重", "body": "若 $\\sqrt n(\\hat\\theta-\\theta)\\to N(0,V)$，有效最小距离用 $W=V^{-1}$，对噪声小的方向赋更高权重。"},
            {"title": "错限制的代价", "body": "正确限制降低方差；固定错误限制把参数空间排除真值，导致不一致。局部错设下会出现偏差—方差权衡。"},
        ],
        "derivation": {
            "title": "线性约束 OLS",
            "setup": "最小化 $(Y-Xb)'(Y-Xb)$，满足 $R'b=c$。令 $A=X'X$。",
            "steps": [
                "Lagrangian 一阶条件：\n$$\n-2X'(Y-Xb)+2R\\lambda=0\n\\Rightarrow b=\\hat\\beta-A^{-1}R\\lambda.\n$$",
                "代入约束：\n$$\nR'\\hat\\beta-R'A^{-1}R\\lambda=c\n\\Rightarrow\\lambda=(R'A^{-1}R)^{-1}(R'\\hat\\beta-c).\n$$",
                "得到\n$$\n\\hat\\beta_R=\\hat\\beta-A^{-1}R(R'A^{-1}R)^{-1}(R'\\hat\\beta-c).\n$$",
            ],
            "reasons": ["Lagrange 一阶条件", "约束回代", "线性代数求解"],
            "conclusion": "约束估计量从无约束估计量中减去违反限制的方向；修正大小由估计曲率和限制方向共同决定。",
        },
        "conditions": ["$R:k\\times q$ 满列秩", "$R'A^{-1}R:q\\times q$ 可逆", "限制必须由理论先验提出", "有效权重需要协方差一致估计"],
        "example": {"title": "例：规模报酬不变", "body": "Cobb–Douglas 回归中限制资本和劳动弹性之和为 1：$R'\\beta=1$，$R=(0,1,1)'$。约束估计提高精度的前提是该经济限制可信。"},
        "misconception": "“受约束估计标准误更小，所以模型更好。”更小只反映缩小参数空间；若限制错，估计量可非常精确地收敛到错误值。",
        "check": {
            "question": "若限制是 $\\beta_2=\\beta_3$，写出 $R,c$ 的维数和具体形式。",
            "answer": "若 $\\beta\\in\\mathbb R^k$，取 $q=1$、$R=(0,1,-1,0,\\ldots,0)'\\in\\mathbb R^{k\\times1}$、$c=0$，于是 $R'\\beta=\\beta_2-\\beta_3=0$。",
            "diagnosis": "若把 $R$ 写成 $1\\times k$，回到课程的 $R'\\beta=c$ 约定；若用两个限制，检查是否重复",
        },
        "takeaways": ["约束估计是加权投影", "有效权重来自无约束估计的不确定性", "精度提升不能替代理论限制的可信度"],
        "practice": "Ch.8 约束 LS、最小距离与错设题",
        "extensions": ["非线性限制的 Jacobian", "不等式限制与边界分布", "Hausman equality 的协方差差公式"],
        "links": [("Ch.8 习题解答", "docs/ch08/Hansen_Ch08_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch08/Hansen_Ch08_Exercises_Solutions.md")],
    },
    {
        "number": 15,
        "semester": 1,
        "title": "假设检验",
        "subtitle": "显著性、功效、Wald/LM/$F$ 与局部备择",
        "chapters": "Ch.9",
        "book_pages": "221–256",
        "pdf_pages": "241–276",
        "position": "把本科检验步骤重建为错误控制、功效与统计量极限的完整决策问题",
        "objectives": ["严格表述第一/二类错误与功效", "从渐近正态推导 Wald 统计量", "区分统计显著、经济显著与证据不足"],
        "prerequisites": ["理解渐近 $t$ 和 $\\chi^2$", "会写限制函数 $r(\\theta)$ 及 Jacobian", "知道置信区间与双侧检验的对偶"],
        "bridge": "本科“算统计量、查临界值”省略了最重要的问题：在什么原假设下控制哪种错误？备择离原假设多远时有多大功效？",
        "bridge_prompt": "不拒绝 $H_0$ 为什么不等于证明 $H_0$ 为真？",
        "route": ["定义拒绝规则和 size", "引入功效函数", "从参数限制构造 Wald", "用区间和量级解释结论"],
        "concepts": [
            {"title": "Size 与功效", "body": "Size 是 $H_0$ 为真时最坏拒绝概率；功效是具体备择下拒绝概率。控制 5% size 不保证对小样本或弱信号有高功效。"},
            {"title": "$p$ 值", "body": "$p$ 值是在 $H_0$ 下观察到至少同样极端统计量的概率，不是 $P(H_0\\mid data)$，也不是结果可重复概率。"},
            {"title": "Wald、LM 与准则差", "body": "Wald 用无约束估计；LM/score 用受约束估计；准则差比较两个最优值。正则条件下渐近等价，有限样本和数值稳定性可不同。"},
            {"title": "局部备择", "body": "$\\theta_n=\\theta_0+c/\\sqrt n$ 与估计误差同阶，给非退化极限功效。固定备择下，一致检验功效通常趋于 1。"},
        ],
        "derivation": {
            "title": "线性限制的 Wald 极限",
            "setup": "已知 $\\sqrt n(\\hat\\theta-\\theta_0)\\to_dN(0,V)$，检验 $H_0:R'\\theta=c$，其中有 $q$ 个限制。",
            "steps": [
                "在 $H_0$ 下：\n$$\n\\sqrt n(R'\\hat\\theta-c)=R'\\sqrt n(\\hat\\theta-\\theta_0)\\to_dN(0,R'VR).\n$$",
                "用一致方差 $R'\\hat VR$ 标准化多元偏离。",
                "二次型\n$$\nW=n(R'\\hat\\theta-c)'(R'\\hat VR)^{-1}(R'\\hat\\theta-c)\\to_d\\chi_q^2.\n$$",
            ],
            "reasons": ["正态线性变换", "Slutsky 一致替代", "标准正态平方和"],
            "conclusion": "Wald 衡量估计限制偏离零假设多少个联合标准误；自由度等于独立限制数，而非参数总数。",
        },
        "conditions": ["限制 Jacobian 满秩", "$V$ 在限制方向非奇异", "统计量在 $H_0$ 下取极限", "多重检验需额外错误率控制"],
        "example": {"title": "例：显著但不重要", "body": "样本极大时，工资回报估计 0.001、SE 0.0002，会高度显著，但一单位教育只对应约 0.1% 工资变化。报告时必须同时给点估计、区间和经济单位。"},
        "misconception": "“$p=0.03$ 表示原假设有 3% 概率为真。”错。频率学派 $p$ 值条件在 $H_0$ 上，不给假设的后验概率。",
        "check": {
            "question": "95% CI 为 $[-0.02,0.50]$。应怎样描述对 $H_0:\\theta=0$ 的证据和效应量？",
            "answer": "双侧 5% 水平下不拒绝零效应，因为区间含 0；但区间也包含相当大的正效应，不能说“证明没有效应”。结论是估计不精确，需要讨论功效和有意义效应范围。",
            "diagnosis": "若说接受 $H_0$，回到检验语言；若只看点估计 0.24，回到区间不确定性",
        },
        "takeaways": ["检验先定义错误控制，再选择统计量", "$p$ 值不衡量假设为真的概率", "不拒绝常常意味着区间太宽而非效应为零"],
        "practice": "Ch.9 功效、Wald、Hausman 与错误推理题",
        "extensions": ["多重检验与 FWER/FDR", "弱识别稳健检验", "等效性检验与最小有意义效应"],
        "links": [("Ch.9 习题解答", "docs/ch09/Hansen_Ch09_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch09/Hansen_Ch09_Exercises_Solutions.md")],
    },
    {
        "number": 16,
        "semester": 1,
        "title": "重抽样方法",
        "subtitle": "Jackknife、Bootstrap、BCa 与零假设下重抽样",
        "chapters": "Ch.10",
        "book_pages": "257–305",
        "pdf_pages": "277–325",
        "position": "用经验分布近似抽样过程，并理解重抽样不能修复识别错误",
        "objectives": ["区分 Jackknife 与 Bootstrap 的目标", "解释 pairs、residual、wild、cluster bootstrap 的重抽样单位", "构造在 $H_0$ 下有效的 bootstrap 检验"],
        "prerequisites": ["理解统计量的抽样分布", "知道经验分布 $F_n$", "能区分估计分布与零假设检验分布"],
        "bridge": "渐近理论解析近似分布；Bootstrap 用样本经验分布模拟重复抽样。模拟哪个抽样过程，取决于数据结构和原假设。",
        "bridge_prompt": "为什么直接从含有显著信号的原样本重抽，会让检验临界值也带着信号？",
        "route": ["经验分布与插件原理", "选择重抽样单位", "构造区间", "在原假设下构造检验"],
        "concepts": [
            {"title": "经验分布", "body": "$F_n$ 给每个观测质量 $1/n$。Pairs bootstrap 从观测对 $(Y_i,X_i)$ 有放回抽样，自动保留样本中的异方差关系。"},
            {"title": "Jackknife", "body": "删除第 $i$ 个观测得到 $\\hat\\theta_{(-i)}$，用 leave-one-out 变化估计偏差和方差。对光滑统计量有效，对中位数等非光滑对象需谨慎。"},
            {"title": "区间层级", "body": "Normal、percentile、basic、BC/BCa、percentile-$t$ 调整偏差和偏斜的能力不同。区间选择应说明枢轴性和计算代价。"},
            {"title": "依赖结构决定重抽单位", "body": "横截面 pairs；回归异方差可用 wild；聚类数据重抽整个簇；时间序列需要 block/bootstrap 或模型式重抽。不能逐行打散依赖。"},
        ],
        "derivation": {
            "title": "为什么检验要施加 $H_0$",
            "setup": "检验 $H_0:\\theta=\\theta_0$，观察统计量 $T_n$。目标是近似 $H_0$ 为真时 $T_n$ 的分布。",
            "steps": [
                "无约束重抽样以 $\\hat\\theta$ 为中心；若样本含强信号，$T_n^*$ 的分布也围绕该信号。",
                "先构造满足 $H_0$ 的受约束拟合或残差，生成 $Y^*$，确保 bootstrap 世界的参数为 $\\theta_0$。",
                "每次重算 $T_n^*$，用 $P^*(|T_n^*|\\ge|T_n|)$ 估计 $p$ 值；临界值来自零假设分布。",
            ],
            "reasons": ["检验参考分布定义", "受约束数据生成", "Monte Carlo 尾概率"],
            "conclusion": "Bootstrap 检验近似的是零假设下分布；不施加 $H_0$ 会把待检测信号带进临界值，常导致过度保守。",
        },
        "conditions": ["重抽单位匹配独立结构", "统计量对经验分布足够正则", "重复次数 $B$ 足够并报告 Monte Carlo 误差", "识别条件必须先成立"],
        "example": {"title": "例：簇随机试验", "body": "若处理在学校层分配，应重抽学校簇或使用 wild cluster bootstrap；逐学生重抽会破坏同校相关和处理分配结构，得到虚假的精度。"},
        "misconception": "“Bootstrap 很灵活，所以能修复内生性。”错。若估计量收敛到错误概率极限，bootstrap 只会精确描述围绕错误目标的抽样波动。",
        "check": {
            "question": "检验回归斜率为零时，为什么不能直接 pairs bootstrap 原数据并取斜率统计量的 95% 分位数作临界值？",
            "answer": "原数据经验分布通常对应 $\\hat\\beta\\ne0$，重抽分布含样本信号；应在 $H_0$ 下构造结果（如受约束残差/wild bootstrap）并重算学生化统计量。",
            "diagnosis": "若说 pairs 永远错误，强调它适合估计分布；若忽略学生化，回到枢轴性",
        },
        "takeaways": ["Bootstrap 模拟的是指定的数据生成世界", "依赖结构决定重抽单位", "重抽样改善推断近似但不创造识别"],
        "practice": "Ch.10 Jackknife、区间与检验题",
        "extensions": ["BCa 的偏差/加速度修正", "block bootstrap", "subsampling 与非正则问题"],
        "links": [("Ch.10 习题解答", "docs/ch10/Hansen_Ch10_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch10/Hansen_Ch10_Exercises_Solutions.md")],
    },
    {
        "number": 18,
        "semester": 1,
        "title": "多元回归",
        "subtitle": "多方程堆叠、SUR 与联合推断",
        "chapters": "Ch.11",
        "book_pages": "307–331",
        "pdf_pages": "327–351",
        "position": "从单方程 OLS 扩展到相关方程系统，并为 VAR 和 GMM 堆叠做准备",
        "objectives": ["用 Kronecker 积堆叠多方程", "说明 SUR 何时比逐方程 OLS 有效", "正确计算跨方程参数函数的联合方差"],
        "prerequisites": ["会读块对角设计矩阵", "理解 GLS 的有效性", "知道协方差项不能在参数差中省略"],
        "bridge": "本科逐方程回归忽略了不同结果方程的误差相关；SUR 把系统看成一个大 GLS。只有回归元不同且误差跨方程相关时，联合估计才获得效率。",
        "bridge_prompt": "若所有方程使用完全相同的 $X$，SUR 为什么退化为 OLS？",
        "route": ["堆叠结果与设计", "写误差协方差", "用 GLS 得 SUR", "进行跨方程联合推断"],
        "concepts": [
            {"title": "方程系统", "body": "对 $j=1,\\ldots,m$：$Y_j=X_j\\beta_j+e_j$。把 $Y_j$ 纵向堆叠，设计矩阵成为 block diagonal，参数向量堆叠。"},
            {"title": "Kronecker 协方差", "body": "若每个观测的方程误差协方差为 $\\Sigma$、跨观测独立，则堆叠误差协方差为 $\\Sigma\\otimes I_n$（取决于堆叠顺序）。"},
            {"title": "SUR 的效率来源", "body": "跨方程误差相关提供关于其他方程冲击的信息；回归元不同使该信息能改变系数加权。若误差不相关或 $X_j$ 相同，SUR 与 OLS 相同。"},
            {"title": "跨方程函数", "body": "对 $\\delta=\\beta_{1r}-\\beta_{2s}$，\n$$\n\\operatorname{var}(\\hat\\delta)=V_{1r,1r}+V_{2s,2s}-2V_{1r,2s}.\n$$\n漏掉跨方程协方差会错估不确定性。"},
        ],
        "derivation": {
            "title": "系统 GLS",
            "setup": "堆叠模型 $Y=X\\beta+e$，$\\operatorname{var}(e\\mid X)=\\Omega$。目标是构造 GLS。",
            "steps": [
                "选择 $C$ 使 $C'C=\\Omega^{-1}$，变换模型 $CY=CX\\beta+Ce$。",
                "变换误差方差为 $C\\Omega C'=I$，在变换模型中应用 OLS。",
                "得到\n$$\n\\hat\\beta_{SUR}=(X'\\Omega^{-1}X)^{-1}X'\\Omega^{-1}Y.\n$$\n实际用一致的 $\\hat\\Omega$ 得 FGLS。",
            ],
            "reasons": ["GLS 白化变换", "变换模型 OLS", "可行协方差替代"],
            "conclusion": "SUR 是系统层面的 GLS；效率增益取决于误差相关与回归元差异的共同存在。",
        },
        "conditions": ["堆叠后维数与顺序一致", "$\\Sigma$ 正定", "FGLS 需要 $\\hat\\Sigma$ 一致", "联合推断使用完整系统协方差"],
        "example": {"title": "例：消费与储蓄方程", "body": "家庭消费和储蓄可能共享未观测收入冲击，误差相关。若两方程控制变量不同，SUR 可利用相关冲击提高效率；若控制变量完全相同，逐方程 OLS 已等价。"},
        "misconception": "“误差相关就必须用 SUR，否则 OLS 有偏。”在各方程外生条件成立时，逐方程 OLS 仍一致；SUR 主要是效率和联合推断问题。",
        "check": {
            "question": "两方程估计同一政策系数的差。为什么不能把两个标准误平方相加后开根号？",
            "answer": "同一观测产生两方程结果，估计量通常相关。必须使用 $V_1+V_2-2\\operatorname{cov}(\\hat\\beta_1,\\hat\\beta_2)$；忽略协方差可能高估或低估差异方差。",
            "diagnosis": "若默认独立，回到系统误差相关；若只写协方差但符号错，重新展开 $\\operatorname{var}(A-B)$",
        },
        "takeaways": ["系统堆叠让跨方程协方差可见", "SUR 效率需要误差相关且回归元不同", "跨方程检验必须用联合方差"],
        "practice": "Ch.11 堆叠、SUR 等价条件与联合协方差题",
        "extensions": ["PCA 与因子模型", "三阶段最小二乘", "高维协方差估计"],
        "links": [("Ch.11 习题解答", "docs/ch11/Hansen_Ch11_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch11/Hansen_Ch11_Exercises_Solutions.md")],
    },
    {
        "number": 19,
        "semester": 1,
        "title": "工具变量 I",
        "subtitle": "内生性、矩条件、识别与 2SLS",
        "chapters": "Ch.12 前半",
        "book_pages": "332–371",
        "pdf_pages": "352–391",
        "position": "从 OLS 正交失败进入外部矩条件，并把 2SLS 解释为投影估计量",
        "objectives": ["区分工具外生、相关与排除限制", "用秩条件表述 IV 识别", "从样本矩/投影推导 2SLS"],
        "prerequisites": ["理解 $E[Xe]\\ne0$ 导致 OLS 不一致", "会用 $P_Z$", "能检查 $E[ZX']$ 的维数和秩"],
        "bridge": "本科常把 2SLS 记成两个回归步骤；Hansen 从 $E[Ze]=0$ 出发。两个阶段只是线性投影的计算实现，识别来自总体矩条件与秩。",
        "bridge_prompt": "第一阶段很强能证明工具变量外生吗？",
        "route": ["诊断 OLS 内生", "提出工具矩条件", "检查相关/秩", "推导 IV 与 2SLS"],
        "concepts": [
            {"title": "内生性的概率极限", "body": "$$\\hat\\beta_{OLS}\\to_p\\beta+E[XX']^{-1}E[Xe].$$\n\n稳健标准误只能估计波动，不能消除非零概率极限偏差。"},
            {"title": "工具的三层要求", "body": "1. 外生矩 $E[Ze]=0$；2. 相关/秩 $\\operatorname{rank}E[ZX']=k$；3. 排除限制说明 $Z$ 不经其他路径影响 $Y$。前两项是统计表述，第三项依赖经济机制。"},
            {"title": "恰好识别与过度识别", "body": "参数 $k$、工具矩 $m$。$m=k$ 且秩满为恰好识别；$m>k$ 为过度识别，需要选择如何组合矩条件。"},
            {"title": "第一阶段不是因果阶段", "body": "$\\hat X=P_ZX$ 提取 $X$ 中由工具线性预测的部分；第二阶段用该部分识别系数。第一阶段拟合值不是新观察变量，也不能单独证明排除限制。"},
        ],
        "derivation": {
            "title": "2SLS 投影公式",
            "setup": "模型 $Y=X\\beta+e$，工具矩阵 $Z:n\\times m$。用投影后的回归元 $\\hat X=P_ZX$。",
            "steps": [
                "第二阶段正规方程：\n$$\n\\hat X'(Y-Xb)=0.\n$$\n注意右侧结构回归元仍是 $X$。",
                "因为 $P_Z'=P_Z$、$P_Z^2=P_Z$，$\\hat X'X=X'P_ZX$，$\\hat X'Y=X'P_ZY$。",
                "解得\n$$\n\\hat\\beta_{2SLS}=(X'P_ZX)^{-1}X'P_ZY.\n$$",
            ],
            "reasons": ["投影回归元的一阶条件", "投影矩阵对称幂等", "线性方程求解"],
            "conclusion": "2SLS 用 $Z$ 所张成空间中的 $X$ 变异识别 $\\beta$；若该投影近乎没有变化，弱工具导致不稳定。",
        },
        "conditions": ["$Z:n\\times m$ 包含所有外生控制", "$E[Ze]=0$", "$\\operatorname{rank}E[ZX']=k$", "$X'P_ZX$ 可逆；弱秩会导致有限样本近似差"],
        "example": {"title": "例：教育回报与距离工具", "body": "离大学距离可能预测教育，但外生性需要论证距离不通过地区劳动力市场、家庭背景等其他路径影响工资。相关性可用第一阶段观察，排除限制不能由同一回归检验。"},
        "misconception": "“第一阶段 $F>10$ 就说明工具有效。”$F$ 只给相关性诊断，而且固定阈值也非普遍；外生性和排除限制仍需制度论证。",
        "check": {
            "question": "为什么第二阶段不能简单把 $Y$ 对保存的 $\\hat X$ 回归后直接使用普通 OLS 标准误？",
            "answer": "普通 OLS SE 把 $\\hat X$ 当作固定观察回归元，忽略它由第一阶段估计以及结构残差与 $X$ 的关系。应使用 2SLS/GMM 的正确方差公式或专业实现。",
            "diagnosis": "若说系数也不同，核对含相同控制时系数等价；错误主要在方差与自由度处理",
        },
        "takeaways": ["IV 从外部正交矩替代失败的 OLS 矩", "识别是秩与外生的共同要求", "2SLS 两阶段是计算表示，不是两次独立推断"],
        "practice": "Ch.12 识别、2SLS 代数与第一阶段题",
        "extensions": ["控制函数法", "异方差下有效 IV", "弱识别稳健区间"],
        "links": [("Ch.12 习题解答", "docs/ch12/Hansen_Ch12_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch12/Hansen_Ch12_Exercises_Solutions.md")],
    },
]


WORKSHOP_SESSIONS = [
    {
        "number": 7,
        "semester": 1,
        "title": "矩阵、投影与 OLS",
        "subtitle": "用手算和 base R 核对第 2–6 次课的代数",
        "chapters": "Ch.2–3",
        "book_pages": "14–96",
        "pdf_pages": "34–116",
        "position": "在进入统计性质前，确保总体投影与样本 OLS 的代数已经可操作",
        "objectives": ["手算简单回归与投影矩阵", "用 R 核对正规方程和残差正交", "用残差化数值验证 FWL"],
        "prerequisites": ["会写 $P_X/M_X$", "知道 BLP 与 OLS 的总体/样本区别", "能解释 FWL 的双残差化"],
        "research_question": "给定四个观测，OLS 到底做了什么几何变换？我们要同时核对系数、拟合值、残差、正交和留一影响。",
        "data_status": "::: {.data-status}\n使用课件内生成人工数据，不依赖 hansen/。代码采用 base R，固定数据无随机性，Quarto 默认不执行。\n:::",
        "sample": "$n=4$，$x=(0,1,2,3)'$，$y=(1,2,4,5)'$。样本刻意很小，目的是每个矩阵都能手算；它不用于统计推断。",
        "variables": "设计矩阵 $X=[1_n,x]$ 为 $4\\times2$。因变量保持原单位；加入常数使残差和为零。",
        "identification": "$X$ 两列线性无关，$X'X$ 可逆。这里验证的是样本代数，不需要 $E[e\\mid X]=0$；因此不能从结果宣称因果。",
        "estimator": "$$\\hat\\beta=(X'X)^{-1}X'y,\\quad \\hat y=P_Xy,\\quad \\hat e=M_Xy.$$\n\n随后检查 $X'\\hat e=0$、$P_X^2=P_X$。",
        "inference": "本工作坊不报告 $p$ 值。$n=4$ 的示例只验证代数；把软件自动输出的 t 值解释为经验结论没有意义。",
        "workflow": "1. 手算 $X'X,X'y$；2. 求系数；3. 构造 $P_X/M_X$；4. 核对正交；5. 改动一个高杠杆点，观察系数变化。",
        "code_setup": clean(r"""
            ~~~r
            x <- 0:3
            y <- c(1, 2, 4, 5)
            X <- cbind(const = 1, x = x)

            XtX <- crossprod(X)
            Xty <- crossprod(X, y)
            beta_hat <- solve(XtX, Xty)
            ~~~
        """),
        "code_estimate": clean(r"""
            ~~~r
            P <- X %*% solve(XtX) %*% t(X)
            M <- diag(length(y)) - P
            fitted <- as.vector(P %*% y)
            resid <- as.vector(M %*% y)

            stopifnot(max(abs(crossprod(X, resid))) < 1e-10)
            stopifnot(max(abs(P %*% P - P)) < 1e-10)
            cbind(y, fitted, resid)
            ~~~
        """),
        "results": "| 对象 | 数值 |\n|---|---:|\n| 截距 $\\hat\\beta_0$ | 0.900 |\n| 斜率 $\\hat\\beta_1$ | 1.400 |\n| 残差和 | 0.000 |\n| $\\max|X'\\hat e|$ | $<10^{-10}$ |\n\n这些是固定数据的精确数值核对，不是总体参数证据。",
        "diagnostics": "将最后一个 $y=5$ 改为 $y=10$，比较斜率与 $h_{44}$。高杠杆点同时在 $x$ 方向极端，结果对其 $y$ 偏离尤其敏感。",
        "sensitivity": "分别删除第 1 个和第 4 个观测重估，报告斜率变化。敏感性来自设计位置与残差共同作用，而不只是残差绝对值。",
        "misconception": "软件核对 $X'\\hat e=0$ 后就说“解释变量外生”。这是把样本一阶条件误当总体识别假设。",
        "check": {
            "question": "若在完整回归中加入控制变量 $z$，如何用 R 只通过残差化得到 $x$ 的系数？",
            "answer": "先取 resid(lm(y ~ z)) 和 resid(lm(x ~ z))；再将前者对后者无截距回归。若完整模型含常数，两个辅助回归也含常数，得到的斜率与 lm(y ~ x + z) 的 x 系数一致。",
            "diagnosis": "若只残差化 y，回到 FWL 双残差化；若最后又加入 z，说明尚未理解控制方向已被剔除",
        },
        "takeaways": ["矩阵公式可用小样本逐项审计", "残差正交是代数事实", "杠杆与残差共同决定影响力"],
        "practice": "提交手算页、R 核对输出和一次留一敏感性说明",
        "extensions": ["用 qr.solve 替代显式求逆", "计算 Cook distance", "用分组虚拟变量演示 within 变换"],
        "links": [("Ch.3 习题解答", "docs/ch03/Hansen_Ch03_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch03/Hansen_Ch03_Exercises_Solutions.md")],
    },
    {
        "number": 12,
        "semester": 1,
        "title": "有限样本与渐近推断",
        "subtitle": "Monte Carlo 比较普通、稳健与错误标准误",
        "chapters": "Ch.4–7",
        "book_pages": "97–195",
        "pdf_pages": "117–215",
        "position": "在进入 OLS 渐近证明前，用覆盖率看见方差公式选择的实际后果",
        "objectives": ["设计异方差 Monte Carlo", "比较同方差与 HC1 区间覆盖率", "报告 Monte Carlo 误差而非过度解释随机波动"],
        "prerequisites": ["知道覆盖率定义", "会计算 OLS 与 HC1 方差", "理解固定种子和重复次数"],
        "research_question": "真实误差方差随 $|X|$ 增大时，使用同方差标准误的 95% 区间还能覆盖真斜率 95% 吗？",
        "data_status": "::: {.data-status}\n使用固定种子 20260802 的自生成数据；$B=2000$、每次 $n=120$。示例输出由 base R 预计算。\n:::",
        "sample": "每次重复独立生成 $n=120$ 个观测。$B=2000$ 时 95% 覆盖率估计的 MCSE 约 $\\sqrt{0.95(0.05)/2000}=0.0049$。",
        "variables": "$X\\sim N(0,1)$；$Y=1+2X+e$；$e=\\sqrt{0.25+4X^2}\\,u$、$u\\sim N(0,1)$。条件均值正确，但方差随 $X^2$ 变化。",
        "identification": "$E[e\\mid X]=0$，所以 OLS 中心正确；挑战只在方差。该设计刻意把“偏误问题”和“标准误问题”分开。",
        "estimator": "每次计算同一个 $\\hat\\beta_1$，分别用 $s^2(X'X)^{-1}$ 和 HC1 夹心构造 $\\hat\\beta_1\\pm1.96SE$。",
        "inference": "重复抽样单位是整份模拟样本。同方差公式错设；HC1 允许异方差。两者都用渐近 1.96 临界值。",
        "workflow": "生成样本 → OLS → 两种 SE → 记录区间是否含 2 → 重复 $B$ 次 → 报覆盖率与 MCSE。",
        "code_setup": clean(r"""
            ~~~r
            set.seed(20260802)
            B <- 2000L
            n <- 120L
            cover_homo <- cover_hc1 <- logical(B)
            ~~~
        """),
        "code_estimate": clean(r"""
            ~~~r
            for (b in seq_len(B)) {
              x <- rnorm(n)
              e <- rnorm(n) * sqrt(0.25 + 4 * x^2)
              y <- 1 + 2 * x + e
              X <- cbind(1, x)
              bhat <- as.vector(solve(crossprod(X), crossprod(X, y)))
              uhat <- as.vector(y - X %*% bhat)
              bread <- solve(crossprod(X))
              V0 <- sum(uhat^2) / (n - 2) * bread
              V1 <- n / (n - 2) * bread %*%
                crossprod(X, X * uhat^2) %*% bread
              cover_homo[b] <- abs(bhat[2] - 2) <= 1.96 * sqrt(V0[2, 2])
              cover_hc1[b] <- abs(bhat[2] - 2) <= 1.96 * sqrt(V1[2, 2])
            }
            ~~~
        """),
        "results": "| 95% 区间 | 覆盖率 | 与 0.95 的差 |\n|---|---:|---:|\n| 同方差 SE | 0.754 | -0.196 |\n| HC1 SE | 0.941 | -0.009 |\n\nHC1 与 0.95 的差约 1.8 个 MCSE；同方差低覆盖远超模拟误差。",
        "diagnostics": "同时记录平均斜率可验证中心接近 2；画 $\\hat e_i^2$ 对 $x_i^2$ 会暴露扇形。诊断不能证明 HC1 小样本完美，只说明同方差假设明显不合适。",
        "sensitivity": "把 $n$ 改为 50、500，观察 HC1 覆盖趋近速度；把异方差系数 4 改为 0，确认两种公式在同方差世界接近。",
        "misconception": "看到 HC1 覆盖 0.941 就断言理论错误。Monte Carlo 结果本身有随机误差，且 $n=120$ 仍有有限样本偏差。",
        "check": {
            "question": "如果把 DGP 改成 $e=X+u$，继续比较两种标准误能否隔离方差错设？",
            "answer": "不能。此时 $E[e\\mid X]=X\\ne0$，OLS 斜率概率极限错误；两种 SE 都围绕错误中心。应保持条件均值为零，只改变条件方差来隔离方差问题。",
            "diagnosis": "若认为 HC1 能修复，回到稳健 SE 不修识别；若只说误差相关，要求写出条件均值",
        },
        "takeaways": ["模拟设计要一次只改变一个理论条件", "覆盖率检验整个区间程序", "MCSE 决定能否解释模拟差异"],
        "practice": "提交 n=50/120/500 的覆盖率表和 150 字解释",
        "extensions": ["比较 HC0–HC3", "加入少簇 cluster DGP", "用非正态厚尾误差比较收敛"],
        "links": [("Ch.7 习题解答", "docs/ch07/Hansen_Ch07_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch07/Hansen_Ch07_Exercises_Solutions.md")],
    },
    {
        "number": 17,
        "semester": 1,
        "title": "检验与 Bootstrap",
        "subtitle": "区间、学生化统计量与零假设下 wild bootstrap",
        "chapters": "Ch.9–10",
        "book_pages": "221–305",
        "pdf_pages": "241–325",
        "position": "把检验语言落实为可重复的重抽样算法",
        "objectives": ["构造 pairs bootstrap 斜率区间", "在 $H_0$ 下构造 wild bootstrap 检验", "区分估计分布与检验参考分布"],
        "prerequisites": ["会解释 percentile 区间", "知道学生化统计量", "理解检验必须在 $H_0$ 下校准"],
        "research_question": "异方差小样本中，斜率区间和 $H_0:\\beta=0$ 的检验应模拟哪个分布？",
        "data_status": "::: {.data-status}\n固定种子 20260802，自生成 $n=80$；$B=1999$。示例输出由 base R 预计算，未依赖外部数据。\n:::",
        "sample": "$n=80$ 独立观测。奇数 $B=1999$ 便于尾概率排序；Monte Carlo 最小正 $p$ 值约为 $1/(B+1)=0.0005$。",
        "variables": "$X\\sim N(0,1)$；$Y=1+0.45X+\\sqrt{0.5+X^2}u$。异方差但 $E[u\\mid X]=0$。",
        "identification": "斜率是正确线性 CEF 参数。Pairs bootstrap 用于估计分布；检验零斜率时，受约束模型只含常数。",
        "estimator": "基准 OLS 斜率 $\\hat\\beta$；pairs bootstrap 重抽 $(Y_i,X_i)$；wild bootstrap 固定 $X$，对受约束残差乘 Rademacher 权重。",
        "inference": "区间展示 percentile 作为直观起点；检验用受约束 wild bootstrap 的 t 统计量。生产分析应优先学生化和合适小样本修正。",
        "workflow": "基准估计 → pairs 区间 → 受约束拟合 → wild 样本 → 每次重算 t → 尾概率。",
        "code_setup": clean(r"""
            ~~~r
            set.seed(20260802)
            n <- 80L
            B <- 1999L
            x <- rnorm(n)
            y <- 1 + 0.45 * x + rnorm(n) * sqrt(0.5 + x^2)
            fit <- lm(y ~ x)
            ~~~
        """),
        "code_estimate": clean(r"""
            ~~~r
            bstar <- replicate(B, {
              ii <- sample.int(n, n, replace = TRUE)
              coef(lm(y[ii] ~ x[ii]))[2]
            })
            ci <- quantile(bstar, c(0.025, 0.975))

            fit0 <- lm(y ~ 1)
            t_obs <- coef(summary(fit))[2, 3]
            t_star <- replicate(B, {
              yb <- fitted(fit0) + resid(fit0) * sample(c(-1, 1), n, TRUE)
              coef(summary(lm(yb ~ x)))[2, 3]
            })
            p_boot <- (1 + sum(abs(t_star) >= abs(t_obs))) / (B + 1)
            ~~~
        """),
        "results": "| 量 | 预计算值 |\n|---|---:|\n| OLS 斜率 | 0.661 |\n| 常规 OLS SE | 0.135 |\n| pairs percentile 95% CI | [0.337, 0.978] |\n| 观察 t | 4.899 |\n| 受约束 wild bootstrap $p$ | 0.0005（加一修正） |",
        "diagnostics": "比较无约束和受约束 bootstrap 的 $T^*$ 分布中心；检查少量极端 $X$ 是否支配区间。$p=0.0005$ 只表示在 1999 次中未出现更极端值，不等于真实概率为零。",
        "sensitivity": "改用 HC1 学生化 t；把 Rademacher 权重换 Mammen 权重；改变 $B$ 并报告 Monte Carlo 误差。",
        "misconception": "用无约束 pairs bootstrap 的斜率分布直接给零假设检验临界值，会把估计信号带进参考分布。",
        "check": {
            "question": "为什么 bootstrap $p$ 值常写 $(1+\\#\\{|T_b^*|\\ge|T|\\})/(B+1)$，而不是简单除以 $B$？",
            "answer": "把观察统计量与 $B$ 个模拟统计量视为 $B+1$ 个可交换值，加一修正避免有限 $B$ 时报告零 $p$ 值，并给有效的 Monte Carlo 检验校准。",
            "diagnosis": "若说只是四舍五入，回到 Monte Carlo 检验；若忽略双侧绝对值，回到备择定义",
        },
        "takeaways": ["区间模拟估计分布，检验模拟零假设分布", "重抽单位和权重必须匹配异方差/依赖", "有限 B 的 p 值也有离散和 Monte Carlo 误差"],
        "practice": "提交两种 bootstrap 分布图、区间和受约束检验说明",
        "extensions": ["BCa 区间", "percentile-t", "wild cluster bootstrap"],
        "links": [("Ch.10 习题解答", "docs/ch10/Hansen_Ch10_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch10/Hansen_Ch10_Exercises_Solutions.md")],
    },
    {
        "number": 20,
        "semester": 1,
        "title": "IV 与识别",
        "subtitle": "2SLS 手算、第一阶段与弱工具模拟",
        "chapters": "Ch.12",
        "book_pages": "332–411",
        "pdf_pages": "352–431",
        "position": "在第二学期深入弱工具与 LATE 前，先让识别强度的后果可见",
        "objectives": ["用投影公式计算 2SLS", "报告第一阶段与识别诊断", "用模拟解释弱工具厚尾和普通近似失效"],
        "prerequisites": ["会写 $E[Ze]=0$ 与秩条件", "会构造 $P_Z$", "知道第一阶段强度不证明外生"],
        "research_question": "当工具外生但与内生变量只弱相关时，2SLS 的抽样分布会怎样变化？",
        "data_status": "::: {.data-status}\n固定种子 20260802，自生成 $B=1000$ 份、每份 $n=500$。比较第一阶段系数 $\\pi=0.8$ 与 $0.1$。\n:::",
        "sample": "每次生成独立横截面。真实结构斜率 $\\beta=1$；工具 $Z$ 外生；第一阶段强弱是唯一改变。",
        "variables": "$X=\\pi Z+v$；$Y=1+X+u$；令 $\\operatorname{corr}(u,v)=0.7$ 制造 OLS 内生。$Z$ 与 $u,v$ 独立。",
        "identification": "$E[Zu]=0$ 保证工具外生；$\\pi\\ne0$ 给识别。弱情形不是完全未识别，但有限样本分布极不规则。",
        "estimator": "$$\\hat\\beta_{2SLS}=(X'P_ZX)^{-1}X'P_ZY.$$\n\n每次同时记录 2SLS、第一阶段 F 和极端估计。",
        "inference": "本工作坊不使用“F>10 就安全”的机械规则。报告强/弱设计下完整分布摘要，强调弱识别稳健推断需要 Anderson–Rubin 等方法。",
        "workflow": "生成 $Z,v,u$ → 构造 $X,Y$ → OLS/2SLS → 第一阶段 F → 重复 → 比较均值、中位数、RMSE 与尾部。",
        "code_setup": clean(r"""
            ~~~r
            set.seed(20260802)
            B <- 1000L
            n <- 500L
            beta_true <- 1
            ~~~
        """),
        "code_estimate": clean(r"""
            ~~~r
            iv_once <- function(pi) {
              z <- rnorm(n)
              v <- rnorm(n)
              u <- 0.7 * v + sqrt(1 - 0.7^2) * rnorm(n)
              x <- pi * z + v
              y <- 1 + beta_true * x + u
              Z <- cbind(1, z)
              X <- cbind(1, x)
              PZX <- crossprod(Z, X)
              bhat <- solve(
                t(PZX) %*% solve(crossprod(Z)) %*% PZX,
                t(PZX) %*% solve(crossprod(Z)) %*% crossprod(Z, y)
              )[2]
              c(beta = bhat, F = unname(summary(lm(x ~ z))$fstatistic[1]))
            }
            ~~~
        """),
        "results": "| 设计 | 平均 2SLS | 中位数 | RMSE | 第一阶段 F 中位数 |\n|---|---:|---:|---:|---:|\n| 强工具 $\\pi=0.8$ | 0.998 | 1.001 | 0.058 | 320.44 |\n| 弱工具 $\\pi=0.1$ | 0.326 | 0.993 | 13.773 | 4.91 |\n\n弱设计的中位数看似正常，但少数巨大离群值摧毁均值与 RMSE。",
        "diagnostics": "画 2SLS 分布时不要只看中心直方图；报告 1%、99% 分位数和最大绝对值。厚尾使普通标准误与正态图非常误导。",
        "sensitivity": "改变 $n$ 与 $\\pi$，保持浓度参数大致固定，观察“样本大”不必自动消除弱识别；比较 Anderson–Rubin 检验。",
        "misconception": "弱工具只会让标准误变大。实际上 2SLS 有限样本分布可偏斜、厚尾，正态近似和点估计均会不稳定。",
        "check": {
            "question": "弱工具模拟中，中位数接近 1，能否据此说 2SLS 表现良好？",
            "answer": "不能。中位数掩盖极厚尾；均值、RMSE 和常规区间都受少数极端比率估计影响。应检查完整分布并使用弱识别稳健推断。",
            "diagnosis": "若只比较偏误均值，补看厚尾；若只看第一阶段显著性，回到识别强度连续而非二元",
        },
        "takeaways": ["2SLS 是投影/矩估计量", "弱识别改变分布形状而非只放大 SE", "相关性诊断不能证明排除限制"],
        "practice": "提交强/弱工具分布摘要、尾部图和一段识别论证",
        "extensions": ["Anderson–Rubin 区间", "多工具与 many-IV 偏误", "LIML"],
        "links": [("Ch.12 习题解答", "docs/ch12/Hansen_Ch12_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch12/Hansen_Ch12_Exercises_Solutions.md")],
    },
]


SLUGS = {
    1: "course-orientation",
    2: "matrix-algebra-i",
    3: "matrix-algebra-ii",
    4: "probability-conditioning",
    5: "cef-and-projection",
    6: "least-squares-algebra",
    7: "workshop-matrix-ols",
    8: "ols-finite-sample",
    9: "robust-and-clustered-se",
    10: "normal-regression-transition",
    11: "asymptotic-toolkit",
    12: "workshop-finite-vs-asymptotic",
    13: "ols-asymptotics",
    14: "restrictions-minimum-distance",
    15: "hypothesis-testing",
    16: "resampling-methods",
    17: "workshop-testing-bootstrap",
    18: "multivariate-regression",
    19: "instrumental-variables-i",
    20: "workshop-iv-identification",
    21: "instrumental-variables-ii",
    22: "gmm",
    23: "time-series-foundations",
    24: "time-series-regression-hac",
    25: "workshop-time-series",
    26: "var-svar",
    27: "unit-roots",
    28: "cointegration",
    29: "workshop-var-unit-root",
    30: "panel-fe-re",
    31: "dynamic-panel-gmm",
    32: "difference-in-differences",
    33: "workshop-panel-did",
    34: "nonparametric-and-series",
    35: "regression-discontinuity",
    36: "m-estimators-nls",
    37: "quantile-discrete-choice",
    38: "censoring-selection",
    39: "model-selection-machine-learning",
    40: "workshop-integration",
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    specs = MAIN_SESSIONS + WORKSHOP_SESSIONS
    expected = {spec["number"] for spec in specs}
    if len(expected) != len(specs):
        raise ValueError("DUPLICATE_SESSION_NUMBER")
    for spec in specs:
        slug = SLUGS[spec["number"]]
        target = OUT / f"{spec['number']:02d}-{slug}.qmd"
        renderer = render_workshop if spec in WORKSHOP_SESSIONS else render_main
        target.write_text(renderer(spec), encoding="utf-8")
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
