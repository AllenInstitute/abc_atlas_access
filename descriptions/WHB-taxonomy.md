# Human brain taxonomy of cell types

The data presented here from [Siletti et al. 2023](https://www.science.org/doi/10.1126/science.add7046),
consists of nuclei collect from over three million single cells (apprixmately two million neurons and one million non-neurons) from 100
locations across the forebrain, midbrain, and hindbrain. The integrated 
transcriptomic taxonomy contains 31 superclusters, 461 clusters, and 3313
subclusters.

The associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component | Current Version | Size   |
|---|--|--------|
| Cell type metadata | [s3://allen-brain-cell-atlas/metadata/WHB-taxonomy/20240330/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/WHB-taxonomy/20240330/) | 1.6 MB |

Data is being shared under the CC BY NC 4.0 license.

Related resources :
* Human brain single nucleus transcriptomes ([WHB-10Xv3](WHB-10Xv3.md))
* Clustering analysis of over 3 million single nucleus transcriptomes spanning the
  whole adult human brain ([WHB-10X-clustering](WHB-10X-clustering.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to
  facilitate data download and usage.
* [**10x snRNA-seq clustering analysis and annotation**](../notebooks/WHB_cluster_annotation_tutorial.ipynb):
  learn about the  whole human brain taxonomy through some example use cases
  and visualization.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  learn how to load individual genes from the 10X expression data.
* **10x snRNA-seq gene expression data**
  * [**Part 1**](../notebooks/WHB-10x_snRNASeq_tutorial_part_1.ipynb): learn about the 10x dataset through some example use
    cases and visualization of cells.
  * [**Part 2**](../notebooks/WHB-10x_snRNASeq_tutorial_part_2.ipynb): explore the whole brain data through visualization and
    analyses of a set of genes of interest.
