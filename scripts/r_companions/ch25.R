## Chapter 25 Binary Choice — probit MLE (Fisher scoring) + CPS empirics
## Translated from docs/ch25/Hansen_Ch25_Exercises_Solutions.ipynb

## bootstrap common helpers
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

probit_mle <- function(y, X, maxiter = 50L, tol = 1e-10, start_scale = 0.1) {
  y <- as.numeric(y); X <- as.matrix(X)
  n <- NROW(X); k <- NCOL(X)
  ## LPM start, scaled into probit range
  b <- as.numeric(qr.solve(X, y)) * start_scale
  for (it in seq_len(maxiter)) {
    eta <- pmin(pmax(as.numeric(X %*% b), -8), 8)
    Phi <- pmin(pmax(pnorm(eta), 1e-12), 1 - 1e-12)
    phi <- dnorm(eta)
    denom <- Phi * (1 - Phi)
    score_w <- (y - Phi) * phi / denom
    fish_w <- (phi^2) / denom
    g <- crossprod(X, score_w)
    H <- crossprod(X * sqrt(fish_w))
    ## H = X' diag(w) X
    H <- crossprod(X, X * fish_w)
    step <- as.numeric(solve(H, g))
    b <- b + step
    if (max(abs(step)) < tol) break
  }
  eta <- pmin(pmax(as.numeric(X %*% b), -8), 8)
  Phi <- pmin(pmax(pnorm(eta), 1e-12), 1 - 1e-12)
  phi <- dnorm(eta)
  denom <- Phi * (1 - Phi)
  score_w <- (y - Phi) * phi / denom
  fish_w <- (phi^2) / denom
  bread <- crossprod(X, X * fish_w)
  meat <- crossprod(X, X * (score_w^2))
  V <- solve(bread) %*% meat %*% solve(bread)
  se <- sqrt(pmax(diag(V), 0))
  ame <- mean(phi) * b
  ll <- sum(y * log(Phi) + (1 - y) * log(1 - Phi))
  list(beta = b, se = se, ame = ame, loglik = ll, iters = it, vcov = V)
}

cps <- read_hansen_dta("cps09mar", "cps09mar.dta")
make_X_demo <- function(d) {
  black <- as.numeric(d$race == 2)
  cbind(1, as.numeric(d$age), as.numeric(d$education), black, as.numeric(d$hisp))
}
married_ind <- function(d) as.numeric(d$marital %in% c(1, 2, 3))
nm <- c("const", "age", "education", "Black", "Hispanic")

print_table <- function(title, names, fit, y) {
  cat(sprintf("\n=== %s ===\nn=%d mean(Y)=%.4f logL=%.1f iters=%d\n",
              title, length(y), mean(y), fit$loglik, fit$iters))
  print(data.frame(var = names, coef = fit$beta, SE = fit$se, AME = fit$ame), row.names = FALSE)
}

## 25.15 men union
men <- cps[cps$female == 0, ]
fit <- probit_mle(as.numeric(men$union), make_X_demo(men))
print_table("25.15 Men union", nm, fit, men$union)

## 25.16 women union
wom <- cps[cps$female == 1, ]
fit <- probit_mle(as.numeric(wom$union), make_X_demo(wom))
print_table("25.16 Women union", nm, fit, wom$union)

## 25.17 college women marriage ~ age + age^2/100
cw <- wom[wom$education >= 16, ]
age <- as.numeric(cw$age)
Xq <- cbind(1, age, age^2 / 100)
fit <- probit_mle(married_ind(cw), Xq)
print_table("25.17 College women marriage quadratic age", c("const", "age", "age2/100"), fit, married_ind(cw))
for (a in c(25, 35, 45, 55, 65)) {
  eta <- fit$beta[1] + fit$beta[2] * a + fit$beta[3] * (a^2) / 100
  cat(sprintf("  age=%d Phi=%.3f\n", a, pnorm(eta)))
}

## 25.18–19 marriage linear index
fit <- probit_mle(married_ind(men), make_X_demo(men))
print_table("25.18 Men marriage", nm, fit, married_ind(men))
fit <- probit_mle(married_ind(wom), make_X_demo(wom))
print_table("25.19 Women marriage", nm, fit, married_ind(wom))
