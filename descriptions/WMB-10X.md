# Clustering analysis of whole adult mouse brain 10X single cell transcriptomes

Clustering analysis of 4.0 million single cell transcriptomes spanning the 
whole adult mouse brain combining the [10Xv2](WMB-10Xv2.md) and [10Xv3](WMB-10Xv3.md) datasets,
resulting in a set of 5196 clusters.

This is one of the steps towards creating a high resolution transcriptomic and
spatial atlas of cell types described in [Yao et al.](https://www.biorxiv.org/content/10.1101/2023.03.06.531121v1).

The associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component | Current Version | Size |
|---|--|--|
| Metadata | [s3://allen-brain-cell-atlas/metadata/WMB-10X/20241115](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/WMB-10X/20241115/) | 2.39 GB |
| MapMyCells resources | [s3://allen-brain-cell-atlas/mapmycells/WMB-10X/20240831/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#mapmycells/WMB-10X/20240831/) | 1.3 GB |

Data is being share under the CC BY NC 4.0 license.

Related resources :
* Whole mouse brain 10Xv2 single cell transcriptomes ([WMB-10Xv2](WMB-10Xv2.md))
* Whole mouse brain 10Xv3 single cell transcriptomes ([WMB-10Xv3](WMB-10Xv3.md))
* Whole mouse brain 10XMulti single cell transcriptomes ([WMB-10XMulti](WMB-10XMulti.md))
* Whole mouse brain mouse taxonomy of cell types ([WMB-taxonomy](WMB-taxonomy.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the AbcProjectCache to
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
