from i2cdevice import MockSMBus
import pytest


def test_setup():
    # Test that library setup succeeds with correct CHIP ID
    import mcp9600
    device = mcp9600.MCP9600(i2c_dev=MockSMBus(1, default_registers={0x20: 0x40}))
    del device


def test_setup_wrong_device():
    # Test that reading the wrong CHIP ID throws a RuntimeError
    import mcp9600
    with pytest.raises(RuntimeError):
        device = mcp9600.MCP9600(i2c_dev=MockSMBus(1, default_registers={0x20: 0x99}))
        del device


def test_setup_no_device():
    class MockSMBusIOError(MockSMBus):
        def read_i2c_block_data(self, i2c_address, register, length):
            raise IOError("Simulated IOError")

    import mcp9600
    with pytest.raises(RuntimeError):
        device = mcp9600.MCP9600(i2c_dev=MockSMBusIOError(1, default_registers={0x20: 0x99}))
        del device


def test_legacy_setup():
    # Test a stub setup function exists despite it being depricated
    import mcp9600
    device = mcp9600.MCP9600(i2c_dev=MockSMBus(1, default_registers={0x20: 0x40}))
    device.setup()
