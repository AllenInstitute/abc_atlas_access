# Whole adult mouse brain taxonomy of cell types

[Clustering analysis](WMB-10X.md) of 4.0 million single cell transcriptomes spanning the whole adult mouse brain combining the [10Xv2](WMB-10Xv2.md) and [10Xv3](WMB-10Xv3.md) datasets 
was conducted resulting in a set of 5196 clusters. A detailed analysis of the clusters were preformed as described in [Yao et. al](https://www.biorxiv.org/content/10.1101/2023.03.06.531121v1). Cells from a [spatial transcriptomics](MERFISH-C57BL6J-638850.md) dataset spanning the whole mouse brain was mapped to the taxonomy to provide anatomical context.

To organize the complex molecular relationships, a hierarchical representation of cell types was defined with 5 nested levels of classification: division, class, subclass, supertype and clusters.
Further neurotransmitter identity was assigned to each cluster based on expression of canonical neurotransmitter transporter genes.


The associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component | Current Version | Size |
|---|--|--|
| Metadata | [s3://allen-brain-cell-atlas/metadata/WMB-taxonomy/20230630](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/WMB-taxonomy/20230630/) | 5.2 MB |

Data is being share under the [Allen Institute Terms of Use](https://alleninstitute.org/terms-of-use/).

Related resources :
* Whole mouse brain 10Xv2 single cell transcriptomes ([WMB-10Xv2](WMB-10Xv2.md))
* Whole mouse brain 10Xv3 single cell transcriptomes ([WMB-10Xv3](WMB-10Xv3.md))
* Whole mouse brain mouse brain clustering ([WMB-10X](WMB-10X.md))
* Whole mouse brain MERFISH spatial transcriptomics dataset ([MERFISH-C57BL6J-638850](MERFISH-C57BL6J-638850.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to faciliate data download and usage.
* [**10x scRNA-seq clustering analysis and annotation**](../notebooks/cluster_annotation_tutorial.ipynb): learn about the whole mouse brain taxonomy through some example use cases and visualization.
* **10x scRNA-seq gene expression data**
  * [**Part 1**](../notebooks/10x_snRNASeq_tutorial_part_1.ipynb): learn about the 10x dataset through some example use cases and visualization of cells in the thalamus.
  * [**Part 2a**](../notebooks/10x_snRNASeq_tutorial_part_2a.ipynb): learn how to iterate through all the data packages, to access data for whole brain example use cases in part 2b.
  * [**Part 2b**](../notebooks/10x_snRNASeq_tutorial_part_2b.ipynb): Explore the whole brain data through visualization and analyses of a set of genes of interest.
* **MERFISH whole brain spatial transcriptomics**
  * [**Part 1**](../notebooks/merfish_tutorial_part_1.ipynb): learn about the MERFISH dataset through some example use cases and visualization for a single brain section.
  * [**Part 2a**](../notebooks/merfish_tutorial_part_2a.ipynb): learn to access data and prepare for whole brain example use cases in part 2b.
  * [**Part 2b**](../notebooks/merfish_tutorial_part_2b.ipynb): Explore the whole brain data through visualization and analyses of a set of genes of interest.

