# wrmXpress-gui

A GUI for wrmXpress using Dash.

## Install and run

***Prerequisites*** - Install [Docker Engine](https://docs.docker.com/engine/install/)

1. Clone this repository
2. Navigate to the cloned repository and build the Docker image:
    `docker build -t wrmxpress_gui .`
3. Run the Docker, exposing the output to the exact port:
    `docker run -h localhost -p 9002:9000 -d --name wrmxpress_gui  wrmxpress_gui`
4. Navigate to the port by inserting `http://localhost:9002/` into a browser search bar.
