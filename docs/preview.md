# Preview

Each pipeline can be previewed by running on a single well (by default, the first well selected). This allows the user to troubleshoot and optimize configuration prior to running a full analysis. The Preview page will provide an Input Preview to confirm that the input images can be properly loaded and an Analysis Preview that shows a default diagnostic image:

![Preview page](img/preview.gif){: style="width:100%"}

If multiple pipelines were selected, relevant diagnostic images can be loaded by selecting the pipeline in the dropdown and clicking "Load image."

Data will be saved to `output/{pipeline}/{plate}_{well}_{wavelength}.csv`.
