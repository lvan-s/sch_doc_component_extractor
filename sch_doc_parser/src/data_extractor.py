import logging

from sch_doc_parser.src.python_schdoc.schdoc import Schematic
from sch_doc_parser.src.python_schdoc import records as types


class ComponentExtractor:
    def __init__(self, schdoc: Schematic):
        self.records = schdoc.records
        self.components = self.extract_components()

    def extract_components(self):
        components = []
        component_record = None
        for record in self.records:
            if isinstance(record, types.ComponentRecord):
                if component_record:
                    component_record = ComponentData(component_record).parse_related_records()
                    if 'PartNumber' in component_record.properties:
                        component_record.part_number = component_record.properties['PartNumber']
                    if 'Comment' in component_record.properties:
                        component_record.comment = component_record.properties['Comment']
                    if 'Manufacturer' in component_record.properties:
                        component_record.manufacturer = component_record.properties['Manufacturer']
                    components.append(component_record)
                component_record = {
                    'libref': record.library_reference,
                    'footprint': None,
                    'related_records': []
                }
                if hasattr(record, 'description'):
                    component_record['description'] = record.description
                if hasattr(record, 'design_item_id'):
                    component_record['design_item_id'] = record.design_item_id
            elif component_record:
                # Pin records does not have value
                if isinstance(record, types.DesignatorRecord) or isinstance(record, types.ParameterRecord)\
                        and ((record.name and record.name != 'PinUniqueId') or record.text):
                    component_record['related_records'].append(record)
                if isinstance(record, types.ImplementationRecord):
                    component_record['footprint'] = record.modelname
        else:
            if component_record:
                component_record = ComponentData(component_record).parse_related_records()
                components.append(component_record)
        return components


class ComponentData:
    def __init__(self, component_record):
        self.libref = component_record['libref']
        if 'description' in component_record:
            self.description = component_record['description']
        if 'design_item_id' in component_record:
            self.design_item_id = component_record['design_item_id']
        self.related_records = component_record['related_records']
        self.footprint = component_record['footprint']
        self.part_count = 1
        self.properties = {}
        self.part_number = None
        self.designator = None
        self.comment = None
        self.manufacturer = None

    def parse_related_records(self):
        for record in self.related_records:
            if isinstance(record, types.DesignatorRecord):
                if self.designator:
                    logging.error(f'There are two designator in the one component!!! Component: {self}')
                self.designator = record.text
            elif hasattr(record, 'name') and record.name:
                self.properties[record.name] = record.text
            elif hasattr(record, 'text') and record.text:
                self.properties[record.text] = None
        return self
