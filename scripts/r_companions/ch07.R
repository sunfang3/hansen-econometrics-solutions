## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.7 Asymptotics — HC1 vs homoskedastic SE under hetero
set.seed(7)
n <- 1000L
X <- cbind(1, rnorm(n))
u <- rnorm(n) * (1 + 0.8*X[,2]^2)  # hetero
y <- as.numeric(X %*% c(1, 0.5) + u)
fit <- ols_hc1(y, X)
s2 <- sum(fit$resid^2) / (n - 2)
se_hom <- sqrt(diag(solve(crossprod(X)) * s2))
print(data.frame(term=c("const","x"), HC1=fit$se, HOM=se_hom))
