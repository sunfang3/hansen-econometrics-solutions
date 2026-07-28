## bootstrap
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})

## Ch.26 Multiple choice — conditional logit via mlogit or hand softmax MLE
## bootstrap common helpers
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})
cat("Ch.26 tools. Prefer package mlogit / dfidx when installed.\n")
cat("Data: Koppelman + cps09mar\n")
if (file.exists(file.path(hansen_data_root(), "Koppelman", "Koppelman.dta"))) {
  k <- read_hansen_dta("Koppelman", "Koppelman.dta")
  cat("Koppelman rows", nrow(k), "alts", length(unique(k$alternative)), "\n")
}
## Softmax conditional logit MLE (base R) can be added for Table 26.1 replication.
