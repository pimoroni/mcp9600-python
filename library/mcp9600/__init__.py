"""MCP9600 Driver."""
from i2cdevice import Device, Register, BitField, _int_to_bytes
from i2cdevice.adapter import LookupAdapter, Adapter
import struct
import math

CHIP_ID = 0x40
I2C_ADDRESS_DEFAULT = 0x66
I2C_ADDRESS_ALTERNATE = 0x67

class RevisionAdapter(Adapter):
   def _decode(self, value):
        major = (value & 0xF0) >> 4 
        minor = (value * 0x0F)
        return major + (minor / 10.0)


class TemperatureAdapter(Adapter):
    def _decode(self, value):
        b = _int_to_bytes(value, 2)
        v = struct.unpack('>h', b)[0]
        return v / 16.0


class AlertLimitAdapter(Adapter):
     def _decode(self, value):
         v = struct.unpack('>h', _int_to_bytes(value, 2))[0]
         return v / 16.0

     def _encode(self, value):
         v = (value * 4) << 2
         v = struct.pack('>h', v)
         v = (ord(v[0]) << 8) | ord(v[1])
         return v


class S16Adapter(Adapter):
    """Convert unsigned 16bit integer to signed."""

    def _decode(self, value):
        h = ("0b{:08b}".format(v) for v in _int_to_bytes(value, 2))
        print(list(h))
        return struct.unpack('>h', _int_to_bytes(value, 2))[0]

    def _encode(self, value):
        return bytes(struct.pack('>h', value))


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
            Register('HOT_JUNCTION', 0x00, fields=(
                BitField('temperature', 0xFFFF, adapter=TemperatureAdapter()),
            ), bit_width=16),
            Register('DELTA', 0x01, fields=(
                BitField('value', 0xFFFF, adapter=TemperatureAdapter()),
            ), bit_width=16),
            Register('COLD_JUNCTION', 0x02, fields=(
                BitField('temperature', 0x1FFF, adapter=TemperatureAdapter()),
            ), bit_width=16),
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
                BitField('type_select', 0b01110000, adapter=LookupAdapter({
                    'K': 0b000,
                    'J': 0b001,
                    'T': 0b010,
                    'N': 0b011,
                    'S': 0b100,
                    'E': 0b101,
                    'B': 0b110,
                    'R': 0b111
                })),
                BitField('filter_coefficients', 0b00000111)
            )),
            Register('DEVICE_CONFIG', 0x06, fields=(
                BitField('cold_junction_resolution', 0b10000000, adapter=LookupAdapter({
                    0.0625: 0b0,
                    0.25: 0b1
                })),
                BitField('adc_resolution', 0b01100000, adapter=LookupAdapter({
                    18: 0b00,
                    16: 0b01,
                    14: 0b10,
                    12: 0b11
                })),
                BitField('burst_mode_samples', 0b00011100, adapter=LookupAdapter({
                    1: 0b000,
                    2: 0b001,
                    4: 0b010,
                    8: 0b011,
                    16: 0b100,
                    32: 0b101,
                    64: 0b110,
                    128: 0b111
                })),
                BitField('shutdown_modes', 0b00000011, adapter=LookupAdapter({
                    'Normal': 0b00,
                    'Shutdown': 0b01,
                    'Burst': 0b10
                }))
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
                BitField('value', 0xFFFF, adapter=AlertLimitAdapter()),
            ), bit_width=16),
            Register('ALERT2_LIMIT', 0x11, fields=(
                BitField('value', 0xFFFF, adapter=AlertLimitAdapter()),
            ), bit_width=16),
            Register('ALERT3_LIMIT', 0x12, fields=(
                BitField('value', 0xFFFF, adapter=AlertLimitAdapter()),
            ), bit_width=16),
            Register('ALERT4_LIMIT', 0x13, fields=(
                BitField('value', 0xFFFF, adapter=AlertLimitAdapter()),
            ), bit_width=16),
            Register('CHIP_ID', 0x20, fields=(
                BitField('id', 0xFF00),
                BitField('revision', 0x00FF, adapter=RevisionAdapter())
            ), bit_width=16)
        ))

        self.alert_registers = [
            self._mcp9600.ALERT1_CONFIG,
            self._mcp9600.ALERT2_CONFIG,
            self._mcp9600.ALERT3_CONFIG,
            self._mcp9600.ALERT4_CONFIG
        ]
        self.alert_limits = [
            self._mcp9600.ALERT1_LIMIT,
            self._mcp9600.ALERT2_LIMIT,
            self._mcp9600.ALERT3_LIMIT,
            self._mcp9600.ALERT4_LIMIT
        ]
        self.alert_hysteresis = [
            self._mcp9600.ALERT1_HYSTERESIS,
            self._mcp9600.ALERT2_HYSTERESIS,
            self._mcp9600.ALERT3_HYSTERESIS,
            self._mcp9600.ALERT4_HYSTERESIS
        ]

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

    def get_hot_junction_temperature(self):
        """Return the temperature measured by the attached thermocouple."""
        return self._mcp9600.HOT_JUNCTION.get_temperature()

    def get_cold_junction_temperature(self):
        """Return the temperature measured by the onboard sensor."""
        return self._mcp9600.COLD_JUNCTION.get_temperature()

    def get_temperature_delta(self):
        """Return the difference between hot and cold junction temperatures."""
        return self._mcp9600.DELTA.get_value()

    def check_alerts(self):
         """Check status flags of all alert registers."""
         with self._mcp9600.STATUS as status:
             return status.get_alert_1(), status.get_alert_2(), status.get_alert_3(), status.get_alert_4()

    def clear_alert(self, index):
        """Clear the interrupt flag on an alert slot.

        :param index: Index of alert to clear, from 1 to 4

        """
        register = self.alert_registers[index - 1]
        register.set_clear_interrupt(1)

    def configure_alert(self, index, limit=None, hysteresis=None, clear_interrupt=True, monitor_junction=0, rise_fall=1, state=1, mode=1, enable=False):
        """Set up one of the 4 alert slots.

        :param index: Index of alert to set, from 1 to 4
        :param limit: Temperature limit
        :param hysteresis: Temperature hysteresis
        :param clear_interrupt: Whether to clear the interrupt flag
        :param monitor_junction: Which junction to monitor: 0 = HOT, 1 = COLD
        :param rise_fall: Monitor for 1=rising or 0=falling temperature
        :param state: Active 1=high or 0=low
        :param mode: 1=Interrupt mode, must clear interrupt to de-assert, 0=Comparator mode
        :param enable: True=Enabled, False=Disabled

        """
        alert_register = self.alert_registers[index - 1]

        if limit is not None:
            alert_limit = self.alert_limits[index - 1]
            alert_limit.set_value(limit)

        if hysteresis is not None:
            alert_hysteresis = self.alert_hysteresis[index - 1]
            alert_hysteresis.set_value(hysteresis)

        with alert_register as alert:
            if clear_interrupt:
                alert.set_clear_interrupt(1)
            alert.set_monitor_junction(monitor_junction)
            alert.set_rise_fall(rise_fall)
            alert.set_state(state)
            alert.set_mode(mode)
            alert.set_enable(1 if enable else 0)
            alert.write()

