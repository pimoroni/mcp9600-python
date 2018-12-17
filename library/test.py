import mcp9600
import time

m = mcp9600.MCP9600()

while True:
    t = m._mcp9600.HOT_JUNCTION.get_temperature()
    c = m._mcp9600.COLD_JUNCTION.get_temperature()
    d = m._mcp9600.DELTA.get_value()
    print(t, c, d)
    time.sleep(1.0)
