# Developing Mouse - Visual Cortex single cell transcriptomes

The Developing Mouse - Visual Cortext taxonomy is derived from a single cell transcriptomic dataset containing 568,654 cells from 53 donors ranging in age from embryonic to adult.

All associated metadata is publicly available as an AWS Public Dataset hosted on Amazon S3 and through the Allen Brain Cell Atlass Access (abc_atlas_access) package. 

The expression matrices and associated metadata are hosted on AWS S3 bucket as
a AWS Public Dataset:

| Component | Current Version | Size    |
|---|--|---------|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/Developing-Mouse-Vis-Cortex-10X/20260131/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/Developing-Mouse-Vis-Cortex-10X/20260131/) | 14.2 GB |
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/Developing-Mouse-Vis-Cortex-10X/20260131/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Developing-Mouse-Vis-Cortex-10X/20260131/) | 180.1 MB |


Data is being shared under the CC BY NC 4.0 license.

Related resources:
* Taxonomy derived from the Developing Mouse - Visual Cortex dataset.
  ([Dev-Mouse-Vis-Cortex-taxonomy](Dev-Mouse-Vis-Cortex-taxonomy.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to
  facilitate data download and usage.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  learn how to load individual genes from the 10X expression data.
* [**Developing Mouse - Visual Cortex Cluster analysis and annotation**](../notebooks/dev_mouse_vis_cortex_clustering_analysis_and_annotation.ipynb):
  Learn about the Developing Mouse - Visual Cortex integrated taxonomy derived from 10X gene expression.
* [**Developing Mouse - Visual Cortex gene expression**](../notebooks/dev_mouse_vis_cortex_10X_scRNASeq.ipynb):
  Learn about gene expression across the Developing Mouse - Visual Cortex 10X data.
