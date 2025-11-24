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

The Fall 2025 public beta data release includes:
* **[Mouse whole-brain transcriptomic cell type atlas](descriptions/WMB_dataset.md)
  (Hongkui Zeng)**
* **[Consensus Whole Mouse Brain cell type atlas](descriptions/Consensus-WMB-dataset.md) (Evan Macosko, Hongkui Zeng)**
* **[Aging Mouse transcriptomic cell type atlas](descriptions/Zeng_Aging_Mouse_dataset.md)
  (Hongkui Zeng)**
* **[A molecularly defined and spatially resolved cell atlas of the whole mouse brain](descriptions/Zhuang_dataset.md)
  (Xiaowei Zhuang)**
* **[Human whole-brain transcriptomic cell type atlas](descriptions/WHB_dataset.md)
  (Kimberly Siletti)**
* **[Human Postmortem-Derived Brain Sequencing Collection](descriptions/ASAP-PMDBS_dataset.md)
  (ASAP)**
* **[Human-Mammalian Brain - Basal Ganglia](descriptions/HMBA-BG_dataset.md)
  (HMBA)**

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
* **[Consensus Whole Mouse Brain Notebooks](descriptions/Consensus-WMB-notebooks.md) (Evan Macosko, Hongkui Zeng)**
* **[Aging Mouse transcriptomic cell type atlas](descriptions/Zeng_Aging_Mouse_notebooks.md)
  (Hongkui Zeng)**
* **[A molecularly defined and spatially resolved cell atlas of the whole
  mouse brain](descriptions/notebook_subtitle4.md)
  (Xiaowei Zhuang)**
* **[Human whole-brain transcriptomic cell type atlas](descriptions/WHB_notebooks.md)
  (Kimberly Siletti)**
* **[Human Postmortem-Derived Brain Sequencing Collection](descriptions/ASAP-PMDBS_notebooks.md)
  (ASAP)**
* **[Human-Mammalian Brain - Basal Ganglia](descriptions/HMBA-BG_notebooks.md)
  (HMBA)**


## Release Notes
* **[Add HMBA-BG spatial data. Update HMBA-BG 10X taxonomy, data, and metadata and MapMyCells files (version 20251031), abc_atlas_access (v1.1.0)]**
  * Add Consensus Whole Mouse brain datasets.
    * New Consensus-WMB-AIBS-10X, ~3.9 million, single cell metadata derived
    from the WMB-10X release hosted through this tool. This release reuses the
    previous WMB-10X(v2/v3), h5ad files.
    * New Consensus-WMB-Macosko-10X data and metadata for ~4 million nuclei.
      * Metadata for ~3.7 million nuclei
      * Expression matrices for all nuclei with files divided by anatomical
      region.
    * New consensus taxonomy derived from the the Allen Institute for Brain
    Science and Broad Institute Macosko lab Whole Mouse Brain data.
* **[Add HMBA-BG spatial data. Update HMBA-BG 10X taxonomy, data, and metadata and MapMyCells files (version 20250930), abc_atlas_access (v1.0.0)]**
  * Added basal ganglia, spatial transcriptomic dataset
    * ~5.4 million human basal ganglia and adjacent cells
    * ~3.2 million macaque basal ganglia and adjacent cells
    * ~1.3 million macaque basal ganglia and adjacent cells
    * Mapping of all cells into the HMBA-BG taxonomy
    * Basal Ganglia, parcellation annotations for each cell and annotation polygons.
  * Updated colors for the cross-species, HMBA-BG taxonomy.
  * AbcProjecctCache: Added explicit accessors for expression_matrices, image_volumes, and mapmycells.
    * get_(metadata)data_path, generalized to get_file_path. Deprecation warning added to get_data_path.
* **[Add HMBA-BG 10X taxonomy, data, and metadata and MapMyCells files (version 20250531), abc_atlas_access (v0.7.0)]**
  * Added the Human-Mammalian Brain - Basal Ganglia (HMBA-BG) 10X dataset.
    * ~2 million single cell transcriptomes with ~16k genes aligned across
      Human, Macaque, and Marmoset.
    * Cross-species taxonomy containing 1435 clusters with annotations
    * Individual single cell transcriptome datasets for each of the species in
      this release including:
      * 1,683,105 Human cells, 36,601 genes
      * 839,102 Macaque cells, 35,219 genes
      * 414,575 Marmoset cells, 35,787 genes
    * MapMyCells files for each of the individual species.
* **[Add ASAP-PMDBS dataset and MapMyCells results (version 20250331), abc_atlas_access (v0.6.0)]**
  * Added single cell transscriptomics from the 3 million cell, Aligning Science
    Across Parkinson’s (ASAP) Human Postmortem-Derived Brain Sequencing
    Collection (PMDBS).
    * 3 million cells from 5 teams over 220 donors.
    * Results of MapMyCells run on the 3 million cells mapping them into
      the Whole Human Brain and SEA-AD taxonomies.
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
