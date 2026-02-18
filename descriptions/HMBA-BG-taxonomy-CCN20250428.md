# Human-Mammalian Brain - Basal Ganglia 10X snRNASeq data: clustering and annotations

The basal ganglia (BG) are a system of interconnected brain structures that
play a crucial role in motor control, learning, behavior, and emotion. With 
approximately 200 million neurons in the human basal ganglia alone, these
structures are involved in a wide range of neurological processes and are
implicated in numerous disorders affecting human health, including Parkinson’s
disease, Huntington’s disease, and substance abuse disorders. To further
understand the complexity of the basal ganglia, researchers have historically
classified its neurons into various types based on their cytoarchitecture,
connectivity, molecular profile, and functional properties. However, recent
advancements in high-throughput transcriptomic profiling have revolutionized
our ability to systematically categorize these cell types within species, while
the maturation of machine learning technologies have enabled the integration of
these taxonomies across species.

Our consensus basal ganglia cell type taxonomy is the result of iterative
clustering and cross-species integration of transcriptomic data linked in the
related resources linked below. The taxonomy encompasses neurons from key
structures within the basal ganglia, including the caudate (Ca), putamen (Pu),
nucleus accumbens (NAc), the external and internal segments of the globus
pallidus (GPe, GPi), subthalamic nucleus (STN), and substantia nigra (SN). By
combining data from multiple primate species, we have developed a consensus
taxonomy that highlights both conserved and species-specific cell types. We
validate our taxonomy through marker gene expression analysis, comparison with
previously published taxonomies, and self-projection, ensuring the accuracy and
robustness of each level in the taxonomic hierarchy across all the species.

For more information on the dataset, please refer to the following webpage:
[Human and Mammalian Brain Atlas Release: Basal Ganglia](https://brain-map.org/consortia/hmba/hmba-release-basal-ganglia).

The associated metadata is hosted in a AWS S3 bucket as a AWS Public Dataset:

| Component              | Current Version | Size   |
|------------------------|--|--------|
| Cell taxonomy metadata | [s3://allen-brain-cell-atlas/metadata/HMBA-BG-taxonomy-CCN20250428/20250630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/HMBA-BG-taxonomy-CCN20250428/20250630/) | 188.9 MB |
| MapMyCells resources | [s3://allen-brain-cell-atlas/mapmycells/HMBA-BG-taxonomy-CCN20250428/20250630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#mapmycells/HMBA-BG-taxonomy-CCN20250428/20250630/) | 2.1 GB |

Data is being shared under the CC BY NC 4.0 license.

Related resources :
* ~2 million single cell transcriptomes with aligned genes across species.
  ([HMBA-10XMultiome-BG-Aligned](HMBA-10XMultiome-BG-Aligned.md))
* Single cell transcriptomes for each individual species in the
  HMBA-BG dataset.([HMBA-10XMultiome-BG](HMBA-10XMultiome-BG.md))
* Spatial transcriptomic data for three species and donors ([HMBA-Spatial-BG](HMBA-Spatial-BG.md))
* 717 Macaque Patch-Seq cells with summary electro-physiology and morphology features.
([HMBA-Macaque-PatchSeq-BG](HMBA-Macaque-PatchSeq-BG.md))

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
* [**Macaque Patch-Seq notebooks**](../notebooks/hmba_bg_macaque_patchseq.ipynb):
  Interact with HMBA-BG spatial transcriptomic gene expression data. [*notebooks/hmba_bg_macaque_patchseq.ipynb*]
