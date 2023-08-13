import csv
import logging
from sch_doc_parser.src.data_extractor import ComponentData


class ResultWriter:
    def __init__(self, bom_components: list[ComponentData]):
        self.bom_components = bom_components

    def spawn_report(self, report_name):
        logging.info('Start write down result file')
        with open(report_name, 'w', encoding='utf-8') as result:
            writer = csv.writer(result)
            writer.writerow(['Part number', 'Comment', 'Footprint', "Description", "Manufacturer", "Qty"])
            for component in self.bom_components:
                pn = component.part_number if component.part_number else ''
                comment = component.comment if component.part_number else ''
                description = component.description if component.part_number else ''
                part_count = component.part_count
                manufacturer = component.manufacturer
                footprint = component.footprint
                writer.writerow([pn, comment, footprint, description, manufacturer, part_count])
        logging.info('Result file generated')
