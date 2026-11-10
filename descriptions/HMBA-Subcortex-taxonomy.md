# Human and Mammalian Brain Atlas (HMBA) - Marmoset Subcortical Cell Atlas (MSCA) Cell Type Taxonomy

The Marmoset Subcortical Cell Atlas (MSCA), is a multiomic atlas of the common marmoset (Callithrix jacchus) subcortex that integrates single nucleus transcriptomics, chromatin accessibility, and spatial transcriptomics. Part of the Human and Mammalian Brain Atlas ([HMBA](https://brain-map.org/consortia/hmba)) effort within the NIH's BRAIN Initiative&reg; Cell Atlas Network ([BICAN](https://brain-bican.org/)), this dataset comprehensively samples key subcortical structures in the non-human primate, including the hippocampal formation, amygdala, olfactory areas, basal forebrain, thalamus, hypothalamus, midbrain, and major hindbrain structures (excluding cerebellar cortex). 

The MSCA reference cell type taxonomy clustered ~680k snRNA-seq cells to resolve 1,737 transcriptomic Clusters, which are hierarchically organized in 212 Groups and 17 Classes. Mapping the Xenium spatial transcriptomics cells to these Clusters provided anatomical anchoring and nomenclature to the annotated Group and Class levels. Clusters localized to basal ganglia nuclei inherited their Group labels from the companion [HMBA Basal Ganglia Cross-Species Consensus Taxonomy](https://brain-map.org/consortia/hmba/hmba-release-basal-ganglia#cell-types).

For more information on the MSCA cell type taxonomy and the associated 10X Multiome and Xenium spatial transcriptomics datasets, please refer to the publication: [Dan, Turner, DeBerardine, et al. (2026). Spatial and regulatory organization of cell identity across the primate subcortex. Cell. https://doi.org/10.1016/j.cell.2026.10.007](https://doi.org/10.1016/j.cell.2026.10.007).


The associated metadata for the cell type taxonomy and files to run MapMyCells using this taxonomy are hosted in a AWS S3 bucket as a AWS Public Dataset:

| Component              | Current Version | Size   |
|------------------------|--|--------|
| Cell taxonomy metadata | [s3://allen-brain-cell-atlas/metadata/HMBA-Subcortex-taxonomy/20261130/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/HMBA-Subcortex-taxonomy/20261130) | 189.0 MB |
| MapMyCells resources | [s3://allen-brain-cell-atlas/mapmycells/HMBA-Subcortex-taxonomy/20261130/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#mapmycells/HMBA-Subcortex-taxonomy/20261130) | 1.9 GB |

Data is being shared under the CC BY NC 4.0 license.

Related resources :
* Single cell/nuclei transcriptomes from that marmoset subcortex ([HMBA-Subcortex-10XMultiome-Marmoset](HMBA-Subcortex-10XMultiome.md))
* Spatial transcriptomic data for the marmoset subcortex ([HMBA-Subcortex-Spatial-Marmoset](HMBA-Subcortex-Spatial.md))

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
