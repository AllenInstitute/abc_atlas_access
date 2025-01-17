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
Community Forum](https://community.brain-map.org/). This repository is intended
for users who wish to download the ABC Atlas data and processes it locally.

Data associated with the ABC Atlas is hosted on Amazon Web Services (AWS) in an
S3 bucket as a AWS Public Dataset, [arn:aws:s3:::allen-brain-cell-atlas](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html).
No account or login is required for access. ***The purpose of this repo is to
provide an overview of the available data, how to download and use it through
example use cases.***

The Winter 2024 public beta data release includes:
* **[Mouse whole-brain transcriptomic cell type atlas](descriptions/WMB_dataset.md)
  (Hongkui Zeng)**
* **[Aging Mouse transcriptomic cell type atlas](descriptions/Zeng_Aging_Mouse_dataset.md)
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

If you have used the ABC Atlas visualization to select cells from a dataset and
with to use your selected cells in an analysis with the data available for
download here, you find a tutorial to do so in the
[Using cells selected in the ABC Atlas](notebooks/abc_atlas_selection_example.ipynb)
notebook.

## Available notebooks:

* [**Getting started**](notebooks/getting_started.ipynb): learn how to use the
  AbcProjectCache to facilitate data download and usage.
* [**Using cells selected in the ABC Atlas**](notebooks/abc_atlas_selection_example.ipynb): learn how
  to use cells selected from an ABC Atlas visualization in your analysis.
* [**Loading genes from expression matrix data**](notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  learn how to select genes from 10X expression matricies and combine them with
  the cell metadata.
* **[Mouse whole-brain transcriptomic cell type atlas](descriptions/notebook_subtitle1.md)
  (Hongkui Zeng)**
* **[Aging Mouse transcriptomic cell type atlas](descriptions/Zeng_Aging_Mouse_notebooks.md)
  (Hongkui Zeng)**
* **[A molecularly defined and spatially resolved cell atlas of the whole
  mouse brain](descriptions/notebook_subtitle4.md)
  (Xiaowei Zhuang)**
* **[Human whole-brain transcriptomic cell type atlas](descriptions/WHB_notebooks.md)
  (Kimberly Siletti)**

## Release Notes
* **[Update aging Mouse UMAP (version 20250131), abc_atlas_access (v0.5.0)]**
  * Fix 588 cells with missing UMAP coordinates.
* **[Aging Mouse data (version 20241130), abc_atlas_access (v0.4.0)]**
  * Add the Jin et al., aging mouse dataset.
    * 1.2 million cells divided into adult and aged mouse cells.
    * 847 cluster taxonomy with identified associations into the supertype and
      above levels of the Whole Mouse Brain taxonomy.
    * 2,449 age differential expression genes.
  * Add aging mouse to create gene expression script.
  * Update WMB cluster annotations to the latest version.
  * Separate dependencies for notebooks and base, cache package.
* **[ABC Sample ID update (version 20241115) abc_atlas_access (v0.3.0)]**
  * Add abc_sample_id to cell_metadatas of the projects listed below. This
    allows users to use cell selections they've downloaded from the ABC Atlas
    visualization.
    * MERFISH-C57BL6J-638850(-imputed)
    * WHB-10Xv3
    * WMB-10X
    * Zhuang-ABCA-(1-4)
  * Added notebook showing how to use abc_sample_id.
* **[Summer 2024 Public Beta (version 20240831) abc_atlas_access (v0.2.0)]**
  * Released ~8k imputed genes for the MERFISH-C57BL6J-638850 dataset.
  * Added new notebooks and pages for the imputed gene dataset.
  * Updated cache object for better compatibility across platforms.
    * Added automatic unittesting via GitHub Actions.
    * Modified cache to autodetect cache type (local or s3) for easier
      compatibility with CodeOcean/s3fs-fuse mounts.
    * Simplified notebooks' use of the cache.
* **[abc_atlas_access (v0.1.2)]**
  * Add matplotlib magic.
  * Fixed bugs in pathlib import in notebooks
  * Added script for selecting genes from expression matrices for use on
    CodeOcean.
* **[abc_atlas_access (v0.1.1)]**
  * Fixed compatibility issue with read only local caches specifically for
    fuse style file mounts such as those used on CodeOcean.
  * Added local cache example to notebooks.
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
