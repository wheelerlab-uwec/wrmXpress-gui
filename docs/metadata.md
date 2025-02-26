# Metadata

By default, wrmXpress will generate a single CSV file for each pipeline selected. If desired, the user can supply experimental metadata that will be merged into final CSVs for easier downstream analysis.

A selection of metadata types have been pre-populated (Batch, SPecies, Strains, Stages, Treatments, Concentrations, and Other). Custom metadata types can be added by providing a title and clicking the "+" button. After finalizing metadata types, click "Update tables."

![Updating metadata tables](img/metadata_tables.gif){: style="width:100%"}

Tables will be generated based on the rows and columns provided in [Instrument Settings](configuration/instrument_settings.md). These tables can each be edited. Clicking "Save metadata" will save these tables as CSV in `metadata/`, and they will be merged with calculated raw data at the completion of each pipeline.
