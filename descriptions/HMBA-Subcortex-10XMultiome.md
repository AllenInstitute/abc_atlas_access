# Human-Mammalian Brain - Subcortex 10X snRNASeq data

[INTRO TEXT, doesn't need to be fancy. I can just write a summary of how many nuclei/genes are in the dataset.]

The expression matrices for both raw counts and log normalized data as well as
the associated metadata are hosted on AWS S3 bucket as
a AWS Public Dataset:

| Component | Current Version | Size    |
|---|--|---------|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/HMBA-Subcortex-10xMultiome-Marmoset/20261130/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/HMBA-Subcortex-10xMultiome-Marmoset/20261130/) | 29.1 GB |
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/HMBA-Subcortex-10xMultiome-Marmoset/20261130/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/HMBA-Subcortex-10xMultiome-Marmoset/20261130/) | 648.1 MB |

Data is being shared under the CC BY NC 4.0 license.

Related resources:
* Taxonomy and Clustering analysis of ~1 million single cell/nuclei
  transcriptomes in Marmoset ([HMBA-Subcortex-taxonomy](HMBA-Subcortex-taxonomy.md))
* Spatial transcriptomic data for the marmoset subcortex ([HMBA-Subcortex-Spatial](HMBA-Subcortex-Spatial.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb):
  Learn how to use the ABCProjectCache object to facilitate data download and
  usage.
* [**Accessing gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  Learn how to load individual genes from the gene expression data.
* [**10X snRNA-seq clustering analysis and annotation**](../notebooks/hmba_subcortex_clustering_analysis_and_annotation.ipynb):
  Learn about the HMBA-Subcortex data/metadata structure and taxonomy through example use cases and
  visualization.
[*notebooks/hmba_subcortex_clustering_analysis_and_annotation.ipynb*]
* [**10X snRNA-seq gene expression**](../notebooks/hmba_subcortex_10X_RNASeq.ipynb):
  Interact with HMBA-Subcortex 10X gene expression data. [*notebooks/hmba_subcortex_10X_RNASeq.ipynb*]
* [**Spatial transcriptomic slab coordinates and annotation**](../notebooks/hmba_subcortex_spatial_slabs_and_taxonomy.ipynb):
  Learn about the HMBA-Subcortex spatial data/metadata structure and mapping to the Subcortex taxonomy through example use
  cases and visualization.
[*notebooks/hmba_subcortex_spatial_slabs_and_taxonomy.ipynb*]
* [**Spatial transcriptomic gene expression**](../notebooks/hmba_subcortex_spatial_genes.ipynb):
  Interact with HMBA-Subcortex spatial transcriptomic gene expression data. [*notebooks/hmba_subcortex_spatial_genes.ipynb*]
