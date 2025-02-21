# ASAP Human Postmortem-Derived Brain Sequencing Collection (PMDBS): Mapping to the Whole Human Brain (WHB) and Seattle Alzheimer’s Disease Brain Cell Atlas (SEA-AD) Taxonomies

We run the Allen Institute’s MapMyCell tool over the ASAP-PMDBS data to provide
cell type insight to the PMDBS dataset. 

[MapMyCells](https://knowledge.brain-map.org/mapmycells/process/)([RRID: SCR_024672](https://scicrunch.org/resources/data/record/nlx_144509-1/SCR_024672/resolver?q=MapMyCells&l=MapMyCells&i=rrid:scr_024672))
transforms cell types from a concept in publications to a tool for public
research. Scientists worldwide can discover what cell types their
transcriptomics and spatial data corresponds with by comparing their data to
massive, high-quality reference datasets using multiple mapping methods.
Currently available taxonomies include 10X whole mouse brain taxonomy, 10X
whole human brain taxonomy and 10X Human MTG SEA-AD taxonomy. Available
algorithms include correlation mapping (flatmap), hierarchical correlation
mapping and a deep generative model-based algorithm. 

We mapped the approximately 3 million cells of PMDBS to the 10X whole human
brain taxonomy (Siletti et. al.) and the SEA-AD taxonomy using the hierarchical
correlation mapping method where assignments are first made at the top level of
the taxonomy using mean gene expression profiles of the reference dataset and
pre-selected set of marker genes to distinguish cluster from its sibling. For
robustness, the process is repeated 100 times, using 50% of the marker genes
each time. A cell is assigned the class that receives the plurality of votes, a
probability and correlation score. This process is repeated down the taxonomy
until the last finest level.

The mappings to the Whole Human Brain (WHB) and SEA-AD taxonomies are available
on S3:

| Component | Current Version                                                                                                                                                                                                    | Size |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|
| Taxonomy  | [s3://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/metadata/ASAP-PMDBS-taxonomy/20250331/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/ASAP-PMDBS-taxonomy/20250331/) | 2 GB |

Data is being shared under the CC BY 4.0 license.

Related resources:
* Overview of the ~3 million cell ASAP-PMDBS, harmonized dataset
  ([ASAP-PMDBS-10X](ASAP-PMDBS-10X.md))

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