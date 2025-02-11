from flirpy.camera.boson import Boson
import flirpy.camera.boson
import pytest
import os
import time

if Boson.find_video_device() is None:
    pytest.skip("Boson not connected, skipping tests", allow_module_level=True)

def test_open_boson():
   camera = Boson()
   camera.close()

@pytest.mark.skipif(os.name != "nt", reason="Skipping Windows-only test")
def test_capture_windows():
    with Boson() as camera:
        # Currently have no way of figuring this out
        res = camera.grab()

        assert res is not None
        assert len(res.shape) == 2
        assert res.dtype == "uint16"

@pytest.mark.skipif(os.name == "nt", reason="Skipping on Windows")
def test_capture_unix():
    with Boson() as camera:
        res = camera.grab()

        assert res is not None
        assert len(res.shape) == 2
        assert res.dtype == "uint16"


def test_get_serial():
    with Boson() as camera:
        assert camera.get_camera_serial() != 0

def test_get_sensor_serial():
    # Skipped until proper CRC is implemented
    with Boson() as camera:
        assert camera.get_sensor_serial() != 0

def test_get_firmware_revision():
    with Boson() as camera:
        rev = camera.get_firmware_revision()
        assert len(rev) == 3

def test_get_fpa_temperature():
    with Boson() as camera:
        # In principle this could be exactly zero, but it's quite unlikely.
        assert camera.get_fpa_temperature() != 0

def test_get_part_number():
    with Boson() as camera:
        pn = camera.get_part_number()
        assert pn != ""

def test_ffc_request():
    with Boson() as camera:
        n_frames = camera.get_frame_count()
        print(n_frames)
        camera.do_ffc()
        time.sleep(1)
        ffc_frame = camera.get_last_ffc_frame_count()
        assert (ffc_frame-n_frames) < 200

def test_ffc_temperature():
    with Boson() as camera:
        assert camera.get_last_ffc_temperature() > 0

def test_frame_count():
    with Boson() as camera:
        assert camera.get_frame_count() > 0

def test_ffc_frame_threshold():
    with Boson() as camera:
        thresh = 6000
        camera.set_ffc_frame_threshold(thresh)
        assert camera.get_ffc_frame_threshold() == thresh

def test_ffc_temperature_threshold():
    with Boson() as camera:
        temp_diff = 5.0
        camera.set_ffc_temperature_threshold(temp_diff)
        assert camera.get_ffc_temperature_threshold() == temp_diff

def test_ffc_mode_manual():
    with Boson() as camera:
        camera.set_ffc_manual()
        mode = camera.get_ffc_mode()
        assert mode == flirpy.camera.boson.FLR_BOSON_MANUAL_FFC

def test_ffc_mode_auto():
    with Boson() as camera:
        camera.set_ffc_auto()
        mode = camera.get_ffc_mode()
        assert mode == flirpy.camera.boson.FLR_BOSON_AUTO_FFC

def test_agc_mode_normal():
    with Boson() as camera:
        camera.set_agc_mode(0)
        agc_mode = camera.get_agc_mode()
        assert agc_mode == flirpy.camera.boson.FLR_AGC_MODE_NORMAL
               
def test_agc_mode_hold():
    with Boson() as camera:
        camera.set_agc_mode(1)
        agc_mode = camera.get_agc_mode()
        assert agc_mode == flirpy.camera.boson.FLR_AGC_MODE_HOLD
        
def test_agc_mode_threshold():
    with Boson() as camera:
        camera.set_agc_mode(2)
        agc_mode = camera.get_agc_mode()
        assert agc_mode == flirpy.camera.boson.FLR_AGC_MODE_THRESHOLD
"""
def test_agc_mode_auto_bright():
    with Boson() as camera:
        camera.set_agc_mode(3)
        agc_mode = camera.get_agc_mode()
        assert agc_mode == flirpy.camera.boson.FLR_AGC_MODE_AUTO_BRIGHT

def test_agc_mode_auto_linear():
    with Boson() as camera:
        camera.set_agc_mode(4)
        agc_mode = camera.get_agc_mode()
        assert agc_mode == flirpy.camera.boson.FLR_AGC_MODE_AUTO_LINEAR
 
def test_agc_mode_auto_manual():
    with Boson() as camera:
        camera.set_agc_mode(5)
        agc_mode = camera.get_agc_mode()
        assert agc_mode == flirpy.camera.boson.FLR_AGC_MODE_MANUAL

def test_agc_mode_auto_end():
    with Boson() as camera:
        camera.set_agc_mode(6)
        agc_mode = camera.get_agc_mode()
        assert agc_mode == flirpy.camera.boson.FLR_AGC_MODE_AUTO_END
"""
