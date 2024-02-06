# Human brain 10Xv3 single cell transcriptomes

This dataset consists of over three million single cells and two million
neurons from 100 locations across the forebrain, midbrain, and hindbrain.

Full details on the dataset can be found in [Siletti et al. 2022](https://www.biorxiv.org/content/10.1101/2022.10.12.511898v1).

The expression matrices and associated metadata is hosted on AWS S3 bucket as a
AWS Public Dataset:

| Component | Current Version | Size    |
|---|--|---------|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/WHB-10Xv3/20240330/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/expression_matrices/WHB-10Xv3/20240330/) | 70.0 GB |

Data is being share under the CC BY NC 4.0 license.

Related resources :
* Whole human brain taxonomy of cell types ([WHB-taxonomy](WHB-taxonomy.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to
  facilitate data download and usage.
* [**10x scRNA-seq clustering analysis and annotation**](../notebooks/cluster_annotation_tutorial.ipynb): learn about the
  whole mouse brain taxonomy through some example use cases and visualization.
* **10x scRNA-seq gene expression data**
  * [**Part 1**](../notebooks/10x_snRNASeq_tutorial_part_1.ipynb): learn about the 10x dataset through some example use
    cases and visualization of cells in the thalamus.
  * [**Part 2**](../notebooks/10x_snRNASeq_tutorial_part_2b.ipynb): Explore the whole brain data through visualization and
    analyses of a set of genes of interest.