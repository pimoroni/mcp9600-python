import sys
import mock
import pytest
from i2cdevice import MockSMBus

class MockSMBusWorking(MockSMBus):
    def __init__(self, bus):
        MockSMBus.__init__(self, bus)
        self.regs[0x00] = 0x01


def test_setup():
    sys.modules['smbus'] = mock.Mock()
    import mcp9600
    device = mcp9600.MCP9600()
    del device


def test_read_thermocouple_timeout():
    sys.modules['smbus'] = mock.Mock()
    sys.modules['smbus'].SMBus = MockSMBus
    import mcp9600
    device = mcp9600.MCP9600(read_timeout=0.1)
    with pytest.raises(RuntimeError):
        device.get_hot_junction_temperature()


def test_read_thermocouple():
    sys.modules['smbus'] = mock.Mock()
    sys.modules['smbus'].SMBus = MockSMBusWorking
    import mcp9600
    device = mcp9600.MCP9600()
    device.get_hot_junction_temperature()
