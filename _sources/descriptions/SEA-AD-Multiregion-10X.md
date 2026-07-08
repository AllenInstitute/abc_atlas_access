# SEA-AD - Multiregion single nucleus transcriptomes

SEA-AD - Multiregion is derived from a single nuclei transcriptomic
dataset containing 8,641,342 nuclei from 84 donors. This includes gene
expression data from both snRNA-seq and Multi-ome data sets. ATAC-seq
information from the Multiome cells and additional nuclei collected from
snATAC-seq are available at [SEA-AD.org](https://brain-map.org/consortia/sea-ad).

All associated metadata is publicly available as an AWS Public Dataset hosted
on Amazon S3 and through the Allen Brain Cell Atlas Access (abc_atlas_access)
package. 

The expression matrices and associated metadata are hosted on AWS S3 bucket as
a AWS Public Dataset:

| Component | Current Version | Size    |
|---|--|---------|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/SEA-AD-Multiregion-10X/20260630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/SEA-AD-Multiregion-10X/20260630/) | 144.2 GB |
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/SEA-AD-Multiregion-10X/20260711/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/SEA-AD-Multiregion-10X/20260711/) | 2.0 GB |


Data is being shared under the CC BY NC 4.0 license.


Related resources:
* Taxonomy derived from from the the SEA-AD Multiregion datasetCaudate Nucleus
  ([SEA-AD-Multiregion-taxonomy](SEA-AD-Multiregion-taxonomy.md))
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
