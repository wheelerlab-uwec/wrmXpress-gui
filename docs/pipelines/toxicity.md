# Toxicity

***Detailed experimental protocols for preparing and imaging filarial nematode microfilariae (mf) can be found at the following links***

- [Protocol for *Brugia malayi* microfilariae](https://protocolexchange.researchsquare.com/article/pex-1916/v2)

## Expected input

Toxicity data should be analyzed in the form of individual TIF images per frame (i.e., the TimePoint structure utilized by ImageXpress). [See the data organization page for more details.](../data_organization.md). The plate directory should have a single TimePoint with individual images for each well:

All experiments should include a single wavelength. Multisite images should be stitched [see the stitching documentation]().

### Validated species and stages

- Filarial nematodes (i.e., *Brugia malayi* and *Dirofilaria immitis*)
  - Microfiliariae
  - L3s
  - Adults (with varying success)
- Schistosomes
  - Adults
  - Schistosomula
  - Cercaria
  - Miracidia (but we recommend using the [Tracking](tracking.md) pipeline instead)
- *C. elegans*
  - Larvae
  - Young adults
  - Gravid adults

### Example plates

- 20210917-p15-NJW_913: *Brugia malayi* microfilariae

## Expected output

A CSV file with at least # columns: . If using [Metadata](), there will be an additional column for each provided metadata data frame.

## Configuration of the GUI