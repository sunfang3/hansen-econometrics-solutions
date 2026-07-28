## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.20 Series regression — polynomial series + OLS
set.seed(20)
n <- 400L
x <- runif(n, -1, 1)
y <- sin(pi*x) + rnorm(n, 0, 0.3)
K <- 5L
X <- cbind(1, outer(x, 1:K, "^"))
fit <- ols_hc1(y, X)
cat("series R2 =", fit$r2, " K=", K, "\n")
