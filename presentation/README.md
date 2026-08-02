# Hansen《Econometrics》全年中文 Quarto 课程

本目录是一套面向本科计量经济学基础学生的研究生过渡课程：40 次、每次 90 分钟，其中 32 次主课、8 次工作坊。课堂演示、教学大纲和 7 份补充阅读材料均以中文 Quarto 源文件维护。

## 目录

| 路径 | 内容 |
|---|---|
| index.qmd | 课程主页与 40 次课入口 |
| syllabus.qmd | 全年大纲、Hansen 页码和掌握门槛 |
| sessions/ | 40 份 RevealJS 课堂演示 |
| supplements/ | 7 份可滚动 HTML 补充讲义 |
| scripts/generate_sessions.py | 课堂内容规格与机械生成器 |
| scripts/check_course.py | 静态课程质量检查 |
| scripts/render.sh | 生成、测试、检查、渲染的一键入口 |

sessions/01–40 的 QMD 由 generate_sessions.py 生成。修改课堂内容时应编辑生成器中的对应课程规格，再重新生成；不要只改生成文件，否则下次生成会覆盖该改动。

## 一键构建

在仓库根目录运行：

~~~bash
presentation/scripts/render.sh
~~~

脚本依次：

1. 重新生成 40 份课堂 QMD；
2. 运行检查器单元测试；
3. 检查 40/32/8、90 分钟元数据、固定区块、讲者备注、Hansen 页码、本地链接、占位符和图片替代文本；
4. 真实渲染课程主页、教学大纲、40 份课件与 7 份补充讲义。

本机 Quarto 不在 PATH 时可显式指定：

~~~bash
QUARTO_BIN=/opt/quarto/bin/quarto presentation/scripts/render.sh
~~~

当前验证环境为 Quarto 1.10.18。课程默认 execute.enabled: false，因此常规 HTML 构建不执行 R，也不要求先安装全部实证包。

## 分步使用

只检查源文件：

~~~bash
python3 presentation/scripts/check_course.py
~~~

只渲染：

~~~bash
quarto render presentation
~~~

开发时预览：

~~~bash
quarto preview presentation
~~~

教师版配置：

~~~bash
quarto render presentation --profile instructor
~~~

## 讲者视图与 PDF

打开任一 RevealJS 课件后：

- 按 S 打开包含当前页、下一页、计时和中文讲者备注的讲者视图；
- 按 O 查看全局缩略图；
- 在课件地址后加入 ?print-pdf 后使用浏览器“打印为 PDF”。

PDF 导出需要 Chromium/Chrome 等可打印浏览器。当前仓库的质量门槛以 HTML 真渲染为必选项；没有浏览器时不会伪装成已经完成 PDF 验收。

## 数据与复现

工作坊课件内的主示例均使用固定种子和已核对的数值结果，因此没有 hansen/ 数据目录时仍能构建。复现教材经验练习时，数据路径统一指向：

~~~text
hansen/econometrics/data/...
~~~

该目录被 Git 忽略，需要授课者按教材数据说明自行下载。代码块默认不在课程构建中运行；课堂复现时应先记录 R 版本、包版本、样本筛选、变量变换、聚类层级和随机种子。

## 输出与版本控制

渲染结果位于 presentation/_output/，Quarto 缓存位于 presentation/.quarto/；两者均被 Git 忽略。提交时只提交 QMD、配置、样式、脚本和必要素材，不提交构建产物或教材数据。
