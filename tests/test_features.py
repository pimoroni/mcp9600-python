from i2cdevice import MockSMBus


def test_get_hot_junction_temperature():
    # Test the junction read and conversion formula
    import mcp9600
    smbus = MockSMBus(1, default_registers={
        0x00: 1,
        0x01: 96,
        0x20: 0x40})
    device = mcp9600.MCP9600(i2c_dev=smbus)
    assert round(device.get_hot_junction_temperature(), 1) == 22.0


def test_get_temperature_delta():
    import mcp9600
    smbus = MockSMBus(1, default_registers={
        0x01: 1,
        0x02: 96,
        0x20: 0x40})
    device = mcp9600.MCP9600(i2c_dev=smbus)
    assert round(device.get_temperature_delta(), 1) == 22.0


def test_get_cold_junction_temperature():
    import mcp9600
    smbus = MockSMBus(1, default_registers={
        0x02: 1,
        0x03: 96,
        0x20: 0x40})
    device = mcp9600.MCP9600(i2c_dev=smbus)
    assert round(device.get_cold_junction_temperature(), 1) == 22.0


def test_alert_flags():
    import mcp9600
    smbus = MockSMBus(1, default_registers={
        0x04: 0b00000101,
        0x20: 0x40})
    device = mcp9600.MCP9600(i2c_dev=smbus)
    assert device.check_alerts() == (1, 0, 1, 0)


def test_alert_configure():
    import mcp9600
    smbus = MockSMBus(1, default_registers={
        0x04: 0b00000101,
        0x20: 0x40})
    device = mcp9600.MCP9600(i2c_dev=smbus)

    device.configure_alert(1,
                           limit=25.25,  # Test to 1/4th degree precision
                           hysteresis=0x99,
                           clear_interrupt=True,
                           monitor_junction=0,
                           rise_fall=1,
                           state=1,
                           mode=1,
                           enable=True)

    assert smbus.regs[0x10:0x12] == [1, 148]
    assert smbus.regs[0x0C] == 0x99
    assert device.get_alert_hysteresis(1) == 0x99
    assert device.get_alert_limit(1) == 25.25


def test_alert_clear():
    import mcp9600
    smbus = MockSMBus(1, default_registers={
        0x04: 0b00000101,
        0x20: 0x40})
    device = mcp9600.MCP9600(i2c_dev=smbus)

    device.clear_alert(1)

    assert smbus.regs[0x08] & 0b10000000 == 0b10000000


def test_set_thermocouple_type():
    import mcp9600
    smbus = MockSMBus(1, default_registers={
        0x04: 0b00000101,
        0x05: 0b00000000,
        0x20: 0x40})
    device = mcp9600.MCP9600(i2c_dev=smbus)

    device.set_thermocouple_type('N')

    assert (smbus.regs[0x05] >> 4) & 0b111 == 0b011


def test_get_thermocouple_type():
    import mcp9600
    smbus = MockSMBus(1, default_registers={
        0x04: 0b00000101,
        0x05: 0b00110000,
        0x20: 0x40})
    device = mcp9600.MCP9600(i2c_dev=smbus)

    assert device.get_thermocouple_type() == 'N'
