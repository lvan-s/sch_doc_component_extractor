from src.python_schdoc.schdoc import Schematic
from src.python_schdoc import records as types


class ComponentExtractor:
    def __init__(self, schdoc: Schematic):
        self.records = schdoc.records
        self.components = self.extract_components()

    def extract_components(self):
        components_raw_data = []
        component_data = None
        for record in self.records:
            if isinstance(record, types.ComponentRecord):
                if component_data:
                    component_data.parse_related_records()
                    components_raw_data, component_data = self.add_component_if_uniq(components_raw_data, component_data)
                current_libref = record.library_reference
                description = record.description
                part_count = 1
                component_data = ComponentData(current_libref, description, part_count)
            elif isinstance(record, types.ParameterRecord):
                if component_data and hasattr(record, 'name') and record.name != 'PinUniqueId':
                    # We don't need the pin records
                    if all(record.name != rec.name for rec in component_data.related_records):
                        component_data.related_records.append(record)
            elif isinstance(record, types.DesignatorRecord):
                if any(record.text == rec.text for rec in component_data.related_records):
                    raise Exception(f'There are two designator records in the component: ${component_data}')
                else:
                    if not hasattr(record, 'name'):
                        record.name = 'Designator_RECORD_34'
                    component_data.related_records.append(record)
                    component_data.designator = [record.text]
        if component_data:
            component_data.parse_related_records()
            components_raw_data, component_data = self.add_component_if_uniq(components_raw_data, component_data)
        return components_raw_data

    @staticmethod
    def add_component_if_uniq(components_raw_data, component_data):
        if components_raw_data:
            for comp in components_raw_data:
                if component_data.libref == comp.libref:
                    if isinstance(comp.designator, list):
                        for design in comp.designator:
                            if component_data.designator == design:
                                break
                        else:
                            new_designator = component_data.designator
                            comp.designator.extend(new_designator)
                            comp.part_count += component_data.part_count
                            break
                    else:
                        raise Exception(f'Uncorect type of designation: ${comp}')
            else:
                components_raw_data.append(component_data)
        else:
            components_raw_data.append(component_data)
        return components_raw_data, None


class ComponentData:
    def __init__(self, libref, description, part_count):
        self.libref = libref
        self.description = description
        self.part_count = part_count
        self.related_records = []
        self.properties = {}

    def parse_related_records(self):
        for record in self.related_records:
            self.properties[record.name] = record.text
        return self
