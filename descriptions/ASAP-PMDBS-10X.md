# ASAP Human Postmortem-Derived Brain Sequencing Collection (PMDBS): Data Overview 

Aligning Science Across Parkinson’s (ASAP), The Michael J. Fox Foundation for
Parkinson’s Research (MJFF), and the Allen Institute for Brain Science (AIBS)
are teaming up to further the mission of the ASAP Collaborative Research
Network (CRN) program, to accelerate discoveries in the Parkinson’s disease
(PD) and neurodegenerative disease research communities. Together we will
annotate, enhance and add knowledge to the growing data catalog in the ASAP CRN
Cloud through integration of cell type taxonomies using the Allen Institute’s
MapMyCells tool and visualization through the Allen Brain Cell (ABC) Atlas web
application. This integration of data and knowledge will allow users to
visualize and explore the changes in gene expression of specific, highly
resolved brain cell types in the context of a large PD cohort of donors.

This initial collaboration focuses on the Human Postmortem-derived Brain
Sequencing Collection (PMDBS), a harmonized repository comprised of single
nucleus and PolyA RNA-seq data contributed by five ASAP CRN teams (Hafler, Lee,
Jakobsson, Scherzer, Hardy). Sequencing data were uniformly aligned to the
GRCh38.p13 reference genome (Gencode V32), quality control was performed and
low-quality cells were filtered out. A set of highly variable genes were
identified and the scVI workflow resulted in an integrated latent variable
representation, 2D UMAP coordinates and a set of 30 clusters. Currently, the
repository spans roughly 3 millions cells obtained from 9 brain regions and 211
donors with various pathologies (including healthy control). For more details
on this dataset and to access the raw data used in its preparation, please
visit the [ASAP CRN Cloud webpage](https://cloud.parkinsonsroadmap.org/collections/postmortem-derived-brain-sequencing-collection/overview).

The simplified data created by AIBS in the form of expression matrices and
associated metadata are hosted on AWS S3 bucket as a AWS Public Dataset:

| Component | Current Version                                                                                                                                                                                                       | Size  |
|---|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| Expression Matrices | [s3://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/expression_matrices/ASAP-PMDBS-10X/20250331/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/ASAP-PMDBS-10X/20250331/) | 29 GB |
| Cell and gene metadata | [s3://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/metadata/ASAP-PMDBS-10X/20250331/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/ASAP-PMDBS-10X/20250331/)                    | 660 MB |

Data is being shared under the CC BY 4.0 license.

Related resources:
* Results of running mapping the ~3 million ASAP-PMDBS cells into the WHB
  and SEA-AD taxonomies ([ASAP-PMDBS-MapMyCells](ASAP-PMDBS-MapMyCells.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to
  facilitate data download and usage.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  learn how to load individual genes from the 10X expression data.
* [**ASAP Data Overview**](../notebooks/asap_pmdbs_data_and_metadata.ipynb):
  Learn about the ASAP-PMDBS harmonized, single cell dataset including
  disease indicators and UMAP.
* [**Mapping to the Whole Human Brain Taxonomy**](../notebooks/asap_pmdbs_siletti_taxonomy.ipynb):
  Explore the mapping of the ASAP-PMDBS cells to the Siletti, Whole Human Brain
  (WHB) taxonomy produced by MapMyCells.
* [**Mapping to the SEA-AD**](../notebooks/asap_pmdbs_seaad_taxonomy.ipynb):
  Explore the mapping of the ASAP-PMDBS cells to the SEA-AD, Whole Human Brain 
  taxonomy produced by MapMyCells.
* [**10X Gene Expression**](../notebooks/asap_pmdbs_gene_expression.ipynb):
  Learn how to extract gene expression data for specific genes and visualize
  them in a UMAP.