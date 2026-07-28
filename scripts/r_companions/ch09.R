## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.9 Testing — Wald for linear restriction
set.seed(9)
n <- 500L
X <- cbind(1, rnorm(n), rnorm(n))
y <- as.numeric(X %*% c(0, 0.2, 0) + rnorm(n))
fit <- ols_hc1(y, X)
## H0: beta2 = 0
R <- matrix(c(0,0,1), 1)
W <- as.numeric(t(R %*% fit$beta) %*% solve(R %*% fit$vcov %*% t(R), R %*% fit$beta))
cat("Wald =", W, " p =", 1 - pchisq(W, 1), "\n")
