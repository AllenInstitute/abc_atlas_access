# Clustering analysis of whole human brain 10X single nucleus transcriptomes

Clustering analysis of over 3 million single nucleus transcriptomes spanning
the whole adult human brain, resulting in a set of 461 clusters and 3313
subclusters. The dataset linked below contains metadata on all cells and geens
in the WHB dataset.

Full details on the dataset can be found in [Siletti et al. 2023](https://www.science.org/doi/10.1126/science.add7046).

The associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component              | Current Version                                                                                                                                              | Size     |
|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/WHB-10Xv3/20241115](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/WHB-10Xv3/20241115/) | 862.1 MB |

Data is being share under the CC BY NC 4.0 license.

Related resources :
* Human brain single nucleus transcriptomes ([WHB-10Xv3](WHB-10Xv3.md))
* Whole human brain taxonomy of cell types ([WHB-taxonomy](WHB-taxonomy.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to 
  facilitate data download and usage.
* [**10x snRNA-seq clustering analysis and annotation**](../notebooks/WHB_cluster_annotation_tutorial.ipynb):
  learn about the whole human brain taxonomy through some example use cases and
  visualization.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  learn how to load individual genes from the 10X expression data.
* **10x snRNA-seq gene expression data**
  * [**Part 1**](../notebooks/WHB-10x_snRNASeq_tutorial_part_1.ipynb): understand the basic structure of the data and metadata,
    and visualize brain region and cell type annotations in a UMAP.
  * [**Part 2**](../notebooks/WHB-10x_snRNASeq_tutorial_part_2.ipynb): explore the whole brain data through visualization and
    analyses of a set of genes of interest.
