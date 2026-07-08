# SEA-AD - Caudate Nucleus taxonomy

The caudate nucleus (Ca) is a "C"-shaped subcortical structure that pairs with the putamen to form the striatum, a component of the basal ganglia. Beyond its role in motor control, the caudate participates in cognitive processes such as procedural memory and associative learning, and it is implicated in several neurodegenerative diseases, including Parkinson's, Huntington's, and Alzheimer's. In Alzheimer's specifically, the presence of amyloid-$\beta$ plaques in the head of the caudate partly defines Thal stage III. Here we introduce the SEA-AD Caudate Head Atlas, a cellular-resolution view of Alzheimer's disease pathology in the caudate head of human donors.

This dataset comprises ~800,000 single cells from a 42-donor subset of the original 84-donor SEA-AD cohort, selected to minimize comorbidities with other known brain diseases. Disease progression is quantified with a continuous pseudo-progression score (`CPS`), derived from a biophysical model of disease progression fit to quantitative neuropathology from the region. Standard staging measures are also included: overall AD neuropathologic change (`ADNC`), `Braak`, and `Thal`. To annotate the data, we integrated two references — the Human and Mammalian Brain Atlas (HMBA) of the basal ganglia and the SEA-AD middle temporal gyrus (MTG) atlas — merging overlapping classes into the SEA-AD taxonomy. Quality control was performed after integration: for each cluster, thresholds were set on standard metrics including `Genes Detected`, `Doublet score`, and `Fraction mitochondrial UMIs`.

The notebooks presented here demonstrate how to access and visualize taxonomy annotations, cell type metadata, donor information, brain region annotations, and AD-associated cellular changes from the SEA-AD CaH dataset. These examples focus on precomputed metadata accessible through the Allen Brain Cell Atlas Access package. Additional data, including links to raw sequencing, spatial transcriptomic, and neuropathology data, are available at [SEA-AD.org](https://brain-map.org/consortia/sea-ad).

All associated metadata is publicly available as an AWS Public Dataset hosted on Amazon S3 and through the Allen Brain Cell Atlass Access (abc_atlas_access) package. 

The associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component              | Current Version | Size   |
|------------------------|--|--------|
| Cell taxonomy metadata | [s3://allen-brain-cell-atlas/metadata/SEA-AD-CaH-taxonomy/20260711/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/SEA-AD-CaH-taxonomy/20260711/) | 79.3 MB |


Data is being shared under the CC BY NC 4.0 license.


Related resources:
* Approximately 800 thousand single nuclei from the Human Caudate.
  ([SEA-AD-CaH-10X](SEA-AD-CaH-10X.md))
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
