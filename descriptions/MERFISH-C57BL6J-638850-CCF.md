# MERFISH CCF mapped coordinates

Each section from the whole brain MERFISH dataset was registered to the Allen
CCFv3 using a combination of global and section-wise mappings. The midline was
manually determined for each section to rotate the section upright and center
in the middle. This set of rectified images were stacked in sequential order to
create an initial configuration for registration. A 3D global affine (12 dof)
mapping was then performed to align the CCF into the MERFISH space. Each
MERFISH section was then deformably registered to its resampled CCF target
section.

Global and section-wise mappings from each of these registration steps were
preserved and concatenated (with appropriate inversions) to allow
point-to-point mapping between the original MERFISH coordinate space and the
CCF space. See [Yao et al.](https://doi.org/10.1101/2023.03.06.531121) for further details.

| Component | Current Version | Size |
|---|--|---|
| Image Volumes | [s3://allen-brain-cell-atlas/image_volumes/MERFISH-C57BL6J-638850-CCF/20230630](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#image_volumes/MERFISH-C57BL6J-638850-CCF/20230630/) | 115.4 MB |
| Metadata | [s3://allen-brain-cell-atlas/metadata/MERFISH-C57BL6J-638850-CCF/20231215](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/MERFISH-C57BL6J-638850-CCF/20231215/) | 2.01 GB |

Data is being share under the CC BY NC 4.0 license.

Related resources :
* Whole mouse brain clustering ([WMB-10X](WMB-10X.md))
* Whole mouse brain mouse taxonomy of cell types ([WMB-taxonomy](WMB-taxonomy.md))
* Whole mouse brain MERFISH spatial transcriptomics dataset ([MERFISH-C57BL6J-638850](MERFISH-C57BL6J-638850.md))
* Imputed, whole mouse brain MERFISH spatial transcriptomics dataset ([MERFISH-C57BL6J-638850-imputed](MERFISH-C57BL6J-638850-imputed.md))
* Allen CCFv3 with a simplified 5-level anatomical hierarchy ([Allen-CCF-2020](Allen-CCF-2020.md))

Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb): learn how to use the AbcProjectCache to
  facilitate data download and usage.
* [**10x scRNA-seq clustering analysis and annotation**](../notebooks/cluster_annotation_tutorial.ipynb): learn about the
  whole mouse brain taxonomy through some example use cases and visualization.
* **MERFISH whole brain spatial transcriptomics**
  * [**Part 1**](../notebooks/merfish_tutorial_part_1.ipynb): Learn about the MERFISH dataset through some example use
    cases and visualization for a single brain section.
  * [**Part 2a**](../notebooks/merfish_tutorial_part_2a.ipynb): Learn to access data and prepare for whole brain
    example use cases in part 2b.
  * [**Part 2b**](../notebooks/merfish_tutorial_part_2b.ipynb): Explore the whole brain data through visualization and
    analyses of a set of genes of interest.
  * [**MERFISH imputed genes**](../notebooks/merfish_imputed_genes_example.ipynb):
    Learn about the using the imputed genes of the MERFISH dataset.
* [**Allen CCFv3 parcellation and annotation**](../notebooks/ccf_and_parcellation_annotation_tutorial.ipynb): learn about the Allen
  CCFv3 and a simplified 5-level anatomical hierarchy through some example use
  cases and visualization.
* [**MERFISH CCF mapped coordinates**](../notebooks/merfish_ccf_registration_tutorial.ipynb): learn about how to download and
  use CCF mapped coordinates through some example use cases and visualization.


