import mcp9600
import time

m = mcp9600.MCP9600()

while True:
    t = m._mcp9600.TEMPERATURE.get_hot_junction()
    c = m._mcp9600.TEMPERATURE.get_cold_junction()
    print(t, c)
    time.sleep(1.0)
