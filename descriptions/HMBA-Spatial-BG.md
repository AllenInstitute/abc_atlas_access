# Human-Mammalian Brain - Basal Ganglia: spatial transcriptomics cells for each species

Data and metadata for the spatial component of the HMBA-BG dataset.

The basal ganglia are a set of subcortical structures critical for motor control, particularly in the context
of action selection, motor learning and emotional state, whose coarse functional organization is
well-described in the literature. Although single-cell RNA-Seq studies have greatly enhanced our
understanding of cellular diversity in the brain, the exact spatial distribution of cell types within the
brain has been difficult to determine. Using spatial transcriptomics platforms such as MERSCOPE or Xenium
enables spatial profiling of hundreds of genes for each cell, enabling the mapping the cells to the
[consensus basal ganglia cell type taxonomy](https://alleninstitute.github.io/abc_atlas_access/notebooks/hmba_bg_clustering_analysis_and_annotation.html).

These data from the basis of the cross species [Basal Ganglia (BG) taxonomy](HMBA-BG-taxonomy-CCN20250428.md).

For more information on the dataset, please refer to the following webpage:
[Mammalian Basal Ganglia Consensus Cell Type Atlas](https://alleninstitute.github.io/HMBA_BasalGanglia_Consensus_Taxonomy/).

The expression matrices and associated metadata are hosted on AWS S3 bucket as
a AWS Public Dataset:

| Component | Current Version | Size    |
|---|--|---------|
| Human: Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/HMBA-MERSCOPE-H22.30.001-BG/20250630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/HMBA-MERSCOPE-H22.30.001-BG/20250630/) | 33.6 GB |
| Human: Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/HMBA-MERSCOPE-H22.30.001-BG/20250630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/HMBA-MERSCOPE-H22.30.001-BG/20250630/) | 33.6 GB |
| Human: Image volumes and polygons | [s3://allen-brain-cell-atlas/image_volumes/HMBA-MERSCOPE-H22.30.001-BG/20250630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#image_volumes/HMBA-MERSCOPE-H22.30.001-BG/20250630/) | 33.6 GB |
| Macaque: Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/HMBA-MERSCOPE-QM23.50.001-BG/20250630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#expression_matrices/HMBA-MERSCOPE-QM23.50.001-BG/20250630/) | 33.6 GB |
| Macaque: Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/HMBA-MERSCOPE-QM23.50.001-BG/20250630](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#metadata/HMBA-MERSCOPE-QM23.50.001-BG/20250630/) | 33.6 GB |
| Macaque: Cell and gene metadata | [s3://allen-brain-cell-atlas/image_volumes/HMBA-MERSCOPE-QM23.50.001-BG/20250630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#image_volumes/HMBA-MERSCOPE-QM23.50.001-BG/20250630/) | 33.6 GB |
| Marmoset: Expression Matrices | [s3://allen-brain-cell-atlas/expression_matrices/HMBA-Xenium-CJ23.56.004-BG/20250630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#/expression_matrices/HMBA-Xenium-CJ23.56.004-BG/20250630/]) | 33.6 GB |
| Marmoset: Cell and gene metadata | [s3://allen-brain-cell-atlas/metadata/HMBA-Xenium-CJ23.56.004-BG/20250630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#/metadata/HMBA-Xenium-CJ23.56.004-BG/20250630/]) | 33.6 GB |
| Marmoset: Cell and gene metadata | [s3://allen-brain-cell-atlas/image_volumes/HMBA-Xenium-CJ23.56.004-BG/20250630/](https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/index.html#/image_volumes/HMBA-Xenium-CJ23.56.004-BG/20250630/]) | 33.6 GB |


Data is being shared under the CC BY NC 4.0 license.


Related resources:
* ~2 million single cell transcriptomes with aligned genes across species.
  ([HMBA-10XMultiome-BG-Aligned](HMBA-10XMultiome-BG-Aligned.md))
* Single cell transcriptomes for each individual species in the
  HMBA-BG dataset.([HMBA-10XMultiome-BG](HMBA-10XMultiome-BG.md))
* Taxonomy and Clustering analysis of ~2 million single cell
  transcriptomes from the aligned dataset.
  ([HMBA-BG-taxonomy-CCN20250428](HMBA-BG-taxonomy-CCN20250428.md))


Associated notebooks:
* [**Getting started**](../notebooks/getting_started.ipynb):
  Learn how to use the ABCProjectCache object to facilitate data download and
  usage.
* [**Accessing 10X gene expression data**](../notebooks/general_accessing_10x_snRNASeq_tutorial.ipynb):
  Learn how to load individual genes from the 10X expression data.
* [**10X scRNA-seq clustering analysis and annotation**](../notebooks/hmba_bg_clustering_analysis_and_annotation.ipynb):
  Learn about the HMBA-BG data/metadata structure and taxonomy through example use cases and
  visualization.
[*notebooks/hmba_bg_clustering_analysis_and_annotation.ipynb*]
* [**10X scRNA-seq gene expression**](../notebooks/hmba_bg_10X_snRNASeq_tutorial.ipynb):
  Interact with HMBA-BG 10X-Aligned gene expression data. [*notebooks/hmba_bg_10X_snRNASeq_tutorial.ipynb*]
* [**Spatial transcriptomic slab coordinates and annotation**](../notebooks/hmba_bg_spatial_slabs_and_taxonomy.ipynb):
  Learn about the HMBA-BG spatial data/metadata structure and mapping to the BG taxonomy through example use
  cases and visualization.
[*notebooks/hmba_bg_spatial_slabs_and_taxonomy.ipynb*]
* [**Spatial transcriptomic gene expression**](../notebooks/hmba_bg_spatial_genes.ipynb):
  Interact with HMBA-BG spatial transcriptomic gene expression data. [*notebooks/hmba_bg_spatial_genes.ipynb*]
