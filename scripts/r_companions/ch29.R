## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.29 Machine learning — ridge path (base R SVD)
set.seed(29)
n <- 100L; p <- 20L
X <- matrix(rnorm(n*p), n, p); X <- scale(X, scale=FALSE)
b_true <- c(runif(5), rep(0, p-5))
y <- as.numeric(X %*% b_true + rnorm(n))
## ridge for lambda grid
svdX <- svd(X)
lam <- 10^seq(-2, 2, length.out=20)
betas <- sapply(lam, function(l) {
  d <- svdX$d / (svdX$d^2 + l)
  svdX$v %*% (d * as.numeric(crossprod(svdX$u, y)))
})
cat("ridge path dim:", dim(betas), " (p x nlambda)\n")
cat("Use glmnet when installed for lasso/elastic net.\n")
