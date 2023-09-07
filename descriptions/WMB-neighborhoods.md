# Cluster groups and neighborhood specific UMAP embeddings

To further investigate the neuronal diversity within each major brain structure, [Yao et. al](https://www.biorxiv.org/content/10.1101/2023.03.06.531121v1) created the concept of cell types "neighborhoods" or groups and used them for visualization and analysis. For each neighborhood, they generated re-embedded UMAPS to reveal fine-grained relationships between neuronal types ([WMB-taxonomy](WMB-taxonomy.md)) within and between brain regions.

The associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component | Current Version | Size |
|---|--|--|
| Metadata | [s3://allen-brain-cell-atlas/metadata/WMB-neighborhoods/20230830](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/WMB-neighborhoods/20230830/) | 5.2 MB |

Data is being shared under the CC BY NC 4.0 license.

Related resources :
* Whole mouse brain 10Xv2 single cell transcriptomes ([WMB-10Xv2](WMB-10Xv2.md))
* Whole mouse brain 10Xv3 single cell transcriptomes ([WMB-10Xv3](WMB-10Xv3.md))
* Whole mouse brain mouse brain clustering ([WMB-10X](WMB-10X.md))
* Whole mouse brain mouse taxonomy of cell types ([WMB-taxonomy](WMB-taxonomy.md))
* Whole mouse brain MERFISH spatial transcriptomics dataset ([MERFISH-C57BL6J-638850](MERFISH-C57BL6J-638850.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to faciliate data download and usage.
* [**10x scRNA-seq clustering analysis and annotation**](../notebooks/cluster_annotation_tutorial.ipynb): learn about the whole mouse brain taxonomy through some example use cases and visualizations.
* **10x scRNA-seq gene expression data**
  * [**Part 1**](../notebooks/10x_snRNASeq_tutorial_part_1.ipynb): learn about the 10x dataset through some example use cases and visualizations of cells in the thalamus.
  * [**Part 2a**](../notebooks/10x_snRNASeq_tutorial_part_2a.ipynb): learn how to iterate through all the data packages, to access data for whole brain example use cases in part 2b.
  * [**Part 2b**](../notebooks/10x_snRNASeq_tutorial_part_2b.ipynb): Explore the whole brain data through visualization and analyses of a set of genes of interest.
* **MERFISH whole brain spatial transcriptomics**
  * [**Part 1**](../notebooks/merfish_tutorial_part_1.ipynb): learn about the MERFISH dataset through some example use cases and visualizations for a single brain section.
  * [**Part 2a**](../notebooks/merfish_tutorial_part_2a.ipynb): learn to access data and prepare for whole brain example use cases in part 2b.
  * [**Part 2b**](../notebooks/merfish_tutorial_part_2b.ipynb): Explore the whole brain data through visualization and analyses of a set of genes of interest.
* [**Cluster groups and embeddings**](../notebooks/cluster_groups_and_embeddings_tutorial.ipynb): learn about cell types neighborhoods and neighborhood specific UMAP embeddings through example use cases.
*  [**Cell type neighborhood gallery**](../notebooks/cluster_neighborhood_gallery.ipynb): explore and visualize a set of cell types neighborhoods.

