import argparse
from sch_doc_parser.src.data_sorter import ComponentSorter
from sch_doc_parser.src.result_writer import ResultWriter


parser = argparse.ArgumentParser(description="Allows to parse Altium Designer .SchDoc files to extract component info",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-p", "--path", default="sch_doc_test_files",
                    help="Path to directory with .SchDoc files (relative is valid)")
parser.add_argument("-r", "--report", default="result.csv",
                    help="""Path include name with .csv where you would like to generate result with 
                    components (relative is valid)""")
parser.add_argument("-d", "--delimiter", default=',',
                    help="""Delimiter uses for a generated result file""")


if __name__ == "__main__":
    args = vars(parser.parse_args())
    project_path = args['path']
    report_name = args['report']
    delimiter = args['delimiter']
    sorter = ComponentSorter(project_path)
    bom_components, file_components = sorter.extract_sorted_components()

    res_writer = ResultWriter(bom_components)
    res_writer.spawn_report(report_name, delimiter)
