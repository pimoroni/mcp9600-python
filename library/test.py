import mcp9600
import time

m = mcp9600.MCP9600()
m.setup()

print("Resetting alerts")
for x in range(1, 5):
    m.clear_alert(x)
    m.configure_alert(x, enable=False)

print("Configuring alerts")
m.configure_alert(1, monitor_junction=0, limit=40, mode=1, enable=True)
m.configure_alert(2, monitor_junction=0, limit=40, mode=1, enable=True, rise_fall=0)
m.configure_alert(3, monitor_junction=0, limit=40, mode=1, enable=True, rise_fall=1)

while True:
    t = m.get_hot_junction_temperature()
    c = m.get_cold_junction_temperature()
    d = m.get_temperature_delta()

    alerts = m.check_alerts()

    for x in range(1, 5):
        if alerts[x-1] == 1:
            m.clear_alert(x)

    print(alerts)

    print(t, c, d)
    time.sleep(0.5)
