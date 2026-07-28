## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Chapter 28 — Hispanic women model selection (parallel to §28.18)
## Experience scaled by /10 for numerical stability of high powers.

cps <- read_hansen_dta("cps09mar", "cps09mar.dta")
df <- cps[cps$female == 1 & cps$hisp == 1, ]
wage <- as.numeric(df$earnings) / (as.numeric(df$hours) * as.numeric(df$week))
ok <- is.finite(wage) & wage > 0
df <- df[ok, ]
y <- log(wage)
educ <- as.numeric(df$education)
expv <- (as.numeric(df$age) - educ - 6) / 10  # scale: 30 years -> 3
married <- as.numeric(df$marital == 1)
reg <- as.numeric(df$region)
n <- length(y)
cat("n =", n, "\n")

make_X <- function(ed_type, exp_pow) {
  X <- cbind(
    const = 1,
    married = married,
    R2 = as.numeric(reg == 2),
    R3 = as.numeric(reg == 3),
    R4 = as.numeric(reg == 4)
  )
  if (ed_type == "college") {
    X <- cbind(X, college = as.numeric(educ >= 16))
  } else if (ed_type == "spline") {
    X <- cbind(X, educ = educ, educ_sp9 = pmax(educ - 9, 0))
  } else {
    X <- cbind(
      X,
      e12 = as.numeric(educ == 12), e13 = as.numeric(educ == 13),
      e14 = as.numeric(educ == 14), e16 = as.numeric(educ == 16),
      e18 = as.numeric(educ == 18), e20 = as.numeric(educ == 20)
    )
  }
  for (k in seq_len(exp_pow)) X <- cbind(X, expv^k)
  colnames(X)[(NCOL(X) - exp_pow + 1):NCOL(X)] <- paste0("z", seq_len(exp_pow))
  ## drop zero-variance / collinear via QR
  q <- qr(X)
  X[, q$pivot[seq_len(q$rank)], drop = FALSE]
}

ols_metrics <- function(X, y) {
  X <- as.matrix(X); y <- as.numeric(y)
  n <- NROW(X); k <- NCOL(X)
  fit <- lm.fit(X, y)
  b <- as.numeric(fit$coefficients)
  names(b) <- colnames(X)
  e <- as.numeric(fit$residuals)
  ## leverage via hat diagonal approximation
  Q <- qr.Q(qr(X))
  h <- pmin(rowSums(Q * Q), 0.999999)
  cv <- sum((e / (1 - h))^2)
  sigma2 <- max(sum(e^2) / n, 1e-12)
  ## HC1 vcov
  XtX_inv <- chol2inv(chol(crossprod(X)))
  V <- XtX_inv %*% crossprod(X * e) %*% XtX_inv * (n / max(n - k, 1))
  list(b = b, V = V, k = k,
       bic = n * log(sigma2) + k * log(n),
       aic = n * log(sigma2) + 2 * k, cv = cv)
}

## Delta log wage for exp years 0 -> 30 (z: 0 -> 3)
focus_delta <- function(b, exp_pow) {
  z30 <- 3
  d <- 0
  g <- setNames(rep(0, length(b)), names(b))
  for (k in seq_len(exp_pow)) {
    nm <- paste0("z", k)
    if (nm %in% names(b) && is.finite(b[[nm]])) {
      d <- d + b[[nm]] * (z30^k)
      g[[nm]] <- z30^k
    }
  }
  list(d = d, g = as.numeric(g))
}

specs <- list(
  list(1, "college", 2L), list(2, "spline", 2L), list(3, "dummy", 2L),
  list(4, "college", 4L), list(5, "spline", 4L), list(6, "dummy", 4L),
  list(7, "college", 6L), list(8, "spline", 6L), list(9, "dummy", 6L)
)

X9 <- make_X("dummy", 6L)
m9 <- ols_metrics(X9, y)
mu_hat <- focus_delta(m9$b, 6L)$d

rows <- list()
cat(sprintf("%2s %8s %2s %7s %6s %7s %9s %9s %8s %8s\n",
            "M", "educ", "p", "100d", "se", "ret%", "BIC", "AIC", "CV", "FIC*"))
for (sp in specs) {
  mid <- sp[[1]]; ed <- sp[[2]]; p <- sp[[3]]
  X <- make_X(ed, p)
  m <- ols_metrics(X, y)
  fd <- focus_delta(m$b, p)
  se <- sqrt(max(as.numeric(crossprod(fd$g, m$V %*% fd$g)), 0))
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
