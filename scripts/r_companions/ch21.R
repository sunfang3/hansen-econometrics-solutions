## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.21 RDD — local linear with triangular kernel (base R)
## bootstrap common helpers
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})
local_linear_rdd <- function(y, x, c = 0, h, kernel = c("triangular", "rectangular")) {
  kernel <- match.arg(kernel)
  u <- (x - c) / h
  w <- if (kernel == "triangular") pmax(1 - abs(u), 0) else as.numeric(abs(u) <= 1)
  d <- as.numeric(x >= c)
  X <- cbind(1, x - c, d, d * (x - c))
  sw <- sqrt(w)
  b <- as.numeric(qr.solve(X * sw, y * sw))
  ## treatment effect = coef on d
  list(tau = b[3], beta = b, n_eff = sum(w > 0))
}
cat("Ch.21 local_linear_rdd() loaded\n")
