# Instrument Settings

wrmXpress can be used with a variety of data structures. Some pipelines require a particular structure - these requirements can be found in the relevant pipeline documentation. For more information, please see the [data organization documentation](../data_organization.md).

## Potential structures

### ImageXpress + Single Well

- Data is structured as TIFF files in TimePoint folders ([see more](../data_organization.md)).
- Each TIFF image includes a single well.
- Potential naming pattern:
  - `{plate name}_{well}.TIF`
  - `{plate name}_{well}_{wavelength}.TIF`

Examples:

![TIFF, Single Site](docs/img/instrument_settings/tiff-singlesite.png){: style="width:400px"}
![TIFF, Single Site](docs/img/instrument_settings/tiff-singlesite2.png){: style="width:400px"}
![TIFF, Single Site](docs/img/instrument_settings/tiff-singlesite3.png){: style="width:400px"}

### ImageXpress + Multi Well

- Data is structured as TIFF files in TimePoint folders ([see more](../data_organization.md)).
- Each TIFF image includes more than 1 well.
- Input the number of wells in each row/column of the image (integers).

### ImageXpress + Multi Site

- Data is structured as TIFF files in TimePoint folders ([see more](../data_organization.md)).
- Each TIFF image includes a portion of a single well.
- If the pipeline should first stitch the images together, select stitch. If the pipeline should analyze each site independently, leave it unselected.
- Potential naming patterns:
  - `{plate name}_{well}_{site}.TIF`
  - `{plate name}_{well}_{wavelength}_{site}.TIF`
  
Examples:

![TIFF, Multi Site](docs//img/instrument_settings/tiff-multisite.png){: style="width:400px"}
***(Post-stitching)

### AVI + Single Well

- Videos are stored in AVI containers ([see more](../data_organization.md)).
- Each AVI video includes a single well.
- Potential naming patterns:
  - `{plate name}_{well}.avi`

### AVI + Multi Well

- Videos are stored in AVI containers ([see more](../data_organization.md)).
- Each AVI video includes more than 1 well (i.e., an entire plate).
- Input the number of wells in each row/column of the video (integers).
- The Grid cropping option will split the video into a grid of `rows` and `columns` based on user input. More cropping options may be developed in the future.
- Potential naming patterns:
  - `{plate name}.avi`

Examples

![AVI, Multi Site](docs/img/instrument_settings/avi-multiwell.png){: style="width:400px"}
![AVI, Multi Site](docs/img/instrument_settings/avi-multiwell2.png){: style="width:400px"}