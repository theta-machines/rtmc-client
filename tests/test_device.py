import pytest
import aio_mgr as aio

@pytest.fixture
def device(emulator):
    # Connect to emulator
    device = aio.Device(emulator.ipv4_addr, emulator.tcp_port)
    response = device.connect(emulator.api_token)
    assert response.get("status") == "OKAY"

    try:
        yield device

    finally:
        # Disconnect from emulator
        response = device.disconnect()
        assert response.get("status") == "OKAY"



# Test that you can send commands to an AIO Card
def test_send(emulator, device):
    response = device.send(f"auth {emulator.api_token}")
    assert response.get("status") == "OKAY"



# Test device discovery
def test_discover(emulator):
    devices = aio.Device.discover("aio*", timeout=0.1, tries=1)
    assert len(devices) > 0



# Test device discovery (explicit iface)
def test_discover_ifaces(emulator):
    devices = aio.Device.discover("aio*", ifaces=["0.0.0.0"], timeout=0.1, tries=1)
    assert len(devices) > 0
