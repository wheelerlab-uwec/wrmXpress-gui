# Toxicity

/// note | Experimental protocol
Detailed procedures for preparing and recording images of filarial nematode microfilariae (mf) can be found at the following link: [Bivariate, high-content screening of *Brugia malayi* microfilariae](https://protocolexchange.researchsquare.com/article/pex-1916/v2)

///

## Expected input

Toxicity data should be analyzed in the form of individual TIF images per frame (i.e., the TimePoint structure utilized by ImageXpress). See the [Data Organization](../../data_organization.md) page for more details. The plate directory should have a single TimePoint with individual images for each well:

![Toxicity file structure](../img/toxicity_structure.png)

All experiments should include a single wavelength. Multisite images should be stitched according the [ImageXpress + Multi Site instructions](../instrument_settings.md#imagexpress-multi-site). The above screenshot shows the structure of unstitched input images that include the `_s[1|2|3|4].TIF` structure.

### Validated species and stages

#### Filarial nematodes (i.e., *Brugia malayi* and *Dirofilaria immitis*)

- Microfiliariae
- L3s
- Adults (with varying success)

#### *Caenorhabditis elegans*

- Larvae
- Young adults
- Gravid adults

### Example plates

- 20210917-p15-NJW_913: *Brugia malayi* microfilariae

## Expected output

A CSV file with at least # columns: . If using [Metadata](), there will be an additional column for each provided metadata data frame.

## Configuration of the GUI

No special configuration is required.