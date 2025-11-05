# Human-Mammalian Brain - Basal Ganglia 10X snRANSeq data: Aligned gene expression across species

The basal ganglia are a set of subcortical structures critical for motor control, particularly in the context
of action selection, motor learning and emotional state, whose coarse functional organization is
well-described in the literature.

This page describes and links to and metadata for the HMBA-BG 10X gene
expression data, with 16,630 genes aligned across the species. In total there
are 2,035,898 cells in this gene aligned dataset. These data are a QCed subset
of those from described in the ([HMBA-10XMultiome-BG](HMBA-10XMultiome-BG.md))
page.

These data from the basis of the cross species [Basal Ganglia (BG) taxonomy](HMBA-BG-taxonomy-CCN20250428.md).

For more information on the dataset, please refer to the following webpage:
[Mammalian Basal Ganglia Consensus Cell Type Atlas](https://alleninstitute.github.io/HMBA_BasalGanglia_Consensus_Taxonomy/).

The expression matrices and associated metadata are hosted on AWS S3 bucket as
a AWS Public Dataset:

| Component | Current Version | Size    |
|---|--|---------|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/HMBA-10xMultiome-BG-Aligned/20250630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/HMBA-10xMultiome-BG-Aligned/20250630/) | 30.7 GB |
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/HMBA-10xMultiome-BG-Aligned/20250630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/HMBA-10xMultiome-BG-Aligned/20250630/) | 535.2 MB |

Data is being shared under the CC BY NC 4.0 license.

Related resources:
* Taxonomy and Clustering analysis of ~2 million single cell
  transcriptomes from the aligned dataset.
  ([HMBA-BG-taxonomy-CCN20250428](HMBA-BG-taxonomy-CCN20250428.md))
* Single cell transcriptomes for each individual species in the
  HMBA-BG dataset.([HMBA-10XMultiome-BG](HMBA-10XMultiome-BG.md))
* Spatial transcriptomic data for three species and donors ([HMBA-Spatial-BG](HMBA-Spatial-BG.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb):
  Learn how to use the ABCProjectCache object to facilitate data download and
  usage.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  Learn how to load individual genes from the 10X expression data.
* [**10X scRNA-seq clustering analysis and annotation**](../notebooks/hmba_bg_clustering_analysis_and_annotation.ipynb):
  Learn about the HMBA-BG data/metadata structure and taxonomy through example use cases and
  visualization.
[*notebooks/hmba_bg_clustering_analysis_and_annotation.ipynb*]
* [**10X scRNA-seq gene expression**](../notebooks/hmba_bg_10X_snRNASeq_tutorial.ipynb):
  Interact with HMBA-BG 10X-Aligned gene expression data. [*notebooks/hmba_bg_10X_snRNASeq_tutorial.ipynb*]
* [**Spatial transcriptomic slab coordinates and annotation**](../notebooks/hmba_bg_spatial_slabs_and_taxonomy.ipynb):
  Learn about the HMBA-BG spatial data/metadata structure and mapping to the BG taxonomy through example use
  cases and visualization.
[*notebooks/hmba_bg_spatial_slabs_and_taxonomy.ipynb*]
* [**Spatial transcriptomic gene expression**](../notebooks/hmba_bg_spatial_genes.ipynb):
  Interact with HMBA-BG spatial transcriptomic gene expression data. [*notebooks/hmba_bg_spatial_genes.ipynb*]
