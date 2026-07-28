## Ch.23 Nonlinear LS — skeleton (Nerlove / RR / PSS paths)
## bootstrap common helpers
local({
  for (cand in c("../..", "..", ".", "../../..")) {
    f <- file.path(cand, "scripts/r_companions/_common.R")
    if (file.exists(f)) { source(f, local = FALSE); break }
  }
})
cat("Ch.23: use nls() / optim() for CES, kink, smooth threshold.\n")
cat("Data root:", hansen_data_root(), "\n")
if (file.exists(file.path(hansen_data_root(), "Nerlove1963", "Nerlove1963.xlsx"))) {
  if (requireNamespace("readxl", quietly = TRUE)) {
    ner <- read_hansen_xlsx("Nerlove1963", "Nerlove1963.xlsx")
    cat("Nerlove rows:", nrow(ner), "cols:", paste(names(ner), collapse=", "), "\n")
  }
}
