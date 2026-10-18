# Analysis environments for ABC Atlas code

The [ABC Atlas](https://knowledge.brain-map.org/abcatlas) can turn the view you are looking at into a
Python or R script that reproduces it. These scripts read the data straight from a public cloud bucket,
so you don't download whole datasets: only the cells and genes the view needs are fetched.

This folder sets up an environment where those scripts, and your own analyses of the same data, run
as they are:

| Folder | What it sets up |
|---|---|
| [`python/`](python/) | a [uv](https://docs.astral.sh/uv/) project: anndata, zarr, obstore, pyarrow, polars, duckdb, scanpy, JupyterLab |
| [`r/`](r/) | a [pixi](https://pixi.sh) project with R, arrow and ggplot2, plus `install.R` for an R you already have |

Each folder has a `check_setup` script that reads a small piece of the cloud data and prints `OK`.

> **Status:** the cloud-native copies of the data are a preview. The bucket layout (below) may change
> before it moves to the main ABC Atlas bucket.

## Get the code

```bash
git clone https://github.com/AllenInstitute/abc_atlas_access.git
cd abc_atlas_access/analysis_environments
```

You only need this folder. If you only run Python scripts from the ABC Atlas, you don't need to
clone anything (see the next section).

## Python

### 1. Install uv

uv installs Python itself, so you don't need an existing Python.

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Open a new terminal afterwards so `uv` is on your `PATH`.

### 2. Run a script from the ABC Atlas

In the ABC Atlas, open **Share → Analysis code**, choose **Python**, and download the script. Then, in
the folder you saved it to, run the command shown in the box:

```bash
uv run my_view.py
```

Each script lists its own dependencies in a header (the `# /// script` block), so `uv run` creates a
cached environment for it the first time. The first run takes a minute while packages download; later
runs start in a few seconds. The script saves a PNG next to itself and prints a summary of the cells it
selected.

### 3. A shared environment for notebooks and your own code

For interactive work, set up the project in [`python/`](python/), which pins a tested set of packages
(`uv.lock`):

```bash
cd python
uv sync                       # creates python/.venv
uv run python check_setup.py  # should end with "OK: ..."
uv run jupyter lab            # notebooks with the same packages
```

To run an ABC Atlas script in this environment instead of its own:

```bash
uv run --project path/to/analysis_environments/python python my_view.py
```

To use the environment as a kernel in VS Code or an existing Jupyter, select the interpreter at
`python/.venv/bin/python` (on Windows, `python\.venv\Scripts\python.exe`), or register it:

```bash
uv run python -m ipykernel install --user --name abc-atlas --display-name "ABC Atlas"
```

## R

The R scripts read the cell and gene tables (parquet) with
[arrow](https://arrow.apache.org/docs/r/) and the expression stores (Zarr v3) with
[Rarr](https://github.com/Huber-group-EMBL/Rarr). The stores use Zarr v3 *sharding*, which needs Rarr
2.1 or later. That version isn't in a Bioconductor release yet, so both setups below install it from
GitHub and build it from source.

### Option A: pixi (recommended; nothing else needed)

[pixi](https://pixi.sh) installs R, the packages and a compiler toolchain into the project folder, so
it doesn't touch any R you already have.

```bash
# macOS / Linux
curl -fsSL https://pixi.sh/install.sh | sh
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

Then:

```bash
cd r
pixi run check     # installs the environment and Rarr, then reads a little data; ends with "OK: ..."
```

Run an ABC Atlas script, or start R, in that environment:

```bash
pixi run --manifest-path path/to/analysis_environments/r Rscript my_view.R
pixi run --manifest-path path/to/analysis_environments/r R
```

The pixi environment supports macOS and Linux. On Windows, use option B.

### Option B: an R you already have (R 4.4 or later)

Rarr is compiled when it's installed, so you need a compiler toolchain first:

- **macOS:** `xcode-select --install`
- **Windows:** [Rtools](https://cran.r-project.org/bin/windows/Rtools/) for your R version
- **Linux:** your distribution's build tools (for example `sudo apt install build-essential`)

Then:

```bash
cd r
Rscript install.R      # arrow, ggplot2, patchwork, remotes, jsonlite, and Rarr from GitHub
Rscript check_setup.R  # should end with "OK: ..."
```

After that, run downloaded scripts with the command shown in the ABC Atlas:

```bash
Rscript my_view.R
```

The scripts also install any missing packages on their first run, so the install step is mostly there
to surface toolchain problems up front.

## Where the data is

Everything is in the public Google Cloud Storage bucket `abc-atlas-data-refactor`. It can be read
anonymously, with no account or credentials. Each dataset release has an AnnData store in Zarr v3,
plus parquet copies of its cell (`obs`) and gene (`var`) tables for fast filtering:

```
gs://abc-atlas-data-refactor/refactor/
  MERFISH-C57BL6J-638850-imputed/20240831/
    C57BL6J-638850-imputed-log2.zarr          4.3M cells x 8,460 genes (imputed), CCF coordinates
    C57BL6J-638850-imputed-log2.obs.parquet
    C57BL6J-638850-imputed-log2.var.parquet
  WMB-10Xv3/20230630/
    WMB-10Xv3-log2.zarr                       2.3M cells x 32,285 genes, UMAP
    WMB-10Xv3-log2.obs.parquet
    WMB-10Xv3-log2.var.parquet
  Consensus-WMB-Macosko-10X/20251031/
    Consensus-WMB-Macosko-10X-log2.zarr       Macosko snRNA-seq on the consensus taxonomy
    Consensus-WMB-Macosko-10X-log2.obs.parquet
    Consensus-WMB-Macosko-10X-log2.var.parquet
```

In the stores, `X` is dense log2(CPM + 1) expression. The `var.parquet` tables have a 0-based
`gene_index` column, which is the column of `X` for each gene. Files can also be fetched over HTTPS
at `https://storage.googleapis.com/abc-atlas-data-refactor/<path>`.

A minimal read in Python:

```python
import io, obstore, pandas as pd, zarr
from obstore.store import GCSStore
from zarr.storage import ObjectStore

prefix = "refactor/WMB-10Xv3/20230630/WMB-10Xv3-log2"
bucket = GCSStore("abc-atlas-data-refactor", skip_signature=True)
var = pd.read_parquet(io.BytesIO(bytes(obstore.get(bucket, f"{prefix}.var.parquet").bytes())))
root = zarr.open_group(ObjectStore(GCSStore("abc-atlas-data-refactor", prefix=f"{prefix}.zarr",
                                            skip_signature=True), read_only=True), mode="r")
gene = int(var.loc[var.gene_symbol == "Slc17a7", "gene_index"].iloc[0])
expression = root["X"][:, gene]   # one gene for every cell
```

## Troubleshooting

- **The first run is slow.** Python: uv is downloading packages, which happens once per set of
  dependencies. R: Rarr is compiling, which happens once.
- **`uv: command not found` / `pixi: command not found`:** open a new terminal after installing, or
  add `~/.local/bin` (uv) or `~/.pixi/bin` (pixi) to your `PATH`.
- **R: errors reading `X` (the expression store):** check `packageVersion("Rarr")`. Versions before
  2.1, including the current Bioconductor release, can't read Zarr v3 shards. Reinstall it from GitHub with
  `Rscript -e 'remotes::install_github("Huber-group-EMBL/Rarr")'`.
- **R: Rarr fails to compile:** the compiler toolchain is missing (see option B), or use pixi
  (option A), which brings its own.
- **R: a warning about zstd support:** harmless. The stores use zstd inside blosc, which Rarr handles.
  The scripts silence it.
- **Behind a proxy or firewall:** the scripts need HTTPS access to `storage.googleapis.com`.
