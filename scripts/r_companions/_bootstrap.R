## Path bootstrap — source this first from any chapter companion
local({
  cands <- c(
    file.path("..", "..", "scripts", "r_companions", "_common.R"),
    file.path("..", "scripts", "r_companions", "_common.R"),
    file.path("scripts", "r_companions", "_common.R"),
    file.path(".", "_common.R")
  )
  for (f in cands) {
    if (file.exists(f)) {
      sys.source(f, envir = globalenv())
      return(invisible(TRUE))
    }
  }
  stop("Cannot find scripts/r_companions/_common.R")
})
