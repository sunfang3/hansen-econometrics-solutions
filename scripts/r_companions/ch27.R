## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Chapter 27 Censoring — Tobit / CLAD / OLS on CHJ, CPS, DDK
## Translated from docs/ch27 notebook

## bootstrap common helpers
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Lower Tobit via Olsen reparameterization (gamma = b/sig, nu = 1/sig)
tobit_lower <- function(y, X) {
  y <- as.numeric(y); X <- as.matrix(X)
  k <- NCOL(X)
  b0 <- as.numeric(qr.solve(X, y))
  s0 <- sd(y - X %*% b0) + 1
  nll <- function(th) {
    g <- th[1:k]; nu <- th[k + 1]
    if (nu <= 1e-8) return(1e12)
    left <- y <= 1e-12
    val <- -sum(pnorm(-(X[left, , drop = FALSE] %*% g), log.p = TRUE))
    yu <- y[!left]
    Xu <- X[!left, , drop = FALSE]
    val <- val - sum(log(nu) - 0.5 * log(2 * pi) - 0.5 * (yu * nu - as.numeric(Xu %*% g))^2)
    as.numeric(val)
  }
  th0 <- c(b0 / s0, 1 / s0)
  opt <- optim(th0, nll, method = "L-BFGS-B",
               lower = c(rep(-Inf, k), 1e-4), upper = rep(Inf, k + 1),
               control = list(maxit = 500))
  nu <- opt$par[k + 1]
  list(beta = opt$par[1:k] / nu, sigma = 1 / nu, loglik = -opt$value, conv = opt$convergence == 0)
}

tobit_upper <- function(y, X, tau) {
  y <- as.numeric(y); X <- as.matrix(X)
  k <- NCOL(X)
  b0 <- as.numeric(qr.solve(X, y))
  s0 <- sd(y - X %*% b0) + 1e-3
  nll <- function(th) {
    g <- th[1:k]; nu <- th[k + 1]
    if (nu <= 1e-8) return(1e12)
    right <- y >= tau - 1e-12
    z <- tau * nu - as.numeric(X[right, , drop = FALSE] %*% g)
    val <- -sum(pnorm(z, lower.tail = FALSE, log.p = TRUE))
    yu <- y[!right]; Xu <- X[!right, , drop = FALSE]
    val <- val - sum(log(nu) - 0.5 * log(2 * pi) - 0.5 * (yu * nu - as.numeric(Xu %*% g))^2)
    as.numeric(val)
  }
  opt <- optim(c(b0 / s0, 1 / s0), nll, method = "L-BFGS-B",
               lower = c(rep(-Inf, k), 1e-4), control = list(maxit = 500))
  nu <- opt$par[k + 1]
  list(beta = opt$par[1:k] / nu, sigma = 1 / nu, loglik = -opt$value)
}

clad <- function(y, X, left = NULL, right = NULL, n_starts = 15) {
  y <- as.numeric(y); X <- as.matrix(X)
  crit <- function(b) {
    xb <- as.numeric(X %*% b)
    if (!is.null(left)) xb <- pmax(xb, left)
    if (!is.null(right)) xb <- pmin(xb, right)
    mean(abs(y - xb))
  }
  x0 <- as.numeric(qr.solve(X, y))
  best <- list(value = Inf, par = x0)
  set.seed(0)
  starts <- cbind(x0, 0.5 * x0, 0, x0 + matrix(rnorm(length(x0) * n_starts, 0, 0.15), length(x0)))
  for (j in seq_len(NCOL(starts))) {
    opt <- optim(starts[, j], crit, method = "BFGS", control = list(maxit = 400))
    if (opt$value < best$value) best <- opt
  }
  list(beta = best$par, mad = best$value)
}

## ---- 27.9 CHJ ----
chj <- read_hansen_dta("CHJ2004", "CHJ2004.dta")
tink <- as.numeric(chj$tinkind) / 1000
inc <- as.numeric(chj$income) / 1000
Dinc <- (inc - 1) * (inc > 1)
X <- cbind(1, inc, Dinc)
cat("27.9 censor rate", mean(tink == 0), "\n")
print(ols_hc1(tink, X)$beta)
print(tobit_lower(tink, X)$beta)
print(clad(tink, X, left = 0)$beta)

## ---- 27.10 CPS ----
cps <- read_hansen_dta("cps09mar", "cps09mar.dta")
sub <- cps[cps$education >= 12, ]
wage <- as.numeric(sub$earnings) / (as.numeric(sub$hours) * as.numeric(sub$week))
ok <- is.finite(wage) & wage > 0
lw <- log(wage[ok]); ed <- as.numeric(sub$education)[ok]
X <- cbind(1, ed, ed^2)
cw <- pmin(lw, 3.4)
cat("27.10 n", length(lw), "cap rate", mean(lw >= 3.4), "\n")
cat("true OLS", ols_hc1(lw, X)$beta, "\n")
cat("capped OLS", ols_hc1(cw, X)$beta, "\n")
cat("Tobit", tobit_upper(cw, X, 3.4)$beta, "\n")
cat("CLAD@3.3", clad(pmin(lw, 3.3), X, right = 3.3)$beta, "\n")

## ---- 27.11 DDK ----
ddk <- read_hansen_dta("DDK2011", "DDK2011.dta")
ts <- as.numeric(ddk$totalscore)
ts <- (ts - mean(ts, na.rm = TRUE)) / sd(ts, na.rm = TRUE)
tr <- as.numeric(ddk$tracking)
perc <- as.numeric(ddk$percentile)
school <- ddk$schoolid
m <- is.finite(ts) & is.finite(tr) & is.finite(perc)
ts <- ts[m]; tr <- tr[m]; perc <- perc[m]; school <- school[m]
X <- cbind(1, tr, perc, perc^2)
ct <- pmax(ts, 0)
cat("27.11 n", length(ts), "P(<0)", mean(ts < 0), "\n")
## cluster SE omitted for brevity; point estimates:
cat("true", qr.solve(X, ts), "\n")
cat("censored", qr.solve(X, ct), "\n")
