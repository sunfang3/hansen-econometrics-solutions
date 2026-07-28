## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.15 VAR(1) by equation-wise OLS
set.seed(15)
n <- 300L
Y <- matrix(0, n, 2)
A <- matrix(c(0.5, 0.1, 0.2, 0.4), 2, 2, byrow=TRUE)
for (t in 2:n) Y[t,] <- as.numeric(A %*% Y[t-1,]) + rnorm(2)
Y0 <- Y[-1,]; Y1 <- Y[-n,]
fit1 <- ols_hc1(Y0[,1], cbind(1, Y1))
fit2 <- ols_hc1(Y0[,2], cbind(1, Y1))
cat("eq1", fit1$beta, "\neq2", fit2$beta, "\n")
