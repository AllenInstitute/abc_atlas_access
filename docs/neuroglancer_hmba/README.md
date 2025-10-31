# HMBA Basal Ganglia: Neuroglancer Views

## Quick Guide

<p><em>Click a section title to expand/collapse.</em></p>

<details>
  <summary><strong>1. Filter annotations by cell types</strong></summary>
  <div>
    <ol>
      <li>From the right pane, pick taxonomic cell types to show or hide (yellow box).</li>
      <li>To filter cell types by taxonomic level, click the + or − buttons next the taxonomic level (red box).</li>
      <li>If right panel is not visible, right-click the <b>cell_types</b> tab on the top left.</li>
      <li>In that panel, select the <b>seg</b> tab.</li>
    </ol>
    <img src="images/guide/cell_types.png" alt="Selecting cell types in the seg tab" width="300">
  </div>
</details>

<details>
  <summary><strong>2. Color annotations by taxonomic level; set annotation size &amp; opacity</strong></summary>
  <div>
    <ol>
      <li>Select the <b>cells</b> tab from the top left, then choose the <b>rendering</b> tab in the right pane.</li>
      <li>Choose a taxonomic level for coloring with the <b>level_color_selector</b>:
        <ul>
          <li><b>1:</b> Neighborhood</li>
          <li><b>2:</b> Class</li>
          <li><b>3:</b> Subclass</li>
          <li><b>4:</b> Group (default)</li>
        </ul>
        <p>
          <img src="images/guide/annotation_taxonomic_colors.png" width="800" alt="taxonomic colors">
        </p>
      </li>
      <li>Adjust <b>annotation size</b> and <b>opacity</b>.</li>
    </ol>
    <img src="images/guide/annotation_rendering.png" width="300" alt="Rendering tab with taxonomic coloring, size, and opacity">
  </div>
</details>

<details>
  <summary><strong>3. View annotation metadata</strong></summary>
  <div>
    <p>To see metadata for an annotation:</p>
    <ol>
      <li>Click the hamburger icon (third icon) from the top right to toggle <i>Selection Details Panel</i>.</li>
      <img src="images/guide/selection_icon.png" alt="Toggle Selection Details Panel icon">
      <li>Mouse over an annotation to view its metadata from the right panel.</li>
    </ol>
    <img src="images/guide/annotation_metadata.png" alt="Viewing annotation metadata in the Selection Details Panel" width="300">
  </div>
</details>

<details>
  <summary><strong>4. Align view with cell sections by tilting cross-section plane</strong></summary>
  <div>
    <p>Tilting the cross-section plane helps match views to cell section planes.</p>
    <ol>
      <li>Click inside a view (coronal, transverse, sagittal) to focus it.</li>
      <li>Rotate with keys: <kbd>e</kbd> (left) and <kbd>r</kbd> (right).</li>
      <li>Alternatively, hold <kbd>Shift</kbd> and <b>drag with the mouse</b> to tilt across all axes.</li>
    </ol>
    <p><i>Before tilting</i></p>
    <img src="images/guide/crosssection_before.png" alt="Before tilting cross-section plane">
    <p><i>After tilting</i></p>
    <img src="images/guide/crosssection_after.png" alt="After tilting cross-section plane">
  </div>
</details>

<details>
  <summary><strong>5. Increase annotation view depth</strong></summary>
  <div>
    <p>If only a partial coronal cell-section plane is visible, increase the annotation view depth.</p>
    <p><b>Shortcut:</b> Hold <kbd>Alt</kbd> and use the <b>mouse wheel</b>.</p>
  </div>
</details>


## Neuroglancer views - coordinate spaces
*Click thumbnails to launch Neuroglancer for each coordinate space*

The cell coordinates are registered to four different reference spaces, each serving a distinct purpose.

### Slab  
The coordinate system of the *slab face images* that each spatial transcriptomics plane belongs to.  
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



| Species | Donor | Slab | Donor | CCF | HiP-CT |
|---|---|---|---|---|---|
| **Human** | **H22.30.001** | [<img src="images/H22.30.001_slab.png" width="220" style="border-radius:10px;border:2px solid #ccc;">](https://neuroglancer-demo.appspot.com/#!s3://allen-hmba-releases/neuroglancer/HMBA-MERSCOPE-H22.30.001-BG/20250630/viewer_state/H22.30.001_slab.json) | — | [<img src="images/H22.30.001_CCF%20template.png" width="220" style="border-radius:10px;border:2px solid #ccc;">](https://neuroglancer-demo.appspot.com/#!s3://neuroglancer-hmba/cifar/neuroglancer/H22.30.001_hipct_ccf.json) | [<img src="images/H22.30.001_HiP-CT.png" width="220" style="border-radius:10px;border:2px solid #ccc;">](https://neuroglancer-demo.appspot.com/#!s3://neuroglancer-hmba/cifar/neuroglancer/H22.30.001_hipct.json) |
| **Macaque** | **QM23.50.001** (Red) | [<img src="images/QM23.50.001_slab.png" width="220" style="border-radius:10px;border:2px solid #ccc;">](https://neuroglancer-demo.appspot.com/#!s3://allen-hmba-releases/neuroglancer/HMBA-MERSCOPE-QM23.50.001-BG/20250630/viewer_state/QM23.50.001_slab.json) | ETA 2026 | ETA 2026 | TBD |
| **Marmoset** | **CJ23.56.004** (Tank) | [<img src="images/CJ23.56.004_slab.png" width="220" style="border-radius:10px;border:2px solid #ccc;">](https://neuroglancer-demo.appspot.com/#!s3://allen-hmba-releases/neuroglancer/HMBA-Xenium-CJ23.56.004-BG/20250630/viewer_state/CJ23.56.004_slab.json) | ETA 2026 | ETA 2026 | TBD |
