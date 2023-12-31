import logging
import glob
from sch_doc_parser.src.python_schdoc.schdoc import Schematic
from sch_doc_parser.src.python_schlib.schlib import SchematicLib
from sch_doc_parser.src.data_extractor import SchematicComponentExtractor, SchematicLibComponentExtractor, ComponentData


class ComponentSorter:
    def __init__(self, project_path):
        self.project_path = project_path

    def extract_sorted_components(self):
        schdoc_files = self.get_schdoc_files_path()
        schlib_files = self.get_schlib_files_path()
        file_components = []
        lib_components = []
        for schdoc_file in schdoc_files:
            schdoc = Schematic(schdoc_file).read()
            file_components.extend(SchematicComponentExtractor(schdoc).components)
            logging.info(f'Finish extract component from {schdoc_file.rsplit("/", 1)[-1]}')
        for schlib_file in schlib_files:
            schlib = SchematicLib(schlib_file).read()
            lib_components.append(SchematicLibComponentExtractor(schlib).get_component())
        logging.info('Components extraction completed. Start component sorting...')
        bom_components = self.sort_components(file_components)
        for bom_component in bom_components:
            if not bom_component.part_number:
                for lib_component in lib_components:
                    if lib_component.libref == bom_component.libref:
                        bom_component.part_number = lib_component.part_number
                        bom_component.manufacturer = lib_component.manufacturer if not bom_component.manufacturer else\
                            bom_component.manufacturer
                        bom_component.description = lib_component.description if not bom_component.description else\
                            bom_component.description
        logging.info('Finish component sorting')
        return bom_components, file_components

    def get_schdoc_files_path(self):
        files = [file for file in glob.glob(f'{self.project_path}/**/*.SchDoc', recursive=True)]
        return files

    def get_schlib_files_path(self):
        files = [file for file in glob.glob(f'{self.project_path}/**/*.SchLib', recursive=True)]
        return files

    def sort_components(self, file_components: list[ComponentData]):
        bom_components = [file_components.pop(0)]
        for file_component in file_components:
            if file_component.part_number:
                for bom_component in bom_components:
                    if bom_component.part_number and bom_component.part_number == file_component.part_number:
                        self.check_designators(bom_component, file_component)
                        break
                else:
                    bom_components.append(file_component)
            elif file_component.comment:
                for bom_component in bom_components:
                    if bom_component.comment and bom_component.comment == file_component.comment:
                        self.check_designators(bom_component, file_component)
                        break
                else:
                    bom_components.append(file_component)
            elif file_component.footprint:
                for bom_component in bom_components:
                    if bom_component.footprint and bom_component.footprint == file_component.footprint:
                        self.check_designators(bom_component, file_component)
                        break
                else:
                    bom_components.append(file_component)
        return bom_components

    @staticmethod
    def check_designators(bom_component, file_component):
        if isinstance(bom_component.designator, str):
            if bom_component.designator != file_component.designator:
                bom_designator = bom_component.designator
                file_designator = file_component.designator
                bom_component.designator = [bom_designator, file_designator]
                bom_component.part_count = 2
                for key, value in file_component.properties.items():
                    if key not in bom_component.properties:
                        bom_component.properties.update({key: value})
        elif isinstance(bom_component.designator, list):
            for bom_designator in bom_component.designator:
                if bom_designator == file_component.designator:
                    break
            else:
                bom_component.designator.append(file_component.designator)
                for key, value in file_component.properties.items():
                    if key not in bom_component.properties:
                        bom_component.properties.update({key: value})
                bom_component.part_count += 1
        else:
            logging.error(f'Component does not have designator!!! {bom_component}')
