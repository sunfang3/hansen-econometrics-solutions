## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.3 Algebra of OLS — Frisch-Waugh residual regression
set.seed(2)
n <- 200L
X1 <- rnorm(n); X2 <- rnorm(n); e <- rnorm(n)
Y <- 1 + X1 + 2*X2 + e
## residual regression of Y,X1 after partialling X2
M2Y <- resid(lm(Y ~ X2))
M2X1 <- resid(lm(X1 ~ X2))
b_fw <- coef(lm(M2Y ~ 0 + M2X1))
b_full <- coef(lm(Y ~ X1 + X2))["X1"]
cat("FW beta1 =", b_fw, " full beta1 =", b_full, "\n")
