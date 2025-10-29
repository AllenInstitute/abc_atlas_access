# Consensus Whole Mouse Brain integrated taxonomy

The Consensus, Whole Mouse Brain (WMB) integrated taxonomy is built upon two publicly released transcriptionally defined WMB taxonomies: one derived from single-cell RNA sequencing (scRNA-seq) data and the other from single-nucleus RNA sequencing (snRNA-seq) data. The[Allen Institute for Brain Science (AIBS) taxonomy](https://alleninstitute.github.io/abc_atlas_access/descriptions/WMB-taxonomy.html), based on over 4 million scRNA-seq profiles, defines 5,322 clusters organized hierarchically into 34 classes, 338 subclasses, and 1,201 supertypes. The set of data products for this release can be found [here](https://alleninstitute.github.io/abc_atlas_access/descriptions/WMB_dataset.html). In parallel, the Broad Institute taxonomy, constructed from 4.4 million snRNA-seq profiles, defines 16 classes, 223 metaclusters, and 5,030 clusters. Integrating these two large-scale taxonomies into a unified framework represents a natural and impactful next step, enabling a consensus view of cell types across the entire mouse brain and benefiting the broader neuroscience community.

To generate this consensus taxonomy, we applied the AIBS Quality Control (QC) and post-integration QC pipelines, retaining 7,651,713 cells and nuclei. Integration of scRNA-seq and snRNA-seq data was performed using scVI, with subsampling by original clusters to mitigate sampling imbalance across cell types and brain regions, followed by projection of all remaining cells into a shared latent space. The same iterative clustering strategy used in the AIBS taxonomy was applied in a hierarchical manner—globally, at nine neighborhood levels, and across eight finer group levels. The resulting comprehensive taxonomy comprises a hierarchically arranged set of cell types with 9 neighborhoods, 42 classes, 414 subclasses, 1,397 supertypes, and 6,721 clusters. A detailed cell type annotation table accompanies the taxonomy, including hierarchical membership, anatomical localization, neurotransmitter identity, marker genes, transcription factors, and neuropeptides. All associated metadata is publicly available as an AWS Public Dataset hosted on Amazon S3
and through the Allen Brain Cell Atlass Access (abc_atlas_access) package.

The associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component              | Current Version | Size   |
|------------------------|--|--------|
| Cell taxonomy metadata | [s3://allen-brain-cell-atlas/metadata/Consensus-Mouse-taxonoy/20251031/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Consensus-WMB-integrated-taxonoy/20251031/) | XX MB |

Data is being shared under the CC BY NC 4.0 license.

Related resources:
* Combined data and metadata for both whole mouse brain datasets containing a total of ~7 million cells
  ([Consensus-WMB-10X](Consensus-WMB-10X.md))
* Previously released WMB-AIBS dataset ([WMB_dataset](WMB_dataset.md))


Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to
  facilitate data download and usage.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  learn how to load individual genes from the 10X expression data.
* [**Consensus Whole Mouse Brian integrated taxonomy and clustering**](../notebooks/consensus_mouse_clustering_analysis_and_annotation.ipynb):
  Learn about the Consensus Whole Mouse Brain integrated taxonomy derived from the WMB-AIBS and WMB-Macosko datasets.
* [**Consensus Whole Mouse Brain gene expression**](../notebooks/consensus_mouse_10X_snRNASeq.ipynb):
  learn about gene expression across the two Consensus Whole Mouse Brain datasets.
