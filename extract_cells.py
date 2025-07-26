import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List
from lib.image_processing import *
from lib.get_cells import *
import cv2
from tqdm.auto import tqdm


@dataclass
class BoxAnnotation:
    x: int  # upper left corner x (absolute)
    y: int  # upper left corner y (absolute)
    width: int  # box width (absolute)
    height: int  # box height (absolute)
    class_name: str  # identifier for row and column starting at 0 (format: f"cell-{row}-{col}")




class TableAnalysis:

    config = {
        "minCellHeight": 15,
        "minCellWidth": 100,
        # config parameters
    }

    # process each image (i.e. list of box annotations)
    def process(self, filepath: Path) -> List[BoxAnnotation]:

        box_annotations: List[BoxAnnotation] = []
        
        img =  get_img(str(filepath))

        annotations = get_cell_images(img, self.config)

        for annotation in annotations:
            box_annotations.append(BoxAnnotation(*annotation))
       
        return box_annotations

    # output/write the results in a directory
    def write_results(self, box_annotations: List[BoxAnnotation], filepath: Path, output_dir: Path):
        # create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        image = cv2.imread(str(filepath), cv2.IMREAD_COLOR)
        
        image_height: int
        image_width: int
        image_height, image_width, *_ = image.shape

        for annotation in box_annotations:            
            x1 = max(0, annotation.x)
            y1 = max(0, annotation.y)
            x2 = min(image_width, x1 + annotation.width)
            y2 = min(image_height, y1 + annotation.height)
            cell = image[y1:y2, x1:x2, ...]
            cv2.imwrite(f"{output_dir/annotation.class_name}.png", cell)

def main(table_dir: str, result_dir: str):
    table_analysis = TableAnalysis()

    tables = list(Path(table_dir).glob("*.png"))

    filepath: Path
    for filepath in tqdm(tables, desc="Processing Tables", unit="tables"):
        box_annotations = table_analysis.process(filepath)
        output_dir = Path(result_dir, filepath.stem)
        table_analysis.write_results(box_annotations, filepath, output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("table_dir", type=str, nargs="?", default="./tables")
    parser.add_argument("result_dir", type=str, nargs="?", default="./results")
    args = parser.parse_args()
    main(table_dir=args.table_dir, result_dir=args.result_dir)
