# MERFISH spatial transcriptomics dataset of a single adult mouse brain (Zhuang-ABCA-4)

0.22 million cell spatial transcriptomics dataset spanning 3 sagittal sections
with a 1122 gene panel and mapped to the  [whole mouse brain taxonomy](WMB-taxonomy.md) and
[Allen-CCF-2020](Allen-CCF-2020.md). We performed MERFISH imaging on 3 sagittal sections from
this animal, obtained 0.22 million segmented cells that passed quality control,
and integrated the MERFISH data (including data from all four animals) with the
scRNA-seq data from the Allen Institute to classify cells. We applied a series
of filters to select a subset of cells to be visualized on the ABC atlas. We
aligned the spatial coordinates of the cells to the Allen-CCF-2020. For all the
three slices that can be registered to the CCF, we used the CCF coordinates to
define the coordinates of the center point of the tissue and removed cells that
substantially passed the posterior edge (which has not been registered to the
CCF). The x, y coordinates are experimentally measured coordinates after
rotating and aligning the tissue slices to the CCF, and the z coordinates are
estimated position of each tissue slice in the 3D Allen-CCF 2020 space along
the medial-lateral axis based on registration results. 0.22 million cells
remained after this step. The cell-by-gene matrix of the 0.22 millions cells
can be downloaded from the AWS bucket of this animal. We then filtered the
cells by cell-classification (label transfer) confidence scores calculated
during MERFISH-scRNAseq data integration. 0.19 million cells passed the
confidence score threshold for cell subclass label transfer and 0.16 million
cells further passed the confidence score threshold for cell cluster label
transfer. These 0.16 million cells are included in the cell metadata file that
can be downloaded from the AWS bucket and are displayed on the ABC Atlas. The
CCF coordinates of the 0.16 million cells that were registered to the 3D
Allen-CCF can be downloaded from the CCF coordinate file in the AWB bucket.
Refer to [Zhang et al. 2023](https://doi.org/10.1101/2023.03.06.531348) for more details.

The expression matrices and associated metadata is hosted on AWS S3 bucket as a
AWS Public Dataset:

| Component | Current Version | Size |
|---|--|---|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/Zhuang-ABCA-4/20230830/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/Zhuang-ABCA-4/20230830/) | 0.16 GB |
| Metadata | [s3://allen-brain-cell-atlas/metadata/Zhuang-ABCA-4/20241115](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Zhuang-ABCA-4/20241115/) | 0.08 GB |
| CCF Coordinates | [s3://allen-brain-cell-atlas/metadata/Zhuang-ABCA-4-CCF/20230830](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Zhuang-ABCA-4-CCF/20230830/) | 0.01 GB |

Data is being share under the CC BY 4.0 license.

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the AbcProjectCache to
  facilitate data download and usage.
* [**MERFISH whole mouse brain spatial transcriptomics**](../notebooks/zhuang_merfish_tutorial.ipynb): learn about the
  MERFISH dataset through some example use cases and visualization
