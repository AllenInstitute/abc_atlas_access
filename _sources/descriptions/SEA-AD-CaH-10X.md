# SEA-AD - Caudate Nucleus single nucleus transcriptomes

SEA-AD - Caudate Nucleus taxonomy is derived from a single nuclei transcriptomic
dataset containing 886,037 nuclei from 41 donors.

All associated metadata is publicly available as an AWS Public Dataset hosted
on Amazon S3 and through the Allen Brain Cell Atlas Access (abc_atlas_access)
package. 

The expression matrices and associated metadata are hosted on AWS S3 bucket as
a AWS Public Dataset:

| Component | Current Version | Size    |
|---|--|---------|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/SEA-AD-CaH-10X/20260630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/SEA-AD-CaH-10X/20260630/) |21.7 GB |
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/SEA-AD-CaH-10X/20260711/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/SEA-AD-CaH-10X/20260711/) | 216.4 MB |


Data is being shared under the CC BY NC 4.0 license.


Related resources:
* Taxonomy derived from from the Caudate Nucleus, reusing Supertypes and Groups
  from the SEA-AD-Multiregion and the HMBA-BG taxonomies
  ([SEA-AD-CaH-taxonomy](SEA-AD-CaH-taxonomy.md))
* Taxonomy derived from from the the SEA-AD Multiregion datasetCaudate Nucleus
  ([SEA-AD-Multiregion-taxonomy](SEA-AD-Multiregion-taxonomy.md))
* Approximately 8 million single nuclei from 84 donors across 10 brain regions.
  ([SEA-AD-Multiregion-10X](SEA-AD-Multiregion-10X.md))


Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to
  facilitate data download and usage.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  learn how to load individual genes from the 10X expression data.
* [**SEA-AD - Caudate Nucleus Cluster analysis and annotation**](../notebooks/sea-ad_cah_clustering_analysis_and_annotation.ipynb):
  Learn about the SEA-AD - Caudate Nucleus integrated taxonomy derived from 10X
  gene expression.
* [**SEA-AD - Caudate Nucleus gene expression**](../notebooks/sea-ad_cah_10X_RNASeq.ipynb):
  Learn about gene expression across the SEA-AD - Caudate Nucleus data.
* [**SEA-AD - Multiregion Cluster analysis and annotation**](../notebooks/sea-ad_multiregion_clustering_analysis_and_annotation.ipynb):
  Learn about the SEA-AD - Multiregion integrated taxonomy derived from 10X
  gene expression.
* [**SEA-AD - Multiregion gene expression**](../notebooks/sea-ad_multiregion_10X_RNASeq.ipynb):
  Learn about gene expression across the SEA-AD - Multiregion data.
