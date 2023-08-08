import glob
import logging
import csv
from src.python_schdoc.schdoc import Schematic
from src.data_extractor import ComponentExtractor


def get_schdoc_files_path():
    test_files = [file for file in glob.iglob(r'.\sch_doc_test_files\*.SchDoc', recursive=True, include_hidden=True)]
    return test_files


def sort_components(bom_components, file_components):
    if not bom_components:
        bom_components = file_components
    else:
        for file_component in file_components:
            for bom_component in bom_components:
                if file_component.libref == bom_component.libref:
                    for file_des in file_component.designator:
                        if file_des not in bom_component.designator:
                            bom_component.designator.append(file_des)
                            bom_component.part_count += 1
                    break
            else:
                bom_components.append(file_component)
    return bom_components, file_components


if __name__ == "__main__":
    schdoc_files = get_schdoc_files_path()
    bom_components = []
    for schdoc_file in schdoc_files:
        schdoc = Schematic(schdoc_file).read()
        file_components = ComponentExtractor(schdoc).components
        bom_components, file_components = sort_components(bom_components, file_components)
        logging.info(f"Finished parsing in ${schdoc_file}")

    with open("result.csv", 'w', encoding='utf-8') as result:
        writer = csv.writer(result)
        writer.writerow(['PartNumber', 'Comment', "Description", "PartCount", "Designator"])
        for component in bom_components:
            pn = component.properties.get('PartNumber', '')
            comment = component.properties.get('Comment', '')
            description = component.description if hasattr(component, 'description') else ''
            part_count = component.part_count
            designator = component.designator
            writer.writerow([pn, comment, description, part_count, designator])
