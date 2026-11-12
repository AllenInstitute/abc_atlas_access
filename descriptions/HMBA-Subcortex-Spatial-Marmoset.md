# Human and Mammalian Brain Atlas (HMBA) - Marmoset Subcortex: 10X Xenium Spatial Transcriptomics Data

The Marmoset Subcortical Cell Atlas (MSCA), is a multiomic atlas of the common marmoset (Callithrix jacchus) subcortex that integrates single nucleus transcriptomics, chromatin accessibility, and spatial transcriptomics. Part of the Human and Mammalian Brain Atlas ([HMBA](https://brain-map.org/consortia/hmba)) effort within the NIH's BRAIN Initiative&reg; Cell Atlas Network ([BICAN](https://brain-bican.org/)), this dataset comprehensively samples key subcortical structures in the non-human primate, including the hippocampal formation, amygdala, olfactory areas, basal forebrain, thalamus, hypothalamus, midbrain, and major hindbrain structures (excluding cerebellar cortex). 

This cellular-resolution Xenium spatial transcriptomic dataset includes 5.6 million cells profiled from 47 coronal hemisections from a single adult male marmoset donor, sampling the rostral-caudal extent of subcortical structures. The spatial cells were mapped to the 1,737 snRNA-seq Clusters defined in the MSCA reference cell type taxonomy, and the resulting spatial localization of the Clusters provided anatomical anchoring and nomenclature to the Group and Class hierarchy levels of the MSCA taxonomy.

For more information on this dataset and the associated 10X Multiome data, please refer to the publication: [Dan, Turner, DeBerardine, et al. (2026). Spatial and regulatory organization of cell identity across the primate subcortex. Cell. https://doi.org/10.1016/j.cell.2026.10.007](https://doi.org/10.1016/j.cell.2026.10.007).

The expression matrices for raw counts, batch-normalized counts, and natural logarithm transformed batch-normalized counts, 
as well as the associated cellular metadata and geojson polygons defining the hemisection outlines are hosted on AWS S3 bucket as
a AWS Public Dataset:
| Component | Current Version | Size    |
|---|--|---------|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/HMBA-Subcortex-Xenium-Marmoset/20261130/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/HMBA-Subcortex-Xenium-Marmoset/20261130/) | 3.3 GB |
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/HMBA-Subcortex-Xenium-Marmoset/20261130/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/HMBA-Subcortex-Xenium-Marmoset/20261130/) | 4.8 GB |
| Image volumes and polygons | [s3://allen-brain-cell-atlas/image_volumes/HMBA-Subcortex-Xenium-Marmoset/20261130/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#image_volumes/HMBA-Subcortex-Xenium-Marmoset/20261130/) | 58.7 KB |

You can find descriptions of the columns on the Resources page under [Metadata Descriptions](https://github.com/AllenInstitute/abc_atlas_access/blob/u/morriscb/hmbabgSpatialUpdate/docs/supplemental_metadata_descriptions/hmba_bg_column_descriptions.csv)


Data is being shared under the CC BY NC 4.0 license.


Related resources:
* Taxonomy and Clustering analysis of ~1 million single nuclei
  transcriptomes in Marmoset ([HMBA-Subcortex-taxonomy-Marmoset](HMBA-Subcortex-taxonomy-Marmoset.md))
* Single nuclei transcriptomes from that marmoset subcortex.([HMBA-Subcortex-10XMultiome-Marmoset](HMBA-Subcortex-10XMultiome-Marmoset.md))


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
