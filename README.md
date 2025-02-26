# wrmXpress GUI

A Dash GUI for wrmXpress

## Releases & Builds

![GitHub release (with filter)](https://img.shields.io/github/v/release/wheelerlab-uwec/wrmXpress-gui)
![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/wheelerlab-uwec/wrmxpress-gui)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/wheelerlab-uwec/wrmxpress-gui/push-docker-image.yml?event=release)](https://hub.docker.com/r/wheelern/wrmxpress_gui/tags)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/wheelern/wrmxpress_gui/latest)
![Docker Pulls](https://img.shields.io/docker/pulls/wheelern/wrmxpress_gui)

<!-- ## Testing

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/wheelerlab-uwec/wrmxpress-gui/dash-test.yml)
-![Code coverage](https://wheelerlab-uwec.github.io/wrmxpress-gui/badges/coverage.svg) - -->

## Installation and usage

Visit the [ReadTheDocs](https://wrmxpress-gui.readthedocs.io/latest/) website to view comprehensive documentation for the wrmXpress GUI.

## Developers

wrmXpress is entirely open-source. The code for the back-end is maintained by the [Zamanian Lab](https://www.zamanianlab.org/) at the University of Wisconsin-Madison and can be found [here](https://github.com/zamanianlab/wrmXpress). The code for the front-end is maintained by the [Wheeler Lab](https://wheelerlab.bio/) at the University of Wisconsin-Eau Claire and can be found in this repository. To receive support for either the GUI or running wrmXpress remotely, please submit a GitHub Issue at the relevant linked repositories.

## Citing wrmXpress

When using the wrmXrpress backend on a remote machine, please cite:

    @ARTICLE{Wheeler2022-ou,
      title    = "{wrmXpress}: A modular package for high-throughput image analysis
                  of parasitic and free-living worms",
      author   = "Wheeler, Nicolas J and Gallo, Kendra J and Rehborg, Elena J G and
                  Ryan, Kaetlyn T and Chan, John D and Zamanian, Mostafa",
      journal  = "PLoS Negl. Trop. Dis.",
      volume   =  16,
      number   =  11,
      pages    = "e0010937",
      month    =  nov,
      year     =  2022,
      language = "en"
    }

When using the GUI, please site the backend (above) as well as this repository:

    @software{Caterer2024,
      author = {Caterer, Zachary and Horejsi, Rachel and Weber, Carly and Mathisen, Blake and 
      Nelson, Chase and Bagatta, Maggie and Coughlin, Ireland and Wettstein, Megan and 
      Zamanian, Mostafa and Wheeler, Nicolas J.},
      title = {A graphical user interface for wrmXpress democratizes phenotypic screening of 
      parasitic worms},
      date = {2024-07-18},
      url = {https://github.com/wheelerlab-uwec/wrmXpress-gui},
      version = {v1.0.0}
    }