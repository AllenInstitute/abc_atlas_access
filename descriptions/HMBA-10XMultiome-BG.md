# Human-Mammalian Brain - Basal Ganglia 10X snRANSeq data: Individual species gene expression

Gene expression data and metadata for each individual species in the HMBA-BG
10X dataset. Currently includes:
- 1,683,105 Human cells, 36,601 genes
- 839,102 Macaque cells, 35,219 genes
- 414,575 Marmoset cells, 35,787 genes

This release also includes data for running [MapMyCells](https://portal.brain-map.org/atlases-and-data/bkp/mapmycells) for each of the currently released species using the associated [taxonomy](HMBA-BG-taxonomy-CCN20250428.md).

For more information on the dataset, please refer to the following webpage:
[Mammalian Basal Ganglia Consensus Cell Type Atlas](https://alleninstitute.github.io/HMBA_BasalGanglia_Consensus_Taxonomy/).

The expression matrices and associated metadata are hosted in a AWS S3 bucket
as a AWS Public Dataset:

| Component | Current Version | Size |
|---|--|---------|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/HMBA-10xMultiome-BG/20250531/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/HMBA-10xMultiome-BG/20250531/) | 50.5 GB |
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/HMBA-10xMultiome-BG/20250531/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/HMBA-10xMultiome-BG/20250531/) | 581 MB |
| MapMyCells resources | [s3://allen-brain-cell-atlas/mapmycells/HMBA-10xMultiome-BG/20250531/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#mapmycells/HMBA-10xMultiome-BG/20250531/) | 2.14 GB |

Data is being shared under the CC BY NC 4.0 license.

Related resources:
* ~2 million single cell transcriptomes with aligned genes across species.
  ([HMBA-10XMultiome-BG-Aligned](HMBA-10XMultiome-BG-Aligned.md))
* Taxonomy and Clustering analysis of ~2 million single cell
  transcriptomes from the aligned dataset.
  ([HMBA-BG-taxonomy-CCN20250428](HMBA-BG-taxonomy-CCN20250428.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb):
  Learn how to use the ABCProjectCache object to facilitate data download and
  usage.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  Learn how to load individual genes from the 10X expression data.
* [**10X scRNA-seq clustering analysis and annotation**](../notebooks/hmba_bg_clustering_analysis_and_annotation.ipynb):
  Learn about the HMBA-BG data/metadata structure and taxonomy through example
  use cases and visualization.
[*notebooks/hmba_bg_clustering_analysis_and_annotation.ipynb*]
* [**10X scRNA-seq gene expression**](../notebooks/hmba_bg_10X_snRNASeq_tutorial.ipynb):
  Interact with HMBA-BG 10X-Aligned gene expression data. [*notebooks/hmba_bg_10X_snRNASeq_tutorial.ipynb*]