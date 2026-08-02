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


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    expected = {spec["number"] for spec in MAIN_SESSIONS}
    if len(expected) != len(MAIN_SESSIONS):
        raise ValueError("DUPLICATE_SESSION_NUMBER")
    for spec in MAIN_SESSIONS:
        slug = {
            1: "course-orientation",
            2: "matrix-algebra-i",
            3: "matrix-algebra-ii",
            4: "probability-conditioning",
            5: "cef-and-projection",
            6: "least-squares-algebra",
        }[spec["number"]]
        target = OUT / f"{spec['number']:02d}-{slug}.qmd"
        target.write_text(render_main(spec), encoding="utf-8")
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
