# Human-Mammalian Brain - Basal Ganglia: Macaque Patch-seq cells multimodal data

Data and metadata for the Patch-seq component of the Human and Mammalian Brain Atlas - Basal Ganglia (HMBA-BG) dataset. 

The basal ganglia (BG) constitute a system of interconnected brain structures that play a crucial role in motor control, learning, behavior, and emotion. These structures are implicated in numerous disorders affecting human health, including Parkinson’s disease, Huntington’s disease, and substance abuse disorders. Despite their importance, little is known about the cellular-level functional properties of the BG in humans and translationally relevant primate species. To address this gap, we performed Patch-seq experiments – integrating patch clamp electrophysiology with single cell RNA-sequencing anchored in the high-resolution, cross-species HMBA consensus basal ganglia cell type taxonomy. This approach enables us to reveal the morpho-electric properties of transcriptomically-defined striatal cell types in primates. Following electrophysiological characterization, nuclei were aspirated for RNA sequencing (SMART-Seq v4), and transcriptomic profiles were mapped to the consensus taxonomy. Each sample was assigned spatial coordinates within an anatomical reference, and cells with high-quality fills and mappings were subsequently reconstructed to obtain morphological features. The data derive from macaque (Macaca mulatta and Macaca nemestrina) striatal tissue obtained through a Tissue Distribution Program. These data are directly comparable to mouse basal ganglia datasets collected using the same protocols.  

Patch-seq samples were mapped to striatal neuronal types using the Hierarchical Approximate Nearest Neighbor (HANN) method implemented in the [Allen Institute MapMyCells package](https://brain-map.org/bkp/analyze/mapmycells), excluding non-neuronal types. After applying quality control to the mapping results, 717 macaque samples were retained. For more information on the taxonomy, please refer to the following webpage: [Human and Mammalian Brain Atlas Release: Basal Ganglia](https://brain-map.org/consortia/hmba/hmba-release-basal-ganglia). Additionally, you can see the associated notebooks linked at the end of this page. 

The expression matrices and associated metadata are hosted on AWS S3 bucket as
a AWS Public Dataset:

| Component | Current Version | Size    |
|---|--|---------|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/HMBA-Macaque-PatchSeq/20260228/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/HMBA-Macaque-PatchSeq/20260228/) | 60.8 MB |
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/HMBA-Macaque-PatchSeq/20260228/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/HMBA-Macaque-PatchSeq/20260228/) | 4.5 MB |

Data is being shared under the CC BY NC 4.0 license.

Related resources:
* ~2 million single cell transcriptomes with aligned genes across species.
  ([HMBA-10XMultiome-BG-Aligned](HMBA-10XMultiome-BG-Aligned.md))
* Single cell transcriptomes for each individual species in the
  HMBA-BG dataset.([HMBA-10XMultiome-BG](HMBA-10XMultiome-BG.md))
* Taxonomy and Clustering analysis of ~2 million single cell
  transcriptomes from the aligned dataset.
  ([HMBA-BG-taxonomy-CCN20250428](HMBA-BG-taxonomy-CCN20250428.md))
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
* [**Macaque Patch-Seq notebooks**](../notebooks/hmba_bg_macaque_patchseq.ipynb):
  Interact with HMBA-BG spatial transcriptomic gene expression data. [*notebooks/hmba_bg_macaque_patchseq.ipynb*]
