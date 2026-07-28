## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Chapter 28 — Hispanic women model selection (parallel to §28.18)
## Translated from docs/ch28 notebook

## bootstrap common helpers
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

cps <- read_hansen_dta("cps09mar", "cps09mar.dta")
df <- cps[cps$female == 1 & cps$hisp == 1, ]
wage <- as.numeric(df$earnings) / (as.numeric(df$hours) * as.numeric(df$week))
ok <- is.finite(wage) & wage > 0
df <- df[ok, ]
y <- log(wage[ok])
educ <- as.numeric(df$education)
exp <- as.numeric(df$age) - educ - 6
married <- as.numeric(df$marital == 1)
reg <- as.numeric(df$region)
R2 <- as.numeric(reg == 2); R3 <- as.numeric(reg == 3); R4 <- as.numeric(reg == 4)
n <- length(y)
cat("n =", n, "\n")

design <- function(ed_type, exp_pow) {
  base <- cbind(1, married, R2, R3, R4)
  if (ed_type == "college") {
    E <- cbind(as.numeric(educ >= 16))
  } else if (ed_type == "spline") {
    E <- cbind(educ, pmax(educ - 9, 0))
  } else {
    E <- sapply(c(12, 13, 14, 16, 18, 20), function(e) as.numeric(educ == e))
  }
  P <- sapply(seq_len(exp_pow), function(k) exp^k)
  cbind(base, E, P)
}

ols_metrics <- function(X, y) {
  X <- as.matrix(X); y <- as.numeric(y)
  n <- NROW(X); k <- NCOL(X)
  XtX_inv <- solve(crossprod(X))
  b <- as.numeric(XtX_inv %*% crossprod(X, y))
  e <- y - as.numeric(X %*% b)
  h <- rowSums((X %*% XtX_inv) * X)
  cv <- sum((e / (1 - h))^2)
  sigma2 <- sum(e^2) / n
  bic <- n * log(sigma2) + k * log(n)
  aic <- n * log(sigma2) + 2 * k
  meat <- crossprod(X * e)
  V <- XtX_inv %*% meat %*% XtX_inv * (n / (n - k))
  list(b = b, V = V, k = k, bic = bic, aic = aic, cv = cv)
}

focus_delta <- function(b, ed_type, exp_pow) {
  n_base <- 5
  n_ed <- c(college = 1, spline = 2, dummy = 6)[[ed_type]]
  idx <- (n_base + n_ed + 1):(n_base + n_ed + exp_pow)
  d <- sum(b[idx] * (30^(seq_len(exp_pow))))
  g <- rep(0, length(b)); g[idx] <- 30^(seq_len(exp_pow))
  list(d = d, g = g)
}

specs <- list(
  list(1, "college", 2), list(2, "spline", 2), list(3, "dummy", 2),
  list(4, "college", 4), list(5, "spline", 4), list(6, "dummy", 4),
  list(7, "college", 6), list(8, "spline", 6), list(9, "dummy", 6)
)

X9 <- design("dummy", 6)
m9 <- ols_metrics(X9, y)
mu_hat <- focus_delta(m9$b, "dummy", 6)$d

rows <- list()
cat(sprintf("%2s %8s %2s %7s %6s %7s %9s %9s %8s %8s\n",
            "M", "educ", "p", "100d", "se", "ret%", "BIC", "AIC", "CV", "FIC*"))
for (sp in specs) {
  mid <- sp[[1]]; ed <- sp[[2]]; p <- sp[[3]]
  X <- design(ed, p)
  m <- ols_metrics(X, y)
  fd <- focus_delta(m$b, ed, p)
  se <- sqrt(as.numeric(t(fd$g) %*% m$V %*% fd$g))
  ret <- 100 * (exp(fd$d) - 1)
  fic <- n * (fd$d - mu_hat)^2 + 2 * n * se^2
  cat(sprintf("%2d %8s %2d %7.1f %6.1f %7.1f %9.1f %9.1f %8.1f %8.1f\n",
              mid, ed, p, 100 * fd$d, 100 * se, ret, m$bic, m$aic, m$cv, fic))
  rows[[length(rows) + 1]] <- list(mid = mid, ed = ed, p = p, d = 100 * fd$d,
                                   bic = m$bic, aic = m$aic, cv = m$cv, fic = fic, ret = ret)
}

for (crit in c("bic", "aic", "cv", "fic")) {
  vals <- sapply(rows, `[[`, crit)
  best <- rows[[which.min(vals)]]
  cat(sprintf("best %s -> Model %d (%s, exp^%d) 100d=%.1f ret%%=%.1f\n",
              crit, best$mid, best$ed, best$p, best$d, best$ret))
}
