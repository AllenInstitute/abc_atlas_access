# MERFISH spatial transcriptomics dataset of a single adult mouse brain (Zhuang-C57BL6J-1)

2.8 million cell spatial transcriptomics dataset spanning 147 coronal sections with a 1122 gene panel and mapped to the  [whole mouse brain taxonomy](WMB-taxonomy.md) and [Allen-CCF-2020](Allen-CCF-2020.md). Refer to [Zhang et al, 2023](https://doi.org/10.1101/2023.03.06.531348) for more details.

The expression matrices and associated metadata is hosted on AWS S3 bucket as an AWS Public Dataset:

| Component | Current Version | Size |
|---|--|---|
| Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/Zhuang-C57BL6J-1/20230830/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/Zhuang-C57BL6J-1/20230830/) | 2.98 GB |
| Metadata | [s3://allen-brain-cell-atlas/metadata/Zhuang-C57BL6J-1/20230830](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Zhuang-C57BL6J-1/20230830/) | 1.27 GB |
| CCF Coordinates | [s3://allen-brain-cell-atlas/metadata/Zhuang-C57BL6J-1-CCF/20230830](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Zhuang-C57BL6J-1-CCF/20230830/) | 0.21 GB |

Data is being shared under the CC BY 4.0 license.

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to faciliate data download and usage.
* [**MERFISH whole mouse brain spatial transcriptomics**](../notebooks/zhuang_merfish_tutorial.ipynb): learn about the MERFISH dataset through some example use cases and visualization
