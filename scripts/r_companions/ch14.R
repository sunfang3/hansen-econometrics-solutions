## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.14 Time series — AR(1) OLS + HAC note
set.seed(14)
n <- 400L
e <- rnorm(n); y <- filter(e, 0.7, method="recursive")
y <- as.numeric(y)
yt <- y[-1]; ylag <- y[-n]
fit <- ols_hc1(yt, cbind(1, ylag))
print(pretty_coef(fit, c("const","AR1")))
cat("For HAC: sandwich::NeweyWest(lm(...)) when sandwich installed\n")
