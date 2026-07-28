## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.10 Bootstrap — pairs bootstrap of slope SE
set.seed(10)
n <- 200L
x <- rnorm(n); y <- 1 + 2*x + rnorm(n)
b_hat <- coef(lm(y ~ x))[2]
B <- 399L
bs <- numeric(B)
for (b in seq_len(B)) {
  i <- sample.int(n, replace = TRUE)
  bs[b] <- coef(lm(y[i] ~ x[i]))[2]
}
cat("beta2 =", b_hat, " boot SE =", sd(bs), "\n")
