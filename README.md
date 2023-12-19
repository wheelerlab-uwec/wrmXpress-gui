# wrmXpress GUI

A Dash GUI for wrmXpress

## Releases

![GitHub release (with filter)](https://img.shields.io/github/v/release/wheelerlab-uwec/wrmXpress-gui)
![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/wheelerlab-uwec/wrmxpress-gui)

## Builds

[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/wheelerlab-uwec/wrmxpress-gui/push-docker-image.yml?event=release)](https://hub.docker.com/r/wheelern/wrmxpress_gui/tags)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/wheelern/wrmxpress_gui/latest)
![Docker Pulls](https://img.shields.io/docker/pulls/wheelern/wrmxpress_gui)

## Installation and usage

***Prerequisites*** - Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

1. Start the Docker engine and open up the Dashboard.
2. Use the search bar to find and pull the latest wheelern/wrmXpress_gui image from DockerHub. Choose the most recent tag. The compressed image size is >1.5 GB, so it will take a few minutes to pull.

    <img src="readme_img/dd1.png" alt="step 2" width="300" />

3. In the Images pane and Local tab, click the Run symbol.

    <img src="readme_img/dd2.png" alt="step 3" width="300" />

4. Under Optional settings, set the Host port to 9000 and click Run.

    <img src="readme_img/dd3.png" alt="step 3" width="300" />

5. Click the link to 9000:9000 or navigate to `http://localhost:9000` to view the app.

    <img src="readme_img/dd4.png" alt="step 4" width="300" />

6. Follow the guidance in the GUI to prepare and run your analysis.

    <img src="readme_img/dd5.png" alt="step 5" width="300" />
