# Consensus Mouse, whole mouse brain single cell/nucleus transcriptomes

Expression matrices and metadata for the two combined whole mouse brain datasets,
[Allen Institute for Brain Science (AIBS), Whole Mouse Brain (WMB)](WMB_dataset.md) and a release from the Broad Institute, Macosko lab. Note here that the acronym, [WMB](WMB_dataset.md), refers to the dataset previously released through this tool containing over 4 million scRNA-seq profiles. The additional whole mouse brain data from Broad Institute data (referred to here as Macosko) contains and additional 4 million snRNA-seq profiles. These two scRNA-seq and snRNA-seq datasets (WMB and Macosko respectively) are combined here into this Consensus Mouse release and [Consensus Mouse Taxonomy](Consensus-Mouse-taxonomy.md).

The expression matrices and associated metadata are hosted on AWS S3 bucket as
a AWS Public Dataset:

Below are links to the data and metadata from the Macosko whole mouse brain, snRNA-seq data.
| Component | Current Version | Size    |
|---|--|---------|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/Consensus-Mouse-Macosko-10X/20251031/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/Consensus-Mouse-Macosko-10X/20251031/) | XX GB |
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/Consensus-Mouse-Macosko-10X/20251031/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Consensus-Mouse-Macosko-10X/20251031/) | XX MB |

This release re-uses the [WMB](WMB_dataset.md) scRNA-seq dataset expression matrices, specifically
the [WMB-10Xv2](WMB-10Xv2.md) and [WMB-10Xv3](WMB-10Xv3.md) data. We do release a set of updated metadata that contain the cells which pass the consensus WMB taxonomy QC. [Consensus Mouse Taxonomy](Consensus-Mouse-taxonomy.md). The set of cells in this metadata are largely the same set of cells as those listed in the [WMB-10X](WMB-10X.md) metadata, differing only by roughly a few thousand.
| Component | Current Version | Size    |
|---|--|---------|
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/Consensus-Mouse-WMB-10X/20251031/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Consensus-Mouse-WMB-10X/20251031/) | XX MB |


Data is being share under the CC BY NC 4.0 license.

Related resources:
* Taxonomy derived from 7 million single nucleus transcriptomes spanning the
  both whole mouse brain datasets ([Consensus-Mouse-taxonomy](Consensus-Mouse-taxonomy.md))
* The WMB dataset ([WMB_dataset](WMB_dataset.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to
  facilitate data download and usage.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  learn how to load individual genes from the 10X expression data.
* [**Consensus taxonomy and clustering**](../notebooks/consensus_mouse_clustering_analysis_and_annotation.ipynb): Learn about the Consensus Mouse taxonomy derived from the AIBS/WMB and Macosko datasets.
* [**Consensus gene expression**](../notebooks/consensus_mouse_10X_snRNASeq.ipynb):
  learn about gene expression across the two Consensus Mouse datasets.
