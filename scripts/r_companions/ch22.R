## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.22 M-estimator — LAD via quantreg or optim
set.seed(22)
n <- 300L
X <- cbind(1, rnorm(n))
y <- as.numeric(X %*% c(1, 2) + rt(n, df=3))
if (requireNamespace("quantreg", quietly=TRUE)) {
  print(coef(quantreg::rq(y ~ X[,2], tau=0.5)))
} else {
  # crude LAD via optim
  lad <- function(b) sum(abs(y - X %*% b))
  print(optim(c(0,0), lad)$par)
}
