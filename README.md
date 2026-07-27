# Hansen Econometrics Solutions

Bruce E. Hansen《Econometrics》习题解答（按 Hansen 体系完整解题）。

## 章节进度

| 章节 | 内容 | 书稿 PDF 页（约） | 格式 |
|------|------|------------------|------|
| Ch.2 | Conditional Expectation and Projection | 80–81 | `.md` / `.ipynb` |
| Ch.3 | The Algebra of Least Squares | 112–116 | `.md` / `.ipynb` |
| Ch.4 | Least Squares Regression | 152–156 | `.md` / `.ipynb` |
| Ch.5 | Normal Regression | 172–173 | `.md` / `.ipynb` |
| Ch.7 | Asymptotic Theory for Least Squares | 209–215 | `.md` / `.ipynb` |
| **Ch.8** | **Restricted Estimation** | **238–240** | **`.md` / `.ipynb`** |
| **Ch.9** | **Hypothesis Testing** | **270–276** | **`.md` / `.ipynb`** |
| **Ch.10** | **Resampling Methods**（**10.1–10.31 全文**） | **321–325** | **`.md` / `.ipynb`** |
| Ch.29 | Machine Learning | 943 等 | `.md` / `.qmd` / `.html` |

解答位于 `docs/chXX/`。

## 数据

教材数据请从 Hansen 官网下载：

- https://users.ssc.wisc.edu/~bhansen/econometrics/

常用子集：`cps09mar`、`Invest1993`、`Nerlove1963`、`MRW1992`、`DDK2011`。

Notebook 中数据路径指向本地 `hansen/econometrics/data/...`（该目录被 `.gitignore` 忽略，需自行下载）。

## 运行

```bash
jupyter notebook docs/ch09/Hansen_Ch09_Exercises_Solutions.ipynb
```

## 许可说明

习题来自 Hansen 公开讲义/教材；解答仅供学习参考。正式出版教材版权归 Princeton University Press / 作者所有。
