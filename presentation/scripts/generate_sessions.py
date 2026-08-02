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


MAIN_SESSIONS += [
    {
        "number": 21, "semester": 2,
        "title": "工具变量 II",
        "subtitle": "弱工具、多工具、LATE 与异质处理效应",
        "chapters": "Ch.12 后半", "book_pages": "332–411", "pdf_pages": "352–431",
        "position": "从 2SLS 计算推进到弱识别与异质效应下的估计对象",
        "objectives": ["解释弱工具为何改变有限样本分布", "从潜在结果推导二元工具的 LATE", "区分第一阶段强度、外生性与排除限制"],
        "prerequisites": [r"会写 $E[Ze]=0$ 与秩条件", "理解 2SLS 投影公式", r"知道潜在结果 $Y(d)$ 与处理状态 $D(z)$"],
        "bridge": "本科 IV 常把 2SLS 系数统称为因果效应；Hansen 进一步追问工具改变了谁的处理，以及异质效应下这个比率平均了谁。",
        "bridge_prompt": "工具相关且外生，为什么仍不能自动把 IV 系数解释为总体平均处理效应？",
        "route": ["识别强度与弱工具", "多工具与过拟合", "潜在处理状态", "LATE 的识别与外推边界"],
        "concepts": [
            {"title": "弱识别不是小标准误问题", "body": r"当 $E[ZX']$ 接近降秩，2SLS 是两个接近零的随机量之比，分布可偏斜、厚尾；常规正态近似和 Wald 区间会失真。"},
            {"title": "多工具的双刃剑", "body": "增加有效工具可提高信息，但大量工具会在第一阶段过拟合内生变量，使 2SLS 向 OLS 偏移。必须报告工具数、第一阶段和弱识别稳健结果。"},
            {"title": "潜在处理状态", "body": r"二元工具下 $D_i(1),D_i(0)\in\{0,1\}$。单调性 $D_i(1)\ge D_i(0)$ 排除 defier；complier 满足 $D_i(1)>D_i(0)$。"},
            {"title": "LATE 是局部对象", "body": clean(r"""
                在独立性、排除限制、单调性和非零第一阶段下，Wald 比率识别
                $$E[Y_i(1)-Y_i(0)\mid D_i(1)>D_i(0)].$$
                局部总体由工具和制度共同定义。
            """)},
        ],
        "derivation": {
            "title": "二元工具的 Wald–LATE",
            "setup": r"令 $Y_i=Y_i(0)+D_i\{Y_i(1)-Y_i(0)\}$，且 $D_i=D_i(Z_i)$。比较 $Z=1$ 与 $Z=0$ 的均值。",
            "steps": [
                r"由工具独立性和排除限制，约化式差为 $$E[(D_i(1)-D_i(0))\{Y_i(1)-Y_i(0)\}].$$",
                r"第一阶段差为 $E[D_i(1)-D_i(0)]$。单调性下差值只对 complier 等于 1，对 never/always-taker 等于 0。",
                clean(r"""两者相除得到
                    $$\frac{E[Y\mid Z=1]-E[Y\mid Z=0]}
                    {E[D\mid Z=1]-E[D\mid Z=0]}
                    =E[Y(1)-Y(0)\mid\text{complier}].$$
                """),
            ],
            "reasons": ["潜在结果代入与工具独立", "单调性分类", "条件均值比率"],
            "conclusion": "IV 在异质效应下识别由工具推动的服从者平均效应，不自动识别 ATE；更换工具可能更换目标总体。",
        },
        "conditions": ["工具对潜在结果和潜在处理独立", r"排除限制：$Z$ 只经 $D$ 影响 $Y$", "单调性与非零第一阶段", "弱识别推断不能只依赖常规 Wald"],
        "example": {"title": "例：资格线作为工具", "body": "奖学金资格提高入学率时，IV 回报针对因资格而改变入学决定的学生。永远入学和永不入学者不进入 LATE；外推到全体需要额外同质性。"},
        "misconception": "“不同有效工具都估计同一个因果效应。”只有处理效应同质或权重恰好相同时才成立；一般不同工具对应不同 complier 和不同 LATE。",
        "check": {"question": "若资格鼓励一部分人入学，却使另一部分人因污名退出，哪条 LATE 条件失败？", "answer": r"单调性失败，因为存在 $D(1)<D(0)$ 的 defier。Wald 比率不再是非负权重的 complier 平均效应。", "diagnosis": "若答排除限制，区分工具的直接结果效应与对处理方向相反"},
        "takeaways": ["弱工具改变近似分布形状", "LATE 的目标总体由工具决定", "相关、外生、排除与单调性缺一不可"],
        "practice": "Ch.12 弱工具、异质效应与 LATE 题",
        "extensions": ["Anderson–Rubin/CLR 推断", "LIML 与 many-instrument 修正", "MTE 与外推"],
        "links": [("Ch.12 习题解答", "docs/ch12/Hansen_Ch12_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch12/Hansen_Ch12_Exercises_Solutions.md")],
    },
    {
        "number": 22, "semester": 2,
        "title": "广义矩估计",
        "subtitle": "矩条件、有效权重、两步 GMM 与 $J$ 检验",
        "chapters": "Ch.13", "book_pages": "412–440", "pdf_pages": "432–460",
        "position": "把 IV 正交条件推广成贯穿动态面板和非线性模型的统一框架",
        "objectives": ["从总体矩构造样本 GMM 准则", "推导 GMM 夹心方差与有效权重", r"正确解释过度识别 $J$ 检验"],
        "prerequisites": ["会对向量函数求 Jacobian", "理解 LLN、CLT 与 Slutsky", r"知道 IV 矩条件 $E[Z(Y-X'\beta)]=0$"],
        "bridge": "2SLS 是线性矩条件配特定权重的 GMM。GMM 不要求完整似然，只要求说明哪些总体平均在真值处为零。",
        "bridge_prompt": "矩条件多于参数时，为什么不能逐条令样本矩精确等于零？",
        "route": ["总体矩与识别", "加权样本距离", "渐近分布与有效权重", "两步 GMM 和规范检验"],
        "concepts": [
            {"title": "矩条件与维数", "body": r"令 $g_i(\theta)\in\mathbb R^\ell$、$\theta\in\mathbb R^q$，真值满足 $E[g_i(\theta_0)]=0$。局部识别要求 $G=E[\partial g_i/\partial\theta']$ 为 $\ell\times q$ 且列满秩。"},
            {"title": "GMM 准则", "body": clean(r"""
                $$\hat\theta=\arg\min_\theta
                \bar g_n(\theta)'W_n\bar g_n(\theta),\qquad W_n>0.$$
                恰好识别时权重不改点估计；过度识别时权重决定折中。
            """)},
            {"title": "有效权重", "body": r"令 $S=\operatorname{avar}(\sqrt n\bar g_n)$。最优权重 $W=S^{-1}$，有效方差为 $(G'S^{-1}G)^{-1}$。实际先初估，再用残差估计 $S$。"},
            {"title": "过度识别检验", "body": r"$J=n\bar g(\hat\theta)'\hat S^{-1}\bar g(\hat\theta)\to\chi^2_{\ell-q}$。拒绝说明整组矩条件与模型不相容；不指出是哪一条，也不证明工具有效。"},
        ],
        "derivation": {
            "title": r"GMM 的根号 $n$ 极限",
            "setup": r"从一阶条件 $\hat G'W_n\bar g_n(\hat\theta)=0$ 出发，在 $\theta_0$ 附近线性化。",
            "steps": [
                r"$\bar g_n(\hat\theta)=\bar g_n(\theta_0)+G(\hat\theta-\theta_0)+o_p(n^{-1/2})$。",
                clean(r"""代入一阶条件并解得
                    $$\sqrt n(\hat\theta-\theta_0)
                    =-(G'WG)^{-1}G'W\sqrt n\bar g_n(\theta_0)+o_p(1).$$
                """),
                clean(r"""由 CLT，$\sqrt n\bar g_n(\theta_0)\to N(0,S)$，故方差为
                    $$(G'WG)^{-1}G'WSWG(G'WG)^{-1}.$$
                """),
            ],
            "reasons": ["均值定理与一致性", "线性方程求解", "向量 CLT 与 Slutsky"],
            "conclusion": "GMM 的渐近结构仍是“逆曲率 × 得分”；有效权重化简方差，但错误矩条件不会被权重修复。",
        },
        "conditions": [r"$E[g_i(\theta_0)]=0$ 且唯一识别", r"$G$ 列满秩", r"$S$ 正定并可一致估计", "两步权重的估计误差由正交一阶条件吸收"],
        "example": {"title": "例：异方差 IV", "body": r"在线性 IV 中 $g_i=Z_i(Y_i-X_i'\beta)$。异方差下 $S=E[Z_iZ_i'e_i^2]$；使用 $(E[ZZ'])^{-1}$ 的 2SLS 通常不再有效。"},
        "misconception": r"“$J$ 检验不拒绝，所以所有工具都外生。”不拒绝可能源于功效低；恰好识别时根本没有 $J$ 检验。",
        "check": {"question": r"$\ell=6$ 个矩估计 $q=3$ 个参数，$J$ 自由度是多少？若 Jacobian 近乎降秩还可放心用吗？", "answer": r"自由度为 $\ell-q=3$；近乎降秩表示弱识别，标准 $\chi^2$ 近似可能很差。", "diagnosis": r"若答 6，区分矩数和过度识别限制数；若只检查 $S$，补查 $G$ 的秩"},
        "takeaways": ["GMM 从可辩护的总体矩出发", "有效权重只在矩正确时提高效率", r"$J$ 是联合规范诊断而非工具认证"],
        "practice": r"Ch.13 GMM 一阶条件、方差、两步估计与 $J$ 检验题",
        "extensions": ["连续更新 GMM", "弱识别 GMM", r"聚类与 HAC 的 $S$"],
        "links": [("Ch.13 习题解答", "docs/ch13/Hansen_Ch13_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch13/Hansen_Ch13_Exercises_Solutions.md")],
    },
    {
        "number": 23, "semester": 2,
        "title": "时间序列基础",
        "subtitle": "平稳、遍历、MDS、Wold 分解与预测",
        "chapters": "Ch.14 前半", "book_pages": "442–474", "pdf_pages": "462–494",
        "position": "把横截面 i.i.d. 工具改造成适用于同一序列依赖观测的概率语言",
        "objectives": ["区分平稳、遍历与鞅差", "解释时间序列 LLN/CLT 的角色", "用线性投影构造一步和多步预测"],
        "prerequisites": ["理解条件期望塔性", "知道协方差与自相关函数", "会解稳定 AR(1)"],
        "bridge": "本科常说“序列有自相关”；研究生计量要说明依赖结构是否仍允许时间平均稳定，以及预测信息集是什么。",
        "bridge_prompt": "观测不独立时，为什么样本均值仍可能一致？",
        "route": ["随机过程与信息集", "平稳和遍历", "MDS 创新", "Wold 表示与最优线性预测"],
        "concepts": [
            {"title": "平稳与遍历分工", "body": "严格平稳要求有限维联合分布对时间平移不变；协方差平稳只固定均值与自协方差。遍历性使时间平均学习到总体矩。"},
            {"title": "鞅差序列", "body": r"相对信息集 $\mathcal F_{t-1}$，若 $E[u_t\mid\mathcal F_{t-1}]=0$，则 $u_t$ 是 MDS。它可条件异方差，但与过去可测变量正交。"},
            {"title": "自协方差不是因果", "body": r"$\gamma_j=\operatorname{cov}(Y_t,Y_{t-j})$ 描述线性依赖；它不说明哪个冲击具有结构含义。预测关系也不自动是政策因果关系。"},
            {"title": "Wold 分解", "body": clean(r"""
                纯非确定协方差平稳过程可写为
                $$Y_t=\mu+\sum_{j=0}^\infty\psi_j e_{t-j},\qquad\psi_0=1,$$
                其中 $e_t$ 是线性创新。
            """)},
        ],
        "derivation": {
            "title": "稳定 AR(1) 的预测",
            "setup": r"$Y_t=c+\rho Y_{t-1}+u_t$，$|\rho|<1$，且 $E[u_t\mid\mathcal F_{t-1}]=0$。求 $h$ 步预测。",
            "steps": [
                r"长期均值 $\mu=c/(1-\rho)$，所以 $Y_t-\mu=\rho(Y_{t-1}-\mu)+u_t$。",
                r"递推 $h$ 次：$Y_{t+h}-\mu=\rho^h(Y_t-\mu)+\sum_{j=0}^{h-1}\rho^j u_{t+h-j}$。",
                r"对 $\mathcal F_t$ 取条件期望，未来创新均值为零：$$E_tY_{t+h}=\mu+\rho^h(Y_t-\mu).$$",
            ],
            "reasons": ["均值方程", "递归代入", "MDS 条件期望与塔性"],
            "conclusion": r"稳定性使冲击影响按 $\rho^h$ 衰减，预测回到长期均值；接近单位根时衰减很慢。",
        },
        "conditions": [r"$|\rho|<1$ 保证稳定因果表示", "信息集必须明确", "MDS 不等于独立同分布", "LLN/CLT 需弱依赖与矩条件"],
        "example": {"title": "例：收益率与波动", "body": "资产收益均值可能近似 MDS，但平方收益高度相关。均值不可预测不表示条件方差不变；这正是 ARCH 模型的入口。"},
        "misconception": "“无自相关就独立。”零线性相关不排除非线性依赖或条件异方差；白噪声、MDS 和 i.i.d. 是强度不同的概念。",
        "check": {"question": r"$u_t$ 是 MDS，能否推出 $E[u_t^2\mid\mathcal F_{t-1}]$ 为常数？", "answer": "不能。MDS 只限制条件一阶矩为零；条件二阶矩可随过去变化。", "diagnosis": "若答能，混淆条件均值与条件方差；若答独立，条件过强"},
        "takeaways": ["遍历性连接时间平均与总体矩", "MDS 是动态外生性的核心语言", "预测创新不自动具有结构因果含义"],
        "practice": "Ch.14 平稳、MDS、Wold 与预测题",
        "extensions": ["mixing 条件", "ARCH/GARCH", "非线性预测"],
        "links": [("Ch.14 习题解答", "docs/ch14/Hansen_Ch14_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch14/Hansen_Ch14_Exercises_Solutions.md")],
    },
    {
        "number": 24, "semester": 2,
        "title": "时间序列回归与 HAC",
        "subtitle": "动态回归、长期方差与稳健推断",
        "chapters": "Ch.14 后半", "book_pages": "475–508", "pdf_pages": "495–528",
        "position": "在平稳基础上重建动态回归的识别、渐近方差与长期效应",
        "objectives": ["区分严格外生、前定与同期外生", "推导时间序列 OLS 的长期方差", "说明 HAC 带宽与核权重为何进入推断"],
        "prerequisites": [r"会写 OLS 根号 $T$ 分解", "理解自协方差函数", "知道 MDS 与平稳遍历"],
        "bridge": "横截面 HC 只允许逐观测异方差；时间序列得分还跨期相关，因此肉矩阵必须累加滞后协方差。",
        "bridge_prompt": "误差有自相关一定使 OLS 有偏吗？",
        "route": ["动态回归的外生性", "得分序列与长期方差", "HAC 构造", "动态乘数和预测诊断"],
        "concepts": [
            {"title": "三种动态外生性", "body": "严格外生要求解释变量所有期都与当前误差正交；前定允许未来解释变量受当前冲击影响；同期外生只限制同一期。"},
            {"title": "长期方差", "body": clean(r"""
                令 $s_t=X_te_t$，则
                $$\Omega=\sum_{j=-\infty}^{\infty}E[s_ts_{t-j}'].$$
                横截面独立时只有 $j=0$；序列相关时滞后项都影响均值波动。
            """)},
            {"title": "HAC 估计", "body": r"$\hat\Omega=\hat\Gamma_0+\sum_{j=1}^{L}k(j/L)(\hat\Gamma_j+\hat\Gamma_j')$。$L$ 太小漏相关，太大引入噪声；核对滞后平滑加权。"},
            {"title": "动态乘数", "body": r"模型 $Y_t=\rho Y_{t-1}+\beta X_t+e_t$ 的当期效应是 $\beta$，在稳定与持续改变 $X$ 的解释下，长期乘数为 $\beta/(1-\rho)$。"},
        ],
        "derivation": {
            "title": "时间序列 OLS 渐近方差",
            "setup": r"对平稳回归 $Y_t=X_t'\beta+e_t$，从精确误差分解形成 LLN 与时间序列 CLT。",
            "steps": [
                r"$$\sqrt T(\hat\beta-\beta)=\left(T^{-1}\sum X_tX_t'\right)^{-1}T^{-1/2}\sum X_te_t.$$",
                r"遍历 LLN 给第一项逆收敛到 $Q^{-1}$；弱依赖 CLT 给得分和趋于 $N(0,\Omega)$。",
                r"Slutsky 得 $$\sqrt T(\hat\beta-\beta)\to N(0,Q^{-1}\Omega Q^{-1}),$$ 用 HAC 一致估计 $\Omega$。",
            ],
            "reasons": ["OLS 代数重排", "遍历 LLN 与依赖 CLT", "Slutsky"],
            "conclusion": "HAC 修正得分和的长期波动，不修正遗漏动态、反向因果或单位根导致的错误中心与非标准极限。",
        },
        "conditions": ["序列平稳遍历或满足相应三角阵条件", r"$E[X_te_t]=0$", "长期方差有限", r"带宽 $L\to\infty$ 且 $L/T\to0$"],
        "example": {"title": "例：政策冲击与滞后反应", "body": "季度政策影响可能跨数季传导。应加入滞后并报告累计乘数；HAC 只能让 SE 适应残余相关，不能替代合理动态设定。"},
        "misconception": "“发现残差自相关后改用 Newey–West，就解决了模型。”HAC 不改变系数；若相关来自遗漏滞后，估计目标和预测也可能错误。",
        "check": {"question": r"若得分 $s_t$ 与 $s_{t-1}$ 正相关，忽略滞后协方差通常怎样影响样本均值方差？", "answer": r"通常低估，因为长期方差含 $\Gamma_1+\Gamma_1'$ 等正贡献；矩阵情形仍需看具体二次型。", "diagnosis": r"若说 OLS 必然有偏，回到正交条件；若只看 $e_t$，强调得分是 $X_te_t$"},
        "takeaways": ["依赖数据的肉矩阵是长期方差", "HAC 带宽是实质设定", "动态系数与长期效应要分开"],
        "practice": "Ch.14 动态回归、长期方差和 HAC 题",
        "extensions": ["固定带宽渐近", "预白化 HAC", "局部投影"],
        "links": [("Ch.14 习题解答", "docs/ch14/Hansen_Ch14_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch14/Hansen_Ch14_Exercises_Solutions.md")],
    },
    {
        "number": 26, "semester": 2,
        "title": "VAR 与结构 VAR",
        "subtitle": "伴随矩阵、脉冲响应、Granger 预测与结构识别",
        "chapters": "Ch.15", "book_pages": "509–546", "pdf_pages": "529–566",
        "position": "把多元回归系统放入动态环境，明确约化式与结构冲击的边界",
        "objectives": ["用伴随矩阵判断 VAR 稳定性", "递推计算约化式脉冲响应", "区分 Granger 预测性与结构因果识别"],
        "prerequisites": ["理解多方程堆叠与协方差矩阵", "会解 AR(p)", "知道正交化需要额外限制"],
        "bridge": "本科 VAR 软件会直接画 IRF；Hansen 要求先问冲击是约化残差还是有经济含义的结构冲击。从前者到后者必须增加可辩护限制。",
        "bridge_prompt": "改变 Cholesky 排序为何会改变正交化 IRF？",
        "route": ["VAR(p) 与伴随形式", "稳定性和 MA 表示", "预测与 IRF", "SVAR 识别限制"],
        "concepts": [
            {"title": "VAR 系统", "body": r"$Y_t=A_1Y_{t-1}+\cdots+A_pY_{t-p}+e_t$，$Y_t:m\times1$。每个方程可用同一滞后集合 OLS，但跨方程协方差用于联合推断。"},
            {"title": "伴随矩阵", "body": r"将 $p$ 个滞后堆成 $mp\times1$ 状态 $S_t=FS_{t-1}+v_t$。稳定要求 $F$ 全部特征根的模小于 1。"},
            {"title": "Granger 非因果", "body": "若控制系统历史后，X 的滞后不改善 Y 预测，则 X 不 Granger 导致 Y。这是相对给定信息集的预测陈述，不是干预效应。"},
            {"title": "结构冲击", "body": r"约化残差协方差 $\Sigma_e$ 非对角。设 $e_t=B\varepsilon_t$、$E[\varepsilon_t\varepsilon_t']=I$，仅 $BB'=\Sigma_e$ 不足以唯一确定 $B$。"},
        ],
        "derivation": {
            "title": "VAR(1) 的脉冲响应",
            "setup": r"$Y_t=AY_{t-1}+e_t$ 且稳定。求约化冲击 $e_t$ 对未来 $Y_{t+h}$ 的响应。",
            "steps": [
                r"向前迭代：$Y_{t+h}=A^hY_t+\sum_{j=0}^{h-1}A^je_{t+h-j}$。",
                r"保持其他未来创新为零，对当期冲击的导数为 $\partial Y_{t+h}/\partial e_t'=A^h$。",
                r"若 $e_t=B\varepsilon_t$，结构 IRF 为 $A^hB$；不同可行 $B$ 给不同经济响应。",
            ],
            "reasons": ["递归代入", "冲击导数", "结构映射链式法则"],
            "conclusion": r"VAR 动力学由 $A$ 决定，冲击含义由 $B$ 的识别限制决定；数据协方差不能独自提供结构标签。",
        },
        "conditions": ["稳定性或明确处理非平稳性", "滞后阶数足够", r"$B$ 需要足够数量的独立限制", "IRF 区间应计入参数估计不确定性"],
        "example": {"title": "例：货币政策冲击", "body": "把利率排在 Cholesky 最前假定其当期不受其他变量冲击；排在最后则相反。排序是经济假设，不是绘图选项。"},
        "misconception": "“某变量 Granger 导致产出，所以对它干预会改变产出。”预测先行可能来自共同信息、代理变量或政策反应函数；结构因果需要额外识别。",
        "check": {"question": r"二维 VAR 的 $\Sigma_e$ 有 3 个不同元素，而 $B$ 有 4 个元素。仅由 $BB'=\Sigma_e$ 还差几个限制？", "answer": "至少差 1 个独立限制。Cholesky 以一个当期零限制补足，但该限制必须有经济解释。", "diagnosis": "若答 4，忽略协方差已提供 3 条；若说排序由拟合优度选，回到结构识别"},
        "takeaways": ["伴随根控制动态稳定性", "IRF 先区分约化与结构冲击", "Granger 因果是预测概念"],
        "practice": "Ch.15 VAR、伴随矩阵、IRF 与结构识别题",
        "extensions": ["符号限制", "外部工具 SVAR", "局部投影与 VAR 比较"],
        "links": [("Ch.15 习题解答", "docs/ch15/Hansen_Ch15_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch15/Hansen_Ch15_Exercises_Solutions.md")],
    },
    {
        "number": 27, "semester": 2,
        "title": "单位根",
        "subtitle": "随机趋势、FCLT、伪回归与 DF/ADF 非标准极限",
        "chapters": "Ch.16 前半", "book_pages": "547–571", "pdf_pages": "567–591",
        "position": "说明平稳渐近理论在随机趋势下何处断裂，并建立非标准推断语言",
        "objectives": ["区分趋势平稳与差分平稳", "用 FCLT 解释 DF 统计量的非标准极限", "正确表述 ADF 的原假设与不拒绝结论"],
        "prerequisites": ["会解 AR(1) 并判断稳定性", "理解部分和与普通 CLT", "知道确定性项会改变检验分布"],
        "bridge": "本科记住“单位根不能查普通 t 表”；本课把原因写完整：回归元是随机游走，样本矩收敛速度和极限对象都变成 Brownian motion 泛函。",
        "bridge_prompt": "为什么样本很大也不能把 DF t 统计量当标准正态？",
        "route": ["随机游走与持久冲击", "伪回归", "FCLT 与非标准比率", "DF/ADF 的设定和语言"],
        "concepts": [
            {"title": "单位根与随机趋势", "body": r"$Y_t=Y_{t-1}+u_t$ 给 $Y_t=Y_0+\sum_{s=1}^tu_s$，冲击永久累积，方差随 $t$ 增长；一阶差分 $\Delta Y_t=u_t$ 可平稳。"},
            {"title": "趋势平稳不等于单位根", "body": r"$Y_t=\alpha+\delta t+v_t$、$v_t$ 平稳时，去趋势后平稳；错误差分会改变长期信息。确定性趋势和随机趋势必须区分。"},
            {"title": "伪回归", "body": r"两个独立随机游走的水平回归可给高 $R^2$ 和显著 t，因为共同持久性破坏平稳回归近似；这不是因果或真实相关。"},
            {"title": "ADF 回归", "body": clean(r"""
                $$\Delta Y_t=\alpha+\delta t+\gamma Y_{t-1}
                +\sum_{j=1}^p\phi_j\Delta Y_{t-j}+e_t.$$
                检验 $H_0:\gamma=0$；确定性项和滞后选择都会影响参考分布或检验质量。
            """)},
        ],
        "derivation": {
            "title": "DF 极限为何不是普通 t",
            "setup": r"在 $H_0$ 下 $Y_t=Y_{t-1}+u_t$。考察无确定性项回归 $\Delta Y_t=\gamma Y_{t-1}+e_t$。",
            "steps": [
                r"OLS 为 $\hat\gamma=\sum Y_{t-1}u_t/\sum Y_{t-1}^2$；因 $Y_{t-1}=O_p(\sqrt T)$，尺度不同于平稳回归。",
                clean(r"""FCLT 给 $T^{-1/2}Y_{\lfloor Tr\rfloor}\Rightarrow\sigma W(r)$，从而
                    $$T^{-1}\sum Y_{t-1}u_t\Rightarrow\sigma^2\int W\,dW,\quad
                    T^{-2}\sum Y_{t-1}^2\Rightarrow\sigma^2\int W^2dr.$$
                """),
                r"因此 $T\hat\gamma\Rightarrow\int WdW/\int W^2dr$；相应 t 统计量也是 Brownian 泛函而非 $N(0,1)$。",
            ],
            "reasons": ["随机游走随机阶", "函数型 CLT 与映射", "非标准随机比率"],
            "conclusion": "非标准临界值不是小样本修正，而是单位根原假设下真正的渐近分布；确定性项会改变 Brownian 泛函。",
        },
        "conditions": ["明确常数/趋势设定", "ADF 滞后使创新近似白噪声", "结构突变会扭曲单位根检验", r"不拒绝 $H_0$ 不是证明单位根"],
        "example": {"title": "例：价格水平与通胀", "body": "价格水平常表现强持久，差分近似通胀。若关心长期购买力关系，直接差分所有变量可能丢失协整信息。"},
        "misconception": r"“ADF $p>0.05$，所以序列就是单位根。”只能说数据不足以在该设定下拒绝；低功效、近单位根、趋势和突变都可能导致不拒绝。",
        "check": {"question": "ADF 回归中加入不必要趋势会有什么后果？", "answer": "通常降低检验功效；若真实有趋势却省略同样会错设。应依据经济机制、图形和嵌套策略说明选择。", "diagnosis": "若说临界值不变，强调无常数、常数、趋势有不同 DF 分布"},
        "takeaways": ["单位根改变收敛速度与极限对象", "ADF 使用 DF 临界值而非普通 t", "检验结论必须附确定性项和滞后设定"],
        "practice": "Ch.16 单位根、FCLT、伪回归和 DF/ADF 题",
        "extensions": ["KPSS 的平稳原假设", "结构突变单位根检验", "local-to-unity 渐近"],
        "links": [("Ch.16 习题解答", "docs/ch16/Hansen_Ch16_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch16/Hansen_Ch16_Exercises_Solutions.md")],
    },
    {
        "number": 28, "semester": 2,
        "title": "协整与误差修正",
        "subtitle": "长期均衡、ECM 与 Johansen 秩",
        "chapters": "Ch.16 后半", "book_pages": "572–596", "pdf_pages": "592–616",
        "position": "说明非平稳序列如何通过稳定线性组合保留长期信息",
        "objectives": ["定义协整向量和协整秩", "从长期关系推导误差修正表示", "区分 Engle–Granger 与 Johansen 的对象"],
        "prerequisites": [r"理解 $I(0)$ 与 $I(1)$", "会读 VAR 与矩阵秩", "知道单位根检验的不拒绝语言"],
        "bridge": "本科常把非平稳变量全部差分；协整说明某些水平组合本身平稳，差分模型需加入偏离长期均衡的修正项。",
        "bridge_prompt": r"两个变量各自 $I(1)$，为什么其线性组合可能 $I(0)$？",
        "route": ["协整定义与秩", "两步残差法", "ECM 短期—长期分解", "Johansen 系统秩与谨慎解释"],
        "concepts": [
            {"title": "协整向量", "body": r"$Y_t\in I(1)^m$，若存在非零 $\beta$ 使 $\beta'Y_t\in I(0)$，则协整。$\beta$ 的尺度需规范化；它不自动是一条结构需求关系。"},
            {"title": "协整秩", "body": r"秩 $r$ 是独立平稳组合数：$r=0$ 无协整；$0<r<m$ 有共同随机趋势；$r=m$ 表示向量本身平稳。"},
            {"title": "误差修正", "body": clean(r"""
                $$\Delta Y_t=\alpha\beta'Y_{t-1}
                +\sum_j\Gamma_j\Delta Y_{t-j}+e_t.$$
                $\beta'Y_{t-1}$ 是长期偏离，$\alpha$ 给各变量调整速度。
            """)},
            {"title": "两步法与系统法", "body": "Engle–Granger 先估长期式再检验残差，适合单一关系且用生成残差临界值；Johansen 在 VECM 中联合估计秩和多个向量。"},
        ],
        "derivation": {
            "title": "从 ARDL 到误差修正",
            "setup": r"$y_t=a+\rho y_{t-1}+b_0x_t+b_1x_{t-1}+u_t$。把水平动态重参数化。",
            "steps": [
                r"两边减 $y_{t-1}$，并用 $x_t=x_{t-1}+\Delta x_t$：$\Delta y_t=a+(\rho-1)y_{t-1}+(b_0+b_1)x_{t-1}+b_0\Delta x_t+u_t$。",
                r"令 $\lambda=1-\rho$、$\theta=(b_0+b_1)/(1-\rho)$、$c=a/(1-\rho)$。",
                r"整理为 $$\Delta y_t=-\lambda(y_{t-1}-c-\theta x_{t-1})+b_0\Delta x_t+u_t.$$",
            ],
            "reasons": ["差分恒等式", "长期参数重参数化", "提取误差修正项"],
            "conclusion": "ECM 同时保留短期变化与长期偏离；调整系数符号决定系统是否把偏离拉回均衡。",
        },
        "conditions": ["变量阶数与确定性项设定明确", "协整秩和滞后阶数需联合诊断", "残差单位根检验用专门临界值", "协整是统计长期关系，不自动是结构因果"],
        "example": {"title": "例：消费与收入", "body": "二者水平可各自 I(1)，但消费减长期收入比例可能平稳。ECM 中收入变化给短期反应，滞后偏离给长期调整。"},
        "misconception": "“协整证明两个变量互为因果。”协整只说明共同随机趋势受约束；因果方向和结构解释仍需外生性或制度限制。",
        "check": {"question": r"三变量系统估计协整秩 $r=2$，有几个共同随机趋势？", "answer": r"$m-r=3-2=1$ 个。存在两条独立平稳长期组合，但向量仍有一个非平稳共同趋势。", "diagnosis": "若答 2，区分协整向量数与共同趋势数；若答平稳，注意 r<m"},
        "takeaways": ["协整保留非平稳变量的长期组合", "ECM 分开短期变化和长期调整", "秩选择与确定性项必须透明报告"],
        "practice": "Ch.16 协整、ECM、Engle–Granger 与 Johansen 题",
        "extensions": ["弱外生与条件 ECM", "结构 VECM", "协整关系的结构突变"],
        "links": [("Ch.16 习题解答", "docs/ch16/Hansen_Ch16_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch16/Hansen_Ch16_Exercises_Solutions.md")],
    },
    {
        "number": 30, "semester": 2,
        "title": "静态面板：FE 与 RE",
        "subtitle": "误差成分、within 变换与聚类推断",
        "chapters": "Ch.17 前半", "book_pages": "597–620", "pdf_pages": "617–640",
        "position": "把本科“去均值”提升为含个体异质性、时间外生性和簇内依赖的完整模型",
        "objectives": ["从误差成分推导 within 估计量", "区分 FE 与 RE 的识别条件", "按面板抽样结构选择聚类方差"],
        "prerequisites": ["理解 FWL 和投影矩阵", "知道严格外生与前定变量", "会读双下标面板数据"],
        "bridge": "本科固定效应常被当作软件选项；Hansen 把它写成消去任意相关个体异质性的线性投影，同时明确代价是不能识别时间不变变量。",
        "bridge_prompt": "Hausman 检验不拒绝，是否就证明随机效应外生？",
        "route": ["误差成分与严格外生", "within 变换", "FE/RE 条件比较", "序列相关和个体聚类"],
        "concepts": [
            {"title": "静态面板模型", "body": r"$Y_{it}=X_{it}'\beta+\alpha_i+u_{it}$，$i=1,\ldots,N$，$t=1,\ldots,T$。$\alpha_i$ 可与整条 $X_i$ 相关；关键是 $E[u_{it}\mid X_{i1},\ldots,X_{iT},\alpha_i]=0$。"},
            {"title": "within 算子", "body": r"令 $\bar Y_i=T_i^{-1}\sum_tY_{it}$、$\dot Y_{it}=Y_{it}-\bar Y_i$，同理定义 $\dot X,\dot u$。个体常数满足 $\alpha_i-\alpha_i=0$。"},
            {"title": "随机效应的额外条件", "body": r"RE 把 $\alpha_i+u_{it}$ 的协方差结构用于 GLS，需 $\alpha_i$ 与所有解释变量正交。若相关，效率优势换成不一致。"},
            {"title": "面板聚类", "body": "同一个体内的冲击通常跨期相关，应把整个个体作为簇构造 sandwich。若处理在更高层分配，聚类层级还要随分配机制上移。"},
        ],
        "derivation": {
            "title": "within 估计量",
            "setup": r"从 $Y_{it}=X_{it}'\beta+\alpha_i+u_{it}$ 出发，对每个个体取时间均值并相减。",
            "steps": [
                r"时间均值为 $\bar Y_i=\bar X_i'\beta+\alpha_i+\bar u_i$。",
                r"相减得 $\dot Y_{it}=\dot X_{it}'\beta+\dot u_{it}$，$\alpha_i$ 精确消失；堆叠后 $\dot Y=M_DY$，其中 $D$ 是个体虚拟变量矩阵。",
                r"若 $\sum_{it}\dot X_{it}\dot X_{it}'$ 可逆，$$\hat\beta_{\mathrm{fe}}=(\dot X'\dot X)^{-1}\dot X'\dot Y.$$",
            ],
            "reasons": ["个体内平均", "线性去均值与 FWL", "OLS 一阶条件"],
            "conclusion": "FE 只使用个体内变化；若某变量个体内不变，它与个体效应完全共线，不能由 FE 单独识别。",
        },
        "conditions": ["个体内严格外生用于静态 FE", r"$\dot X$ 满列秩", "横截面个体独立或采用合适更高层聚类", r"固定 $T$ 时小样本自由度修正需透明"],
        "example": {"title": "例：最低工资与就业", "body": "州固定效应消除不随时间变化的产业结构；年份效应消除全国冲击。但州内随时间变化且同时影响政策和就业的因素仍会混杂。"},
        "misconception": "“加入个体固定效应就消除了所有遗漏变量。”只消除个体内时间不变部分；时变混杂、反向因果和测量误差仍在。",
        "check": {"question": r"若 $X_{it}=X_i$ 对每个个体不随时间变化，within 后是什么？能否估计其系数？", "answer": r"$\dot X_{it}=X_i-\bar X_i=0$，与个体固定效应共线，FE 不能识别该系数。需要额外结构、组间信息或相关随机效应设定。", "diagnosis": "若说系数为零，区分无法识别与真实效应为零"},
        "takeaways": ["FE 是投影，不是因果保险箱", "FE 识别来自个体内变化", "聚类层级必须匹配依赖和处理分配"],
        "practice": "Ch.17 静态面板、within、FE/RE 与聚类方差题",
        "extensions": ["非平衡面板", "Mundlak correlated RE", "双向聚类"],
        "links": [("Ch.17 习题解答", "docs/ch17/Hansen_Ch17_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch17/Hansen_Ch17_Exercises_Solutions.md")],
    },
    {
        "number": 31, "semester": 2,
        "title": "动态面板 GMM",
        "subtitle": "Nickell 偏误、AB/BB 矩条件与工具膨胀",
        "chapters": "Ch.17 后半", "book_pages": "621–649", "pdf_pages": "641–669",
        "position": "把 GMM 应用于含滞后因变量的短面板，并把工具矩阵维数放到中心",
        "objectives": ["解释 within 动态面板的 Nickell 偏误", "逐期写出 Arellano–Bond 工具矩条件", "诊断序列相关和工具膨胀"],
        "prerequisites": ["会做一阶差分", "理解 GMM 的矩数与参数数", "知道前定变量和 MDS"],
        "bridge": "本科面板加一个滞后因变量后直接做 FE；短 T 下，去均值后的滞后因变量与去均值误差机械相关，不能靠增大 N 消失。",
        "bridge_prompt": "为什么 FE 消除了个体效应，却制造了动态回归元与误差的相关？",
        "route": ["动态 FE 的相关性", "差分方程", "滞后水平工具", "系统 GMM 与工具控制"],
        "concepts": [
            {"title": "Nickell 偏误", "body": r"$Y_{it}=\rho Y_{i,t-1}+\alpha_i+u_{it}$。within 误差含 $-\bar u_i$，而 within 后的 $Y_{i,t-1}$ 含过去 $u$；固定 $T$、$N\to\infty$ 时相关不消失。"},
            {"title": "差分 GMM", "body": r"一阶差分消去 $\alpha_i$：$\Delta Y_{it}=\rho\Delta Y_{i,t-1}+\Delta u_{it}$。若 $u$ 无序列相关，$Y_{i,t-2}$ 及更早滞后与 $\Delta u_{it}$ 正交。"},
            {"title": "系统 GMM", "body": "差分方程的滞后水平工具在高持久性下很弱；Blundell–Bond 再加入水平方程，以滞后差分作工具，但需要额外初始条件/平稳性矩限制。"},
            {"title": "工具膨胀", "body": r"可用滞后随 $T$ 快速增加，工具列数可达 $O(T^2)$。过多工具会过拟合内生变量、削弱 Hansen 检验并产生不可靠两步结果。"},
        ],
        "derivation": {
            "title": "AB 矩条件从哪里来",
            "setup": r"假设 $E[u_{it}\mid Y_{i0},\ldots,Y_{i,t-1},\alpha_i]=0$ 且 $u_{it}$ 无序列相关。考察差分误差 $\Delta u_{it}=u_{it}-u_{i,t-1}$。",
            "steps": [
                r"对 $s\le t-2$，$Y_{is}$ 只由 $u_{i1},\ldots,u_{is}$ 和初值构成，与 $u_{it}$ 正交。",
                r"因 $s\le t-2$，同样有 $E[Y_{is}u_{i,t-1}]=0$，所以 $E[Y_{is}\Delta u_{it}]=0$。",
                r"把每期可用的 $(Y_{i1},\ldots,Y_{i,t-2})$ 放入块状工具矩阵 $Z_i$，得到 $E[Z_i'\Delta u_i]=0$ 并用 GMM 估计。",
            ],
            "reasons": ["前定性与时间顺序", "线性期望", "逐期矩堆叠"],
            "conclusion": "工具集合不是越多越好：每一列都对应一条时序正交条件，并应接受理论、强度和数量审计。",
        },
        "conditions": ["差分残差允许 AR(1) 但不应有 AR(2)", "工具滞后范围由变量外生性类型决定", r"报告 $N,T$、工具数与参数数", "两步 SE 使用有限样本修正"],
        "example": {"title": "例：企业投资持续性", "body": "投资率高度持续时，滞后水平对差分的解释力弱；系统 GMM 可能改善，但额外水平方程矩条件必须由初始状态论证。"},
        "misconception": "“Hansen J 的 p 值越大越好。”接近 1 可能是工具过多导致检验无力；应折叠工具、限制滞后并报告敏感性。",
        "check": {"question": r"差分方程在 $t=3$ 时，为什么 $Y_{i2}$ 不能作 $\Delta Y_{i2}$ 的工具，而 $Y_{i1}$ 可以？", "answer": r"$\Delta u_{i3}=u_{i3}-u_{i2}$，$Y_{i2}$ 含 $u_{i2}$，所以相关；在无序列相关与前定性下 $Y_{i1}$ 与两项都正交。", "diagnosis": "若只说滞后越长越外生，要求写出与差分误差两项的协方差"},
        "takeaways": ["短 T 动态 FE 有非消失偏误", "AB 工具来自明确时序矩条件", "工具数量、强度与检验功效需共同报告"],
        "practice": "Ch.17 动态面板、AB/BB 与工具矩阵题",
        "extensions": ["forward orthogonal deviations", "Windmeijer 修正", "偏误修正 LSDV"],
        "links": [("Ch.17 习题解答", "docs/ch17/Hansen_Ch17_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch17/Hansen_Ch17_Exercises_Solutions.md")],
    },
    {
        "number": 32, "semester": 2,
        "title": "双重差分",
        "subtitle": "潜在结果、平行趋势、TWFE 与错位处理",
        "chapters": "Ch.18", "book_pages": "650–664", "pdf_pages": "670–684",
        "position": "把回归中的组×后系数还原为反事实趋势假设和明确 ATT",
        "objectives": ["从潜在结果推导 2×2 DiD", "陈述条件平行趋势与无提前反应", "解释异质错位处理下 TWFE 的权重问题"],
        "prerequisites": ["理解潜在结果和 ATT", "会读个体与时间固定效应", "知道处理分配层级决定聚类"],
        "bridge": "本科 DiD 常背四格相减；Hansen 语言要求指出处理组未处理结果的反事实变化由谁提供，以及估计对象是哪个时间和群组的 ATT。",
        "bridge_prompt": "处理前趋势看起来平行，为什么仍不能证明平行趋势？",
        "route": ["2×2 潜在结果", "平行趋势识别", "事件研究诊断", "错位处理与 TWFE 限制"],
        "concepts": [
            {"title": "目标与反事实", "body": r"目标为处理组后期 $ATT=E[Y_1(1)-Y_1(0)\mid G=1]$。缺失的是 $E[Y_1(0)\mid G=1]$，控制组变化用于构造它。"},
            {"title": "平行趋势", "body": r"$E[Y_1(0)-Y_0(0)\mid G=1]=E[Y_1(0)-Y_0(0)\mid G=0]$。这是未处理潜在结果的条件，不能直接由处理后数据检验。"},
            {"title": "事件研究", "body": "处理前 lead 可检验明显预趋势并展示动态，但不显著可能因功效低；处理前最后一期通常作基准，系数解释必须附相对时间。"},
            {"title": "错位处理与 TWFE", "body": "不同群组不同时间处理且效应异质时，TWFE 可把已处理组当控制并形成非凸权重。应报告群组×时间 ATT 或采用异质稳健聚合。"},
        ],
        "derivation": {
            "title": "2×2 DiD 识别",
            "setup": r"组 $G\in\{0,1\}$、时期 $t\in\{0,1\}$，只有 $G=1,t=1$ 受处理。",
            "steps": [
                r"观察处理组变化：$E[Y_1(1)\mid G=1]-E[Y_0(0)\mid G=1]$。",
                r"平行趋势把缺失的处理组未处理变化替换为控制组变化：$E[Y_1(0)-Y_0(0)\mid G=1]=E[Y_1(0)-Y_0(0)\mid G=0]$。",
                r"两组变化相减后共同未处理趋势抵消，剩下 $E[Y_1(1)-Y_1(0)\mid G=1]=ATT$。",
            ],
            "reasons": ["潜在结果分解", "平行趋势代换", "加减消元"],
            "conclusion": "DiD 的识别来自不可观察未处理趋势的跨组等式，而不是固定效应本身；设计论证应围绕该反事实展开。",
        },
        "conditions": ["平行趋势可条件在预处理协变量上", "无提前反应和处理定义稳定", "样本构成不因处理差异变化", "标准误在处理分配或序列相关层级聚类"],
        "example": {"title": "例：分省政策分期实施", "body": "早实施省份后期已受处理，不能无条件作为晚实施省份的未处理对照。按 cohort 和相对时间估计，再以透明权重聚合。"},
        "misconception": "“事件研究处理前系数都不显著，所以平行趋势成立。”不拒绝不等于证明；还需看区间能否排除有实质意义的预趋势和制度性同期冲击。",
        "check": {"question": "若政策使部分低收入者迁出处理地区，标准 DiD 哪个条件受到威胁？", "answer": "样本构成/稳定总体受到威胁，观察到的组均值变化混合了处理效应与人群选择。需固定个体、研究迁移结果或重定义目标总体。", "diagnosis": "若只答平行趋势，要求说明潜在结果对象为何随样本成员改变"},
        "takeaways": ["四格相减背后是反事实平行趋势", "预趋势图是诊断而非证明", "错位处理需异质稳健的群组—时间比较"],
        "practice": "Ch.18 DiD 识别、事件研究和错误推理题",
        "extensions": ["合成控制", "三重差分", "连续处理 DiD"],
        "links": [("Ch.18 习题解答", "docs/ch18/Hansen_Ch18_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch18/Hansen_Ch18_Exercises_Solutions.md")],
    },
    {
        "number": 34, "semester": 2,
        "title": "非参数与级数回归",
        "subtitle": "核、局部多项式、带宽、部分线性与 NPIV",
        "chapters": "Ch.19–20", "book_pages": "666–738", "pdf_pages": "686–758",
        "position": "撤去全局线性形状限制，用平滑与基函数理解偏差—方差和正则化",
        "objectives": ["推导核/局部线性 CEF 估计", "解释带宽和级数维数的偏差—方差权衡", "识别部分线性与 NPIV 的额外困难"],
        "prerequisites": ["理解 CEF 与局部加权 LS", "会读基函数设计矩阵", "知道维数灾难和 IV 矩条件"],
        "bridge": "本科回归选一次项或二次项；非参数方法不预先固定有限维形状，但必须用带宽、基函数数或惩罚控制复杂度。",
        "bridge_prompt": "模型更灵活为什么不可能同时无偏又低方差？",
        "route": ["核权重与局部样本", "局部多项式和边界", "级数与部分线性", "NPIV 的逆问题"],
        "concepts": [
            {"title": "核回归", "body": r"Nadaraya–Watson 估计 $\hat m(x)=\sum_iK((X_i-x)/h)Y_i/\sum_iK((X_i-x)/h)$。$h$ 决定“邻近”的尺度。"},
            {"title": "局部线性", "body": r"在每个 $x$ 处加权最小化 $\sum_iK_h(X_i-x)\{Y_i-a-b(X_i-x)\}^2$，取 $\hat a$。它自动做一阶偏差修正，边界表现优于局部常数。"},
            {"title": "级数估计", "body": r"用 $p_K(X)=(p_1,\ldots,p_K)'$ 近似 $m(X)$，再 OLS。$K$ 随样本增大，但增长过快使估计方差和数值不稳定。"},
            {"title": "部分线性与 NPIV", "body": r"$Y=D\theta+g(X)+e$ 可先残差化 $Y,D$ 再估 $\theta$。若 $D$ 内生且 $E[e\mid Z]=0$，求解条件期望算子的逆通常病态，需要正则化。"},
        ],
        "derivation": {
            "title": "局部线性正规方程",
            "setup": r"固定评价点 $x$，令 $r_i=(1,X_i-x)'$、$w_i=K((X_i-x)/h)$。估计局部截距和斜率。",
            "steps": [
                r"写加权准则 $Q(a,b)=\sum_iw_i(Y_i-r_i'(a,b)')^2$。",
                r"一阶条件为 $\sum_iw_ir_i(Y_i-r_i'\hat\gamma)=0$，故 $\hat\gamma=(R'WR)^{-1}R'WY$。",
                r"$\hat m(x)=e_1'\hat\gamma$；$\hat b$ 吸收邻域内一阶趋势，使边界处不必依赖对称样本。",
            ],
            "reasons": ["局部 Taylor 近似", "加权 LS 一阶条件", "选择局部截距"],
            "conclusion": "非参数估计仍是投影，只是设计和权重随评价点及复杂度改变；推断必须把平滑偏差纳入考虑。",
        },
        "conditions": [r"评价点附近密度 $f_X(x)>0$", "CEF 足够光滑", r"$h\to0$ 且 $nh\to\infty$（一维典型）", "数据驱动带宽与偏差修正需配套推断"],
        "example": {"title": "例：班级规模与成绩", "body": "局部线性曲线可显示小班区间斜率更陡。它描述 CEF；若班级规模选择内生，灵活曲线仍不是因果剂量反应。"},
        "misconception": "“非参数等于没有假设。”它用平滑、支持、维数和复杂度增长假设替代函数形式假设；高维下这些假设更强。",
        "check": {"question": "带宽减半通常怎样影响偏差、方差和有效局部样本？", "answer": "邻域更窄，平滑偏差通常下降；有效样本减少，方差上升。具体阶数取决于核、维数和多项式阶数。", "diagnosis": "若说样本总数不变所以方差不变，强调只有带权邻域贡献信息"},
        "takeaways": ["带宽和级数维数就是复杂度参数", "局部线性改善边界偏差", "灵活拟合不能修复内生性"],
        "practice": "Ch.19–20 核、局部多项式、级数、部分线性与 NPIV 题",
        "extensions": ["交叉验证带宽", "undersmoothing/robust bias correction", "sieve NPIV"],
        "links": [
            ("Ch.19 习题解答", "docs/ch19/Hansen_Ch19_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch19/Hansen_Ch19_Exercises_Solutions.md"),
            ("Ch.20 习题解答", "docs/ch20/Hansen_Ch20_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch20/Hansen_Ch20_Exercises_Solutions.md"),
        ],
    },
    {
        "number": 35, "semester": 2,
        "title": "断点回归",
        "subtitle": "Sharp/Fuzzy RDD、带宽、操纵与局部推断",
        "chapters": "Ch.21", "book_pages": "739–751", "pdf_pages": "759–771",
        "position": "把局部多项式用于阈值制度，以连续性假设识别局部因果效应",
        "objectives": ["从潜在结果连续性推导 sharp RDD", "区分 fuzzy RDD 的分子与第一阶段", "设计带宽、操纵和协变量平滑诊断"],
        "prerequisites": ["理解局部线性和边界估计", "知道 LATE/Wald 比率", "能区分识别窗口与估计带宽"],
        "bridge": "RDD 不是在阈值两侧做任意回归；其识别来自若无处理，潜在结果在 running variable 阈值处连续。",
        "bridge_prompt": "为什么阈值附近可比不等于阈值两侧完全随机分配？",
        "route": ["制度规则与目标", "左右极限识别", "局部多项式和带宽", "fuzzy、操纵与稳健推断"],
        "concepts": [
            {"title": "Sharp RDD", "body": r"$D_i=1\{X_i\ge c\}$。目标 $\tau=E[Y_i(1)-Y_i(0)\mid X_i=c]$ 是阈值处局部效应，不是全样本 ATE。"},
            {"title": "Fuzzy RDD", "body": "若阈值只改变处理概率，结果跳跃除以处理概率跳跃给阈值处 complier 的局部效应；需要排除限制、单调性和非零第一阶段。"},
            {"title": "带宽与多项式", "body": "左右分别做低阶局部多项式。小带宽降偏但增方差；全局高阶多项式会用远端数据并产生边界振荡，不是推荐主规格。"},
            {"title": "诊断边界", "body": "密度跳跃提示 running variable 操纵；预处理协变量跳跃提示可比性问题。诊断不显著也不能证明所有潜在结果连续。"},
        ],
        "derivation": {
            "title": "Sharp RDD 的左右极限",
            "setup": r"观察 $Y=D Y(1)+(1-D)Y(0)$，且 $D=1\{X\ge c\}$。假设 $E[Y(d)\mid X=x]$ 在 $c$ 连续。",
            "steps": [
                r"从右侧逼近，$D=1$，所以 $\lim_{x\downarrow c}E[Y\mid X=x]=E[Y(1)\mid X=c]$。",
                r"从左侧逼近，$D=0$，所以 $\lim_{x\uparrow c}E[Y\mid X=x]=E[Y(0)\mid X=c]$。",
                r"右极限减左极限得到 $\tau=E[Y(1)-Y(0)\mid X=c]$。",
            ],
            "reasons": ["确定处理规则", "潜在结果连续性", "左右极限相减"],
            "conclusion": "RDD 识别是阈值处的极限比较；离阈值越远，结论越依赖函数形式外推而非设计本身。",
        },
        "conditions": ["阈值规则和 running variable 事前确定", "潜在结果条件均值在阈值连续", "个体不能精确操纵阈值或需解释排序机制", "带宽选择、偏差修正和聚类结构配套"],
        "example": {"title": "例：考试分数资格线", "body": "资格在 60 分跳变。应绘制原始分箱均值和局部拟合，检查 60 分附近密度与预处理成绩；效应只适用于临界学生。"},
        "misconception": "“加入 5 次全局多项式并控制很多协变量就更可靠。”高阶全局拟合可产生虚假跳跃；协变量用于精度和诊断，不能替代连续性设计。",
        "check": {"question": "结果在阈值跳 4，处理概率跳 0.5。fuzzy RDD 点估计是多少，还需哪些解释条件？", "answer": "Wald 比率为 8。解释为阈值 complier LATE 还需连续性/局部独立、排除限制、单调性和有效第一阶段。", "diagnosis": "若答 4，漏除第一阶段；若答 ATE，回到局部 complier"},
        "takeaways": ["RDD 识别阈值处局部效应", "带宽体现设计可信度与精度权衡", "图形和操纵诊断必须与正式推断并列"],
        "practice": "Ch.21 sharp/fuzzy RDD、带宽与诊断题",
        "extensions": ["离散 running variable", "donut RDD", "回归 kink 设计"],
        "links": [("Ch.21 习题解答", "docs/ch21/Hansen_Ch21_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch21/Hansen_Ch21_Exercises_Solutions.md")],
    },
    {
        "number": 36, "semester": 2,
        "title": "M 估计与非线性最小二乘",
        "subtitle": "极值一致性、线性化与 sandwich 推断",
        "chapters": "Ch.22–23", "book_pages": "753–779", "pdf_pages": "773–799",
        "position": "用统一极值框架整理 OLS、MLE、分位数和非线性模型的共同证明",
        "objectives": ["用识别和一致收敛证明极值估计一致", "从一阶条件推导 M 估计渐近方差", "把 NLS 的函数形式、导数与识别分开核对"],
        "prerequisites": ["会做 Taylor 展开", "理解均匀收敛与点态收敛差别", "会求梯度和 Hessian"],
        "bridge": "本科非线性回归多从软件迭代开始；Hansen 先定义总体准则的唯一极值，再问样本准则是否整体靠近它。",
        "bridge_prompt": "为什么对每个固定参数点收敛，仍不保证样本最优点收敛？",
        "route": ["极值估计与识别", "一致收敛和 argmin", "一阶条件线性化", "NLS 的 Jacobian 与稳健方差"],
        "concepts": [
            {"title": "M 估计", "body": r"$\hat\theta=\arg\min_{\theta\in\Theta}Q_n(\theta)$，总体准则 $Q(\theta)=E[q(W_i,\theta)]$ 在 $\theta_0$ 唯一最小。识别是总体性质，不由优化器成功替代。"},
            {"title": "均匀收敛", "body": r"$\sup_{\theta\in\Theta}|Q_n(\theta)-Q(\theta)|\to_p0$ 防止样本准则在随 $n$ 移动的参数点出现虚假深谷；配合紧致性和唯一极小给 argmin 一致性。"},
            {"title": "sandwich 结构", "body": r"令得分 $\psi_i(\theta)=\partial q_i/\partial\theta$、$A=E[\partial\psi_i/\partial\theta']$、$B=E[\psi_i\psi_i']$，渐近方差为 $A^{-1}BA^{-1'}$。"},
            {"title": "非线性最小二乘", "body": r"$Y_i=m(X_i,\theta_0)+e_i$，NLS 最小化残差平方。条件均值正确给识别；导数 $D_i=\partial m(X_i,\theta_0)/\partial\theta$ 决定局部信息。"},
        ],
        "derivation": {
            "title": "M 估计的一阶线性化",
            "setup": r"内点解满足 $n^{-1}\sum_i\psi_i(\hat\theta)=0$。在 $\theta_0$ 展开。",
            "steps": [
                r"$0=n^{-1}\sum_i\psi_i(\theta_0)+\hat A(\tilde\theta)(\hat\theta-\theta_0)$。",
                r"乘 $\sqrt n$ 并求解：$\sqrt n(\hat\theta-\theta_0)=-\hat A^{-1}n^{-1/2}\sum_i\psi_i(\theta_0)$。",
                r"由 LLN、CLT 与 Slutsky，$\sqrt n(\hat\theta-\theta_0)\to N(0,A^{-1}BA^{-1'})$。",
            ],
            "reasons": ["向量均值定理", "矩阵求解", "LLN、CLT 与 Slutsky"],
            "conclusion": "一致性保证展开点靠近真值，Hessian 给局部曲率，得分方差给随机扰动；三者缺一不可。",
        },
        "conditions": ["总体准则唯一识别", "一致收敛与可测/矩包络条件", r"$A$ 非奇异", "边界、非光滑或多重极值需要不同理论"],
        "example": {"title": "例：指数增长曲线", "body": r"$m(x,\theta)=\theta_1\exp(\theta_2x)$。起始值不同可能落到不同数值解；应画准则、检查梯度并报告参数尺度，而非只信“converged”。"},
        "misconception": "“优化器收敛，所以估计量一致。”数值收敛只表示算法停止；统计一致还需模型识别、样本准则逼近总体准则和全局/足够好极值。",
        "check": {"question": r"若 $A$ 近乎奇异，点估计和推断会出现什么症状？", "answer": "准则在某方向很平，参数对数据和起始值敏感，标准误很大或数值不稳定。这是弱局部识别/参数化问题，不应靠增加迭代次数掩盖。", "diagnosis": "若只答优化慢，补充统计信息不足；若说 B 决定识别，区分曲率 A 与得分波动 B"},
        "takeaways": ["极值一致性是识别加均匀收敛", "M 估计方差仍是 sandwich", "数值成功不等于统计识别"],
        "practice": "Ch.22–23 极值一致性、M 估计线性化和 NLS 题",
        "extensions": ["非光滑 M 估计", "边界参数", "多起点和自动微分"],
        "links": [
            ("Ch.22 习题解答", "docs/ch22/Hansen_Ch22_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch22/Hansen_Ch22_Exercises_Solutions.md"),
            ("Ch.23 习题解答", "docs/ch23/Hansen_Ch23_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch23/Hansen_Ch23_Exercises_Solutions.md"),
        ],
    },
    {
        "number": 37, "semester": 2,
        "title": "分位数与离散选择",
        "subtitle": "条件分位数、二元/多项选择与边际效应",
        "chapters": "Ch.24–26", "book_pages": "780–841", "pdf_pages": "800–861",
        "position": "从条件均值扩展到分布位置和离散结果，同时保持估计对象—函数形式—效应解释分离",
        "objectives": ["解释分位数损失为何识别条件分位数", "区分 Logit/Probit 潜在指数系数与概率效应", "正确计算并汇总离散选择边际效应"],
        "prerequisites": ["知道分位数定义", "理解 M 估计与似然", "会用链式法则"],
        "bridge": "OLS 只描述条件均值；分位数回归考察条件分布不同位置，二元选择则把线性指数通过 CDF 映射到 0–1 概率。",
        "bridge_prompt": "Probit 系数为什么不能直接读成概率增加几个百分点？",
        "route": ["check loss 与条件分位数", "分位数回归推断", "二元响应概率", "边际效应与多项选择"],
        "concepts": [
            {"title": "分位数损失", "body": r"$\rho_\tau(u)=u\{\tau-1(u<0)\}$ 对正负残差不对称加权。条件于 $X=x$ 最小化 $E[\rho_\tau(Y-a)\mid X=x]$ 得条件 $\tau$ 分位数。"},
            {"title": "分位数回归对象", "body": r"设 $Q_\tau(Y\mid X)=X'\beta(\tau)$，不同 $\tau$ 的系数描述条件分布位置随 X 的变化；它不自动是同一个体潜在结果分位数效应。"},
            {"title": "二元响应", "body": r"$P(Y=1\mid X)=F(X'\beta)$。Logit 取 logistic CDF，Probit 取标准正态 CDF。概率被限制在 0–1，但指数尺度需规范化。"},
            {"title": "边际效应", "body": r"连续变量的概率边际效应为 $f(X'\beta)\beta_j$，随 X 改变。可报告样本平均边际效应；虚拟变量应计算 0→1 的离散概率差。"},
        ],
        "derivation": {
            "title": "check loss 识别分位数",
            "setup": r"固定 $X=x$，令 $Q(a)=E[\rho_\tau(Y-a)\mid X=x]$，考察对 $a$ 的次梯度。",
            "steps": [
                r"当 $Y\ne a$，$\partial\rho_\tau(Y-a)/\partial a=1(Y<a)-\tau$。",
                r"取条件期望得次梯度 $F_{Y\mid X}(a\mid x)-\tau$。",
                r"令零进入次梯度集合，即 $F(a^-\mid x)\le\tau\le F(a\mid x)$，这正是条件 $\tau$ 分位数定义。",
            ],
            "reasons": ["分段线性求导", "条件期望", "分位数集合定义"],
            "conclusion": "绝对值式不对称损失不是计算技巧，而是直接把目标对准条件分位数；非光滑性也决定了推断不同于 OLS。",
        },
        "conditions": ["条件分位数线性是函数形式假设", "分位点附近条件密度影响 QR 方差", "离散选择需避免完全预测", "边际效应必须说明评价点和变量单位"],
        "example": {"title": "例：教育与工资分布", "body": "教育在工资第 10、50、90 分位的系数不同，说明条件分布关联异质；不能直接说同一个人教育增加后的个体分位处理效应。"},
        "misconception": "“Probit 教育系数 0.2 表示入学概率提高 20 个百分点。”0.2 是潜在指数尺度；概率变化还乘密度并取决于其他协变量。",
        "check": {"question": r"在 Logit 中 $\hat\beta_j>0$，边际效应会不会为负？会不会对所有人相同？", "answer": r"因 logistic 密度为正，连续变量边际效应符号与 $\beta_j$ 相同；大小为 $f(X'\beta)\beta_j$，随 X 改变，不对所有人相同。", "diagnosis": "若直接答等于 beta，回到链式法则；若虚拟变量也求导，改用离散变化"},
        "takeaways": ["QR 改变的是条件分布目标", "离散选择系数处在指数尺度", "边际效应需报告评价方式和单位"],
        "practice": "Ch.24–26 分位数回归、二元与多项选择题",
        "extensions": ["分位数处理效应", "有序选择", "平均部分效应的半参数识别"],
        "links": [
            ("Ch.24 习题解答", "docs/ch24/Hansen_Ch24_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch24/Hansen_Ch24_Exercises_Solutions.md"),
            ("Ch.25 习题解答", "docs/ch25/Hansen_Ch25_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch25/Hansen_Ch25_Exercises_Solutions.md"),
            ("Ch.26 习题解答", "docs/ch26/Hansen_Ch26_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch26/Hansen_Ch26_Exercises_Solutions.md"),
        ],
    },
    {
        "number": 38, "semester": 2,
        "title": "删失、截断与样本选择",
        "subtitle": "Tobit、观测机制与排除变量",
        "chapters": "Ch.27", "book_pages": "842–858", "pdf_pages": "862–878",
        "position": "把“缺失或堆在边界的结果”建模为观测机制，并区分结果方程和选择方程",
        "objectives": ["区分删失、截断和选择样本", "解释 Tobit 系数与观察结果边际效应", "推导正态选择模型中的逆 Mills 修正"],
        "prerequisites": ["理解潜变量二元选择", "知道条件正态公式", "会区分识别与函数形式外推"],
        "bridge": "本科常把零消费观测删掉或直接 OLS；研究生计量先问零是真实结果、左删失，还是样本从未被观察。三者的似然和目标不同。",
        "bridge_prompt": "只在就业者中回归工资，误差条件均值为什么可能不再为零？",
        "route": ["观测机制分类", "Tobit 潜变量", "选择方程与截断均值", "排除变量和敏感性"],
        "concepts": [
            {"title": "删失与截断", "body": "删失时边界观测仍在样本，如支出低于检测限记为 0；截断时这部分个体完全不进入数据。二者对总体规模和似然贡献不同。"},
            {"title": "Tobit 潜变量", "body": r"$Y^*=X'\beta+u$、$Y=\max(0,Y^*)$。同一参数同时约束参与概率和正值结果；若两个过程不同，这个限制会错设。"},
            {"title": "样本选择", "body": r"结果 $Y=X'\beta+u$ 仅当 $S=1\{Z'\gamma+v>0\}$ 被观察。若 $u$ 与 $v$ 相关，$E[u\mid X,Z,S=1]\ne0$。"},
            {"title": "排除变量", "body": "依靠正态非线性也可形式识别，但往往脆弱。最好有影响观察/参与、却不直接影响结果的 Z 变量，并给制度论证。"},
        ],
        "derivation": {
            "title": "选择样本中的逆 Mills 项",
            "setup": r"设 $(u,v)$ 联合正态，$\operatorname{cov}(u,v)=\sigma_{uv}$、$\operatorname{var}(v)=1$，观察条件为 $v>-Z'\gamma$。",
            "steps": [
                r"联合正态条件均值给 $E[u\mid v]=\sigma_{uv}v$。",
                r"对截断事件再取期望：$E[v\mid v>-Z'\gamma]=\phi(Z'\gamma)/\Phi(Z'\gamma)=\lambda(Z'\gamma)$。",
                r"所以 $E[Y\mid X,Z,S=1]=X'\beta+\sigma_{uv}\lambda(Z'\gamma)$；省略该项会把选择相关混入斜率。",
            ],
            "reasons": ["联合正态线性条件均值", "截断正态均值", "迭代期望"],
            "conclusion": "Heckman 两步修正高度依赖联合正态和选择方程；逆 Mills 项不是通用控制变量，排除限制决定可信度。",
        },
        "conditions": ["明确边界值的实际生成机制", "Tobit 的正态同方差和单指数限制需诊断", "选择模型最好有可信排除变量", "严重删失/弱排除导致外推不稳定"],
        "example": {"title": "例：就业者工资", "body": "托儿服务距离可能影响就业但未必直接影响市场工资，可作选择排除候选；若也影响可去岗位范围，排除限制就需重新评估。"},
        "misconception": "“样本量大后只在观察样本 OLS 就没问题。”选择偏误是错误条件均值，不随样本量消失；大样本只会更精确地估计错误目标。",
        "check": {"question": "家庭支出数据中大量精确零值，何时不应使用 Tobit？", "answer": "若零是实际最优选择而非潜在连续支出的删失，或参与与正值强度由不同机制决定，应考虑 two-part/hurdle 等模型，而非 Tobit 单一潜变量。", "diagnosis": "若仅凭零多就用 Tobit，要求先写观测机制"},
        "takeaways": ["先分类观测机制，再选模型", "Tobit 系数不是观察结果的统一边际效应", "选择修正的可信度依赖排除限制"],
        "practice": "Ch.27 Tobit、截断与样本选择题",
        "extensions": ["two-part model", "半参数选择模型", "区间删失"],
        "links": [("Ch.27 习题解答", "docs/ch27/Hansen_Ch27_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch27/Hansen_Ch27_Exercises_Solutions.md")],
    },
    {
        "number": 39, "semester": 2,
        "title": "模型选择与机器学习",
        "subtitle": "预测风险、正则化、树/森林与双重机器学习",
        "chapters": "Ch.28–29", "book_pages": "859–944", "pdf_pages": "879–964",
        "position": "在全年结尾区分预测优化和因果估计，并用正交化连接现代高维方法",
        "objectives": ["用训练/验证/测试划分定义预测风险", "解释 Lasso 与树模型的复杂度控制", "推导部分线性模型的正交残差矩与 cross-fitting"],
        "prerequisites": ["理解样本外损失", "知道偏差—方差权衡", "会用 FWL 残差化"],
        "bridge": "传统计量从低维参数和可解释标准误出发；机器学习擅长高维预测。把 ML 用于因果时，仍必须先给识别，再用正交得分控制 nuisance 估计误差。",
        "bridge_prompt": "交叉验证预测最好，为什么不等于因果效应最可信？",
        "route": ["风险与数据划分", "收缩和选择", "树/森林与模型平均", "DML 的正交化和交叉拟合"],
        "concepts": [
            {"title": "预测风险", "body": r"目标为新样本损失 $R(f)=E[L(Y,f(X))]$。训练误差用于拟合，验证/CV 用于调参，独立测试集只作最终一次评估，避免信息泄漏。"},
            {"title": "Lasso 与选择", "body": r"$\min_\beta n^{-1}\sum(Y_i-X_i'\beta)^2+\lambda\|\beta\|_1$。$\lambda$ 越大越收缩并产生稀疏；选择后的普通 OLS p 值一般忽略了搜索过程。"},
            {"title": "树与森林", "body": "树递归切分并易高方差；装袋和随机森林通过重抽与随机特征平均降方差。变量重要性是预测贡献，不自动是结构效应。"},
            {"title": "DML 思路", "body": r"部分线性模型 $Y=\theta D+g(X)+u$、$D=m(X)+v$。用 ML 估计 $g,m$，再以 cross-fitting 的残差估计 $\theta$，避免同样本过拟合偏差。"},
        ],
        "derivation": {
            "title": "正交残差矩",
            "setup": r"令 $\tilde Y=Y-E[Y\mid X]$、$\tilde D=D-E[D\mid X]$。目标是从高维 X 中分离 D 的剩余变化。",
            "steps": [
                r"由模型与迭代期望，$\tilde Y=\theta_0\tilde D+u$，且 $E[\tilde D\,u]=0$。",
                r"矩条件 $E[(D-m(X))\{Y-g(X)-\theta(D-m(X))\}]=0$ 在真 nuisance 附近对一阶估计误差不敏感。",
                r"分折估计 $g,m$ 并在未参与训练的折上构造残差；合并后 $\hat\theta=\sum\tilde D_i\tilde Y_i/\sum\tilde D_i^2$，再用正交得分方差推断。",
            ],
            "reasons": ["FWL 与条件期望", "Neyman 正交性", "cross-fitting 和样本矩"],
            "conclusion": "DML 允许灵活 nuisance，但不创造因果识别；仍需部分线性结构、条件外生性、重叠和足够快的预测误差收敛。",
        },
        "conditions": ["训练、调参与最终评估隔离", "正则化参数选择规则预先说明", "DML 需要正交得分和 cross-fitting", "高维弱信号、重叠差和选择后推断需谨慎"],
        "example": {"title": "例：高维工资预测与教育效应", "body": "随机森林可能很好预测工资，却把教育与家庭背景共同使用。教育因果效应仍需条件外生或 IV；DML 只帮助灵活控制高维混杂。"},
        "misconception": "“CV 最优模型就是正确模型，因此变量重要性可作因果效应。”CV 优化指定分布下的预测损失，不验证反事实识别或干预稳定性。",
        "check": {"question": "为何 cross-fitting 要在未训练 nuisance 的观测上计算残差得分？", "answer": "它削弱过拟合造成的自身残差相关，使 nuisance 误差更接近外部预测误差，并配合正交性得到可控余项；它不是增加样本的技巧。", "diagnosis": "若说为了更高 R²，回到推断目的；若说完全消除偏差，补充仍需率条件和识别"},
        "takeaways": ["预测风险与因果参数是不同目标", "正则化选择会改变普通推断", "DML 是识别加正交化加交叉拟合"],
        "practice": "Ch.28–29 风险、收缩、树/森林、正交得分与 DML 题",
        "extensions": ["causal forests", "debiased Lasso", "分布漂移与外部有效性"],
        "links": [
            ("Ch.28 习题解答", "docs/ch28/Hansen_Ch28_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch28/Hansen_Ch28_Exercises_Solutions.md"),
            ("Ch.29 教材配套材料", "docs/ch29", "https://github.com/sunfang3/hansen-econometrics-solutions/tree/master/docs/ch29"),
        ],
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


WORKSHOP_SESSIONS += [
    {
        "number": 25, "semester": 2,
        "title": "时间序列建模与 HAC",
        "subtitle": "AR(1) 诊断、长期方差与多步预测",
        "chapters": "Ch.14", "book_pages": "442–508", "pdf_pages": "462–528",
        "position": "把平稳、MDS、动态回归和 HAC 落到一条可复现序列",
        "objectives": ["估计并诊断稳定 AR(1)", "手工计算 Bartlett–HAC 方差", "报告递推预测及其设定边界"],
        "prerequisites": ["会判断 AR 根稳定性", "知道长期方差含滞后协方差", "能解释样本内拟合与样本外预测"],
        "research_question": "一条均值回复序列的持久性有多强？残差是否仍含线性依赖？HAC 与模型式预测分别解决什么问题？",
        "data_status": "::: {.data-status}\n使用固定种子 20260802 自生成 AR(1)，无需外部包或教材数据；示例输出由 base R 预计算。\n:::",
        "sample": r"先生成 340 期并丢弃前 100 期，保留 $T=240$，减轻初值影响。时间顺序绝不随机打散。",
        "variables": r"$Y_t=2(1-0.65)+0.65Y_{t-1}+u_t$，$u_t\sim N(0,1)$。均值 2、稳定根 0.65；代码只观察 $Y_t$。",
        "identification": r"AR 系数由 $E[Y_{t-1}u_t]=0$ 识别。模拟创新 i.i.d.；HAC 只修正回归得分方差。",
        "estimator": "同时用 arima 的 AR(1) 似然和带截距 OLS 动态回归。比较参数化模型 SE 与 Bartlett–HAC（带宽 4）SE。",
        "inference": "HAC 带宽固定为 4 作教学比较，并报告改为 2、8 的敏感性。多步点预测由估计 AR 递推；正式区间还应加入未来创新和参数不确定性。",
        "workflow": "生成并去 burn-in → 时序图/ACF → AR(1) → 残差 ACF → 手工 HAC → 4 步预测 → 带宽和阶数敏感性。",
        "code_setup": clean(r"""
            ~~~r
            set.seed(20260802)
            n <- 240L
            u <- rnorm(n + 100L)
            y <- numeric(n + 100L)
            for (tt in 2:length(y)) {
              y[tt] <- 2 * (1 - 0.65) + 0.65 * y[tt - 1] + u[tt]
            }
            y <- tail(y, n)
            fit_ml <- arima(y, order = c(1, 0, 0), include.mean = TRUE)
            fit_ols <- lm(y[-1] ~ y[-n])
            ~~~
        """),
        "code_estimate": clean(r"""
            ~~~r
            X <- model.matrix(fit_ols)
            e <- resid(fit_ols)
            bread <- solve(crossprod(X))
            meat <- crossprod(X, X * e^2)
            L <- 4L
            for (j in seq_len(L)) {
              w <- 1 - j / (L + 1)
              Gj <- crossprod(X[(j + 1):nrow(X), ] * e[(j + 1):length(e)],
                              X[1:(nrow(X) - j), ] * e[1:(length(e) - j)])
              meat <- meat + w * (Gj + t(Gj))
            }
            V_hac <- nrow(X) / (nrow(X) - ncol(X)) *
              bread %*% meat %*% bread
            ~~~
        """),
        "results": "| 对象 | 预计算值 |\n|---|---:|\n| ML 的 $\\hat\\rho$ | 0.704 |\n| ML 长期均值 | 2.066 |\n| OLS 的 $\\hat\\rho$ | 0.707 |\n| OLS SE / HAC(4) SE | 0.0460 / 0.0465 |\n| ML 残差一阶 ACF | 0.019 |\n| 未来 1–4 期点预测 | 1.468, 1.645, 1.770, 1.857 |",
        "diagnostics": r"检查伴随根 $|\hat\rho|<1$、残差 ACF 和平方残差 ACF。残差一阶 ACF 接近零只支持线性动态已大致吸收，不证明独立或正态。",
        "sensitivity": "比较 AR(0)、AR(1)、AR(2) 的信息准则与滚动预测误差；HAC 带宽改为 2、8。预测评价必须保持时间顺序。",
        "misconception": "把 HAC SE 和 AR 模型当成可互换修正。前者改变推断方差，后者改变条件均值与预测；若动态均值错设，仅换 HAC 不会修好预测。",
        "check": {"question": r"若 $\hat\rho=0.98$ 且样本只有 80 期，为什么不能只因 $|\hat\rho|<1$ 就放心用平稳近似？", "answer": "近单位根时均值回复极慢，有限样本分布接近单位根非标准情形；应报告持久性区间和更谨慎预测。", "diagnosis": "若只说根小于 1，区分点估计分类与近单位根近似质量"},
        "takeaways": ["模型动态与 HAC 推断承担不同任务", "预测验证必须尊重时间顺序", "根接近 1 时要承认近单位根不确定性"],
        "practice": "提交带宽 2/4/8 的 SE 表、AR(1)/AR(2) 诊断与四步预测图",
        "extensions": ["rolling-origin cross-validation", "ARCH 检验与 GARCH", "局部投影预测"],
        "links": [("Ch.14 习题解答", "docs/ch14/Hansen_Ch14_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch14/Hansen_Ch14_Exercises_Solutions.md")],
    },
    {
        "number": 29, "semester": 2,
        "title": "VAR、单位根与协整",
        "subtitle": "从设定、非标准临界值到长期秩的诊断链",
        "chapters": "Ch.15–16", "book_pages": "509–596", "pdf_pages": "529–616",
        "position": "把平稳系统和非平稳检验放在同一流程中，防止先回归后判断",
        "objectives": ["估计二维 VAR 并核对稳定根", "按确定性项和滞后写 ADF 回归", "用协整残差与 Johansen 思路解释长期关系"],
        "prerequisites": ["会读 VAR 系数矩阵", "知道 DF 统计量不用普通 t 临界值", "理解协整秩与共同趋势"],
        "research_question": "面对多条持久序列，应如何依次判断动态阶数、单位根、长期组合和结构冲击，而不把软件默认值当结论？",
        "data_status": "::: {.data-status}\n固定种子 20260802，生成 $T=220$ 的稳定二维 VAR、一个随机游走和一对协整序列；base R 可完整复现。Johansen 作为可选 urca 扩展。\n:::",
        "sample": "VAR 先生成 270 期并丢弃 50 期；单位根和协整样本均为 220 期。各检验的有效样本因差分和滞后减少，输出必须报告。",
        "variables": r"VAR 真值 $A=\begin{pmatrix}.5&.2\\-.1&.4\end{pmatrix}$；随机游走为创新累积；协整对满足 $y_t=1.5x_t+v_t$、$v_t$ 为稳定 AR(1)。",
        "identification": "VAR 首先是约化式预测系统。ADF 的零假设是单位根；协整残差平稳识别统计长期组合。任何 SVAR 结构标签仍需独立限制。",
        "estimator": "逐方程 OLS 估 VAR(1)；ADF(1) 含截距回归；Engle–Granger 先估长期斜率，再对生成残差做 ADF。残差检验需协整专用临界值。",
        "inference": "不报告 lm 自动生成的普通 ADF p 值。课堂把 t 统计量与对应 DF/EG 临界值表比较；Johansen trace/max-eigen 也需匹配确定性项。",
        "workflow": "时序图 → 水平/差分 ACF → 确定性项与滞后 → ADF/KPSS 互补 → VAR 稳定根 → 协整秩 → ECM → 最后讨论结构 IRF。",
        "code_setup": clean(r"""
            ~~~r
            set.seed(20260802)
            TT <- 220L
            A <- matrix(c(.5, .2, -.1, .4), 2, 2, byrow = TRUE)
            Y <- matrix(0, TT + 50L, 2)
            for (tt in 2:nrow(Y)) {
              e1 <- rnorm(1)
              e2 <- .4 * e1 + sqrt(1 - .4^2) * rnorm(1)
              Y[tt, ] <- A %*% Y[tt - 1, ] + c(e1, e2)
            }
            Y <- tail(Y, TT)
            ~~~
        """),
        "code_estimate": clean(r"""
            ~~~r
            var1 <- lm(Y[-1, 1] ~ Y[-TT, 1] + Y[-TT, 2])
            var2 <- lm(Y[-1, 2] ~ Y[-TT, 1] + Y[-TT, 2])
            rw <- cumsum(rnorm(TT))
            x_ci <- cumsum(rnorm(TT))
            v_ci <- as.numeric(arima.sim(list(ar = .5), n = TT))
            y_ci <- 1.5 * x_ci + v_ci
            coint_fit <- lm(y_ci ~ x_ci)
            # ADF 应显式构造 Δy、y_{t-1} 和滞后 Δy，
            # 再使用与常数/趋势设定一致的 DF 或 EG 临界值。
            ~~~
        """),
        "results": "| 结果 | 预计算值 |\n|---|---:|\n| VAR 方程 1 滞后系数 | 0.439, 0.264 |\n| VAR 方程 2 滞后系数 | -0.051, 0.382 |\n| 真伴随根模 | 0.469, 0.469 |\n| 随机游走 ADF(1) t | -2.149（不能查普通 t） |\n| 协整斜率 | 1.416 |\n| 协整残差 ADF(1) t | -7.978（用 EG 临界值） |",
        "diagnostics": "对 ADF 残差检查剩余自相关；改变常数/趋势和滞后。对 VAR 检查所有根和残差互相关；对协整检查关系是否由结构突变驱动。",
        "sensitivity": "ADF 滞后取 0–4；以 KPSS 平稳原假设作互补；VAR 阶数取 1–3；协整关系加入趋势并改变样本端点。",
        "misconception": "把 ADF 不拒绝、KPSS 拒绝和 Johansen 选秩当成自动真相。它们都依赖确定性项、滞后、窗口和结构稳定性。",
        "check": {"question": "ADF 不拒绝单位根、KPSS 也不拒绝平稳，是否矛盾？", "answer": "不矛盾。两个检验原假设相反，有限样本都可能功效不足；应报告不确定性、图形和设定敏感性。", "diagnosis": "若称序列既平稳又单位根，回到“不拒绝不是证明”"},
        "takeaways": ["先决定确定性项和滞后，再解释检验", "DF/EG/Johansen 使用各自非标准临界值", "约化动态和结构冲击严格分开"],
        "practice": "提交 ADF/KPSS 设定表、VAR 根和协整敏感性说明",
        "extensions": ["Johansen 系统实现", "结构突变检验", "SVAR 外部工具"],
        "links": [
            ("Ch.15 习题解答", "docs/ch15/Hansen_Ch15_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch15/Hansen_Ch15_Exercises_Solutions.md"),
            ("Ch.16 习题解答", "docs/ch16/Hansen_Ch16_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch16/Hansen_Ch16_Exercises_Solutions.md"),
        ],
    },
    {
        "number": 33, "semester": 2,
        "title": "面板、动态 GMM 与 DiD",
        "subtitle": "个体内识别、聚类和设计诊断",
        "chapters": "Ch.17–18", "book_pages": "597–664", "pdf_pages": "617–684",
        "position": "把静态 FE、动态面板工具和 DiD 反事实放入一份面板审计表",
        "objectives": ["复现双向 FE/DiD 并手工个体聚类", "比较普通与聚类标准误", "为动态面板写出工具和 AR(2) 诊断"],
        "prerequisites": ["会做 within 和双向 FE", "知道 AB 滞后工具条件", "能陈述 DiD 平行趋势"],
        "research_question": "一项在第 5 期对半数个体实施的政策如何估计？个体序列相关、固定效应和动态结果分别要求哪些处理？",
        "data_status": "::: {.data-status}\n固定种子 20260802，自生成平衡面板 $N=80,T=8$；真实政策效应 1.2。代码仅用 base R。\n:::",
        "sample": "640 个个体—时期观测。前 40 个体自第 5 期持续处理，后 40 个从未处理；没有缺失和错位实施，以隔离聚类与 FE。",
        "variables": r"$Y_{it}=\alpha_i+\lambda_t+0.4X_{it}+1.2D_{it}+u_{it}$；$u_{it}$ 个体内 AR(1)，系数 0.5；$X$ 与 $\alpha_i$ 有相关。",
        "identification": "基准设计以无提前反应和未处理趋势平行为识别。个体 FE 处理时间不变相关异质性，时间 FE 处理共同冲击；二者不消除差异趋势。",
        "estimator": "用含个体和时间虚拟变量的 OLS 实现双向 FE；对个体簇的 score 求和构造 cluster sandwich。动态扩展另写差分方程和滞后水平工具。",
        "inference": "处理在个体层变化且误差个体内相关，按个体聚类。只有 80 簇时报告簇数和自由度修正；若政策在更高地区层分配，应上移聚类层级。",
        "workflow": "面板键唯一性 → 每期处理份额 → 个体内变换 → TWFE → 个体聚类 → 事件时间图 → 动态规格的 AR(2)/工具数 → 设计敏感性。",
        "code_setup": clean(r"""
            ~~~r
            set.seed(20260802)
            N <- 80L; TT <- 8L
            id <- rep(seq_len(N), each = TT)
            tt <- rep(seq_len(TT), N)
            alpha <- rnorm(N)
            x <- rnorm(N * TT) + rep(.3 * alpha, each = TT)
            treat <- rep(as.integer(seq_len(N) <= 40), each = TT) *
              as.integer(tt >= 5)
            # 完整源码继续按个体生成 AR(1) 误差与时间效应。
            ~~~
        """),
        "code_estimate": clean(r"""
            ~~~r
            fit <- lm(y ~ treat + x + factor(id) + factor(tt))
            X <- model.matrix(fit)
            e <- resid(fit)
            bread <- solve(crossprod(X))
            score_g <- rowsum(X * e, id, reorder = FALSE)
            G <- nrow(score_g); nobs <- nrow(X); k <- ncol(X)
            V_cl <- G / (G - 1) * (nobs - 1) / (nobs - k) *
              bread %*% crossprod(score_g) %*% bread
            ~~~
        """),
        "results": "| 规格 | 政策系数 | SE |\n|---|---:|---:|\n| 无个体/时间 FE | 1.226 | — |\n| 双向 FE，i.i.d. SE | 1.146 | 0.135 |\n| 双向 FE，个体聚类 SE | 1.146 | 0.218 |\n\n观测数 640、个体簇 80；真实效应 1.2。",
        "diagnostics": "验证个体—时期键唯一、处理吸收路径正确。事件研究检查预趋势；动态面板报告差分残差 AR(1)/AR(2)、工具数和折叠/滞后限制。",
        "sensitivity": "加入组别线性趋势；删去可能提前反应窗口；动态模型比较 FE、差分 GMM 和限制工具的系统 GMM。",
        "misconception": "因聚类 SE 较大就改回普通 SE 以保持显著。标准误由抽样和依赖结构决定，不能按结果选择；FE 系数仍依赖平行趋势。",
        "check": {"question": "若政策由 10 个省实施，数据有 1000 家企业，应按企业还是省聚类？", "answer": "至少按政策分配和共同冲击所在的省聚类；1000 家企业不等于 1000 个独立政策实验。只有 10 簇时还需少簇修正。", "diagnosis": "若按企业，回到处理分配层级；若双向聚类，仍需说明第二维来源"},
        "takeaways": ["FE、GMM、DiD 解决不同识别问题", "聚类层级由独立冲击和处理分配决定", "动态面板必须公开工具矩阵和诊断"],
        "practice": "提交聚类手算核对、事件研究设定和一页 AB 工具矩阵",
        "extensions": ["异质稳健 staggered DiD", "wild cluster bootstrap", "Mundlak RE 对照"],
        "links": [
            ("Ch.17 习题解答", "docs/ch17/Hansen_Ch17_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch17/Hansen_Ch17_Exercises_Solutions.md"),
            ("Ch.18 习题解答", "docs/ch18/Hansen_Ch18_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch18/Hansen_Ch18_Exercises_Solutions.md"),
        ],
    },
    {
        "number": 40, "semester": 2,
        "title": "全年综合项目",
        "subtitle": "从研究问题、识别、估计到局部推断的完整闭环",
        "chapters": "Ch.19–29；全年整合", "book_pages": "666–944", "pdf_pages": "686–964",
        "position": "用一个 sharp RDD 项目复用全年四层框架并完成课程交付",
        "objectives": ["写出明确局部因果对象和连续性假设", "实现局部线性 RDD 与 HC1 方差", "用带宽、密度/协变量和外推边界完成审计"],
        "prerequisites": ["会做局部线性和 robust SE", "理解 RDD 左右极限识别", "能区分预测拟合、统计显著和政策外推"],
        "research_question": "资格分数跨过 0 是否提高结果？目标是阈值处平均处理效应，而非全样本平均；最终报告必须从制度规则讲到局部区间。",
        "data_status": "::: {.data-status}\n固定种子 20260802，生成 $n=2000$ 的 sharp RDD；真实阈值效应 1.2。无外部依赖，适合作为结课模板。\n:::",
        "sample": r"$X\sim U[-3,3]$，处理 $D=1\{X\ge0\}$。主带宽 $h=1$；同时报告 0.6 和 1.5。不得删除不利结果后才宣布主带宽。",
        "variables": r"$Y=1+0.5X+0.3X^2+1.2D+0.2DX+u$，$u\sim N(0,0.9^2)$。曲率刻意让宽带宽产生可见函数形式偏差。",
        "identification": r"Sharp 规则、阈值处潜在结果连续、无法精确操纵 $X$。模拟中条件成立；实际项目必须用制度细节、密度和预处理协变量诊断。",
        "estimator": r"在 $|X|\le h$ 内估 $Y=\alpha+\tau D+\beta_-X+\delta(DX)+e$，即阈值两侧独立局部线性斜率；$\hat\tau$ 为阈值跳跃。",
        "inference": "主表用 HC1 作教学实现，并明确正式 RDD 应采用带宽选择与 robust bias correction 配套区间。若 running variable 有簇或重复值，还要调整方差。",
        "workflow": "研究对象 → 制度/样本 → running variable 图 → 密度/协变量 → 预定主带宽 → 局部线性 → robust 区间 → 带宽敏感性 → 外推限制。",
        "code_setup": clean(r"""
            ~~~r
            set.seed(20260802)
            n <- 2000L
            x <- runif(n, -3, 3)
            d <- as.integer(x >= 0)
            y <- 1 + .5 * x + .3 * x^2 + 1.2 * d +
              .2 * d * x + rnorm(n, sd = .9)
            ~~~
        """),
        "code_estimate": clean(r"""
            ~~~r
            rd_once <- function(h) {
              keep <- abs(x) <= h
              fit <- lm(y ~ d + x + d:x, subset = keep)
              X <- model.matrix(fit); e <- resid(fit)
              nn <- nrow(X); kk <- ncol(X)
              bread <- solve(crossprod(X))
              V <- nn / (nn - kk) * bread %*%
                crossprod(X, X * e^2) %*% bread
              c(tau = coef(fit)["d"], se = sqrt(V["d", "d"]), n = nn)
            }
            sapply(c(.6, 1, 1.5), rd_once)
            ~~~
        """),
        "results": "| 带宽 $h$ | $\\hat\\tau$ | HC1 SE | 局部样本 |\n|---:|---:|---:|---:|\n| 0.6 | 1.427 | 0.172 | 404 |\n| 1.0（主） | 1.282 | 0.130 | 676 |\n| 1.5 | 1.273 | 0.106 | 1008 |\n\n真阈值效应 1.2；宽带宽更精确但依赖更远处函数形状。",
        "diagnostics": "同时画原始分箱均值、左右局部线性、running variable 密度和预处理协变量。模拟密度连续；真实数据出现堆积时必须解释制度。",
        "sensitivity": "带宽网格 0.4–1.8、删去阈值极近观测的 donut 规格、局部二次仅作对照；明确哪些改变 estimand，哪些只改变估计近似。",
        "misconception": "从多个带宽中挑最显著的一个作主结果。这把研究者选择引入推断；主设定应由设计和预先规则决定，敏感性表完整呈现。",
        "check": {"question": "主带宽结果显著且密度检验不拒绝连续，能否把 1.282 外推为所有分数者的平均政策效应？", "answer": "不能。RDD 识别阈值处局部效应；密度不拒绝也只是诊断。外推需要额外结构、实验或可辩护同质性。", "diagnosis": "若答能，区分内部局部识别与外部有效性；若只看显著性，回到 estimand"},
        "takeaways": ["最终报告按对象—识别—估计—推断—限制闭环", "每个敏感性改变都要说明理由", "可复现代码、固定数字表和谨慎语言同等重要"],
        "practice": "提交 6 页项目报告、可运行 QMD、固定结果表、诊断图和 3 分钟口头汇报",
        "extensions": ["替换为本地 Hansen 数据的研究设计", "fuzzy RDD 与弱第一阶段", "DML 控制高维协变量但不替代 RDD 识别"],
        "links": [
            ("Ch.21 习题解答", "docs/ch21/Hansen_Ch21_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch21/Hansen_Ch21_Exercises_Solutions.md"),
            ("Ch.28 习题解答", "docs/ch28/Hansen_Ch28_Exercises_Solutions.md", "https://github.com/sunfang3/hansen-econometrics-solutions/blob/master/docs/ch28/Hansen_Ch28_Exercises_Solutions.md"),
        ],
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
