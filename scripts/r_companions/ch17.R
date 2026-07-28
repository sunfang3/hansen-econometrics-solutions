## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.17 Panel — within estimator; AB/BB require custom GMM (see notebook)
## bootstrap common helpers
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})
within_fe <- function(y, X, id) {
  ## demean by id then OLS
  y <- as.numeric(y); X <- as.matrix(X)
  id <- as.factor(id)
  yd <- y - ave(y, id)
  Xd <- apply(X, 2, function(col) col - ave(col, id))
  ols_hc1(yd, Xd)
}
cat("Ch.17 within_fe() loaded; full AB/BB GMM: port from Python notebook as needed.\n")
