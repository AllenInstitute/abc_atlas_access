# Developing Mouse - Visual Cortex taxonomy

The Developing Mouse - Visual Cortex taxonomy is derived from a single cell transcriptomic dataset containing 568,654 cells from donors ranging in age from embryonic to adult. The cell-type assignment is a four level taxonomy defining 15 classes, 40 subclasses, 148 clusters and 714 subclusters. This cell-type assignment is broadly consistent with those from the previous studies from the [Allen Institute for Brain Science, Whole Mouse Brain (WMB)](WMB-taxonomy.md) and the [Broad Institute whole mouse brain taxonomy](Consensus-WMB-taxonomy.md) at the subclass level while providing finer cell-type and temporal resolutions with additional subcluster annotations.

To generate this developing taxonomy, we applied the Quality Control (QC) and post-integration QC pipelines. Integration and label transfer of scRNA-seq between ages was performed using Seurat/scVI. A detailed cell type annotation table accompanies the taxonomy, including hierarchical membership and anatomical localization.

All associated metadata is publicly available as an AWS Public Dataset hosted on Amazon S3 and through the Allen Brain Cell Atlass Access (abc_atlas_access) package. 

The associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component              | Current Version | Size   |
|------------------------|--|--------|
| Cell taxonomy metadata | [s3://allen-brain-cell-atlas/metadata/Developing-Mouse-Vis-Cortex-10X/20260131/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Developing-Mouse-Vis-Cortex-10X/20260131/) | 1.2 GB |

Data is being shared under the CC BY NC 4.0 license.

Related resources:
* Approximately 500 thousand single cells from mouse brains ranging in age from
  embryo to adult. ([Dev-Mouse-Vis-Cortex-10X](Dev-Mouse-Vis-Cortex-10X.md))


Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to
  facilitate data download and usage.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  learn how to load individual genes from the 10X expression data.
* [**Developing Mouse - Visual Cortex Cluster analysis and annotation**](../notebooks/dev_mouse_vis_cortex_clustering_analysis_and_annotation.ipynb):
  Learn about the Developing Mouse - Visual Cortex integrated taxonomy derived from 10X gene expression.
* [**Developing Mouse - Visual Cortex gene expression**](../notebooks/dev_mouse_vis_cortex_10X_scRNASeq.ipynb):
  Learn about gene expression across the Developing Mouse - Visual Cortex 10X data.
