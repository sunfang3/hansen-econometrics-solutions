## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.2 CEF / projection numerics (simulation)
set.seed(1)
n <- 5000L
X <- rnorm(n); U <- rnorm(n)
Y <- 1 + 2*X + U
## CEF is linear: E[Y|X]=1+2X; projection same
fit <- ols_hc1(Y, cbind(1, X))
print(pretty_coef(fit, c("const","X")))
cat("true beta = (1,2)\n")
