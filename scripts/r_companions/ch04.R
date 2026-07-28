## Chapter 4 — OLS with HC0/HC1/HC2/HC3 sandwich (from notebook helpers)

## bootstrap common helpers
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

ols_hc <- function(y, X) {
  y <- as.numeric(y); X <- as.matrix(X)
  n <- NROW(X); k <- NCOL(X)
  XXinv <- solve(crossprod(X))
  beta <- as.numeric(XXinv %*% crossprod(X, y))
  e <- y - as.numeric(X %*% beta)
  h <- rowSums((X %*% XXinv) * X)
  sand <- function(scale) {
    u <- X * as.numeric(scale * e)
    XXinv %*% crossprod(u) %*% XXinv
  }
  Vhom <- XXinv * (sum(e^2) / (n - k))
  V0 <- sand(1)
  V1 <- sand(sqrt(n / (n - k)))
  V2 <- sand(1 / sqrt(pmax(1 - h, 1e-12)))
  V3 <- sand(1 / pmax(1 - h, 1e-12))
  list(beta = beta, se_hom = sqrt(diag(Vhom)), se_hc0 = sqrt(diag(V0)),
       se_hc1 = sqrt(diag(V1)), se_hc2 = sqrt(diag(V2)), se_hc3 = sqrt(diag(V3)))
}

cat("Ch.4 R tools: ols_hc()\n")
## Demo on cps if available
if (file.exists(file.path(hansen_data_root(), "cps09mar", "cps09mar.dta"))) {
  cps <- read_hansen_dta("cps09mar", "cps09mar.dta")
  d <- cps[cps$female == 0 & cps$education >= 12, ]
  y <- log(as.numeric(d$earnings) / (as.numeric(d$hours) * as.numeric(d$week)))
  ok <- is.finite(y)
  y <- y[ok]
  ed <- as.numeric(d$education)[ok]
  exp <- as.numeric(d$age)[ok] - ed - 6
  X <- cbind(1, ed, exp, exp^2)
  fit <- ols_hc(y, X)
  print(data.frame(term = c("const", "educ", "exp", "exp2"), b = fit$beta, HC1 = fit$se_hc1))
}
