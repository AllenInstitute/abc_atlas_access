# Consensus Whole Mouse Brain single cell/nucleus transcriptomes

Expression matrices and metadata for the two combined whole mouse brain datasets,
[Allen Institute for Brain Science (AIBS), Whole Mouse Brain (WMB)](WMB_dataset.md) and a release from the Broad Institute, Macosko lab. The previously, released WMB-AIBS, dataset released through this tool contains over 4 million scRNA-seq profiles. The additional whole mouse brain data from Broad Institute data (referred to here as WMB-Macosko) contains and additional 4 million snRNA-seq profiles. These two scRNA-seq and snRNA-seq datasets (WMB and Macosko respectively) are combined here into this Consensus Mouse release and [Consensus Mouse Taxonomy](Consensus-WMB-taxonomy.md).

The expression matrices and associated metadata are hosted on AWS S3 bucket as
a AWS Public Dataset:

Below are links to the data and metadata from the WMB-Macosko whole mouse brain, snRNA-seq data.
| Component | Current Version | Size    |
|---|--|---------|
| Macosko: Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/Consensus-WMB-Macosko-10X/20251031/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/Consensus-WMB-Macosko-10X/20251031/) | 42.7 GB |
| Macosko: Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/Consensus-WMB-Macosko-10X/20251031/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Consensus-WMB-Macosko-10X/20251031/) | 798.3 MB |

This release re-uses the AIBS [WMB](WMB_dataset.md) scRNA-seq dataset expression matrices, specifically
the [WMB-10Xv2](WMB-10Xv2.md) and [WMB-10Xv3](WMB-10Xv3.md) data. We do release a set of updated metadata that contain the cells which pass the Consensus WMB taxonomy QC. [Consensus Mouse Taxonomy](Consensus-WMB-taxonomy.md). The set of cells in this metadata are largely the same set of cells as those listed in the [WMB-10X](WMB-10X.md) metadata, differing only by roughly a few thousand.
| Component | Current Version | Size    |
|---|--|---------|
| AIBS: Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/Consensus-WMB-AIBS-10X/20251031/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Consensus-WMB-AIBS-10X/20251031/) | 634.9 MB |


Data is being shared under the CC BY NC 4.0 license.

Related resources:
* Taxonomy derived from 7 million single nucleus transcriptomes spanning the
  both whole mouse brain datasets ([Consensus-WMB-integrated-taxonomy](Consensus-WMB-taxonomy.md))
* The WMB-AIBS dataset ([WMB-AIBS dataset](WMB_dataset.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to
  facilitate data download and usage.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  learn how to load individual genes from the 10X expression data.
* [**Consensus Whole Mouse Brian integrated taxonomy and clustering**](../notebooks/consensus_mouse_clustering_analysis_and_annotation.ipynb):
  Learn about the Consensus Whole Mouse Brain integrated taxonomy derived from the WMB-AIBS and WMB-Macosko datasets.
* [**Consensus Whole Mouse Brain gene expression**](../notebooks/consensus_mouse_10X_snRNASeq.ipynb):
  learn about gene expression across the two Consensus Whole Mouse Brain datasets.
