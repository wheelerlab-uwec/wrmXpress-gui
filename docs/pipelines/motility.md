# Motility

***Detailed experimental protocols for preparing and recording videos of filarial microfilariae (mf) or adult can be found at the following links***

- [Protocol for *Brugia malayi* microfilariae](https://protocolexchange.researchsquare.com/article/pex-1916/v2)
- [Protocol for *Brugia malayi* adults](https://protocolexchange.researchsquare.com/article/pex-1918/v2)

## Data organization

Motility data may be analyzed in the form of individual TIF images per frame (i.e., the TimePoint structure utilized by ImageXpress) or in the form of raw, uncompressed AVI video containers. [See the data organization page for more details.](../data_organization.md). In the case of individual TIF images per frame, the directory structure should look like this:

![Structure for individual TIF images](../img/tif_structure.png)

In this experiment, the plate directory (`20210819-p01-NJW_753`) has 10 TimePoint directories. TimePoint directories have a single TIF image for each well.

In the case of AVIs, the directory structure should look like this:

![Structure for individual AVI videos](../img/avi_structure.png)

In this experiment, the plate directory (`20240307-p01-RVH`) has 6 videos, 1 video for each well.

## Configuration of the GUI