# MERFISH spatial transcriptomics dataset of a single adult mouse brain

A 4.0 million cell spatial transcriptomics dataset spanning a single adult
mouse brain with a 500 gene panel and mapped to the
[whole mouse brain taxonomy](WMB-taxonomy.md). It was used in the creation of a high
resolution transcriptomic and spatial atlas of cell types described in
[Yao et al.](https://www.biorxiv.org/content/10.1101/2023.03.06.531121v1).

The expression matrices and associated metadata is hosted on AWS S3 bucket as a
AWS Public Dataset:

| Component | Current Version | Size |
|---|--|---|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/MERFISH-C57BL6J-638850/20230830](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/MERFISH-C57BL6J-638850/20230830/) | 14.2 GB |
| Metadata | [s3://allen-brain-cell-atlas/metadata/MERFISH-C57BL6J-638850/20231215](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/MERFISH-C57BL6J-638850/20231215/) | 1.81 GB |

Data is being share under the CC BY NC 4.0 license.

Related resources :
* Whole mouse brain clustering ([WMB-10X](WMB-10X.md))
* Whole mouse brain mouse taxonomy of cell types ([WMB-taxonomy](WMB-taxonomy.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the AbcProjectCache to
  facilitate data download and usage.
* [**10x scRNA-seq clustering analysis and annotation**](../notebooks/cluster_annotation_tutorial.ipynb): learn about the
  whole mouse brain taxonomy through some example use cases and visualization.
* * **MERFISH whole brain spatial transcriptomics**
  * [**Part 1**](../notebooks/merfish_tutorial_part_1.ipynb): learn about the MERFISH dataset through some example use
    cases and visualization for a single brain section.
  * [**Part 2a**](../notebooks/merfish_tutorial_part_2a.ipynb): learn to access data and prepare for whole brain
    example use cases in part 2b.
  * [**Part 2b**](../notebooks/merfish_tutorial_part_2b.ipynb): Explore the whole brain data through visualization and
    analyses of a set of genes of interest.
