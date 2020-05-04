# MCP9600

- [MCP9600](#mcp9600)
  - [Installing](#installing)
  - [Function Reference](#function-reference)
    - [Set Thermocouple Type](#set-thermocouple-type)
    - [Get Hot Junction Temperature](#get-hot-junction-temperature)
    - [Get Cold Junction Temperature](#get-cold-junction-temperature)
    - [Get Temperature Delta](#get-temperature-delta)
    - [Get Alert Status](#get-alert-status)
    - [Configure Alerts](#configure-alerts)

The MCP9600 is a thermocouple to temperature converted with four configurable alerts and an onboard "cold junction" temperature sensor.

It supports K, J, T, N, S, E, B and R thermocouple types and is typically accurate to 1.6 degrees.

## Installing

```
pip3 install mcp9600
```

## Function Reference

In all cases you will need to create an instance of the MCP9600 class using the relevant i2c address for your sensor:

```
from mcp9600 import MCP9600
mcp9600 = MCP9600(i2c_addr=0x66)
```

By default the i2c address for the Pimoroni breakout is `0x66`, cutting the ADDR+1 jumper will set the breakout i2c address to `0x67`.

### Set Thermocouple Type

```python
mcp9600.set_thermocouple_type('K')
```

The MCP9600 supports K, J, T, N, S, E, B and R thermocouple types and you should set the type that corresponds with your thermocouple.

### Get Hot Junction Temperature

```python
mcp9600.get_hot_junction_temperature()
```

Returns the temperature as measured from the thermocouple.

### Get Cold Junction Temperature

```python
mcp9600.get_cold_junction_temperature()
```

Returns the temperature as measured by the sensor onboard the MCP9600.

### Get Temperature Delta

```python
mcp9600.get_temperature_delta()
```

Returns the delta (in degrees C) between the thermocouple and onboard temperature sensors.

### Get Alert Status

```python
alert1, alert2, alert3, alert4 = mcp9600.check_alerts()
```

Returns the status of the four customisable user alerts.

### Configure Alerts

```python
mcp9600.configure_alert(index, limit, hysteresis, clear_interrupt, monitor_junction, rise_fall, state, mode, enable)
```

The MCP9600 has four configurable interrupts, indexed 1, 2, 3 and 4 in terms of this function. These can be used to measure the onboard or thermocouple temperature and monitor for a temperature rising above or dropping below a value.

* `index` - one of 1, 2, 3 or 4 (corresponds to alert1, alert2, alert3 and alert4 from `check_alerts`)
* `limit` - Temperature limit (in degrees) at which the alert will be triggered
* `hysteresis` - Hysteresis value (in degrees) for temperature changes (minimum value by which the temperature must change to trigger/clear an interrupt)
* `clear_interrupt` - Whether the interrupt flag should be automatically cleared when the condition is no longer met
* `monitor_junction` - Junction to monitor: 0 for HOT (thermocouple), 1 for COLD (onboard)
* `rise_fall` - Whether to monitor a temperature that rises above `limit` or falls below `limit`.
* `state` - If the interrupt should be active high (1) or low (0)
* `mode` - Interrupt mode (1) or comparator mode (0)
* `enable` - Whether this alert is enabled (True/False)
