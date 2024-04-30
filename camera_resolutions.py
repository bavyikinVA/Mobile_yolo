import jnius
from android import request_permissions, Permission
from android import run_on_ui_thread


def get_camera_resolutions():
    PythonActivity = jnius.autoclass('org.kivy.android.PythonActivity')
    context = PythonActivity.mActivity

    camera_manager = jnius.autoclass('android.hardware.camera2.CameraManager')
    manager = camera_manager.getSystemService(context, camera_manager)

    camera_id = manager.getCameraIdList()[0]
    camera_characteristics = manager.getCameraCharacteristics(camera_id)

    stream_configuration_map = camera_characteristics.get(
        camera_characteristics.SCALER_STREAM_CONFIGURATION_MAP)

    output_formats = [
        stream_configuration_map.getOutputSizes(format)
        for format in stream_configuration_map.getOutputFormats()
    ]

    resolutions = []
    for output_format in output_formats:
        resolutions.extend([(w, h) for w, h in output_format])

    return resolutions
