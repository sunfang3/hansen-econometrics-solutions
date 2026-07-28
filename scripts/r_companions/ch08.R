## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.8 Restricted OLS — R beta = r via Lagrange / residual projection
set.seed(8)
n <- 400L
X <- cbind(1, matrix(rnorm(n*2), n, 2))
b0 <- c(1, 1, 1)
y <- as.numeric(X %*% b0 + rnorm(n))
## restrict b1 = b2 (R = c(0,1,-1), r=0)
R <- matrix(c(0,1,-1), 1)
r <- 0
XtX <- crossprod(X); Xty <- crossprod(X, y)
bun <- as.numeric(solve(XtX, Xty))
# restricted: b_r = bun - XtX^{-1} R' (R XtX^{-1} R')^{-1} (R bun - r)
A <- solve(XtX)
br <- bun - as.numeric(A %*% t(R) %*% solve(R %*% A %*% t(R), R %*% bun - r))
cat("unrestricted", bun, "\nrestricted", br, "\n")
