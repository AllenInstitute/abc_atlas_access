# Consensus Mouse single nucleus transcriptomes

Expression matrices and metadata for the two combined whole mouse brain datasets, Macosko and
[Allen Institute for Brain Science (AIBS) WMB](WMB_dataset.md). The ABIS data is, based on over 4 million
scRNA-seq profile the Broad Institute data (referred to here as Macosko), contains and additional 4 million
snRNA-seq profiles.

The expression matrices and associated metadata are hosted on AWS S3 bucket as
a AWS Public Dataset:

The Macosko dataset used in constructing the [consensus mouse taxonomy](Consensus-Mouse-taxonomy.md)
| Component | Current Version | Size    |
|---|--|---------|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/Consensus-Mouse-Macosko-10X/20251031/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/Consensus-Mouse-Macosko-10X/20251031/) | XX GB |
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/Consensus-Mouse-Macosko-10X/20251031/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Consensus-Mouse-Macosko-10X/20251031/) | XX MB |

This release re-uses the [AIBS Whole Mouse Brain (WMB)](WMB_dataset.md) dataset expression matrices, specifically
the [WMB-10Xv2](WMB-10Xv2.md) and [WMB-10Xv3](WMB-10Xv3.md) datasets. We do release, a set of updated metadata
that contain a slightly different set of cells compared to the previous [WMB-10X](WMB-10X.md) dataset by a few
thousand cells.
| Component | Current Version | Size    |
|---|--|---------|
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/Consensus-Mouse-WMB-10X/20251031/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Consensus-Mouse-WMB-10X/20251031/) | XX MB |


Data is being share under the CC BY NC 4.0 license.

Related resources:
* Taxonomy derived from 7 million single nucleus transcriptomes spanning the
  both whole mouse brain datasets ([Consensus-Mouse-taxonomy](Consensus-Mouse-taxonomy.md))
* AIBS WMB dataset ([WMB_dataset](WMB_dataset.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to
  facilitate data download and usage.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  learn how to load individual genes from the 10X expression data.
* [**Consensus taxonomy and clustering**](../notebooks/consensus_mouse_clustering_analysis_and_annotation.ipynb):
  Learn about the Consensus Mouse taxonomy derived from the AIBS/WMB and Macosko datasets.
* [**Consensus gene expression**](../notebooks/consensus_mouse_10X_snRNASeq.ipynb):
  learn about gene expression across the two Consensus Mouse datasets.
