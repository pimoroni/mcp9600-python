"""MCP9600 Driver."""
from i2cdevice import Device, Register, BitField, _int_to_bytes
from i2cdevice.adapter import LookupAdapter, Adapter
import struct

CHIP_ID = 0x40
I2C_ADDRESS_DEFAULT = 0x66
I2C_ADDRESS_ALTERNATE = 0x67

class RevisionAdapter(Adapter):
   def _decode(self, value):
        major = (value & 0xF0) >> 4 
        minor = (value * 0x0F)
        return major + (minor / 10.0)

class S16Adapter(Adapter):
    """Convert unsigned 16bit integer to signed."""

    def _decode(self, value):
        return struct.unpack('<h', _int_to_bytes(value, 2))[0]

    def _encode(self, value):
        return bytes(struct.pack('<h', value))


class U16Adapter(Adapter):
    """Convert from bytes to an unsigned 16bit integer."""

    def _decode(self, value):
        return struct.unpack('<H', _int_to_bytes(value, 2))[0]


class MCP9600:
    def __init__(self, i2c_addr=I2C_ADDRESS_DEFAULT, i2c_dev=None):
        self._is_setup = False
        self._i2c_addr = i2c_addr
        self._i2c_dev = i2c_dev
        self._mcp9600 = Device([I2C_ADDRESS_DEFAULT, I2C_ADDRESS_ALTERNATE], i2c_dev=self._i2c_dev, bit_width=8, registers=(
            Register('TEMPERATURE', 0x00, fields=(
                BitField('hot_junction', 0xFFFF, adapter=S16Adapter()),
                BitField('delta', 0xFFFF, adapter=S16Adapter()),
                BitField('cold_junction', 0xFFFF, adapter=S16Adapter())
            ), bit_width=48),
            Register('RAW_DATA', 0x03, fields=(
                BitField('adc', 0xFFFFFF),
            ), bit_width=24),
            Register('STATUS', 0x04, fields=(
                BitField('burst_complete', 0b10000000),
                BitField('updated', 0b01000000),
                BitField('input_range', 0b00010000),
                BitField('alert_4', 0b00001000),
                BitField('alert_3', 0b00000100),
                BitField('alert_2', 0b00000010),
                BitField('alert_1', 0b00000001)
            )),
            Register('THERMOCOUPLE_CONFIG', 0x05, fields=(
                BitField('type_select', 0b01110000),
                BitField('filter_coefficients', 0b00000111)
            )),
            Register('DEVICE_CONFIG', 0x06, fields=(
                BitField('cold_junction_resolution', 0b10000000),
                BitField('adc_resolution', 0b01100000),
                BitField('burst_mode_samples', 0b00011100),
                BitField('shutdown_modes', 0b00000011)
            )),
            Register('ALERT1_CONFIG', 0x08, fields=(
                BitField('clear_interrupt', 0b10000000),
                BitField('monitor_junction', 0b00010000),  # 1 Cold Junction, 0 Thermocouple
                BitField('rise_fall', 0b00001000),         # 1 rising, 0 cooling
                BitField('state', 0b00000100),             # 1 active high, 0 active low
                BitField('mode', 0b00000010),              # 1 interrupt mode, 0 comparator mode
                BitField('enable', 0b00000001)             # 1 enable, 0 disable
            )),
            Register('ALERT2_CONFIG', 0x09, fields=(
                BitField('clear_interrupt', 0b10000000),
                BitField('monitor_junction', 0b00010000),  # 1 Cold Junction, 0 Thermocouple
                BitField('rise_fall', 0b00001000),         # 1 rising, 0 cooling
                BitField('state', 0b00000100),             # 1 active high, 0 active low
                BitField('mode', 0b00000010),              # 1 interrupt mode, 0 comparator mode
                BitField('enable', 0b00000001)             # 1 enable, 0 disable
            )),
            Register('ALERT3_CONFIG', 0x0A, fields=(
                BitField('clear_interrupt', 0b10000000),
                BitField('monitor_junction', 0b00010000),  # 1 Cold Junction, 0 Thermocouple
                BitField('rise_fall', 0b00001000),         # 1 rising, 0 cooling
                BitField('state', 0b00000100),             # 1 active high, 0 active low
                BitField('mode', 0b00000010),              # 1 interrupt mode, 0 comparator mode
                BitField('enable', 0b00000001)             # 1 enable, 0 disable
            )),
            Register('ALERT4_CONFIG', 0x0B, fields=(
                BitField('clear_interrupt', 0b10000000),
                BitField('monitor_junction', 0b00010000),  # 1 Cold Junction, 0 Thermocouple
                BitField('rise_fall', 0b00001000),         # 1 rising, 0 cooling
                BitField('state', 0b00000100),             # 1 active high, 0 active low
                BitField('mode', 0b00000010),              # 1 interrupt mode, 0 comparator mode
                BitField('enable', 0b00000001)             # 1 enable, 0 disable
            )),
            Register('ALERT1_HYSTERESIS', 0x0C, fields=(
                BitField('value', 0xFF),
            )),
            Register('ALERT2_HYSTERESIS', 0x0D, fields=(
                BitField('value', 0xFF),
            )),
            Register('ALERT3_HYSTERESIS', 0x0E, fields=(
                BitField('value', 0xFF),
            )),
            Register('ALERT4_HYSTERESIS', 0x0F, fields=(
                BitField('value', 0xFF),
            )),
            Register('ALERT1_LIMIT', 0x10, fields=(
                BitField('value', 0xFFFF, adapter=S16Adapter()),
            ), bit_width=16),
            Register('ALERT2_LIMIT', 0x11, fields=(
                BitField('value', 0xFFFF, adapter=S16Adapter()),
            ), bit_width=16),
            Register('ALERT3_LIMIT', 0x12, fields=(
                BitField('value', 0xFFFF, adapter=S16Adapter()),
            ), bit_width=16),
            Register('ALERT4_LIMIT', 0x13, fields=(
                BitField('value', 0xFFFF, adapter=S16Adapter()),
            ), bit_width=16),
            Register('CHIP_ID', 0x20, fields=(
                BitField('id', 0xFF00),
                BitField('revision', 0x00FF, adapter=RevisionAdapter())
            ), bit_width=16)
        ))

    def setup(self):
        if self._is_setup:
            return
        self._is_setup = True

        self._mcp9600.select_address(self._i2c_addr)

        try:
            if self._mcp9600.CHIP_ID.get_id() != CHIP_ID:
                raise RuntimeError("Unable to find mcp9600 on 0x{:02x}, CHIP_ID returned {:02x}".format(self._i2c_addr, self._mcp9600.CHIP_ID.get_id()))
        except IOError:
            raise RuntimeError("Unable to find mcp9600 on 0x{:02x}, IOError".format(self._i2c_addr))


