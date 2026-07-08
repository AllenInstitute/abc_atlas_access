# SEA-AD - Multiregion taxonomy

Alzheimer's disease (AD) is characterized by the progressive accumulation of amyloid-beta (Aβ) plaques and hyperphosphorylated tau (pTau) tangles across brain regions. While these regions differ in architecture, function, and susceptibility to pathology, many share common cellular populations. The SEA-AD Multiregion Taxonomy was developed to provide a unified cellular framework for studying cellular vulnerability and molecular change across the full arc of canonical AD progression. 

This taxonomy is derived from a multimodal dataset generated from 84 deeply characterized donors spanning the full spectrum of AD pathology. The dataset presented here contains approximately 6 million high-quality nuclei from single-nucleus RNA-seq and Multiome profiling, along with an additional 2.6 million nuclei that did not pass quality-control criteria. These data were generated alongside approximately 1 million single-nucleus ATAC-seq profiles, which informed multimodal analyses but are not included in the resources described here. Single-nucleus profiling was performed across ten brain regions: medial entorhinal cortex (MEC), lateral entorhinal cortex (LEC), hippocampus (HIP), inferior temporal gyrus (ITG), middle temporal gyrus (MTG), superior temporal gyrus (STG), dorsolateral prefrontal cortex (BA9), frontal insula (FI), angular gyrus (AnG), and primary visual cortex (V1C). Nuclei were mapped to an expanded reference taxonomy comprising 207 cell types, organized into 28 subclasses and 3 major cellular classes, including both broadly shared and regionally specialized populations. Cell type names are harmonized between studies; for example, Sst 25 from Gabitto, Travaglini et al. (2024) and Sst 25 in this taxonomy refer to the same cell population. 

To generate this taxonomy, nuclei were subjected to standardized quality control, integrated across regions and modalities, and hierarchically mapped using deep-learning approaches based on scVI and scANVI. The resulting taxonomy provides consistent cell-type nomenclature across SEA-AD resources while preserving region-specific cellular specializations found in allocortical and neocortical regions. Spatial transcriptomic datasets were additionally used to anatomically localize newly defined excitatory populations within the hippocampus and entorhinal cortex. 

The notebooks presented here demonstrate how to access and visualize taxonomy annotations, cell type metadata, donor information, brain region annotations, and AD-associated cellular changes from the SEA-AD multiregional dataset. These examples focus on precomputed metadata accessible through the Allen Brain Cell Atlas Access package. Additional data, including links to raw sequencing, spatial transcriptomic, and neuropathology data, are available at [SEA-AD.org](https://brain-map.org/consortia/sea-ad). 

All associated metadata is publicly available as an AWS Public Dataset hosted on Amazon S3 and through the Allen Brain Cell Atlass Access (abc_atlas_access) package. 

The associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component              | Current Version | Size   |
|------------------------|--|--------|
| Cell taxonomy metadata | [s3://allen-brain-cell-atlas/metadata/SEA-AD-Multiregion-taxonomy/20260711/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/SEA-AD-Multiregion-taxonomy/20260711/) | 541.5 MB |

Data is being shared under the CC BY NC 4.0 license.

Related resources:
* Approximately 8 million single nuclei from 84 donors across 10 brain regions.
  ([SEA-AD-Multiregion-10X](SEA-AD-Multiregion-10X.md))
* Taxonomy derived from from the Caudate Nucleus, reusing Supertypes and Groups
  from the SEA-AD-Multiregion and the HMBA-BG taxonomies
  ([SEA-AD-CaH-taxonomy](SEA-AD-CaH-taxonomy.md))
* Approximately 800 thousand single nuclei from the Human Caudate.
  ([SEA-AD-CaH-10X](SEA-AD-CaH-10X.md))


Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to
  facilitate data download and usage.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  learn how to load individual genes from the 10X expression data.
* [**SEA-AD - Multiregion Cluster analysis and annotation**](../notebooks/sea-ad_multiregion_clustering_analysis_and_annotation.ipynb):
  Learn about the SEA-AD - Multiregion integrated taxonomy derived from 10X
  gene expression.
* [**SEA-AD - Multiregion gene expression**](../notebooks/sea-ad_multiregion_10X_RNASeq.ipynb):
  Learn about gene expression across the SEA-AD - Multiregion data.
* [**SEA-AD - Caudate Nucleus Cluster analysis and annotation**](../notebooks/sea-ad_cah_clustering_analysis_and_annotation.ipynb):
  Learn about the SEA-AD - Caudate Nucleus integrated taxonomy derived from 10X
  gene expression.
* [**SEA-AD - Caudate Nucleus gene expression**](../notebooks/sea-ad_cah_10X_RNASeq.ipynb):
  Learn about gene expression across the SEA-AD - Caudate Nucleus data.
