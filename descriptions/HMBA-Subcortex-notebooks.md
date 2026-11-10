# Human and Mammalian Brain Atlas (HMBA) - Marmoset Subcortex: Notebooks

The Marmoset Subcortical Cell Atlas (MSCA), is a multiomic atlas of the common marmoset (Callithrix jacchus) subcortex that integrates single nucleus transcriptomics, chromatin accessibility, and spatial transcriptomics. Part of the Human and Mammalian Brain Atlas ([HMBA](https://brain-map.org/consortia/hmba)) effort within the NIH's BRAIN Initiative&reg; Cell Atlas Network ([BICAN](https://brain-bican.org/)), this dataset comprehensively samples key subcortical structures in the non-human primate, including the hippocampal formation, amygdala, olfactory areas, basal forebrain, thalamus, hypothalamus, midbrain, and major hindbrain structures (excluding cerebellar cortex). 

The MSCA reference cell type taxonomy clustered ~680k snRNA-seq cells to resolve 1,737 transcriptomic Clusters, which are hierarchically organized in 212 Groups and 17 Classes. Mapping 5.6 million Xenium spatial transcriptomics cells to these Clusters provided anatomical anchoring and nomenclature to the annotated Group and Class levels. Clusters localized to basal ganglia nuclei inherited their Group labels from the companion [HMBA Basal Ganglia Cross-Species Consensus Taxonomy](https://brain-map.org/consortia/hmba/hmba-release-basal-ganglia#cell-types).

For more information on the MSCA cell type taxonomy and the associated 10X Multiome and Xenium spatial transcriptomics datasets, please refer to the publication: [Dan, Turner, DeBerardine, et al. (2026). Spatial and regulatory organization of cell identity across the primate subcortex. Cell. https://doi.org/10.1016/j.cell.2026.10.007](https://doi.org/10.1016/j.cell.2026.10.007).

Tutorial notebooks to access the cell type taxonomy and datasets:

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
