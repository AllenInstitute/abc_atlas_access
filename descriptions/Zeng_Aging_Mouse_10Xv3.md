# Zeng Aging Mouse 10Xv3 single cell transcriptomes

The Mouse Aging dataset [Jin et al] is a comprehensive single-cell RNA
sequencing (scRNA-seq) dataset containing ~1.2 million high-quality single-cell
transcriptomes of brain cells from young adult and aged mice of both sexes,
from regions spanning the forebrain, midbrain, and hindbrain.

The adult mouse portion of the dataset is a subset of the [Whole Mouse Brain
Data](WMB-10Xv3.md). 

The expression matrices and associated metadata is hosted on AWS S3 bucket as a
AWS Public Dataset:

| Component           | Current Version                                                                                                                                                                                              | Size   |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/Zeng-Aging-Mouse-10Xv3/20241130](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/Zeng-Aging-Mouse-10Xv3/20241130/) | 26 GB  |
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/Zeng-Aging-Mouse-10Xv3/20241130](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Zeng-Aging-Mouse-10Xv3/20241130/)                       | 702 MB |

Data is being share under the CC BY NC 4.0 license.

Related resources :
* 847 clusters and map into Whole Mouse Brain Taxonomy [Zeng Aging Mouse Taxonomy](Zeng_Aging_Mouse_taxonomy))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): Learn how to use
  the AbcProjectCache to facilitate data download and usage.
* [**10x scRNA-seq clustering analysis and annotation**](../notebooks/Zeng_Aging_Mouse_clustering_analysis_and_annotation.ipynb):
  Learn the aging mouse dataset metadata through some example use cases and
  visualization.
* [**10x scRNA-seq gene expression and ageDE genes**](../notebooks/Zeng_Aging_Mouse_10x_snRNASeq_tutorial.ipynb):
  Learn about the aging mouse gene expression and age differential expression
  genes through some example use cases and visualization.
