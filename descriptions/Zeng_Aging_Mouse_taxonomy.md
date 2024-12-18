# Zeng Aging Mouse clustering and mapping to the WMB taxonomy of cell types

The Mouse Aging dataset [Jin et al] is a comprehensive single-cell RNA
sequencing (scRNA-seq) dataset containing ~1.2 million high-quality single-cell
transcriptomes of brain cells from young adult and aged mice of both sexes,
from regions spanning the forebrain, midbrain, and hindbrain. High-resolution
de novo clustering of all cells results in 847 cell clusters and reveals at
least 14 age-biased clusters that are mostly glial types. Clusters in the study
were mapped to the Whole Mouse Brain taxonomy ([WMB-taxonomy](WMB-taxonomy.md))
to provide class, subclass and supertype annotations. At the broader cell
subclass and supertype levels, age-associated gene expression signatures were
analyzed resulting in a list of 2,449 differentially expressed genes (age-DE
genes) for many neuronal and non-neuronal cell types.

The associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component | Current Version                                                                                                                                                                                      | Size   |
|---|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| Metadata | [s3://allen-brain-cell-atlas/metadata/Zeng-Aging-Mouse-WMB-taxonomy/20241130](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Zeng-Aging-Mouse-WMB-taxonomy/20241130/) | 286 MB |

Data is being share under the CC BY NC 4.0 license.

Related resources :
* Gene expression data and metadata ([Zeng Aging Mouse 10Xv3](Zeng_Aging_Mouse_10Xv3))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): Learn how to use
  the AbcProjectCache to facilitate data download and usage.
* [**clustering analysis and annotation**](../notebooks/Zeng_Aging_Mouse_clustering_analysis_and_annotation.ipynb):
  Learn the aging mouse dataset metadata through some example use cases and
  visualization.
* [**10x scRNA-seq gene expression and ageDE genes**](../notebooks/Zeng_Aging_Mouse_10x_snRNASeq_tutorial.ipynb):
  Learn about the aging mouse gene expression and age differential expression
  genes through some example use cases and visualization.

