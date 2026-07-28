## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.13 GMM — just-identified = IV; overID Hansen J skeleton
set.seed(13)
n <- 800L
z <- rnorm(n); v <- rnorm(n)
x <- 0.7*z + v
e <- 0.5*v + rnorm(n)  # endogeneity
y <- 1 + 0.5*x + e
## IV via 2SLS
xhat <- fitted(lm(x ~ z))
b_iv <- coef(lm(y ~ xhat))
b_ols <- coef(lm(y ~ x))
cat("OLS", b_ols, "\nIV", b_iv, "\n")
