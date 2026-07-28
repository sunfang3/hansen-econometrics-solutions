## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.18 DiD — two-way FE / 2x2 DiD
set.seed(18)
# units i=1..100, t=1,2; treat i>50 from t=2
i <- rep(1:100, each=2); t <- rep(1:2, 100)
treat <- as.numeric(i > 50)
post <- as.numeric(t == 2)
y <- 1 + 0.5*treat + 0.2*post + 1.0*treat*post + rnorm(length(i))
X <- cbind(1, treat, post, treat*post)
fit <- ols_hc1(y, X)
print(pretty_coef(fit, c("const","treat","post","did")))
cat("true ATT interaction = 1\n")
