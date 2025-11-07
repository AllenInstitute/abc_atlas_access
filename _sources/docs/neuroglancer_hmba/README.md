# HMBA Basal Ganglia: Neuroglancer Views

## Neuroglancer Views – Coordinate Spaces
*Click thumbnails to launch Neuroglancer for each coordinate space.*

```{list-table} Neuroglancer links
:header-rows: 1

* - **Species**
  - **Donor**
  - **Slab**
  - **Donor**
  - **CCF**
  - **HiP-CT**

* - **Human**
  - **H22.30.001**
  - ```{image} images/H22.30.001_slab.png
    :alt: H22.30.001 slab
    :width: 400px
    :target: https://neuroglancer-demo.appspot.com/#!s3://allen-hmba-releases/neuroglancer/HMBA-MERSCOPE-H22.30.001-BG/20250630/viewer_state/H22.30.001_slab.json
    ```
  - —
  - ```{image} images/H22.30.001_CCF_template.png
    :alt: H22.30.001 CCF
    :width: 400px
    :target: https://neuroglancer-demo.appspot.com/#!s3://neuroglancer-hmba/cifar/neuroglancer/H22.30.001_hipct_ccf.json
    ```
  - ```{image} images/H22.30.001_HiP-CT.png
    :alt: H22.30.001 HiP-CT
    :width: 400px
    :target: https://neuroglancer-demo.appspot.com/#!s3://neuroglancer-hmba/cifar/neuroglancer/H22.30.001_hipct.json
    ```

* - **Macaque**
  - **QM23.50.001 (Red)**
  - ```{image} images/QM23.50.001_slab.png
    :alt: QM23.50.001 slab
    :width: 400px
    :target: https://neuroglancer-demo.appspot.com/#!s3://allen-hmba-releases/neuroglancer/HMBA-MERSCOPE-QM23.50.001-BG/20250630/viewer_state/QM23.50.001_slab.json
    ```
  - *ETA 2026*
  - *ETA 2026*
  - *TBD*

* - **Marmoset**
  - **CJ23.56.004 (Tank)**
  - ```{image} images/CJ23.56.004_slab.png
    :alt: CJ23.56.004 slab
    :width: 400px
    :target: https://neuroglancer-demo.appspot.com/#!s3://allen-hmba-releases/neuroglancer/HMBA-Xenium-CJ23.56.004-BG/20250630/viewer_state/CJ23.56.004_slab.json
    ```
  - *ETA 2026*
  - *ETA 2026*
  - *TBD*
```

The cell coordinates are registered to four different reference spaces, each serving a distinct purpose.

### Slab
The coordinate system of the *slab-face images* that each spatial transcriptomics plane belongs to.  
This view shows cells in the context of the imaging assets used for mosaicking (e.g., block-face and slab-face images).

### Donor
The native *MRI space* corresponding to the individual donor from whom the spatial transcriptomics sections were sampled.  
This view preserves subject-specific anatomy before normalization to any common template.

### CCF (Common Coordinate Framework)
The standardized reference space for the donor’s species, enabling cross-donor and cross-dataset comparisons.  
[See this link for more details.](https://alleninstitute.github.io/CCF-MAP/index.html)

### HiP-CT (Cellular-Resolution Volumetric Scan)
A *cellular-resolution (25 µm)* volumetric scan of the human brain.  
[Details about the HiP-CT dataset and donor](https://human-organ-atlas.esrf.fr/datasets/1773964319).  
**Note:** The spatial transcriptomics data were not sampled from the same donor; alignment is used only for anatomical correspondence.

---

## Quick Guide
*Click a section title to expand/collapse.*

:::{dropdown} 1 · Filter annotations by cell types
1. From the right pane, pick taxonomic cell types to show or hide (yellow box).  
2. To filter by taxonomic level, click the + or − buttons next to each taxonomic level (red box).  
3. If the right panel is not visible, right-click the **cell_types** tab on the top left.  
4. In that panel, select the **seg** tab.

```{image} images/guide/cell_types.png
:alt: Selecting cell types in the seg tab
:width: 300px
```
:::

:::{dropdown} 2 · Color annotations by taxonomic level – set annotation size & opacity
1. Select the **cells** tab from the top left, then choose the **rendering** tab in the right pane.  
2. Choose a taxonomic level for coloring with the **level_color_selector**:  

   • **1:** Neighborhood  
   • **2:** Class  
   • **3:** Subclass  
   • **4:** Group (default)

```{image} images/guide/annotation_taxonomic_colors.png
:alt: Taxonomic coloring examples
:width: 800px
```

3. Adjust **annotation size** and **opacity**.

```{image} images/guide/annotation_rendering.png
:alt: Rendering tab with taxonomic coloring, size, and opacity
:width: 300px
```
:::

:::{dropdown} 3 · View annotation metadata
To see metadata for an annotation:

1. Click the hamburger icon (third icon) from the top right to toggle *Selection Details Panel*.

```{image} images/guide/selection_icon.png
:alt: Toggle Selection Details Panel icon
:width: 200px
```

2. Mouse over an annotation to view its metadata from the right panel.

```{image} images/guide/annotation_metadata.png
:alt: Viewing annotation metadata
:width: 300px
```
:::

:::{dropdown} 4 · Align view with cell sections by tilting cross-section plane
Tilting the cross-section plane helps match views to cell section planes.

1. Click inside a view (coronal, transverse, sagittal) to focus it.  
2. Rotate with keys: **e** (left) and **r** (right).  
3. Or hold **Shift** and drag with the mouse to tilt across all axes.  

*Before tilting*

```{image} images/guide/crosssection_before.png
:alt: Before tilting cross-section plane
```

*After tilting*

```{image} images/guide/crosssection_after.png
:alt: After tilting cross-section plane
```
:::

:::{dropdown} 5 · Increase annotation view depth
If only a partial coronal cell-section plane is visible, increase the annotation view depth.  
**Shortcut:** Hold `Alt` and use the mouse wheel.
:::

---