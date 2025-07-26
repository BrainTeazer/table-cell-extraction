# Table Extraction

This is a project for extracting cells from images of tables based on [this](https://towardsdatascience.com/a-table-detection-cell-recognition-and-text-extraction-algorithm-to-convert-tables-to-excel-files-902edcf289ec?gi=b77a4167d5c1) article.

## Running the Progam

### Setup

```shell
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# After completion
deactivate
```

### Run

Make sure you are in the parent directory.

```shell
python extract_cells.py [tables_dir] [results_dir]
```

By default, `tables_dir` is "./tables" and `results_dir` is "./results".
If any code is changed it is best to delete `results_dir` before re-running the program.

## File Structure

`lib/` -> contains all neccessary functions for extracting cells

`lib/helper.py` -> contains methods to display image (with and without contours)

`lib/kernel.py` -> contains methods related to creating structuring elements (kernels)

`lib/image_processing.py` -> contains methods for processing images (e.g., threshold, finding contours)

`lib/table_contour.py` -> file that separates logic for getting the corners of the table

`lib/get_cells.py` -> file contains the logic for extracting the cells by using the other files in `lib/`
