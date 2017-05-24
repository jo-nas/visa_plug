import math


class ResourceManager:
    def __init__(self):
        self.resources = {}
        for i in range(20):
            self.resources.update({"GPIB0::{:02d}::INSTR".format(i): i})

    def list_resources(self):
        return self.resources.keys()

    def open_resource(self, address_str):
        return Instrument(address_str, self.resources[address_str])


class Instrument:
    def __init__(self, address_str, serial_number):
        self._address_str = address_str
        self._instrument_buffer = None
        self._write_count = 0
        self.supported_messages = {
            "idn": 0,
            "cls": 0,
            "rst": 0,
            "wai": 0,
            "esr": 0,
            "tst": 0,
            "stb": 0,
            "ese": 0,
            "opc": 0,
            "sre": 0
        }

    def close(self):
        return "closed"

    def query(self, query_string):
        if "?" in query_string:
            return self.supported_messages[query_string.replace("*", "").replace("?", "")]

    def write(self, write_string):
        if "?" in write_string:
            self._instrument_buffer = write_string
        self.supported_messages[write_string.replace("*", "").replace("?", "")] += 1

    def read(self):
        if "?" in self._instrument_buffer:
            self._instrument_buffer = None
            return self.supported_messages[self._instrument_buffer.replace("*", "").replace("?", "")]
        else:
            return None

