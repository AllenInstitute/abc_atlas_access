# Human-Mammalian Brain - Subcortex 10X RNASeq data: clustering and annotations

[INTRO TEXT]

The associated metadata is hosted in a AWS S3 bucket as a AWS Public Dataset:

| Component              | Current Version | Size   |
|------------------------|--|--------|
| Cell taxonomy metadata | [s3://allen-brain-cell-atlas/metadata/HMBA-Subcortex-taxonomy/20261130/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/HMBA-Subcortex-taxonomy/20261130) | 189.0 MB |
| MapMyCells resources | [s3://allen-brain-cell-atlas/mapmycells/HMBA-Subcortex-taxonomy/20261130/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#mapmycells/HMBA-Subcortex-taxonomy/20261130) | 1.9 GB |

Data is being shared under the CC BY NC 4.0 license.

Related resources :
* Single cell/nuclei transcriptomes from that marmoset subcortex.([HMBA-Subcortex-10XMultiome](HMBA-Subcortex-10XMultiome.md))
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