# Allen Brain Cell Atlas - Data Access

The Allen Brain Cell Atlas (ABC Atlas) aims to empower researchers worldwide to explore and analyze multiple whole-brain datasets simultaneously. As the Allen Institute and its collaborators continue to add new modalities, species, and insights to the ABC Atlas, this groundbreaking platform will keep growing, opening up endless possibilities for groundbreaking discoveries and breakthroughs in neuroscience. With the ABC Atlas, researchers everywhere can gain new insights into the brain’s complex workings, advancing our understanding of this amazing organ in ways we never thought possible.

Data associated with the ABC Atlas is hosted on Amazon Web Services (AWS) in an S3 bucket as a AWS Public Dataset, [arn:aws:s3:::allen-brain-cell-atlas](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html). No account or login is required for access. The purpose of this repo is to provide an overview of the available data, how to download and use it through example use cases.

The fall 2023 public beta data release includes:
* **Mouse whole-brain transcriptomic cell type atlas (Hongkui Zeng)**
  * 1.7 million single cell transcriptomes spanning the whole adult mouse brain using 10Xv2 chemistry ([WMB-10Xv2](descriptions/WMB-10Xv2.md))
  * 2.3 million single cell transcriptomes spanning the whole adult mouse brain using 10Xv3 chemistry ([WMB-10Xv3](descriptions/WMB-10Xv3.md))
  * 1687 single cell transcriptomes spanning the whole adult mouse brain using the 10X Multiome chemistry ([WMB-10XMulti](descriptions/WMB-10XMulti.md))
  * Clustering analysis of 4.0 million single cell transcriptomes spanning the whole adult mouse brain combining the 10Xv2, 10Xv3 and 10XMulti datasets ([WMB-10X](descriptions/WMB-10X.md))
  * A four level whole adult mouse brain taxonomy of cell types ([WMB-taxonomy](descriptions/WMB-taxonomy.md))
  * 3.9 million cell spatial transcriptomics dataset spanning a single adult mouse brain with a 500 gene panel and mapped to the whole mouse brain taxonomy ([MERFISH-C57BL6J-638850](descriptions/MERFISH-C57BL6J-638850.md))
  * Definition of 8 cell types neighborhoods and UMAP embeddings for fine grain visualization and analysis of neuronal types within and between brain regions ([WMB-neighborhoods](descriptions/WMB-neighborhoods.md))
  * An updated Allen CCFv3 with additional annotations for layers of Ammon's horns, main olfactory blub and a simplifed 5-level anatomical heirarchy ([Allen-CCF-2020](descriptions/Allen-CCF-2020.md))
  * CCF mapped coordinates for cells in the whole brain spatial transcriptomics dataset ([MERFISH-C57BL6J-638850-CCF](descriptions/MERFISH-C57BL6J-638850-CCF.md))
* **A molecularly defined and spatially resolved cell atlas of the whole mouse brain (Xiaowei Zhuang)**
  * 2.8 million cell spatial transcriptomics dataset spanning 147 coronal sections with a 1122 gene panel and mapped to the whole mouse brain taxonomy and Allen CCFv3 ([Zhuang-C57BL6J-1](descriptions/Zhuang-C57BL6J-1.md))
  * 1.2 million cell spatial transcriptomics dataset spanning 66 coronal sections with a 1122 gene panel and mapped to the whole mouse brain taxonomy and Allen CCFv3 ([Zhuang-C57BL6J-2](descriptions/Zhuang-C57BL6J-2.md))
  * 1.5 million cell spatial transcriptomics dataset spanning 23 sagittal sections with a 1122 gene panel and mapped to the whole mouse brain taxonomy and Allen CCFv3 ([Zhuang-C57BL6J-3](descriptions/Zhuang-C57BL6J-3.md))
  * 0.2 million cell spatial transcriptomics dataset spanning 3 sagittal sections with a 1122 gene panel and mapped to the whole mouse brain taxonomy and Allen CCFv3 ([Zhuang-C57BL6J-4](descriptions/Zhuang-C57BL6J-4.md))

Each release has an associated **manifest.json** which list all the specific version of directories and files that are part of the release. We recommend using the manifest as the starting point of data download and usage.

Expression matrices are stored in the [anndata h5ad format](https://anndata.readthedocs.io/en/latest/) and needs to be downloaded to a local file system for usage. To make data transfer, download and access more efficient, 
the 10x transcriptomics datasets have been subdivided into smaller packages grouped by method and anatomical origin. The notebooks provide example code on how to access data across these individual files.

Available notebooks:

* [**Getting started**](notebooks/getting_started.ipynb): learn how to use the manifest.json file to faciliate data download and usage.
*  **Mouse whole-brain transcriptomic cell type atlas (Hongkui Zeng)**
   * [**10x scRNA-seq clustering analysis and annotation**](notebooks/cluster_annotation_tutorial.ipynb): learn about the whole mouse brain taxonomy through some example use cases and visualization.
   * **10x scRNA-seq gene expression data**
     * [**Part 1**](notebooks/10x_snRNASeq_tutorial_part_1.ipynb): learn about the 10x dataset through some example use cases and visualization of cells in the thalamus.
     * [**Part 2a**](notebooks/10x_snRNASeq_tutorial_part_2a.ipynb): learn how to iterate through all the data packages, to access data for whole brain example use cases in part 2b.
     * [**Part 2b**](notebooks/10x_snRNASeq_tutorial_part_2b.ipynb): explore the whole brain data through visualization and analyses of a set of genes of interest.
   * **MERFISH whole brain spatial transcriptomics**
     * [**Part 1**](notebooks/merfish_tutorial_part_1.ipynb): learn about the MERFISH dataset through some example use cases and visualization for a single brain section.
     * [**Part 2a**](notebooks/merfish_tutorial_part_2a.ipynb): learn to access data and prepare for whole brain example use cases in part 2b.
     * [**Part 2b**](notebooks/merfish_tutorial_part_2b.ipynb): explore the whole brain data through visualization and analyses of a set of genes of interest.
    * [**Cluster groups and embeddings**](notebooks/cluster_groups_and_embeddings_tutorial.ipynb): learn about cell types neighborhoods and neighborhood specific UMAP embeddings through example use cases.
    * [**Cell type neighborhood gallery**](notebooks/cluster_neighborhood_gallery.ipynb): explore and visualize a set of cell types neighborhoods.
    * [**Allen CCFv3 parcellation and annotation**](notebooks/ccf_and_parcellation_annotation_tutorial.ipynb): learn about the Allen CCFv3 and a simplified 5-level anatomical heirarchy through some example use cases and visualization.
    * [**MERFISH CCF mapped coordinates**](notebooks/merfish_ccf_registration_tutorial.ipynb): learn about how to download and use CCF mapped coordinates through some example use cases and visualization.
* **A molecularly defined and spatially resolved cell atlas of the whole mouse brain (Xiaowei Zhuang)**
  * [**MERFISH whole mouse brain spatial transcriptomics**](notebooks/zhuang_merfish_tutorial.ipynb): learn about the MERFISH dataset through some example use cases and visualization

## Level of support
We are not currently supporting this code, but simply releasing it to the community AS IS but are not able to provide any guarantees of support. The community is welcome to submit issues, but you should not expect an active response.
