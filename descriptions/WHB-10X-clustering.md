# Clustering analysis of whole human brain 10X single cell transcriptomes

Clustering analysis of over 3 million single cell transcriptomes spanning the
whole adult human brain, resulting in a set of 461 clusters and 3313
subclusters.

Full details on the dataset can be found in [Siletti et al. 2022](https://www.biorxiv.org/content/10.1101/2022.10.12.511898v1).

The associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component | Current Version                                                                                                                                              | Size     |
|---|--------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| Metadata | [s3://allen-brain-cell-atlas/metadata/WHB-10Xv3/20240330](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/WHB-10Xv3/20240330/) | 862.1 MB |

Data is being share under the CC BY NC 4.0 license.

Related resources :
* Human brain single cell transcriptomes ([WHB-10Xv3](WHB-10Xv3.md))
* Whole human brain taxonomy of cell types ([WHB-taxonomy](WHB-taxonomy.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to faciliate data download and usage.
* [**10x scRNA-seq clustering analysis and annotation**](../notebooks/cluster_annotation_tutorial.ipynb): learn about the whole mouse brain taxonomy through some example use cases and visualization.
* **10x scRNA-seq gene expression data**
  * [**Part 1**](../notebooks/10x_snRNASeq_tutorial_part_1.ipynb): learn about the 10x dataset through some example use cases and visualization of cells in the thalamus.
  * [**Part 2a**](../notebooks/10x_snRNASeq_tutorial_part_2a.ipynb): learn how to iterate through all the data packages, to access data for whole brain example use cases in part 2b.
  * [**Part 2b**](../notebooks/10x_snRNASeq_tutorial_part_2b.ipynb): Explore the whole brain data through visualization and analyses of a set of genes of interest.
