# Whole adult mouse brain taxonomy of cell types

The Mouse Whole Brain Atlas is a high-resolution transcriptomic and spatial
cell-type atlas across the entire mouse brain, integrating several whole-brain
single-cell RNA-sequencing (scRNA-seq) datasets. The datasets contain a total
of ~4 million cells passing rigorous quality-control (QC) criteria. The
integrated transcriptomic taxonomy contains 5,322 clusters that are organized
in a hierarchical manner with nested groupings of 34 classes, 338 subclasses,
1,201 supertypes and 5,322 types/clusters. The scRNA-seq data reveal
transcriptome-wide gene expression and co-expression patterns for each cell
type. The anatomical location of each cell type has been annotated using a
comprehensive brain-wide MERFISH dataset with a total of ~4 million segmented
and QC-passed cells, probed with a 500-gene panel and registered to the Allen
Mouse Brain Common Coordinate Framework (CCF v3). The MERFISH data not only
provide accurate spatial annotation of cell types at subclass, supertype and
cluster levels, but also reveal fine-resolution spatial distinctions or
gradients for cell types. The combination of scRNA-seq and MERFISH data
reveals a high degree of correspondence between transcriptomic identity and
spatial specificity for each cell type, as well as unique features of cell
type organization in different brain regions. 

A detailed cell type [annotation table](https://allen-brain-cell-atlas.s3-us-west-2.amazonaws.com/metadata/WMB-taxonomy/20231215/cl.df_CCN202307220.xlsx)
is also provided along with data downloads detailing information about the
hierarchical membership, anatomical annotation, neurotransmitter type, cell
type marker genes, transcription factor and neuropeptide markers, and other
metadata types for each cluster.

The associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component | Current Version | Size |
|---|--|--|
| Metadata | [s3://allen-brain-cell-atlas/metadata/WMB-taxonomy/20231215](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/WMB-taxonomy/20231215/) | 0.01 GB |

Data is being share under the CC BY NC 4.0 license.

Related resources :
* Whole mouse brain mouse brain clustering ([WMB-10X](WMB-10X.md))
* Whole mouse brain MERFISH spatial transcriptomics dataset ([MERFISH-C57BL6J-638850](MERFISH-C57BL6J-638850.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to
  facilitate data download and usage.
* [**10x scRNA-seq clustering analysis and annotation**](../notebooks/cluster_annotation_tutorial.ipynb): learn about the
  whole mouse brain taxonomy through some example use cases and visualization.
* **10x scRNA-seq gene expression data**
  * [**Part 1**](../notebooks/10x_snRNASeq_tutorial_part_1.ipynb): learn about the 10x dataset through some example use
    cases and visualization of cells in the thalamus.
  * [**Part 2a**](../notebooks/10x_snRNASeq_tutorial_part_2a.ipynb): learn how to iterate through all the data packages, to
    access data for whole brain example use cases in part 2b.
  * [**Part 2b**](../notebooks/10x_snRNASeq_tutorial_part_2b.ipynb): Explore the whole brain data through visualization and
    analyses of a set of genes of interest.
* **MERFISH whole brain spatial transcriptomics**
  * [**Part 1**](../notebooks/merfish_tutorial_part_1.ipynb): learn about the MERFISH dataset through some example use
    cases and visualization for a single brain section.
  * [**Part 2a**](../notebooks/merfish_tutorial_part_2a.ipynb): learn to access data and prepare for whole brain
    example use cases in part 2b.
  * [**Part 2b**](../notebooks/merfish_tutorial_part_2b.ipynb): Explore the whole brain data through visualization and
    analyses of a set of genes of interest.

