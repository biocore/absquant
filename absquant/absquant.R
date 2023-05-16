#!/usr/bin/env Rscript

# Much of this is taken from q2-diversity's run_adonis script

library(MASS)

### ERROR HANDLING ###
options(error = function() {
  sink(stderr())
  on.exit(sink(NULL))
  traceback(3)
  if (!interactive()) {
    q(status = 1)
  }
})

cat(R.version$version.string, "\n")
args <- commandArgs(TRUE)

# Arguments:
# 1) File with counts (named abs_counts) & metadata
# 2) Formula
# 3) Output directory
# 4) Feature name

md.file <- args[[1]]
formula <- args[[2]]
outdir <- args[[3]]
feat.name <- args[[4]]

output <- paste0(outdir, "/", feat.name, ".tsv")
formula <- paste0("abs_counts ~ ", formula, " + offset(log(depth))")
formula <- as.formula(formula)

# NOTE: R will just sometimes change the names of your columns
# NOTE: Need to add offset?
md <- read.table(md.file, sep="\t", row.names=1, header=TRUE)
model <- glm.nb(formula, data=md)

coefs <- as.data.frame(coef(summary(model)))
write.table(coefs, output, sep="\t", quote=FALSE, col.names=NA)
