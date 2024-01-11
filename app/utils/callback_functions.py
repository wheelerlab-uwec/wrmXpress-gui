########################################################################
####                                                                ####
####                             Imports                            ####
####                                                                ####
########################################################################
import pandas as pd

########################################################################
####                                                                ####
####                             LAYOUT                             ####
####                                                                ####
########################################################################
def create_df_from_inputs(_rows, _cols):
    rows_total = list("ABCDEFGHIJKLMNOP")
    rows = rows_total[:int(_rows)]
    columns = [str(num).zfill(2) for num in range(1, int(_cols) + 1)]
    data = [[row + col for col in columns] for row in rows]
    df = pd.DataFrame(data, columns=columns, index=rows)
    return df

def create_empty_df_from_inputs(_rows, _cols):
    rows_total = list("ABCDEFGHIJKLMNOP")
    rows = rows_total[:int(_rows)]
    columns = [str(num).zfill(2) for num in range(1, int(_cols) + 1)]
    empty_data = [[None for _ in columns] for _ in rows]
    df = pd.DataFrame(empty_data, columns=columns, index=rows)
    return df

def eval_bool(v):
  return str(v).lower() in ("yes", "true", "t", "1", "True")

def prep_yaml(
        imagingmode,
        filestructure,
        multiwellrows,
        multiwellcols,
        multiwelldetection,
        species,
        stages,
        motilityrun,
        conversionrun,
        conversionscalevideo,
        conversionrescalemultiplier,
        segmentrun,
        wavelength,
        cellprofilerrun,
        cellprofilerpipeline,
        diagnosticdx,
        wellselection):
    
    if isinstance(wellselection, list):
        if len(wellselection) == 96:
            wellselection = ['All']
        else:
            wellselection = wellselection
    elif isinstance(wellselection, str):
        wellselection = [wellselection]
    
    if multiwellrows is None:
        multiwellrows = 0
    if multiwellcols is None:
        multiwellcols = 0
    if conversionrescalemultiplier is None:
        conversionrescalemultiplier = 0

    yaml_dict = {
        "imaging_mode": [imagingmode],
        "file_structure": [filestructure],
        "multi-well-rows": int(multiwellrows),
        "multi-well-cols": int(multiwellcols),
        "multi-well-detection": [multiwelldetection],
        "species": [species],
        "stages": [stages],
        "modules": {
            "motility": {"run": eval_bool(motilityrun)},
            "convert": {
                "run": eval_bool(conversionrun),
                "save_video": conversionscalevideo,
                "rescale_multiplier": float(conversionrescalemultiplier)
            },
            "segment": {
                "run": eval_bool(segmentrun),
                "wavelength": [wavelength]
            },
            "cellprofiler": {
                "run": eval_bool(cellprofilerrun),
                "pipeline": [cellprofilerpipeline]
            },
            "dx": {
                "run": eval_bool(diagnosticdx)
            }
        },
        "wells": wellselection,
        "directories": {
            "work": ['/work'],
            "input": ['/input'],
            "output": ['/output']
        }
    }

    return yaml_dict
