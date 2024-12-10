# Run-Time Settings

This part of the run configuration directs wrmXpress to the proper folder and plate to use as input. It also allows the user to select the wells to analyze or to analyze the full plate.

## Directories

If running the GUI with Docker Desktop as outlined in [Usage](../index.md#usage), you should have set your working directory (a location on your computer) to be mounted as a Volume in the Docker container. The volume's container path should be set to in the `/home/` when starting the GUI, and the "Volume path" in the GUI should also be set to `/home/`. The GUI running in the container cannot access your file system except through this mounting functionality.

The "Plate name" should be the name of the plate that was copied to the working directory that was mounted to the container. The folder should with the plate name should include all the images as instructed in the [Data Organization page](../data_organization.md).

## Wells

Invidual or groups of wells can be selected for analysis instead of an entire plate. By default, the entire plate will be analyzed. To select specifc wells of interest, simply remove the well ID from the table. 

!!! warning
    wrmXpress will give a warning if wells are selected that don't have corresponding data in the input plate name directory, but the analysis will still run.

!!! note
    Multiple wells can be selected and deleted by holding Shift while clicking on the table. If some wells are inadvertently deselected, simply refresh the page.