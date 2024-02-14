# Allen Brain Cell Atlas - Data Access

The Allen Brain Cell Atlas (ABC Atlas) aims to empower researchers worldwide to
explore and analyze multiple whole-brain datasets simultaneously. As the Allen
Institute and its collaborators continue to add new modalities, species, and
insights to the ABC Atlas, this groundbreaking platform will keep growing,
opening up endless possibilities for groundbreaking discoveries and
breakthroughs in neuroscience. With the ABC Atlas, researchers everywhere can
gain new insights into the brain’s complex workings, advancing our
understanding of this amazing organ in ways we never thought possible.

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
* **[Mouse whole-brain transcriptomic cell type atlas](descriptions/notebook_subtitle1.md)
  (Hongkui Zeng)**
* **[A molecularly defined and spatially resolved cell atlas of the whole
  mouse brain](descriptions/notebook_subtitle4.md)
  (Xiaowei Zhuang)**
* **[Human whole-brain transcriptomic cell type atlas](descriptions/WHB_dataset.md)
  (Kimberly Siletti)**

## Release Notes
* **[Spring 2024 Public Beta (version 20240330)]**
  * Added Whole Human Brain transcriptomic, taxonomy and clustering datasets
    from Siletti et al. 2022 to the ABC Atlas.
  * Added new AbcProjectCache python class to facilitate data download and
    usage.
    * Added file hashes to the manifest.json to facilitate data integrity
      checks in the cache class.
  * Updated all jupyter notebooks to use the new AbcProjectCache class.
  * Added new notebooks for the whole human brain datasets.
  * Re-organized jupyter-book webpages.
