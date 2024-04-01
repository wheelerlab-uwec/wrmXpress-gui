# Table of Contents

| Section        | Header                                           |
|:---------------:|:---------------------------------------------------:|
| I.            | [Project Title](#i-project-title)                 | 
| II.           | [Project Description](#ii-project-description)    | 
| III.          | [Installations](#iii-installation)                |
| IV.           | [Useage](#iv-usage)                               |
| V.            | [Configurations](#v-configurations)               |
| VI.           | [Contributions](#vi-contributions)                |
| VII.          | [License](#vii-license)                           |
| VIII.         | [Authors](#viii-authors)                          |
| IX.           | [Acknowledgements](#ix-acknowledgements)          |
| X.            | [Support](#x-support)                             |
| XI.           | [Project Status](#xi-project-status)              |
| XII.          | [Changelog](#xii-changelog)                       |
| XIII.         | [Roadmaps](#xiii-roadmaps)                        |
| IVX.          | [References](#ivx-references)                     |

## I. Project Title
- wrmXpress GUI

## II. Project Description
    wrmXpress is a unified framework for the analysis of diverse phenotypic imaging data in high-throughput and high-content experiments involving free-living and parasitic nematodes and flatworms. wrmXpress is a versatile solution capable of handling large datasets and generating relevant phenotypic measurements across various worm species and experimental assays. This software, designed to analyze a spectrum of phenotypes such as motility, development/size, fecundity, and feeding, not only addresses current research needs but also establishes itself as a platform for future extensibility, enabling the development of custom phenotypic modules.

## III. Installation 

***Prerequisites*** - Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

1. Create a folder that contains all the input images. This folder is where temporary working files/images will be stored, where output data will be written, and will be mounted as a volume in the Docker container.
2. Start the Docker engine and open up the Dashboard.
3. Use the search bar to find and pull the latest images from DockerHub:
   + `wheelern/wrmxpress_gui`
   + `zamanianlab/wrmxpress`
  
   Choose the most recent tags. The compressed images are >1.5 GB and >7 GB respectively, so they will take a few minutes to pull.

    <img src="readme_img/dd1.png" alt="step 2" width="500" />

4. In the Images pane and Local tab, click the Run symbol.

    <img src="readme_img/dd2.png" alt="step 3" width="500" />

5. Under Optional settings, make the following changes:
   + Under Ports, set the Host port to 9000
   + Under Volumes, set the Host and Container paths to be the path to the working directory created in step #1 (in the example below, the Host path is `/Users/njwheeler/mount`)
   + Add a new volume by clicking the + syumbol and set the Host and Container paths to `/var/run/docker.sock`

    <img src="readme_img/dd3.png" alt="step 3" width="500" />

6. Click Run

7. Click the link to 9000:9000 or navigate to `http://localhost:9000` to view the app.

    <img src="readme_img/dd4.png" alt="step 4" width="500" />

8. Follow the guidance in the GUI to prepare and run your analysis.

    <img src="readme_img/dd5.png" alt="step 5" width="500" />

## IV. Useage
1. Remotely
    
    wrmXpress was originally designed to be invoked remotely, using a high-performance or high-throughput computer. There are many ways to go about this, but we recommend encapsulating the entire process in a Docker container. The container should include the Python libraries required by wrmXpress (see the Zamanian Lab's Dockerfile/conda environment for an example), the cloned wrmXpress repository, the input data in a directory called input/, and a YAML file that configures the analysis. A user can use this graphical user interface (GUI) to produce the YAML by selecting the options and modules and clicking Save YAML.

2. Locally

    Many analyses, such as those that include a few dozen separate videos or images, can be performed on a desktop computer without the need for high-performance or high-throughput computing. For these, a user can use this GUI to select the options and modules and run the analysis by clicking the Preview and Run button.


3. Include videos here

## V. Configurations
   - If your project requires any configuration settings, explain how to set them up.

## VI. Contributions
   - wrmXpress is entirely open-source. The code for the back-end is maintained by the [Zamanian Lab](https://www.zamanianlab.org/) at the University of Wisconsin-Madison and can be found [here](https://github.com/zamanianlab/wrmXpress). The code for the front-end is maintained by the [Wheeler Lab](https://wheelerlab.bio/) at the University of Wisconsin-Eau Claire and can be found [here](https://github.com/wheelerlab-uwec/wrmXpress-gui).

## VII. License
   - License information can be found [here](https://github.com/wheelerlab-uwec/wrmXpress-gui/blob/main/LICENSE)

## VIII. Authors
   - [Nic Wheeler](https://github.com/wheelern)
   - [Zachary Caterer](https://github.com/caterer-z-t)
   - [Sage Mathisen](https://github.com/mathisensage)

## IX Acknowledgements
   - Optional. Thank any individuals or organizations that have contributed to the project or inspired its development.

## X. Support
   - Include information on how users can get support for your project, such as links to documentation, community forums, or support channels.

## XI. Project Status

  ### Releases

![GitHub release (with filter)](https://img.shields.io/github/v/release/wheelerlab-uwec/wrmXpress-gui)
![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/wheelerlab-uwec/wrmxpress-gui)

### Builds

[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/wheelerlab-uwec/wrmxpress-gui/push-docker-image.yml?event=release)](https://hub.docker.com/r/wheelern/wrmxpress_gui/tags)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/wheelern/wrmxpress_gui/latest)
![Docker Pulls](https://img.shields.io/docker/pulls/wheelern/wrmxpress_gui)

### Testing

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/wheelerlab-uwec/wrmxpress-gui/dash-test.yml)

## XII. Changelog
   - Optional. Include a brief summary of changes in each version of the project.

## XIII. Roadmaps
   - Optional. Outline future plans or enhancements for the project.

## IVX. References
   - Optional. Include any references or external resources that are relevant to your project.


## All Thanks To Our Contributors:

<a href="https://github.com/wheelerlab-uwec/wrmXpress-gui/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=wheelerlab-uwec/wrmXpress-gui" />
</a>


