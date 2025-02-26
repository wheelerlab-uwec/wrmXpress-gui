# Fecundity

/// note | Experimental protocols
Detailed procedures for preparing and recording images of filarial nematode or schistosome progeny can be found at the following links***

- [Multivariate screening of *Brugia* spp. adults](https://protocolexchange.researchsquare.com/article/pex-1918/v2)
- [wrmXpress: A modular package for high-throughput image analysis of parasitic and free-living worms](https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0010937#sec002)
///

## Configuration of the GUI

Fecundity can be analyzed using the generic segmentation methods. In Pipeline Selection, choose Segmentation. The following parameters can be adjusted:

1. `model_type`: Select either Python or Cellpose. If Cellpose, select the appropriate model in the `cellpose_model` dropdown. If Python, enter the standard deviation to be used for the Gaussian kernel (`sigma`).
2. `cellpose_model`: Select the trained Cellpose model to be used for worm identification. For fecundity, models are provided for microfilaria identification, but this will ignore pretzels and embryos. If interested in all stages of development, select Python in `model_type`.
3. `sigma` (Default = 2.5): Details found at [the SciPy documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_filter.html). A larger value result in blurier images to segment.
4. `wavelengths` (Default = 'All): The wavelength(s) to use as input for segmentation.

## Expected input

Fecundity data may be analyzed in the form of individual TIF images per frame (i.e., the TimePoint structure utilized by ImageXpress). See the [Data Organization](../../data_organization.md) page for more details. The plate directory should have a single TimePoint with individual images for each well:

![Fecundity file structure](../img/fecundity_structure.png)

Each well should include all the progeny from a single parent.

All experiments should include a single wavelength. Multisite images should be stitched according the [ImageXpress + Multi Site instructions](../instrument_settings.md#imagexpress-multi-site).

### Validated species and stages

- Filarial nematodes (i.e., *Brugia malayi* and *Dirofilaria immitis*)
- Schistosomes

### Example plates

- 20220722-p04-JDC_1606: *Schistosoma mansoni* with adults and eggs in the well
- 20220722-p06-JDC_1608: *Schistosoma mansoni* without adults and eggs in the well
- 20210906-p01-NJW_857: *Brugia pahangi*

## Expected output

A CSV file with at least two columns: Well and Worm Area. Variation in the number of worms per well can be corrected for by diving the motility value by the area value. If using [Metadata](), there will be an additional column for each provided metadata data frame.
