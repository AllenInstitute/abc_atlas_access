import argparse
from pathlib import Path

from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache
from abc_atlas_access.abc_atlas_cache.anndata_utils import get_gene_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load expression matrix data from the ABC Atlas and "
                    "extract specific genes across multiple files and all "
                    "cells."
    )
    parser.add_argument(
        "--abc_atlas_cache_path",
        type=str,
        default="/root/capsule/data/abc_atlas",
        help="Path to the ABC Atlas cache directory."
    )
    parser.add_argument(
        "--manifest_version",
        type=str,
        default="releases/20240330/manifest.json",
        help="The version of the ABC Atlas manifest to use."
    )
    parser.add_argument(
        "--use_s3_cache",
        action="store_true",
        help="Use an S3 cache where the data is downloaded to disk instead of "
             "a local cache already stored on disk."
    )
    parser.add_argument(
        "--species",
        help="Which data to load? `mouse` or `human`?",
        choices=["human", "mouse", "aging_mouse"]
    )
    parser.add_argument(
        "--use_raw",
        action="store_true",
        help="Use raw gene expression values instead of log2 values."
    )
    parser.add_argument(
        "--output_file_path",
        type=str,
        help="Path to file to write to.",
        default="~/capsule/results/gene_data.csv"
    )
    parser.add_argument(
        '--genes',
        type=str,
        default="",
        help="A comma-separated list of gene symbols to extract from the "
             "expression matrix."
    )
    args = parser.parse_args()

    genes = args.genes.split(",")
    for idx, gene in enumerate(genes):
        genes[idx] = gene.replace(" ", "")

    print("Loading ABC Atlas cache from:", args.abc_atlas_cache_path)
    cache_path = Path(args.abc_atlas_cache_path)
    if args.use_s3_cache:
        abc_cache = AbcProjectCache.from_s3_cache(cache_path)
    else:
        abc_cache = AbcProjectCache.from_local_cache(cache_path)
    abc_cache.load_manifest(args.manifest_version)

    if args.species == "human":
        directory_name = "WHB-10Xv3"
        gene_directory = "WHB-10Xv3"
    elif args.species == "mouse":
        directory_name = "WMB-10X"
        gene_directory = "WMB-10X"
    elif args.species == "aging_mouse":
        directory_name = "Zeng-Aging-Mouse-10Xv3"
        gene_directory = "WMB-10X"
    else:
        raise ValueError(f"Unknown species requested: {args.species}")

    cell = abc_cache.get_metadata_dataframe(
        directory=directory_name,
        file_name='cell_metadata'
    ).set_index('cell_label')
    gene = abc_cache.get_metadata_dataframe(
        directory=gene_directory,
        file_name='gene'
    ).set_index('gene_identifier')

    print("Processing genes:", genes)
    gene_data = get_gene_data(
        abc_atlas_cache=abc_cache,
        all_cells=cell,
        all_genes=gene,
        selected_genes=genes,
        data_type="raw" if args.use_raw else "log2"
    )

    print("Writing gene data to:", args.output_file_path)
    gene_data.to_csv(args.output_file_path)