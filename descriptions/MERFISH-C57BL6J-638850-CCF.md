# MERFISH CCF mapped coordinates

Each section from the whole brain MERFISH dataset was registered to the Allen CCFv3 using a combination of global and section-wise mappings.
The midline was manually determined for each section to rotate the section upright and center in in the middle. 
This set of rectified images were stacked in sequential order to create an inital configuration for registration.
A 3D global affine (12 dof) mapping was then performed to align the CCF into the MERFISH space.
Each MERFISH section was then deformably registered to its resampled CCF target section.

Global and section-wise mappings from each of these registration steps were preserved and concatenated (with appropriate inversions) to allow point-to-point mapping between the original MERFISH coordinate space and the CCF space. See [Yao et al](https://doi.org/10.1101/2023.03.06.531121) for further details.

| Component | Current Version | Size |
|---|--|---|
| Image Volumes | [s3://allen-brain-cell-atlas/image_volumes/MERFISH-C57BL6J-638850-CCF/20230630](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#image_volumes/MERFISH-C57BL6J-638850-CCF/20230630/) | 115.4 MB |
| Metadata | [s3://allen-brain-cell-atlas/metadata/MERFISH-C57BL6J-638850-CCF/20230630](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/MERFISH-C57BL6J-638850-CCF/20230630/) | 2.14 GB |

Data is being share under the [Allen Institute Terms of Use](https://alleninstitute.org/terms-of-use/).

Related resources :
* Whole mouse brain mouse brain clustering ([WMB-10X](WMB-10X.md))
* Whole mouse brain mouse taxonomy of cell types ([WMB-taxonomy](WMB-taxonomy.md))
* Whole mouse brain MERFISH spatial transcriptomics dataset ([MERFISH-C57BL6J-638850](MERFISH-C57BL6J-638850.md))
* Allen CCFv3 with a simplifed 5-level anatomical heirarchy ([Allen-CCF-2020](descriptions/Allen-CCF-2020.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the manifest.json file to faciliate data download and usage.
* [**10x scRNA-seq clustering analysis and annotation**](../notebooks/cluster_annotation_tutorial.ipynb): learn about the whole mouse brain taxonomy through some example use cases and visualization.
* * **MERFISH whole brain spatial transcriptomics**
  * [**Part 1**](../notebooks/merfish_tutorial_part_1.ipynb): learn about the MERFISH dataset through some example use cases and visualization for a single brain section.
  * [**Part 2a**](../notebooks/merfish_tutorial_part_2a.ipynb): learn to access data and prepare for whole brain example use cases in part 2b.
  * [**Part 2b**](../notebooks/merfish_tutorial_part_2b.ipynb): Explore the whole brain data through visualization and analyses of a set of genes of interest.
* [**Allen CCFv3 parcellation and annotation**](notebooks/ccf_and_parcellation_annotation_tutorial.ipynb): learn about the Allen CCFv3 and a simplified 5-level anatomical heirarchy through some example use cases and visualization.
* [**MERFISH CCF mapped coordinates**](notebooks/merfish_ccf_registration_tutorial.ipynb): learn about how to download and use CCF mapped coordinates through some example use cases and visualization.


