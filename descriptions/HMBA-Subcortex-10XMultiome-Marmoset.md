# Human and Mammalian Brain Atlas (HMBA) - Marmoset Subcortex: 10X snRNA-seq Data

The Marmoset Subcortical Cell Atlas (MSCA), is a multiomic atlas of the common marmoset (Callithrix jacchus) subcortex that integrates single nucleus transcriptomics, chromatin accessibility, and spatial transcriptomics. Part of the Human and Mammalian Brain Atlas ([HMBA](https://brain-map.org/consortia/hmba)) effort within the NIH's BRAIN Initiative&reg; Cell Atlas Network ([BICAN](https://brain-bican.org/)), this dataset comprehensively samples key subcortical structures in the non-human primate, including the hippocampal formation, amygdala, olfactory areas, basal forebrain, thalamus, hypothalamus, midbrain, and major hindbrain structures (excluding cerebellar cortex). 

The dataset includes the gene expression data from the snRNA-seq component of ~680k high-quality nuclei collected via 10x Multiome (paired snRNA-seq + ATAC-seq). The entire subcortex of four adult marmoset donors (2M, 2F) was sampled via contiguous tiles and resulted in ~680k cells passing rigorous quality control (QC). The data were clustered to resolve 1,737 transcriptomic Clusters. Coupled with the anatomical anchoring provided by the Xenium spatial transcriptomics dataset, these Clusters were hierarchically organized 212 Groups and 17 Classes to form a reference cell type taxonomy of the non-human primate subcortex.

For more information on this dataset and the associated Xenium spatial transcriptomics data, please refer to the publication: [Dan, Turner, DeBerardine, et al. (2026). Spatial and regulatory organization of cell identity across the primate subcortex. Cell. https://doi.org/10.1016/j.cell.2026.10.007](https://doi.org/10.1016/j.cell.2026.10.007).

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
  transcriptomes in Marmoset ([HMBA-Subcortex-taxonomy-Marmoset](HMBA-Subcortex-taxonomy-Marmoset.md))
* Spatial transcriptomic data for the marmoset subcortex ([HMBA-Subcortex-Spatial-Marmoset](HMBA-Subcortex-Spatial-Marmoset.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb):
  Learn how to use the ABCProjectCache object to facilitate data download and
  usage.
* [**Accessing gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  Learn how to load individual genes from the gene expression data.
* [**10X snRNA-seq clustering analysis and annotation**](../notebooks/hmba_subcortex_marmoset_clustering_analysis_and_annotation.ipynb):
  Learn about the HMBA-Subcortex data/metadata structure and taxonomy through example use cases and
  visualization.
[*notebooks/hmba_subcortex_marmoset_clustering_analysis_and_annotation.ipynb*]
* [**10X snRNA-seq gene expression**](../notebooks/hmba_subcortex_marmoset_10X_RNASeq.ipynb):
  Interact with HMBA-Subcortex 10X gene expression data. [*notebooks/hmba_subcortex_marmoset_10X_RNASeq.ipynb*]
* [**Spatial transcriptomic slab coordinates and annotation**](../notebooks/hmba_subcortex_marmoset_spatial_slabs_and_taxonomy.ipynb):
  Learn about the HMBA-Subcortex spatial data/metadata structure and mapping to the Subcortex taxonomy through example use
  cases and visualization.
[*notebooks/hmba_subcortex_marmoset_spatial_slabs_and_taxonomy.ipynb*]
* [**Spatial transcriptomic gene expression**](../notebooks/hmba_subcortex_marmoset_spatial_genes.ipynb):
  Interact with HMBA-Subcortex spatial transcriptomic gene expression data. [*notebooks/hmba_subcortex_marmoset_spatial_genes.ipynb*]
