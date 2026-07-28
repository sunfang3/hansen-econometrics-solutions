## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.11 Multivariate regression — SUR-style stacked OLS
set.seed(11)
n <- 300L
X <- cbind(1, rnorm(n))
Y1 <- as.numeric(X %*% c(1, 0.5) + rnorm(n))
Y2 <- as.numeric(X %*% c(0, 1.0) + rnorm(n))
fit1 <- ols_hc1(Y1, X); fit2 <- ols_hc1(Y2, X)
print(list(eq1 = fit1$beta, eq2 = fit2$beta))
