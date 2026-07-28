## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.5 Normal regression — residual diagnostics simulation
set.seed(5)
n <- 300L
X <- cbind(1, rnorm(n))
b <- c(0.5, 1.2)
y <- as.numeric(X %*% b + rnorm(n))
fit <- ols_hc1(y, X)
print(pretty_coef(fit))
cat("sigma hat =", sd(fit$resid), "\n")
