## Shared helpers for Hansen chapter QMD (R toolset)

hansen_repo_root <- function() {
  cands <- c("../..", "..", ".", "../../..")
  for (p in cands) {
    if (dir.exists(file.path(p, "hansen", "econometrics", "data")) ||
        dir.exists(file.path(p, "scripts", "r_companions"))) {
      return(normalizePath(p, mustWork = FALSE))
    }
  }
  normalizePath(".", mustWork = FALSE)
}

hansen_data_root <- function() {
  p <- file.path(hansen_repo_root(), "hansen", "econometrics", "data")
  if (!dir.exists(p)) {
    warning("Data root not found: ", p)
    return(p)
  }
  p
}

read_hansen_dta <- function(...) {
  path <- file.path(hansen_data_root(), ...)
  if (!file.exists(path)) stop("Missing data file: ", path)
  if (!requireNamespace("haven", quietly = TRUE))
    stop("Need package haven: install.packages(\"haven\")")
  haven::read_dta(path)
}

read_hansen_xlsx <- function(..., sheet = 1) {
  path <- file.path(hansen_data_root(), ...)
  if (!file.exists(path)) stop("Missing data file: ", path)
  if (!requireNamespace("readxl", quietly = TRUE))
    stop("Need package readxl: install.packages(\"readxl\")")
  readxl::read_excel(path, sheet = sheet)
}

ols_hc1 <- function(y, X, add_intercept = FALSE) {
  y <- as.numeric(y)
  X <- as.matrix(X)
  if (isTRUE(add_intercept)) X <- cbind(`(Intercept)` = 1, X)
  storage.mode(X) <- "double"
  n <- NROW(X); k <- NCOL(X)
  XtX <- crossprod(X)
  b <- as.numeric(solve(XtX, crossprod(X, y)))
  e <- as.numeric(y - X %*% b)
  meat <- crossprod(X * e)
  bread <- solve(XtX)
  V <- bread %*% meat %*% bread * (n / max(n - k, 1))
  se <- sqrt(pmax(diag(V), 0))
  names(b) <- names(se) <- colnames(X)
  list(beta = b, se = se, resid = e, vcov = V, n = n, k = k, r2 = 1 - sum(e^2) / sum((y - mean(y))^2))
}

pretty_coef <- function(fit, names_ = NULL) {
  b <- fit$beta; se <- fit$se
  if (!is.null(names_)) names(b) <- names(se) <- names_
  data.frame(term = names(b), estimate = as.numeric(b), std.error = as.numeric(se),
             z = as.numeric(b / se), row.names = NULL)
}

message("[hansen] helpers OK | root=", hansen_repo_root())
