# wrmXpress

GUI: ![GitHub release (with filter)](https://img.shields.io/github/v/release/wheelerlab-uwec/wrmXpress-gui)
![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/wheelerlab-uwec/wrmxpress-gui)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/wheelerlab-uwec/wrmxpress-gui/push-docker-image.yml?event=release)](https://hub.docker.com/r/wheelern/wrmxpress_gui/tags)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/wheelern/wrmxpress_gui/latest)
![Docker Pulls](https://img.shields.io/docker/pulls/wheelern/wrmxpress_gui)

Back-end: ![GitHub Release](https://img.shields.io/github/v/release/zamanianlab/wrmXpress)
![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/zamanianlab/wrmxpress)

wrmXpress is a suite of tools to analyze images and videos of free-living and parasitic flatworms and nematodes. It is designed to work out-of-the-box with data generated with a Molecular Devices ImageXpress high-content imager, but will work with any image type that is organized in an idiosyncratic manner (described in [Data Organization](data_organization.md)). Analytical pipelines featured in wrmXpress include:

- [Optical Flow (Motility)](configuration/pipelines/optical_flow.md)
- [Segmentation](configuration/pipelines/segmentation.md)
    - Segmentation is used for fecundity experiments or to estimate the number of worms in a well to assist in normalization of optical flow data
- Custom CellProfiler pipelines:
    - [Viability](configuration/pipelines/viability.md)
    - [Feeding](configuration/pipelines/feeding.md)
    - [Development](configuration/pipelines/development.md)
- [Tracking](configuration/pipelines/tracking.md)

Some pipelines require specific experimental procedures to generate the proper data (i.e., the Feeding pipeline requires images of worms that have been fed fluorescent dyes), while other pipelines are generalizable across multiple worm species, stages, and imaging environments. Detailed documentation for each pipeline can be found at the corresponding links above.

## Usage

For large high-throughput analyses, wrmXpress can be run using a command-line interface and is deployable to high-throughput or high-performance remote computer clusters. If running small to medium sized analyses (i.e., 96 wells or less), wrmXpress can also be run using a graphical-user interface (GUI) on any computer operating system (Windows, MacOS, Linux) with Docker Desktop. This documentation is oriented toward users of the GUI and includes screenshots and videos of GUI configuration and usage.

### Installing and starting the GUI

/// note | Prerequisites
Before starting, download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
///

The GUI is deployed via Docker Desktop and is run in any modern browser (i.e., Chrome, Firefox, Safari, etc.). Installation through Docker Desktop is simple and allows for pain-free updates when desired.

1. Create a working directory on your computer that contains all the input images. This folder is where temporary working files/images and output data will be stored. The folder will be mounted as a volume in the Docker container.
    - In the example below, this directory is `Users/njwheeler/mount`

2. Open Docker Desktop.
3. Use the search bar to find and download ("pull") the latest `wheelern/wrmxpress_gui` image from DockerHub:
    - Choose the most recent tag. The compressed image is >9 GB, so it will take a few minutes to download.

    ![Pulling the GUI image](img/pull.gif){: style="width:100%"}

4. After downloading, in the Images pane of Docker Desktop, click the Run symbol.
5. Under Optional settings, make the following changes:
    1. Under Ports, set the Host port to 9000
    2. Under Volumes, set the Host path to be the path to the working directory created in step #1. Set the Container path to be `/home/`
6. Click Run
    - Click OK if a warning pops up.
  
    ![Running the GUI image](img/run.gif){: style="width:100%"}

7. Once running, click the link to 9000:9000 or navigate to `http://localhost:9000` to view the app.

    ![Starting the GUI image](img/start.gif){: style="width:100%"}

    /// warning | Be patient
    It may take 15-30 seconds for the GUI to start. Refresh the page if the GUI is not showing up in your browser.
    ///

## Quick start

To configure and run analyses, use the navigation column at left-hand side of the GUI. Full documentation for the Configure, Metadata, Preview, and Run steps can be found in the corresponding sections of this documentation site.

1. **Configure** allows you to select relevant experimental and imaging parameters, as well as select the pipeline that you wish to run. Note that some selections will clash and be disallowed.
2. **Metadata** allows you to include well-based metadata. Each metadata type (i.e., concentration, treatment, time point, etc.) will be saved in a separate CSV with the same number of rows/columns selected in Configure - [Run-Time Settings](configuration/runtime.md).
Custom metadata types can be added. Metadata will be merged with raw output after completing the analysis. Metadata is not required for a pipeline to run.
3. **Preview** will allow you to preview the output of the pipeline's analysis on well A01 (or on the first well selected).
4. **Run** is where the final pipeline will be run on all of the selected wells. Logs are written dynamically to the screen but also to the working directory.

After running, raw data or data merged with metadata can be found in `{working_directory}/output/`. The `{working_directory}/work/` folder will contain log files and some intermediary images. `{working_directory}/input/` will contain the  pre-processed input files copied from `{working_directory}`. The wrmXpress GUI never edits or deletes the original images in `{working_directory}`.

### Video walkthrough

<div style="padding:49.12% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/986779390?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write" style="position:absolute;top:0;left:0;width:100%;height:100%;" title="wrmXpress GUI Walkthrough"></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>


### Example data

Validated example data can be downloaded in the GUI by clicking Zenodo button at the bottom left-hand corner of the interface. In the popup, select the plates to download. After downloading, move the plate folder into the working directory set in step 1 of the [installation/startup instructions above](#installing-and-starting-the-gui).

![Download example data](img/download.png){: style="width:100%"}

## Getting support

To receive support for either the GUI or running wrmXpress remotely, please submit a GitHub Issue at the relevant linked repositories:

- [wrmXpress back-end](https://github.com/zamanianlab/wrmXpress)
- [wrmXpress GUI](https://github.com/wheelerlab-uwec/wrmXpress-gui)

Log files for preview/run attempts will be written to the `work/` directory and should be included in any raised Issue.

## Developers

wrmXpress is entirely open-source. The code for the back-end is maintained by the [Zamanian Lab](https://www.zamanianlab.org/) at the University of Wisconsin-Madison and can be found [here](https://github.com/zamanianlab/wrmXpress). The code for the front-end is maintained by the [Wheeler Lab](https://wheelerlab.bio/) at the University of Wisconsin-Eau Claire and can be found [here](https://github.com/wheelerlab-uwec/wrmXpress-gui).

## Citing wrmXpress

When using the wrmXrpress back-end on a remote machine, please cite:

    @article{Wheeler2022,
      title     = {wrmXpress: A modular package for high-throughput image analysis of parasitic and free-living worms},
      author    = {Wheeler, Nicolas J. AND Gallo, Kendra J. AND Rehborg, Elena J. G. AND Ryan, Kaetlyn T. AND Chan, John D. AND Zamanian, Mostafa},
      journal   = {PLOS Neglected Tropical Diseases},
      volume    = {16},
      number    = {11},
      pages     = {1-15},
      year      = {2022},
      month     = {11},
      doi       = {10.1371/journal.pntd.0010937},
      publisher = {Public Library of Science},
      doi       = {https://doi.org/10.1371/journal.pntd.0010937},
      url       = {https://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0010937},

}

When using the GUI, please site the back-end (above) as well as the following:

    @article{Caterer2025,
      title    = {A graphical user interface for wrmXpress 2.0 streamlines helminth phenotypic screening},
      author   = {Zachary Caterer and Rachel V. Horejsi and Carly Weber and Blake Mathisen and Chase N. Nelson and Maggie Bagatta and Ireland Coughlin and Megan Wettstein and Ankit Kulshrestha and Hui Siang Benjamin Lee and Leonardo R. Nunn and Mostafa Zamanian and Nicolas J. Wheeler}
      journal  = {International Journal for Parasitology: Drugs and Drug Resistance},
      volume   = {27},
      pages    = {100588},
      year     = {2025},
      issn     = {2211-3207},
      doi      = {https://doi.org/10.1016/j.ijpddr.2025.100588},
      url      = {https://www.sciencedirect.com/science/article/pii/S2211320725000119},
    }
