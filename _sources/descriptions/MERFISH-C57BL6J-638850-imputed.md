# Imputed MERFISH spatial transcriptomics of a single adult mouse brain

The MERFISH spatial transcriptomics dataset ([MERFISH-C57BL6J-638850](MERFISH-C57BL6J-638850.md)) was mapped
to the whole mouse brain taxonomy ([WMB-taxonomy](WMB-taxonomy.md)) using a [hierarchical
correlation method](https://github.com/AllenInstitute/scrattch.mapping). To further integrate the transcriptomics and spatial
profiles of each cell type, 10Xv3 expression was projected or imputed into the
MERFISH space. The basic idea is to compute the k-nearest neighbors (KNNs)
among the 10Xv3 cells for each MERFISH cell and use the average expression of
these neighbors for each gene as the imputed values. Imputed expression values
were generated for 8,460 marker genes.  Further details can be found in the
methods section of [Yao et. al](https://www.nature.com/articles/s41586-023-06812-z).

| Component | Current Version                                                                                                                                                                                                              | Size  |
|---|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/MERFISH-C57BL6J-638850-imputed/20240831](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/MERFISH-C57BL6J-638850-imputed/20240831/) | 47 GB |
| Metadata | [s3://allen-brain-cell-atlas/metadata/MERFISH-C57BL6J-638850-imputed/20240831](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/MERFISH-C57BL6J-638850-imputed/20240831/)                       | 1 MB  |

Data is being share under the CC BY NC 4.0 license.

Related resources :
* Whole mouse brain clustering ([WMB-10X](WMB-10X.md))
* Whole mouse brain mouse taxonomy of cell types ([WMB-taxonomy](WMB-taxonomy.md))
* Whole mouse brain MERFISH spatial transcriptomics dataset ([MERFISH-C57BL6J-638850](MERFISH-C57BL6J-638850.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the AbcProjectCache to
  facilitate data download and usage.
* [**10x scRNA-seq clustering analysis and annotation**](../notebooks/cluster_annotation_tutorial.ipynb): learn about the
  whole mouse brain taxonomy through some example use cases and visualization.
* **MERFISH whole brain spatial transcriptomics**
  * [**Part 1**](../notebooks/merfish_tutorial_part_1.ipynb): Learn about the MERFISH dataset through some example use
    cases and visualization for a single brain section.
  * [**Part 2a**](../notebooks/merfish_tutorial_part_2a.ipynb): Learn to access data and prepare for whole brain.
    example use cases in part 2b.
  * [**Part 2b**](../notebooks/merfish_tutorial_part_2b.ipynb): Explore the whole brain data through visualization and
    analyses of a set of genes of interest.
  * [**MERFISH imputed genes**](../notebooks/merfish_imputed_genes_example.ipynb):
    Learn about the using the imputed genes of the MERFISH dataset.