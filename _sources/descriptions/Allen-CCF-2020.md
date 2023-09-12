# Allen Mouse Common Coordinate Framework (2020 version)
Allen Mouse Brain Common Coordinate Framework (CCFv3, [Wang et al, 2020](https://doi.org/10.1016/j.cell.2020.04.007)) is a 3D reference space is an average brain at 10um voxel resolution created from serial two-photon tomography images of 1,675 young adult C57Bl6/J mice. Using multimodal reference data, the entire brain parcellated directly in 3D, labeling every voxel with a brain structure spanning 43 isocortical areas and their layers, 314 subcortical gray matter structures, 81 fiber tracts, and 8 ventricular structures. The 2020 version adds new annotations for layers of the Ammon’s horn (CA), main olfactory bulb (MOB) and minor modification of surrounding fiber tracts. For the purpose of ABC atlas visualization and analysis, we have also created a simplifed 5 level anatomical heirarchy. 

The associated metadata is hosted on AWS S3 bucket as a AWS Public Dataset:

| Component | Current Version | Size |
|---|--|--|
| Image Volumes | [s3://allen-brain-cell-atlas/image_volumes/Allen-CCF-2020/20230630](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#image_volumes/Allen-CCF-2020/20230630/) | 379.1 MB |
| Metadata | [s3://allen-brain-cell-atlas/metadata/Allen-CCF-2020/20230630](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/Allen-CCF-2020/20230630/) | 1.18 MB |

Data is being share under the [Allen Institute Terms of Use](https://alleninstitute.org/terms-of-use/).

Associated notebooks:
* [**Allen CCFv3 parcellation and annotation**](../notebooks/ccf_and_parcellation_annotation_tutorial.ipynb): learn about the Allen CCFv3 and a simplified 5-level anatomical heirarchy through some example use cases and visualization.
