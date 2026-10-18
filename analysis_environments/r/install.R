# Install the R packages the ABC Atlas analysis scripts use, into an existing R (>= 4.4).
#
#   Rscript install.R
#
# Rarr (Zarr v3 with sharding) is built from source, which needs a compiler toolchain:
#   macOS:   xcode-select --install
#   Windows: Rtools matching your R version (https://cran.r-project.org/bin/windows/Rtools/)
#   Linux:   your distribution's build tools (e.g. build-essential)

repos <- "https://cloud.r-project.org"
for (pkg in c("arrow", "ggplot2", "patchwork", "remotes", "jsonlite")) {
  if (!requireNamespace(pkg, quietly = TRUE)) install.packages(pkg, repos = repos)
}
# Rarr >= 2.1 reads Zarr v3 with sharding; until that reaches a Bioconductor release it comes from GitHub
if (!requireNamespace("Rarr", quietly = TRUE) || packageVersion("Rarr") < "2.1") {
  remotes::install_github("Huber-group-EMBL/Rarr", upgrade = "never")
}
message("Installed. Check the setup with:  Rscript check_setup.R")
