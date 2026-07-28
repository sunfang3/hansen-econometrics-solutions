## Shared helpers for Hansen chapter QMD (R toolset)

hansen_repo_root <- function() {
  cands <- c(
    if (exists("root", inherits = TRUE)) get("root", inherits = TRUE),
    "../..", "..", ".", "../../.."
  )
  for (p in cands) {
    if (is.null(p) || !nzchar(p)) next
    if (dir.exists(file.path(p, "hansen", "econometrics", "data")) ||
        dir.exists(file.path(p, "scripts", "r_companions"))) {
      return(normalizePath(p, mustWork = FALSE))
    }
  }
  normalizePath(".", mustWork = FALSE)
}

hansen_data_root <- function() {
  p <- file.path(hansen_repo_root(), "hansen", "econometrics", "data")
  if (!dir.exists(p)) stop("Cannot find hansen/econometrics/data under ", hansen_repo_root())
  p
}

read_hansen_dta <- function(...) {
  path <- file.path(hansen_data_root(), ...)
  if (!file.exists(path)) stop("Missing data file: ", path)
  if (!requireNamespace("haven", quietly = TRUE)) stop("install.packages(\"haven\")")
  haven::read_dta(path)
}

read_hansen_xlsx <- function(..., sheet = 1) {
  path <- file.path(hansen_data_root(), ...)
  if (!file.exists(path)) stop("Missing data file: ", path)
  if (!requireNamespace("readxl", quietly = TRUE)) stop("install.packages(\"readxl\")")
  readxl::read_excel(path, sheet = sheet)
}

ols_hc1 <- function(y, X, add_intercept = FALSE) {
  y <- as.numeric(y)
  X <- as.matrix(X)
  if (add_intercept) X <- cbind(1, X)
  n <- NROW(X); k <- NCOL(X)
  XtX <- crossprod(X)
  b <- as.numeric(solve(XtX, crossprod(X, y)))
  e <- y - as.numeric(X %*% b)
  meat <- crossprod(X * e)
  bread <- solve(XtX)
  V <- bread %*% meat %*% bread * (n / (n - k))
  se <- sqrt(pmax(diag(V), 0))
  list(beta = b, se = se, resid = e, vcov = V, n = n, k = k)
}

pretty_coef <- function(fit, names_ = NULL) {
  b <- fit$beta; se <- fit$se
  if (is.null(names_)) names_ <- paste0("b", seq_along(b) - 1L)
  data.frame(term = names_, estimate = b, std.error = se, z = b / se, row.names = NULL)
}

message("Hansen R helpers loaded. data_root = ", tryCatch(hansen_data_root(), error = function(e) NA))
