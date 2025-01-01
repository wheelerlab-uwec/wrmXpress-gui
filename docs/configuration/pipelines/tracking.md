# Tracking

/// warning | Note
Tracking is implemented for worms that are native to a liquid environment. So far, the tracking pipeline has only been tested with schistosome miracidia. It is unlikely to perform well for worms that only thrash and do not demonstrate translational movement in liquid culture. For situations such as this, we recommend the [optical flow motility pipeline](motility.md).
///

## Configuration of the GUI

Tracking of worms is implemented with [Trackpy](https://soft-matter.github.io/trackpy/v0.6.4/) and is split into two steps: object identification and object linking. Some information below is copied from the Trackpy documentation. Tracking can run on data in the ImageXpress file structure or the AVI file structure (see [Expected input](#expected-input) below).

Three parameters can be set for object identification (used to configure [`trackpy.locate`](https://soft-matter.github.io/trackpy/v0.6.4/generated/trackpy.locate.html#trackpy.locate)):

1. `diameter` (Default = 35): The diameter in pixels of the objects of interest.
2. `minmass` (Default = 1200): The minimum integrated brightness of objects of interest. Lower values will maintain dimmer objects. Set to 0 to disable all object filtering (may cause problems in the object linking step).
3. `noise_size` (Default = 2): The standard deviation to be used for the Gaussian kernel used to add blur and denoise the image prior to object identification.

Three parameters can be set for object identification (used to configure [`trackpy.link`](https://soft-matter.github.io/trackpy/v0.6.4/generated/trackpy.link.html#trackpy.link)):

1. `search_range` (Default = 45): The maximum distance features can move between frames. This is related to the maximum speed of the worm (use larger values for faster animals).
2. `memory` (Default = 25): The maximum number of frames during which a feature can vanish, then reappear nearby, and be considered the same particle.
3. `adaptive_stop` (Default = 30): If an object cannot be linked between two frames by searching within `search_range` becasue there are two many objects within that range, the algorithm will reduce `search_range` and search again. When `search_range` becomes less than or equal to `adaptive_stop`, the search will stop and an error will be raised.

## Expected input

Tracking data may be analyzed in the form of individual TIF images per frame (i.e., the TimePoint structure utilized by ImageXpress) or in the form of raw, uncompressed AVI video containers. See the [Data Organization](../../data_organization.md) page for more details. All experiments should include a single wavelength and single site.

### File structure: ImageXpress + Single Well

In the case of individual TIF images per frame, the directory structure should look like this:

![Structure for individual TIF images](../../img/tif_structure.png)

In this experiment, the plate directory (`20210819-p01-NJW_753`) has 10 TimePoint directories. TimePoint directories have a single TIF image for each well.

In [Instrument Settings](../instrument_settings.md), choose ImageXpress + Single Well as the File Structure. Tracking has not been tested with a Multi Well or Multi Site format.

### File structure: AVI + Single Well

In the case of AVIs, the directory structure should look like this:

![Structure for individual AVI videos](../../img/avi_structure.png)

In this experiment, the plate directory (`20240307-p01-RVH`) has 6 videos, 1 video for each well.

In [Instrument Settings](../instrument_settings.md), choose AVI + Single Well as the File Structure. Tracking has not been tested with a Multi Well format.

### Validated species and stages

- Schistosome miracidia  

### Example plates

- 20240307-p01-RVH: *Schistosoma mansoni* miracidia

## Expected output

A CSV file with at least 11 columns: well, y, x, mass, size, ecc, signal, raw_mass, ep, frame, and particle. If using [Metadata](), there will be an additional column for each provided metadata data frame.
