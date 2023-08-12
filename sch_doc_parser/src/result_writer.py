import csv


class ResultWriter:
    def __init__(self, bom_components):
        self.bom_components = bom_components

    def spawn_report(self, report_name):
        with open(report_name, 'w', encoding='utf-8') as result:
            writer = csv.writer(result)
            writer.writerow(['PartNumber', 'Comment', "Description", "PartCount", "Designator"])
            for component in self.bom_components:
                pn = component.properties.get('PartNumber', '')
                comment = component.properties.get('Comment', '')
                description = component.description if hasattr(component, 'description') else ''
                part_count = component.part_count
                designator = component.designator
                writer.writerow([pn, comment, description, part_count, designator])
