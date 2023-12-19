# Use the official Miniconda base image
FROM continuumio/miniconda3

# Install a few opencv dependencies
RUN apt-get update
RUN apt-get install -y libgl1

# Set the working directory inside the container
WORKDIR /app

# Copy the environment.yml file to the container
COPY environment_minimal.yml .

# Create a Conda environment from the environment.yml file
RUN conda env create --name wrmxpress_gui_minimal -f environment_minimal.yml

# Copy files to the image
RUN mkdir app
COPY app/* app/
COPY app.py .

# Activate the Conda environment
# SHELL ["conda", "run", "-n", "wrmxpress_gui_minimal", "/bin/bash", "-c"]

# Demonstrate the environment is activated:
# RUN echo "Make sure cv2 is installed:"
# RUN python -c "import cv2"

EXPOSE 9000

# The code to run when container is started:
# COPY Main_Page/main_page.py entrypoint.sh ./
ENTRYPOINT ["conda", "run", "-n", "wrmxpress_gui_minimal", "python", "app.py"]