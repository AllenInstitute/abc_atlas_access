# Allen Brain Cell Atlas - Data Access

The Allen Brain Cell Atlas (ABC Atlas) aims to empower researchers worldwide to
explore and analyze multiple whole-brain datasets simultaneously. As the Allen
Institute and its collaborators continue to add new modalities, species, and
insights to the ABC Atlas, this groundbreaking platform will keep growing,
opening up endless possibilities for groundbreaking discoveries and
breakthroughs in neuroscience. With the ABC Atlas, researchers everywhere can
gain new insights into the brain’s complex workings, advancing our
understanding of this amazing organ in ways we never thought possible. The
ABC Atlas can be accessed at [here](https://portal.brain-map.org/atlases-and-data/bkp/abc-atlas)
and is the primary method of interacting with these data. Any questions or
issues associated with the ABC Atlas are best directed to the [Allen Institute
Commnituy Forum](https://community.brain-map.org/). This repository is intended
for users who wish to download the ABC Atlas data and processes it locally.

Data associated with the ABC Atlas is hosted on Amazon Web Services (AWS) in an
S3 bucket as a AWS Public Dataset, [arn:aws:s3:::allen-brain-cell-atlas](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html).
No account or login is required for access. The purpose of this repo is to
provide an overview of the available data, how to download and use it through
example use cases.

The spring 2024 public beta data release includes:
* **[Mouse whole-brain transcriptomic cell type atlas](descriptions/WMB_dataset.md)
  (Hongkui Zeng)**
* **[A molecularly defined and spatially resolved cell atlas of the whole mouse brain](descriptions/Zhuang_dataset.md)
  (Xiaowei Zhuang)**
* **[Human whole-brain transcriptomic cell type atlas](descriptions/WHB_dataset.md)
  (Kimberly Siletti)**

We provide a lightweight python object, the AbcProjectCache, to handle
downloading of the data and managing different release versions for the user.
See the [Getting Started](notebooks/getting_started.ipynb) notebook for more
details and examples on how to use the AbcProjectCache.

Expression matrices are stored in the
[anndata h5ad format](https://anndata.readthedocs.io/en/latest/) and need to
be downloaded to a local file system for usage. To make data transfer, download
and access more efficient, the 10x transcriptomics datasets have been
subdivided into smaller packages grouped by method and anatomical origin. The
notebooks provide example code on how to access data across these individual
files using the AbcProjectCache.

Available notebooks:

* [**Getting started**](notebooks/getting_started.ipynb): learn how to use the
  AbcProjectCache to facilitate data download and usage.
[*notebooks/getting_started.ipynb*]
* [**Loading genes from expression matrix data**](notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  learn how to select genes from 10X expression matricies and combine them with
  the cell metadata.
* **[Mouse whole-brain transcriptomic cell type atlas](descriptions/notebook_subtitle1.md)
  (Hongkui Zeng)**
* **[A molecularly defined and spatially resolved cell atlas of the whole
  mouse brain](descriptions/notebook_subtitle4.md)
  (Xiaowei Zhuang)**
* **[Human whole-brain transcriptomic cell type atlas](descriptions/WHB_notebooks.md)
  (Kimberly Siletti)**

## Release Notes
* **[abc_atlas_access (v0.1.0)]**
  * Fixed issue with loading 10X mouse data with the `get_gene_data` function.
* **[Spring 2024 Public Beta (version 20240330)]**
  * Added Whole Human Brain transcriptomic, taxonomy and clustering datasets
    from Siletti et al. 2023 to the ABC Atlas.
  * Added new AbcProjectCache python class to facilitate data download and
    usage.
    * Added file hashes to the manifest.json to facilitate data integrity
      checks in the cache class.
  * Updated all jupyter notebooks to use the new AbcProjectCache class.
  * Added new notebooks for the whole human brain datasets.
  * Re-organized jupyter-book webpages.
