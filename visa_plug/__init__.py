# -*- coding: utf-8 -*-
import visa
import openhtf.plugs as plugs

__author__ = 'Jonas Steinkamp'
__email__ = 'jonas@steinka.mp'
__version__ = '0.1.0'


class VisaDeviceException(Exception):
    """A basic Visa Device Exception"""


class VisaPlug(plugs.BasePlug):
    def __init__(self, ident_code, **resource_kwargs):
        self.rm = visa.ResourceManager()

        device = self.find_device(ident_code, **resource_kwargs).next()

        self.connection = self.rm.open_resource(device["port"], **resource_kwargs)
        self.vendor = device["vendor"]
        self.device_name = device["device_name"]
        self.serial_number = device["serial_number"]
        self.firmware_version = device["firmware_version"]

    def tearDown(self):
        self.connection.close()
        self.connection = None

    def write(self, data):
        self.connection.write(data)

    def query(self, data):
        return self.connection.query(data)

    def read(self):
        return self.connection.read()

    # ------------------------------------------------------------------------------------------------------------------
    # identification
    # ------------------------------------------------------------------------------------------------------------------
    def idn(self):
        return self.query('*IDN?')

    def get_identification(self):
        return self.idn()

    # ------------------------------------------------------------------------------------------------------------------
    # clear status command
    # ------------------------------------------------------------------------------------------------------------------
    def cls(self):
        self.write("*CLS")

    def clear_status_command(self):
        self.cls()

    # ------------------------------------------------------------------------------------------------------------------
    # reset command
    # ------------------------------------------------------------------------------------------------------------------
    def rst(self):
        self.write("*RST")

    def reset(self):
        self.rst()

    # ------------------------------------------------------------------------------------------------------------------
    # wait to continue
    # ------------------------------------------------------------------------------------------------------------------
    def wai(self):
        self.write("*WAI")

    def wait_to_continue(self):
        self.wai()

    # ------------------------------------------------------------------------------------------------------------------
    # event status register
    # ------------------------------------------------------------------------------------------------------------------
    def esr(self):
        return self.query("*ESR?")

    def get_event_status_register(self):
        return self.esr()

    # ------------------------------------------------------------------------------------------------------------------
    # get identification
    # ------------------------------------------------------------------------------------------------------------------
    def tst(self):
        return self.query("*TST?")

    def self_test(self):
        return self.tst()

    # ------------------------------------------------------------------------------------------------------------------
    # status byte
    # ------------------------------------------------------------------------------------------------------------------
    def stb(self):
        return self.query("*STB?")

    def get_status_byte(self):
        self.stb()

    # ------------------------------------------------------------------------------------------------------------------
    # event status
    # ------------------------------------------------------------------------------------------------------------------
    def ese(self, get=False):
        if get:
            return self.query("*ESE?")
        self.write("*ESE")

    def enable_event_status(self):
        self.ese()

    def is_event_status_enabled(self):
        return self.ese(True)

    # ------------------------------------------------------------------------------------------------------------------
    # operation complete command
    # ------------------------------------------------------------------------------------------------------------------
    def opc(self, get=False):
        if get:
            return self.query("*OPC?")
        self.write("*OPC")

    def set_operation_complete_command(self):
        self.opc()

    def get_operation_complete(self):
        return self.opc(True)

    # ------------------------------------------------------------------------------------------------------------------
    # service request command
    # ------------------------------------------------------------------------------------------------------------------
    def sre(self, get=False):
        if get:
            return self.query("*SRE?")
        self.write("*SRE")

    def get_service_request_enabled(self):
        return self.sre(True)

    def enable_service_request(self):
        self.sre()

    @staticmethod
    def find_device(ident_code="", **resource_kwargs):
        rm = visa.ResourceManager()

        for port in rm.list_resources():
            try:
                idn = rm.open_resource(port, kwargs=resource_kwargs).query("*IDN?").split(",")

                # device sends no serial number
                if len(idn) <= 3:
                    idn[3], idn[2] = idn[2], ""

                if any(ident_code in s for s in idn):
                    yield {
                        'vendor': idn[0],
                        'device_name': idn[1],
                        'serial_number': idn[2],
                        'firmware_version': idn[3],
                        'port': port
                    }

            except:
                continue
        else:
            raise VisaDeviceException("Device can't be found.")
