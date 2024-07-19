# wrmXpress GUI

A Dash GUI for wrmXpress

## Releases

![GitHub release (with filter)](https://img.shields.io/github/v/release/wheelerlab-uwec/wrmXpress-gui)
![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/wheelerlab-uwec/wrmxpress-gui)

## Builds

[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/wheelerlab-uwec/wrmxpress-gui/push-docker-image.yml?event=release)](https://hub.docker.com/r/wheelern/wrmxpress_gui/tags)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/wheelern/wrmxpress_gui/latest)
![Docker Pulls](https://img.shields.io/docker/pulls/wheelern/wrmxpress_gui)

## Testing

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/wheelerlab-uwec/wrmxpress-gui/dash-test.yml)
<!---![Code coverage](https://wheelerlab-uwec.github.io/wrmxpress-gui/badges/coverage.svg) --->

## Installation and usage

***Prerequisites*** - Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

1. Create a working directory that contains all the input images. This folder is where temporary working files/images will be stored, where output data will be written, and will be mounted as a volume in the Docker container.
   + In the example below, this directory is `Users/njwheeler/mount`

2. Start the Docker engine and open up the Dashboard.
3. Use the search bar to find and pull the latest `wheelern/wrmxpress_gui` image from DockerHub:
   + Choose the most recent tag. The compressed image is >9 GB, so it will take a few minutes to pull.

    <img src="readme_img/dd1.png" alt="step 2" width="500" />

4. In the Images pane, click the Run symbol.

    <img src="readme_img/dd2.png" alt="step 3" width="500" />

5. Under Optional settings, make the following changes:
   + Under Ports, set the Host port to 9000
   + Under Volumes, set the Host path to be the path to the working directory created in step #1. Set the Container path to be `/home/`

    <img src="readme_img/dd3.png" alt="step 3" width="500" />

6. Click Run

7. Click the link to 9000:9000 or navigate to `http://localhost:9000` to view the app.

    <img src="readme_img/dd4.png" alt="step 4" width="500" />

8. Follow the guidance in the GUI to prepare and run your analysis.

    <img src="readme_img/dd5.png" alt="step 5" width="500" />

## Video walkthrough
<a href="https://vimeo.com/986779390?share=copy" target="_blank"><img src="readme_img/thumb.jpg" 
alt="wrmXpress Tutorial" width="500"/></a>

*Will open a new tab*