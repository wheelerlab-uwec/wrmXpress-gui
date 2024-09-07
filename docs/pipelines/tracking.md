# Tracking

## Expected input

Tracking data may be analyzed in the form of individual TIF images per frame (i.e., the TimePoint structure utilized by ImageXpress) or in the form of raw, uncompressed AVI video containers. [See the data organization page for more details.](../data_organization.md). In the case of individual TIF images per frame, the directory structure should look like this:

![Structure for individual TIF images](../img/tif_structure.png)

In this experiment, the plate directory (`20210819-p01-NJW_753`) has 10 TimePoint directories. TimePoint directories have a single TIF image for each well.

In the case of AVIs, the directory structure should look like this:

![Structure for individual AVI videos](../img/avi_structure.png)

In this experiment, the plate directory (`20240307-p01-RVH`) has 6 videos, 1 video for each well.

All experiments should include a single wavelength and single site.

### Validated species and stages

- Schistosome miracidia  

### Example plates

- 20240307-p01-RVH: *Schistosoma mansoni* miracidia

## Expected output

A CSV file with at least # columns: . If using [Metadata](), there will be an additional column for each provided metadata data frame.

## Configuration of the GUI