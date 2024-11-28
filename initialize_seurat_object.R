#!/usr/bin/env Rscript
library("Seurat")
library("tidyverse")

args = commandArgs(trailingOnly=TRUE)
output_dir <- args[1]
data_input_dir <- args[2]

a <- data.frame(t1 = 1:5)
a$t2 <- output_dir
a$t3 <- data_input_dir

data <- Read10X(data.dir = data_input_dir)
seurat_object = CreateSeuratObject(counts = data)

saveRDS(seurat_object,file = "test.rds")


