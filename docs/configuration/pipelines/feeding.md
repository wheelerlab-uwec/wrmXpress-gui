# Feeding

***Detailed experimental protocols for preparing and recording images of filarial microfilariae (mf) or adults can be found at the following links***

***Detailed experimental protocols for preparing and imaging Caenorhabditis elegans phenotypes can be found at the following link:***

- [Protocol for *Caenorhabditis elegans* image-based screening](https://protocolexchange.researchsquare.com/article/pex-2018/v1)

## Expected input

Feeding data may be analyzed in the form of individual TIF images per frame (i.e., the TimePoint structure utilized by ImageXpress). [See the data organization page for more details.](../data_organization.md). In the case of individual TIF images per frame, the directory structure should look like this:

All experiments should include three wavelengths and single site.

### Validated species and stages

- *Caenorhabditis elegans* young adults

### Example plates

- 20210823-p01-KJG_795: *Caenorhabditis elegans* young adults

## Expected output

A CSV file with at least three columns: Well, Total Motility, and Worm Area. Variation in the number of worms per well can be corrected for by diving the motility value by the area value. If using [Metadata](), there will be an additional column for each provided metadata data frame.

## Configuration of the GUI