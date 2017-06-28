import sys
import pytest
import mock_visa
sys.modules['visa'] = mock_visa

import visa_plug


# Test visa_plug.find_device() function ========================================
def test_it_returns_a_iterable():
    import collections
    assert isinstance(visa_plug.VisaPlug.find_device(), collections.Iterable)


def test_it_returns_all_available_devices_if_no_parameter_is_given():
    assert len(list(visa_plug.VisaPlug.find_device())) == 20


def test_it_finds_the_device_by_serial():
    assert len(list(visa_plug.VisaPlug.find_device("serial_number02"))) == 1


def test_it_finds_the_device_by_vendor():
    assert len(list(visa_plug.VisaPlug.find_device("vendor"))) == 20


# Test VisaPlug constructor ====================================================
@pytest.fixture
def visa_device():
    return visa_plug.VisaPlug(ident_code="serial_number02")


def test_it_raise_a_exception_if_no_device_was_found():
    with pytest.raises(visa_plug.VisaDeviceException):
        visa_plug.VisaPlug(ident_code="wrong_string")


def test_it_build_up_a_connection_selected_by_serial_number(visa_device):
    visa_device = visa_plug.VisaPlug(ident_code="serial_number01")
    assert visa_device.connection is not None


def test_it_build_up_a_connection_selected_by_vendor():
    visa_device = visa_plug.VisaPlug(ident_code="vendor")
    assert visa_device.connection is not None


def test_it_has_the_vendor_set(visa_device):
    assert visa_device.vendor == "vendor"


def test_it_has_the_serial_number_set(visa_device):
    assert visa_device.serial_number == "serial_number02"


def test_it_has_the_firmware_version_set(visa_device):
    assert visa_device.firmware_version == "firmware_version"


# Test VisaPlug.tearDown() =====================================================
def test_it_teardown_the_connection(visa_device):
    visa_device.tearDown()
    assert visa_device.connection is None


# Test VisaPlug.write() ========================================================
def test_it_writes_to_a_visa_device(visa_device):
    visa_device.write("TESTDATA")
    assert visa_device.connection._instrument_buffer == "TESTDATA\n"


def test_it_writes_multiple_times_to_a_visa_device(visa_device):
    for i in range(10):
        visa_device.write("TESTDATA")
    assert visa_device.connection._instrument_buffer == "TESTDATA\n"*10


# Test VisaPlug.query() ========================================================
def test_it_get_data_from_visa_device_on_a_query(visa_device):
    assert visa_device.query("*IDN?") == "vendor,device_name,serial_number02,firmware_version\n"


# Test VisaPlug.read() =========================================================
def test_it_gets_data_after_writing_and_reading_from_visa_device(visa_device):
    visa_device.write("FORMAT:ELEMENTS?")
    assert visa_device.read() == "volt, curr\n"


def test_it_gets_data_after_multiple_writings_and_reading_visa_device(visa_device):
    for i in range(10):
        visa_device.write("FORMAT:ELEMENTS?")
    assert visa_device.read() == "volt, curr\n"


def test_it_gets_the_idn_string(visa_device):
    assert visa_device.get_identification() == "vendor,device_name,serial_number02,firmware_version\n"


def test_it_sends_a_reset(visa_device):
    visa_device.reset()
    assert visa_device.connection._instrument_buffer == "*RST\n"


def test_it_sends_a_clear_status_command(visa_device):
    visa_device.clear_status_command()
    assert visa_device.connection._instrument_buffer == "*CLS\n"


def test_it_sends_a_wait_to_continue_command(visa_device):
    visa_device.wait_to_continue()
    assert visa_device.connection._instrument_buffer == "*WAI\n"


def test_it_querys_the_event_status_register(visa_device):
    assert visa_device.get_event_status_register() == "event_status_register"


def test_it_sends_a_self_test_command(visa_device):
    assert visa_device.self_test() == "self_test"


def test_it_gets_the_status_byte(visa_device):
    assert visa_device.get_status_byte() == "status_byte"


def test_it_gets_the_event_status_enabled_bit(visa_device):
    assert visa_device.is_event_status_enabled() == "is_enabled"


def test_it_enable_the_event_status(visa_device):
    visa_device.enable_event_status()
    assert visa_device.connection._instrument_buffer == "*ESE\n"


def test_it_gets_the_operation_complete_command(visa_device):
    assert visa_device.get_operation_complete() == "operation_complete"


def test_it_enable_the_event_status(visa_device):
    visa_device.set_operation_complete()
    assert visa_device.connection._instrument_buffer == "*OPC\n"


def test_it_gets_service_request_enabled(visa_device):
    assert visa_device.get_service_request_enabled() == "service_request"


def test_enable_service_request(visa_device):
    visa_device.enable_service_request()
    assert visa_device.connection._instrument_buffer == "*SRE\n"