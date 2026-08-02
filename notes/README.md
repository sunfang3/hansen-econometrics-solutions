# Hansen《Econometrics》详细中文学习笔记

notes/ 是独立的 Quarto Book 项目。章节按原书顺序编排，正文使用中文，Hansen 原书公式保留原编号并提供稳定锚点。

构建：

~~~bash
quarto render notes
~~~

质量检查：

~~~bash
python3 notes/scripts/check_notes.py
python3 notes/scripts/check_notes.py --scope appendices
quarto render notes && python3 notes/scripts/check_notes.py --scope chapters-1-2 --rendered
~~~

章节写作要求：

- 每节说明原书位置、问题、条件、路线、推导和结论；
- 非显然步骤不能只写“显然”“类似可得”；
- 矩阵首次出现时说明维数；
- Hansen 公式使用原书编号，教学补充公式不占用原书编号；
- 章节达到内容和结构门槛后才加入 _quarto.yml。
