# Fecundity

***Detailed experimental protocols for preparing and recording images of filarial nematode or schistosome progeny can be found at the following links***

- [Protocol for *Brugia malayi* fecundity](https://protocolexchange.researchsquare.com/article/pex-1918/v2)
- [Protocol for *Schisotsoma mansoni* fecundity](https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0010937)

## Expected input

Fecundity data may be analyzed in the form of individual TIF images per frame (i.e., the TimePoint structure utilized by ImageXpress).  See the [Data Organization](../data_organization.md) page for more details. The plate directory should have a single TimePoint with individual images for each well:

Each well should include all the progeny from a single parent.

All experiments should include a single wavelength. Multisite images should be stitched according the [ImageXpress + Multi Site instructions](../../instrument_settings/#imagexpress-multi-site).

### Validated species and stages

- Filarial nematodes (i.e., *Brugia malayi* and *Dirofilaria immitis*)
- Schistosomes

### Example plates

- 20220722-p04-JDC_1606: *Schistosoma mansoni* with adults and eggs in the well
- 20220722-p06-JDC_1608: *Schistosoma mansoni* without adults and eggs in the well
- 20210906-p01-NJW_857: *Brugia pahangi* 

## Expected output

A CSV file with at least two columns: Well and Worm Area. Variation in the number of worms per well can be corrected for by diving the motility value by the area value. If using [Metadata](), there will be an additional column for each provided metadata data frame.

## Configuration of the GUI