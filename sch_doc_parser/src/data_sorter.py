import logging
import glob
from sch_doc_parser.src.python_schdoc.schdoc import Schematic
from sch_doc_parser.src.data_extractor import ComponentExtractor


class ComponentSorter:
    def __init__(self, project_path):
        self.project_path = project_path

    def extract_sorted_components(self):
        schdoc_files = self.get_schdoc_files_path()
        bom_components = []
        file_components = None
        for schdoc_file in schdoc_files:
            schdoc = Schematic(schdoc_file).read()
            file_components = ComponentExtractor(schdoc).components
            bom_components, file_components = self.sort_components(bom_components, file_components)
            logging.info(f"Finished parsing in ${schdoc_file}")
        return bom_components, file_components

    def get_schdoc_files_path(self):
        test_files = [file for file in glob.glob(f'{self.project_path}/**/*.SchDoc', recursive=True)]
        return test_files

    @staticmethod
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
