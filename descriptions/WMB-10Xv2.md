# Whole mouse brain 10Xv2 single cell transcriptomes

This dataset consists of 1.7 million single cell transcriptomes spanning the whole adult mouse brain using 10Xv2 chemistry. 
It was used in the creation of a high resolution transcriptomic and spatial atlas of cell types describe in [Yao et. al](https://www.biorxiv.org/content/10.1101/2023.03.06.531121v1).

The expression matrices and associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component | Current Version |
|---|--|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/WMB-10Xv2/20230630](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/WMB-10Xv2/20230630/) |

Related resources :
* Whole mouse brain 10Xv3 single cell transcriptomes ([WMB-10Xv3](WMB-10Xv3.md))
* Whole mouse brain mouse brain clustering ([WMB-10X](WMB-10X.md))
* Whole mouse brain mouse taxonomy of cell types ([WMB-taxonomy](WMB-taxonomy.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to faciliate data download and usage.
* [**10x scRNA-seq clustering analysis and annotation**](../notebooks/cluster_annotation_tutorial.ipynb): learn about the whole mouse brain taxonomy through some example use cases and visualization.
* **10x scRNA-seq gene expression data**
  * [**Part 1**](../notebooks/10x_snRNASeq_tutorial_part_1.ipynb): learn about the 10x dataset through some example use cases and visualization of cells in the thalamus.
  * [**Part 2a**](../notebooks/10x_snRNASeq_tutorial_part_2a.ipynb): learn how to iterate through all the data packages, to access data for whole brain example use cases in part 2b.
  * [**Part 2b**](../notebooks/10x_snRNASeq_tutorial_part_2b.ipynb): Explore the whole brain data through visualization and analyses of a set of genes of interest.
