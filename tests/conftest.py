import pytest
import aio_mgr as aio

@pytest.fixture
def emulator():
    api_token = "dummy_token"

    # Start the emulator
    emulator = aio.EmulationServer(api_token)
    emulator.start()

    try:
        yield emulator
    finally:
        emulator.stop()
