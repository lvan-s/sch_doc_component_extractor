import logging

import olefile
from sch_doc_parser.src.python_schdoc import records as types
from sch_doc_parser.src.python_schdoc.schdoc import DataStreamer


class SchematicLib:
    def __init__(self, path: str):
        self.part_number = None
        self.path = path
        self.records = []
        self.name = path.split("/")[-1].upper()
        self.raw_header = None
        self.raw_data = None

    def __str__(self) -> str:
        return f"SchematicLib<{self.name}>"

    def __repr__(self) -> str:
        return f"SchematicLib<{self.name}>"

    @staticmethod
    def check_header(header: str) -> bool:
        return (
            "Protel for Windows - Schematic Library Editor Binary File Version 5.0" in header
        )

    def read(self):
        with open(self.path, 'rb') as datastream:
            ole = olefile.OleFileIO(datastream)
            self.raw_header = ole.openstream('FileHeader').read()

            raw_data_stream_name = self.get_data_datastream_name(ole)
            self.raw_data = ole.openstream(raw_data_stream_name).read()
            unparsed_records = self.read_records(self.raw_data)

            for ur in unparsed_records:
                self.records.append(self.parse_record(ur))
            return self

    def get_data_datastream_name(self, ole):
        stream_names = ole.listdir()
        for stream in stream_names:
            if 'Data' in stream:
                self.part_number = stream[0]
                return stream

    def read_records(self, data):
        blocks = []
        streamer = DataStreamer(data)
        while not streamer.eof():
            try:
                payload_size = streamer.read_int(2)
                pad = streamer.read_int(1)
                typ = streamer.read_int(1)
                payload = streamer.read(payload_size)
                assert pad == 0, "Bad pad in header"
                assert typ == 0, "Bad type in header"
                assert payload[-1] == 0, "Invalid ending byte"
                blocks.append(payload[:-1].decode("latin1"))
            except AssertionError as exp:
                logging.warning(exp)

        if self.check_header(blocks[0]):
            return blocks[1:]
        return blocks

    @staticmethod
    def parse_record(data):
        record_id = None
        parameters = {}
        for field in data.split("|"):
            if field:
                (name, value) = field.split("=", 1)
                if name == "RECORD":
                    record_id = int(value)
                parameters[name] = value
        if not record_id:
            logging.error(data)
        if not record_id in types.RECORD_MAP:
            logging.warning(f'Record with ${record_id} not supported')
        else:
            return types.RECORD_MAP[record_id](parameters)
