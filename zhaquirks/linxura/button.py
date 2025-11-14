"""Linxura button device."""

from zigpy.profiles import zha
from zigpy.quirks import CustomCluster, CustomDevice
from zigpy.zcl.clusters.general import Basic
from zigpy.zcl.clusters.security import IasZone
from zigpy.zcl.clusters.general import PowerConfiguration

from zhaquirks.const import (
    BUTTON,
    BUTTON_1,
    BUTTON_2,
    BUTTON_3,
    BUTTON_4,
    BUTTON_5,
    BUTTON_6,
    CLUSTER_ID,
    COMMAND,
    DEVICE_TYPE,
    DOUBLE_PRESS,
    ENDPOINTS,
    INPUT_CLUSTERS,
    LONG_PRESS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PRESS_TYPE,
    PROFILE_ID,
    SHORT_PRESS,
    ZHA_SEND_EVENT,
)
# from zhaquirks.linxura import LINXURA
LINXURA = "Linxura"
BUTTON_7 = "button_7"
BUTTON_8 = "button_8"
BUTTON_9 = "button_9"
BUTTON_10 = "button_10"
BUTTON_11 = "button_11"
BUTTON_12 = "button_12"
PRESS_TYPES = {
    1: SHORT_PRESS,
    2: DOUBLE_PRESS,
    3: LONG_PRESS,
}


class LinxuraIASCluster(CustomCluster, IasZone):
    """IAS cluster used for Linxura button."""

    def _update_attribute(self, attrid, value):
        super()._update_attribute(attrid, value)
        if attrid == self.AttributeDefs.zone_status.id and 0 < value < 72:
            if 0 < value < 6:
                button = BUTTON_1
                press_type = PRESS_TYPES[value // 2 + 1]
            elif 6 < value < 12:
                button = BUTTON_2
                press_type = PRESS_TYPES[value // 2 - 3 + 1]
            elif 12 < value < 18:
                button = BUTTON_3
                press_type = PRESS_TYPES[value // 2 - 6 + 1]
            elif 18 < value < 24:
                button = BUTTON_4
                press_type = PRESS_TYPES[value // 2 - 9 + 1]
            elif 24 < value < 30:
                button = BUTTON_5
                press_type = PRESS_TYPES[value // 2 - 12 + 1]
            elif 30 < value < 36:
                button = BUTTON_6
                press_type = PRESS_TYPES[value // 2 - 15 + 1]
            elif 36 < value < 42:
                button = BUTTON_7
                press_type = PRESS_TYPES[value // 2 - 18 + 1]
            elif 42 < value < 48:
                button = BUTTON_8
                press_type = PRESS_TYPES[value // 2 - 21 + 1]
            elif 48 < value < 54:
                button = BUTTON_9
                press_type = PRESS_TYPES[value // 2 - 24 + 1]
            elif 54 < value < 60:
                button = BUTTON_10
                press_type = PRESS_TYPES[value // 2 - 27 + 1]
            elif 60 < value < 66:
                button = BUTTON_11
                press_type = PRESS_TYPES[value // 2 - 30 + 1]
            elif 66 < value < 72:
                button = BUTTON_12
                press_type = PRESS_TYPES[value // 2 - 33 + 1]
            else:
                # discard invalid values: 0, 6, 12, 18
                return

            action = f"{button}_{press_type}"
            event_args = {
                BUTTON: button,
                PRESS_TYPE: press_type,
            }
            self.listener_event(ZHA_SEND_EVENT, action, event_args)


class LinxuraButton(CustomDevice):
    """Linxura button device."""

    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=1026
        # device_version=0
        # input_clusters=[0, 3, 1280]=>input_clusters=[0, 1280]
        # output_clusters=[3]>=>output_clusters=[]
        MODELS_INFO: [(LINXURA, "Smart Controller")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.IAS_ZONE,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    IasZone.cluster_id,
                ],
                OUTPUT_CLUSTERS: [],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    LinxuraIASCluster,
                ],
                OUTPUT_CLUSTERS: [],
            },
        }
    }

class LinxuraButton_Aura(CustomDevice):
    """Linxura button device."""

    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=1026
        # device_version=0
        # input_clusters=[0, 3, 1280]=>input_clusters=[0, 1280]
        # output_clusters=[3]>=>output_clusters=[]
        MODELS_INFO: [("Linxura", "Aura Smart Button")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.IAS_ZONE,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    IasZone.cluster_id,
                ],
                OUTPUT_CLUSTERS: [],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.IAS_ZONE,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    LinxuraIASCluster,
                ],
                OUTPUT_CLUSTERS: [],
            },
        }
    }

    device_automation_triggers = {
        (press_type, button): {
            COMMAND: f"{button}_{press_type}",
            CLUSTER_ID: IasZone.cluster_id,
        }
        for press_type in (SHORT_PRESS, DOUBLE_PRESS, LONG_PRESS)
        for button in (BUTTON_1, BUTTON_2, BUTTON_3, BUTTON_4, BUTTON_5, BUTTON_6, BUTTON_7, BUTTON_8, BUTTON_9, BUTTON_10, BUTTON_11, BUTTON_12)
    }


