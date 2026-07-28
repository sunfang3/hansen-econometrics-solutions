## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.24 Quantile regression
## bootstrap common helpers
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})
cat("Ch.24: quantreg::rq(y ~ X, tau=0.5)\n")
if (requireNamespace("quantreg", quietly = TRUE) &&
    file.exists(file.path(hansen_data_root(), "cps09mar", "cps09mar.dta"))) {
  cps <- read_hansen_dta("cps09mar", "cps09mar.dta")
  d <- cps[cps$female == 0 & cps$education >= 12, ]
  y <- log(as.numeric(d$earnings)/(as.numeric(d$hours)*as.numeric(d$week)))
  ok <- is.finite(y); y <- y[ok]
  ed <- as.numeric(d$education)[ok]
  fit <- quantreg::rq(y ~ ed, tau = c(0.25, 0.5, 0.75))
  print(coef(fit))
}
