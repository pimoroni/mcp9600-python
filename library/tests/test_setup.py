import sys
import mock


def test_setup():
    sys.modules['smbus'] = mock.Mock()
    import mcp9600
    device = mcp9600.MCP9600()
    del device
