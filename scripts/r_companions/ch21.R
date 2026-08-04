## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.21 RDD — local linear with explicit kernel convention (base R)
## bootstrap common helpers
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})
local_linear_rdd <- function(
    y, x, c = 0, h,
    kernel = c("triangular_normalized", "triangular_unnormalized", "rectangular")) {
  kernel <- match.arg(kernel)
  u <- (x - c) / h
  if (kernel == "triangular_normalized") {
    ## Hansen Table 19.1: support |u| < sqrt(6).
    ## Published Ex.21.6 uses h = 8, 4, 12 under this convention.
    a <- sqrt(6)
    w <- pmax((1 - abs(u) / a) / a, 0)
  } else if (kernel == "triangular_unnormalized") {
    ## Common software/Stata convention: support |u| < 1.
    ## Equivalent h = sqrt(6) * h_normalized: 19.6, 9.8, 29.4.
    w <- pmax(1 - abs(u), 0)
  } else {
    w <- as.numeric(abs(u) <= 1)
  }
  d <- as.numeric(x >= c)
  X <- cbind(1, x - c, d, d * (x - c))
  sw <- sqrt(w)
  b <- as.numeric(qr.solve(X * sw, y * sw))
  ## treatment effect = coef on d
  list(tau = b[3], beta = b, n_eff = sum(w > 0))
}
normalized_to_unnormalized_bandwidth <- function(h) sqrt(6) * h
cat("Ch.21 local_linear_rdd() loaded\n")
