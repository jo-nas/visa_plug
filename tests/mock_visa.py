class ResourceManager:
    def __init__(self, backend):
        self.resources = {}
        for i in range(20):
            self.resources.update({"GPIB0::{:02d}::INSTR".format(i): i})#

        self.resources.update({"GPIB0::42::INSTR": 42})  # sends only vendor, device_name, firmware_version on idn
        self.resources.update({"GPIB0::43::INSTR": 43})  # throws a exception on init

    def list_resources(self):
        return self.resources.keys()

    def open_resource(self, address_str, timeout):
        return Instrument(address_str, self.resources[address_str])


class Instrument:
    def __init__(self, address_str, serial_number):
        self._address_str = address_str
        self._instrument_buffer = ""
        self._write_count = 0
        self.supported_messages = {
            "idn": "vendor,device_name,serial_number{:02d},firmware_version\n".format(serial_number),
            "cls": 0,
            "rst": 0,
            "wai": 0,
            "esr": "event_status_register",
            "tst": "self_test",
            "stb": "status_byte",
            "ese": "is_enabled",
            "opc": "operation_complete",
            "sre": "service_request",
            "format:elements": "volt, curr\n"
        }

        if serial_number == 42:
            self.supported_messages["idn"] = "vendor,device_name,firmware_version\n"

        if serial_number == 43:
            raise Exception

    def close(self):
        return "closed"

    def query(self, query_string):
        if "?" in query_string:
            return self.supported_messages[query_string.replace("*", "").replace("?", "").lower()]
        return None

    def write(self, write_string):
        self._instrument_buffer += write_string+"\n"

    def read(self):
        last_message = self._instrument_buffer.split("\n")[-2]
        if "?" in last_message:
            return_value = self.supported_messages[last_message.replace("*", "").replace("?", "").lower()]
            self._instrument_buffer = ""
            return return_value
        return None

