## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Chapter 12 IV / 2SLS helpers and typical CPS-style IV skeleton
## Notebooks vary by exercise; this companion provides reusable R IV tools.

## bootstrap common helpers
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

ols <- function(y, X) {
  X <- as.matrix(X); y <- as.numeric(y)
  b <- as.numeric(solve(crossprod(X), crossprod(X, y)))
  list(beta = b, resid = y - as.numeric(X %*% b))
}

## 2SLS: y on X, instruments Z (Z must include exogenous parts of X)
tsls <- function(y, X, Z) {
  X <- as.matrix(X); Z <- as.matrix(Z); y <- as.numeric(y)
  PZ_X <- Z %*% solve(crossprod(Z), crossprod(Z, X))  # X-hat
  b <- as.numeric(solve(crossprod(PZ_X, X), crossprod(PZ_X, y)))
  e <- y - as.numeric(X %*% b)
  ## heteroskedastic robust (White) SE for 2SLS
  Q <- crossprod(PZ_X, X) / NROW(X)
  ## score X_hat * e
  meat <- crossprod(PZ_X * e) / NROW(X)
  V <- solve(Q) %*% meat %*% solve(Q) / NROW(X)
  list(beta = b, se = sqrt(pmax(diag(V), 0)), resid = e, vcov = V)
}

## Example: if AJR / Card / etc. data present, load and estimate
## Adjust variable names to match the chapter notebook for a given exercise.
cat("Ch.12 R tools loaded: ols(), tsls(), read_hansen_dta()\n")
cat("Data root:", hansen_data_root(), "\n")
