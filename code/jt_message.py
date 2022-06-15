# Copyright (c) Quectel Wireless Solution, Co., Ltd.All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file      :jt_message.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :<description>
@version   :1.0.0
@date      :2022-05-19 16:04:13
@copyright :Copyright (c) 2022
"""

import ustruct
import ubinascii
from usr.common import str_fill
from usr.logging import getLogger

logger = getLogger(__name__)

JTT808_VERSION = {
    "2011": -1,
    "2013": 0,
    "2019": 1,
}

_BPS_CODE = {
    4800: 0x00,
    9600: 0x01,
    19200: 0x02,
    38400: 0x03,
    57600: 0x04,
    115200: 0x05,
}

_CODE_BPS = {
    0x00: 4800,
    0x01: 9600,
    0x02: 19200,
    0x03: 38400,
    0x04: 57600,
    0x05: 115200,
}

_CODE_FREQUENCY = {
    0x00: 500,
    0x01: 1000,
    0x02: 2000,
    0x03: 3000,
    0x04: 4000,
}

_FREQUENCY_CODE = {
    500: 0x00,
    1000: 0x01,
    2000: 0x02,
    3000: 0x03,
    4000: 0x04,
}

_jtt808_version = "2019"
_protocol_version = 1  # [2019]Protocol version
_version = True  # Message Body Properties - Version Flag
_client_id = ""  # Terminal Phone
_encryption = False  # Whether RSA encryption

_TERMINAL_PARAMS = {
    "STRING": [
        0x0010, 0x0011, 0x0012, 0x0013, 0x0014, 0x0015, 0x0016, 0x0017, 0x001A,
        0x001D, 0x0023, 0x0024, 0x0025, 0x0026, 0x0040, 0x0041, 0x0042, 0x0043,
        0x0044, 0x0048, 0x0049, 0x0083
    ],
    "DWORD": [
        # JTT808 Version 2019
        0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006, 0x0007, 0x001B, 0x001C,
        0x0020, 0x0021, 0x0022, 0x0027, 0x0028, 0x0029, 0x002C, 0x002D, 0x002E,
        0x002F, 0x0030, 0x0045, 0x0046, 0x0047, 0x0050, 0x0051, 0x0052, 0x0053,
        0x0054, 0x0055, 0x0056, 0x0057, 0x0058, 0x0059, 0x005A, 0x0064, 0x0065,
        0x0070, 0x0071, 0x0072, 0x0073, 0x0074, 0x0080, 0x0093, 0x0095, 0x0100,
        0x0102,
        # JTT808 Version 2013
        0x0018, 0x0019,
    ],
    "WORD": [
        0x0031, 0x005B, 0x005C, 0x005E, 0x0081, 0x0082, 0x0101, 0x0103
    ],
    "BYTE": [
        0x0084, 0x0090, 0x0091, 0x0092, 0x0094
    ],
    "BYTE[8]": list(range(0x0110, 0x200)),
    "BYTE[4]": [
        0x0032
    ],
}

_RESERVATION_TERMINAL_PARAM_ID = list(range(0x0008, 0x0010)) + \
    list(range(0x0018, 0x001A)) + list(range(0x001E, 0x0020)) + \
    list(range(0x002A, 0x002C)) + list(range(0x0033, 0x0040)) + \
    list(range(0x004A, 0x0050)) + list(range(0x005F, 0x0064)) + \
    list(range(0x0066, 0x0070)) + list(range(0x0075, 0x0080)) + \
    list(range(0xF000, 0x10000))


def set_jtmsg_config(jtt808_version="2019", client_id="", encryption=False):
    """Set JTT808 message global config
    Args:
        jtt808_version(str): (default: {"2019"})
        client_id(str): (default: {""})
        encryption(bool): (default: {False})

    Raises:
        ValueError: [description]
    """
    global _jtt808_version
    global _protocol_version
    global _client_id
    global _version
    global _encryption

    _jtt808_version = jtt808_version

    if JTT808_VERSION.get(jtt808_version) is None:
        raise ValueError("JT808 version only in 2011, 2013, 2019. not %" % jtt808_version)
    _protocol_version = JTT808_VERSION.get(jtt808_version) if JTT808_VERSION.get(jtt808_version) > 0 else ""

    _version = True if _protocol_version != "" and _protocol_version > 0 else False

    if not client_id:
        raise ValueError("client_id is not exists.")
    client_id_len = 20 if _protocol_version > 0 else 12
    _client_id = str_fill(client_id, target_len=client_id_len)

    _encryption = encryption


def get_jtmsg_config():
    """Get JTT808 message global config

    Returns:
        tuple: (_jtt808_version, _client_id, _encryption,)
    """
    global _jtt808_version
    global _client_id
    global _encryption

    return _jtt808_version, _client_id, _encryption


class ResultCode(object):
    """0x0001, 0x8001 result code"""
    success = 0  # 成功、确认
    failure = 1  # 失败
    message_error = 2  # 消息有误
    not_support = 3  # 不支持
    alarm_ack = 4  # 报警处理确认 [add][2019]


class LicensePlateColor(object):
    """License plate color"""
    blue = 1
    yellow = 2
    black = 3
    white = 4
    green = 5  # [add][2019]
    other = 9


class RegistrationResultCode(object):
    """Terminal registration result code"""
    success = 0
    vehicle_registered = 1
    vehicle_not_exist = 2
    terminal_registered = 3
    terminal_not_exist = 4


class TerminalParams(object):
    """This class is for convert terminal params value

    1. Convert int/str to hex
    2. Convert hex to int/str
    """
    def __init__(self, param_id, parse=False):
        """Terminal param init

        Args:
            param_id(int): param id
                STRING:
                    0x0010 - Main server APN
                    0x0011 - Main server wireless communication dial-up user name
                    0x0012 - Main server wireless communication dial-up password
                    0x0013 - Main server address, ip or domian. Separate the host and port with a colon. Multiple servers are separated by semicolons.
                        e.g. `host:port;doamin:port`
                    0x0014 - Backup Server APN
                    0x0015 - Backup server wireless communication user name
                    0x0016 - Backup server wireless communication password
                    0x0017 - Backup server address, ip or domian. Separate the host and port with a colon. Multiple servers are separated by semicolons.
                        e.g. `host:port;doamin:port`
                    0x001A - IP address or domain name of the main server for road transport license IC card authentication
                    0x001D - IP address or domain name of the backup server for road transport license IC card authentication. The port is the same as the main server.
                    0x0023 - Slave server apn
                    0x0024 - Slave server wireless communication dial-up user name
                    0x0025 - Slave server wireless communication dial-up password
                    0x0026 - Slave server address, ip or domian. Separate the host and port with a colon. Multiple servers are separated by semicolons.
                    0x0040 - Monitoring platform phone number
                    0x0041 - You can use this phone number to dial the terminal to restore the terminal.
                    0x0042 - You can use this phone number to dial the terminal to reset factory settings of the terminal.
                    0x0043 - Monitoring platform SMS phone number
                    0x0044 - Receiving terminal SMS text alarm number
                    0x0048 - Monitor phone number
                    0x0049 - Supervision platform privileged SMS number
                    0x0083 - Motor vehicle plate number according to the measures of the public security traffic management department.

                DWORD:
                    -- JTT808-2019
                    0x0001 - Terminal heartbeat sending interval. unit: second
                    0x0002 - TCP message response timeout. unit: second
                    0x0003 - Number of TCP message retransmissions
                    0x0004 - UDP message response timeout. unit: second
                    0x0005 - Number of UDP message retransmissions
                    0x0006 - SMS message response timeout. unit: second
                    0x0007 - Number of SMS message retransmissions
                    0x001B - TCP port of the main/backup server for road transport license IC card authentication
                    0x001C - UDP port of the main/backup server for road transport license IC card authentication
                    0x0020 - Location reporting strategy. 0 - report by timing, 1 - report by distance, 2 - report by timing and distance
                    0x0021 - Location reporting program. 0 - According to ACC status, 1 - According to login status and ACC status. First check login status, if logged in, then check ACC status.
                    0x0022 - Driver not logged in report interval. unit: second
                    0x0027 - Report interval when sleeping. unit: second
                    0x0028 - Report interval when emergency alarm. unit: second
                    0x0029 - Default time reporting interval. unit: second
                    0x002C - Default distance reporting interval. unit: meter
                    0x002D - Driver not logged in report distance interval. unit: meter
                    0x002E - Report distance interval when sleeping. unit: meter
                    0x002F - Report distance interval when emergency alarm. unit: meter
                    0x0030 - Inflection point supplementary pass angle. unit: angle, range: (0:180)
                    0x0045 - Terminal call answering policy. 0 - auto answer, 1 - auto answer when ACC on, answer manually when ACC off.
                    0x0046 - Maximum call time per session. range [0:0xFFFFFFFF], 0: Call not allowed, 0xFFFFFFFF: Not limit
                    0x0047 - Maximum call time of the month. range [0:0xFFFFFFFF], 0: Call not allowed, 0xFFFFFFFF: Not limit
                    0x0050 - Corresponds to the alarm criteria in the location information report message, when the corresponding bit is 1, the corresponding alarm is masked.
                    0x0051 - Corresponds to the alarm criteria in the location information report message, when the corresponding bit is 1, send text SMS when corresponding alarm.
                    0x0052 - Corresponds to the alarm criteria in the location information report message, when the corresponding bit is 1, camera shot when corresponding alarm.
                    0x0053 - Corresponds to the alarm criteria in the location information report message, when the corresponding bit is 1, the corresponding alarm is a key alarm.
                    0x0054 - Corresponds to the alarm criteria in the location information report message, when the corresponding bit is 1, store captured photos when corresponding alarm, when the corresponding bit is 0, live upload.
                    0x0055 - Top speed. unit: km/h
                    0x0056 - Overspeed Duration time. unit: second
                    0x0057 - Continuous driving time threshold. unit: second
                    0x0058 - Cumulative driving time threshold for the day. unit: second
                    0x0059 - Minimum rest time. unit: second
                    0x005A - Maximum parking time. unit: second
                    0x0070 - Image/Video quality. range: [1:10], 1 is the best quality.
                    0x0071 - Brightness. range: [0:255].
                    0x0072 - Contrast. range: [0:127].
                    0x0073 - Saturation. range: [0:127].
                    0x0074 - Chroma. range: [0:255].
                    0x0080 - Vehicle odometer reading. unit: 1/10km.
                    0x0093 - GNSS module detailed positioning data collection frequency (default: {1}).
                    0x0095 - GNSS module detailed positioning data upload method setting params.
                        unit: seconds when upload_method is 0x01 or 0x0B
                        unit: meter when upload_method is 0x02 or 0x0C
                        unit: item when upload_method is 0x0D
                    0x0100 - CAN bus channel 1 acquisition time interval. unit: ms, 0 - not collect.
                    0x0102 - CAN bus channel 2 acquisition time interval. unit: ms, 0 - not collect.

                    -- JTT808-2013
                    0x0108 - Server TCP port.
                    0x0109 - Server UDP port.

                WORD:
                    0x0031 - Electronic fence radius(Illegal displacement threshold). unit: meter
                    0x005B - Overspeed warning difference. unit: 1/10km/h
                    0x005C - Fatigue driving warning difference. unit: second
                    0x005E - Rollover Alarm Parameters. unit: rollover angle (default: {30})
                    0x0081 - The province id where the vehicle is located
                    0x0082 - The city id where the vehicle is located
                    0x0101 - CAN bus channel 1 upload time interval. unit: s, 0 - not upload.
                    0x0103 - CAN bus channel 2 upload time interval. unit: s, 0 - not upload.

            parse(bool): True: value is hex, to parse, False: value is int, to hex. (default: {False})
        """
        self.__parse = parse
        self.__param_id = param_id
        self.__param_id_hex = "0x" + str_fill(hex(param_id)[2:], target_len=4)
        if self.__parse is False:
            if self.__param_id in (_TERMINAL_PARAMS["BYTE"] + _TERMINAL_PARAMS["BYTE[4]"]):
                self.convert = getattr(self, "__convert_" + self.__param_id_hex)
            elif self.__param_id in _TERMINAL_PARAMS["BYTE[8]"]:
                self.convert = self.__convert_0x0110
            elif self.__param_id in (0x005D, 0x0064, 0x0065):
                self.convert = getattr(self, "__convert_" + self.__param_id_hex)
            else:
                self.convert = self.__convert_fun
        else:
            self.convert = self.__parse_fun

    def __convert_fun(self, value):
        """Format reservation terminal param

        Args:
            value(int/str): reservation terminal param value

        Returns:
            string: format value
        """
        if self.__param_id in _TERMINAL_PARAMS["STRING"]:
            return self.__convert_hex(value, data_type=str, length=0)
        elif self.__param_id in _TERMINAL_PARAMS["DWORD"]:
            return self.__convert_hex(value, data_type=int, length=8)
        elif self.__param_id in _TERMINAL_PARAMS["WORD"]:
            return self.__convert_hex(value, data_type=int, length=4)
        else:
            return self.__convert_hex(value, data_type=type(value), length=0)

    def __convert_hex(self, value, data_type=int, length=0):
        """Format terminal param value to hex.

        Args:
            value(int/str): terminal param value
            data_type(object): int or str (default: {int})
            length(int): param double bytes length (default: {0})

        Returns:
            string: format value to hex

        Raises:
            TypeError: data_type is int or str.
        """
        if isinstance(value, data_type) is False:
            raise TypeError("This value type is %s, not %s" % (data_type.__name__, type(value).__name__))

        if data_type is int:
            if length == 0:
                return hex(int(value))[2:].upper()
            else:
                return str_fill(hex(int(value))[2:], target_len=length).upper()
        elif data_type is str:
            if length == 0:
                return ubinascii.hexlify(str(value).encode("gbk")).decode("gbk").upper()
            else:
                return str_fill(ubinascii.hexlify(str(value).encode("gbk")).decode("gbk"), target_len=length).upper()
        else:
            raise TypeError("data_type is int or str, not %s" % data_type.__name__)

    def __parse_fun(self, value):
        if self.__param_id in _TERMINAL_PARAMS["STRING"]:
            return self.__parse_hex(value, data_type=str)
        elif self.__param_id in (_TERMINAL_PARAMS["DWORD"] + _TERMINAL_PARAMS["WORD"]):
            return self.__parse_hex(value, data_type=int)
        elif self.__param_id in (_TERMINAL_PARAMS["BYTE"] + _TERMINAL_PARAMS["BYTE[4]"]):
            return getattr(self, "__parse_" + self.__param_id_hex)(value)
        elif self.__param_id in _TERMINAL_PARAMS["BYTE[8]"]:
            return self.__parse_0x0110(value)
        elif self.__param_id in (0x005D, 0x0064, 0x0065):
            return getattr(self, "__parse_" + self.__param_id_hex)(value)
        else:
            return self.__parse_hex(value)

    def __parse_hex(self, value, data_type=int):
        """Parse terminal param value from hex.

        Args:
            value(int/str): terminal param value
            data_type(object): int or str (default: {int})
            length(int): param double bytes length (default: {0})

        Returns:
            string/int: format value from hex

        Raises:
            TypeError: data_type is int or str.
        """
        if data_type is int:
            return int(value, 16)
        elif data_type is str:
            return ubinascii.unhexlify(value).decode("gbk")
        else:
            raise TypeError("data_type is int or str, not %s" % data_type.__name__)

    def __parse_0x0032(self, value):
        data = {}
        if len(value) == 8:
            data = {
                "start_hour": int(value[:2], 16),
                "start_minute": int(value[2:4], 16),
                "end_hour": int(value[4:6], 16),
                "end_minute": int(value[6:8], 16),
            }
        return data

    def __parse_0x0084(self, value):
        return self.__parse_hex(value, data_type=int)

    def __parse_0x0090(self, value):
        param_value = self.__parse_hex(value, data_type=int)
        data = {
            "gps_onoff": param_value & 0b1,
            "bds_onoff": param_value & (0b1 << 1),
            "glonass_onoff": param_value & (0b1 << 2),
            "galileo_onoff": param_value & (0b1 << 3),
        }
        return data

    def __parse_0x0091(self, value):
        param_value = self.__parse_hex(value, data_type=int)
        return _CODE_BPS[param_value]

    def __parse_0x0092(self, value):
        param_value = self.__parse_hex(value, data_type=int)
        return _CODE_FREQUENCY[param_value]

    def __parse_0x0094(self, value):
        return self.__parse_hex(value, data_type=int)

    def __parse_0x0110(self, value):
        param_value = bin(int(value, 16))[2:]
        data = {
            "collection_time_interval": int(param_value[:32], 2),
            "can_channel_no": int(param_value[32:33], 2),
            "frame_type": int(param_value[33:34], 2),
            "collection_method": int(param_value[34:35], 2),
            "can_bus_id": int(param_value[35:], 2),
        }
        return data

    def __parse_0x005D(self, value):
        param_value = bin(int(value, 16))[2:]
        data = {
            "millisecond": int(param_value[8:], 2),
            "acceleration": int(param_value[:8], 2),
        }
        return data

    def __parse_0x0064(self, value):
        param_value = int(value, 16)
        data = {
            "camera_1_onoff": param_value & (0b1 << 0),
            "camera_2_onoff": param_value & (0b1 << 1),
            "camera_3_onoff": param_value & (0b1 << 2),
            "camera_4_onoff": param_value & (0b1 << 3),
            "camera_5_onoff": param_value & (0b1 << 4),
            "camera_1_storage": param_value & (0b1 << 8),
            "camera_2_storage": param_value & (0b1 << 9),
            "camera_3_storage": param_value & (0b1 << 10),
            "camera_4_storage": param_value & (0b1 << 11),
            "camera_5_storage": param_value & (0b1 << 12),
            "unit": param_value & (0b1 << 16),
            "interval": param_value & (0xFFFF << 17) >> 17,
        }
        return data

    def __parse_0x0065(self, value):
        param_value = int(value, 16)
        data = {
            "camera_1_onoff": param_value & (0b1 << 0),
            "camera_2_onoff": param_value & (0b1 << 1),
            "camera_3_onoff": param_value & (0b1 << 2),
            "camera_4_onoff": param_value & (0b1 << 3),
            "camera_5_onoff": param_value & (0b1 << 4),
            "camera_1_storage": param_value & (0b1 << 8),
            "camera_2_storage": param_value & (0b1 << 9),
            "camera_3_storage": param_value & (0b1 << 10),
            "camera_4_storage": param_value & (0b1 << 11),
            "camera_5_storage": param_value & (0b1 << 12),
            "unit": param_value & (0b1 << 16),
            "interval": param_value & (0xFFFF << 17) >> 17,
        }
        return data

    def __convert_0x0032(self, start_hour, start_minute, end_hour, end_minute):
        """Illegal driving time range

        Use the 24-time method.

        Args:
            start_hour(int): Hours of start time of illegal driving.
            start_minute(int): Minutes of start time of illegal driving.
            end_hour(int): Hours of end time of illegal driving.
            end_minute(int): Minutes of end time of illegal driving.

        Returns:
            string: format time
        """
        return (hex(start_hour)[2:] + hex(start_minute)[2:] + hex(end_hour)[2:] + hex(end_minute)[2:]).upper()

    def __convert_0x0084(self, color_code):
        """License plate color code

        Args:
            color_code(int): `LicensePlateColor.{color_name}`

        Returns:
            string: format color_code
        """
        return self.__convert_hex(value, data_type=int, length=2)

    def __convert_0x0090(self, gps_onoff, bds_onoff, glonass_onoff, galileo_onoff):
        """GNSS positioning mode

        Args:
            gps_onoff(int): 0 - off, 1 - on
            bds_onoff(int): 0 - off, 1 - on
            glonass_onoff(int): 0 - off, 1 - on
            galileo_onoff(int): 0 - off, 1 - on

        Returns:
            string: format positioning mode
        """
        value = int("0b" + str(galileo_onoff) + str(glonass_onoff) + str(bds_onoff) + str(gps_onoff), 2)
        return self.__convert_hex(value, data_type=int, length=2)

    def __convert_0x0091(self, bps):
        """GNSS baud rate

        Args:
            bps(int): baud rate
                0x00 - 4800
                0x01 - 9600
                0x02 - 19200
                0x03 - 38400
                0x04 - 57600
                0x05 - 115200

        Returns:
            string: format baud rate
        """
        value = _BPS_CODE[bps]
        return self.__convert_hex(value, data_type=int, length=2)

    def __convert_0x0092(self, frequency=1000):
        """GNSS module detailed positioning data output frequency.

        Args:
            frequency(int): output frequency. unit: ms. range [500, 1000, 2000, 3000, 4000]. (default: {1000}).
                0x00 - 500ms
                0x01 - 1000ms
                0x02 - 2000ms
                0x03 - 3000ms
                0x04 - 4000ms

        Returns:
            string: format output frequency
        """
        value = _FREQUENCY_CODE[frequency]
        return self.__convert_hex(value, data_type=int, length=2)

    def __convert_0x0094(self, upload_method=0x00):
        """GNSS module detailed positioning data upload method

        Args:
            upload_method: upload method (default: {0x00})
                0x00 - local storage, no upload
                0x01 - Upload by time interval
                0x02 - Upload by distance interval
                0x0B - Upload according to the accumulated time, and automatically stop uploading when the transmission time is reached
                0x0C - Upload according to the cumulative distance, and automatically stop uploading when the transmission distance is reached
                0x0D - Upload according to the cumulative number of pieces, and automatically stop uploading when the number of transmitted pieces is reached

        Returns:
            string: format upload_method
        """
        return self.__convert_hex(value, data_type=int, length=2)

    def __convert_0x0110(self, can_bus_id, collection_method, frame_type, can_channel_no, collection_time_interval):
        """CAN bus ID separate acquisition settings

        Args:
            can_bus_id: CAN bus id.
            collection_method: 0 - raw data, 1 - Calculated value of collection interval
            frame_type: 0 - standard frame, 1 - extended frame
            can_channel_no: 0 - CAN1, 1 - CAN2
            collection_time_interval: acquisition time interval, unit: ms, 0 - not collect.

        Returns:
            string: separate acquisition settings
        """
        value = "0b"
        value += str_fill(bin(collection_time_interval)[2:], target_len=32)
        value += str(can_channel_no)
        value += str(frame_type)
        value += str(collection_method)
        value += str_fill(bin(can_bus_id)[2:], target_len=29)
        return self.__convert_hex(value, data_type=int, length=8)

    def __convert_0x005D(self, millisecond, acceleration=10):
        """Collision alarm parameters

        Args:
            millisecond(int): collision time. TODO: Range [0:255] ?
            acceleration(int): crash acceleration, unit: 0.1g; range: [0:79], (default: {10}).

        Returns:
            string: format collision alarm parameters
        """
        return (str_fill(hex(millisecond)[2:], target_len=2) + str_fill(hex(acceleration)[2:], target_len=2)).upper()

    def __convert_0x0064(self, camera_1_onoff, camera_2_onoff, camera_3_onoff, camera_4_onoff, camera_5_onoff,
                         camera_1_storage, camera_2_storage, camera_3_storage, camera_4_storage, camera_5_storage,
                         unit, interval):
        """Timing camera control settings

        Args:
            camera_1_onoff(int): 0 - off, 1 - on
            camera_2_onoff(int): 0 - off, 1 - on
            camera_3_onoff(int): 0 - off, 1 - on
            camera_4_onoff(int): 0 - off, 1 - on
            camera_5_onoff(int): 0 - off, 1 - on
            camera_1_storage(int): 0 - storage, 1 - upload
            camera_2_storage(int): 0 - storage, 1 - upload
            camera_3_storage(int): 0 - storage, 1 - upload
            camera_4_storage(int): 0 - storage, 1 - upload
            camera_5_storage(int): 0 - storage, 1 - upload
            unit(int): 0 - seconds, 1 - minutes
            interval(int): this value is greater than 5 when unit is 0.

        Returns:
            string: format value
        """
        interval = 5 if unit == 0 and interval < 5 else interval
        value = bin(interval)[2:] + str(unit) + "000" + \
            str(camera_5_storage) + str(camera_4_storage) + str(camera_3_storage) + str(camera_2_storage) + str(camera_1_storage) + \
            "000" + str(camera_5_onoff) + str(camera_4_onoff) + str(camera_3_onoff) + str(camera_2_onoff) + str(camera_1_onoff)
        value = int("0b" + value, 2)
        return self.__convert_hex(value, data_type=int, length=8)

    def __convert_0x0065(self, camera_1_onoff, camera_2_onoff, camera_3_onoff, camera_4_onoff, camera_5_onoff,
                         camera_1_storage, camera_2_storage, camera_3_storage, camera_4_storage, camera_5_storage,
                         unit, interval):
        """Fixed distance camera control settings

        Args:
            camera_1_onoff(int): 0 - off, 1 - on
            camera_2_onoff(int): 0 - off, 1 - on
            camera_3_onoff(int): 0 - off, 1 - on
            camera_4_onoff(int): 0 - off, 1 - on
            camera_5_onoff(int): 0 - off, 1 - on
            camera_1_storage(int): 0 - storage, 1 - upload
            camera_2_storage(int): 0 - storage, 1 - upload
            camera_3_storage(int): 0 - storage, 1 - upload
            camera_4_storage(int): 0 - storage, 1 - upload
            camera_5_storage(int): 0 - storage, 1 - upload
            unit(int): 0 - meter, 1 - kilometer
            interval(int): this value is greater than 100 when unit is 0.

        Returns:
            string: format value
        """
        interval = 100 if unit == 0 and interval < 100 else interval
        value = bin(interval)[2:] + str(unit) + "000" + \
            str(camera_5_storage) + str(camera_4_storage) + str(camera_3_storage) + str(camera_2_storage) + str(camera_1_storage) + \
            "000" + str(camera_5_onoff) + str(camera_4_onoff) + str(camera_3_onoff) + str(camera_2_onoff) + str(camera_1_onoff)
        value = int("0b" + value, 2)
        return self.__convert_hex(value, data_type=int, length=8)


class LocStatusConfig(object):
    """Location status config

    location status name:

        acc_onoff
            value(int): 0 - off, 1 - on

        loc_status
            value(int): 0 - not targeted, 1 - target

        NS_latitude
            value(int): 0 - North latitude, 1 - South latitude

        EW_longitude
            value(int): 0 - East longitude, 1 - West longitude

        operational_status
            value(int): 0 - operation, 1 - outage

        long_lat_encryption
            value(int): 0 - unencrypted, 1 - encrypted

        forward_collision_warning
            value(int): 0 - none, 1 - forward collision warning collected by emergency braking system

        lane_departure_warning
            value(int): 0 - none, 1 - lane departure warning

        load_status
            value(int): 0x00 - empty car, 0x01 - half load, 0x10 - reservation, 0x11 - fully loaded

        vehicle_oil_status
            value(int): 0 - normal, 1 - disconnection

        vehicle_circuit_status
            value(int): 0 - normal, 1 - disconnection

        door_lock
            value(int): 0 - unlock, 1 - locked

        door_1_status
            value(int): 0 - closed, 1 - open

        door_2_status
            value(int): 0 - closed, 1 - open

        door_3_status
            value(int): 0 - closed, 1 - open

        door_4_status
            value(int): 0 - closed, 1 - open

        door_5_status
            value(int): 0 - closed, 1 - open

        gps_onoff
            value(int): 0 - off, 1 - on

        bds_onoff
            value(int): 0 - off, 1 - on

        glonass_onoff
            value(int): 0 - off, 1 - on

        galileo_onoff
            value(int): 0 - off, 1 - on

        running_status
            value(int): 0 - stopped, 1 - running
    """
    class _loc_cfg_offset(object):
        acc_onoff = 0
        loc_status = 1
        NS_latitude = 2
        EW_longitude = 3
        operational_status = 4
        long_lat_encryption = 5
        forward_collision_warning = 6
        lane_departure_warning = 7
        load_status = 8
        vehicle_oil_status = 10
        vehicle_circuit_status = 11
        door_lock = 12
        door_1_status = 13
        door_2_status = 14
        door_3_status = 15
        door_4_status = 16
        door_5_status = 17
        gps_onoff = 18
        bds_onoff = 19
        glonass_onoff = 20
        galileo_onoff = 21
        running_status = 22

    def __init__(self):
        self.__loc_status = 0b0

    def __set_status(self, value, offset):
        """Set status general approach

        When status value is 1 or 0

        Args:
            value(int): 1 or 0
            offset(int): `_offset.{status_type}`

        Returns:
            bool: True - success, False - Failed
        """
        try:
            if value == 1:
                self.__loc_status |= (0b1 << offset)
            else:
                self.__loc_status ^= (self.__loc_status & (0b1 << offset))
            return True
        except:
            return False

    def __get_status(self, offset, base_no=0b1):
        """Get location item status

        Args:
            int: status value
        """
        return (self.__loc_status & (base_no << offset)) >> offset

    def set_config(self, name, value):
        """Set location status config value

        Args:
            name(str): location status name
            value(int): status value

        Returns:
            bool: True - success, False - Failed

        Raises:
            TypeError: if Location status name is not exist, raise error.
        """
        if hasattr(self._loc_cfg_offset, name):
            return self.__set_status(value, getattr(self._loc_cfg_offset, name))
        else:
            raise TypeError("Location status name %s is not exists." % name)

    def get_config(self, name):
        """Get location status config value

        Args:
            name(str): location status name

        Returns:
            int: status value

        Raises:
            TypeError: if Location status name is not exist, raise error.
        """
        if hasattr(self._loc_cfg_offset, name):
            base_no = 0b1
            if name == "load_status":
                base_no = 0b11
            return self.__get_status(hasattr(self._loc_cfg_offset, name), base_no=base_no)
        else:
            raise TypeError("Alarm %s is not exists." % name)

    def value(self):
        """Get location value

        Returns:
            string: location value format by hex
        """
        return str_fill(hex(self.__loc_status)[2:], target_len=8)


class LocAlarmWarningConfig(object):
    """Location alarm and warning config

    alarm names:
        emergency_alarm
        over_speed_alarm
        fatigue_driving_alarm
        dangerous_driving_behaviour_alarm
        gnss_module_failure_alarm
        gnss_antenna_disconnection_alarm
        gnss_antenna_short_circuit_alarm
        terminal_main_power_supply_undervoltage_alarm
        terminal_main_power_failure_alarm
        terminal_lcd_or_display_failure_alarm
        tts_module_fault_alarm
        camera_failure_alarm
        road_transport_license_ic_card_module_fault_alarm
        over_speed_warning
        fatigue_driving_warning
        illegal_driving_alarm
        tire_pressure_warning
        right_turn_blind_spot_abnormal_alarm
        cumulative_driving_overtime_alarm_for_the_day
        overtime_parking_alarm
        in_and_out_of_the_area_alarm
        entry_and_exit_route_alarm
        insufficient_or_too_long_driving_time_on_the_road_section_alarm
        route_departure_alarm
        vehicle_vss_failure_alarm
        vehicle_fuel_abnormality_alarm
        vehicle_theft_alarm
        vehicle_illegal_ignition_alarm
        vehicle_illegal_displacement_alarm
        collision_rollover_alarm
        rollover_alarm
        illegal_door_opening_alarm
    """

    class _alarm_flag_offset(object):
        emergency_alarm = 0
        over_speed_alarm = 1
        fatigue_driving_alarm = 2
        dangerous_driving_behaviour_alarm = 3
        gnss_module_failure_alarm = 4
        gnss_antenna_disconnection_alarm = 5
        gnss_antenna_short_circuit_alarm = 6
        terminal_main_power_supply_undervoltage_alarm = 7
        terminal_main_power_failure_alarm = 8
        terminal_lcd_or_display_failure_alarm = 9
        tts_module_fault_alarm = 10
        camera_failure_alarm = 11
        road_transport_license_ic_card_module_fault_alarm = 12
        over_speed_warning = 13
        fatigue_driving_warning = 14
        illegal_driving_alarm = 15
        tire_pressure_warning = 16
        right_turn_blind_spot_abnormal_alarm = 17
        cumulative_driving_overtime_alarm_for_the_day = 18
        overtime_parking_alarm = 19
        in_and_out_of_the_area_alarm = 20
        entry_and_exit_route_alarm = 21
        insufficient_or_too_long_driving_time_on_the_road_section_alarm = 22
        route_departure_alarm = 23
        vehicle_vss_failure_alarm = 24
        vehicle_fuel_abnormality_alarm = 25
        vehicle_theft_alarm = 26
        vehicle_illegal_ignition_alarm = 27
        vehicle_illegal_displacement_alarm = 28
        collision_rollover_alarm = 29
        rollover_alarm = 30
        illegal_door_opening_alarm = 31

    def __init__(self):
        self.__flag_bit = 0b0

    def __get_flag(self, offset):
        """Get Alarm Warning Flag

        Args:
            int: 1 - alarm, 0 - clear alarm
        """
        return (self.__flag_bit & (0b1 << offset)) >> offset

    def __set_flag(self, value, offset):
        """Set Alarm Warning Flag

        Args:
            value(int): 1 or 0
            offset(int): `_offset.{flag_type}`

        Returns:
            bool: True - success, False - Failed
        """
        try:
            if value == 1:
                self.__flag_bit |= (0b1 << offset)
            else:
                self.__flag_bit ^= (self.__flag_bit & (0b1 << offset))
            return True
        except:
            return False

    def set_alarm(self, name, onoff):
        """Set alarm status

        Args:
            name(str): alarm name
            onoff(int): 0 - off alarm, 1 - on alarm

        Returns:
            bool: True - success, False - Failed

        Raises:
            TypeError: if alarm is not exist, raise error.
        """
        if hasattr(self._alarm_flag_offset, name):
            return self.__set_flag(onoff, getattr(self._alarm_flag_offset, name))
        else:
            raise TypeError("Alarm %s is not exists." % name)

    def get_alarm(self, name):
        """Get alarm status

        Args:
            name(str): alarm name

        Returns:
            int: 0 - off alarm, 1 - on alarm

        Raises:
            TypeError: if alarm is not exist, raise error.
        """
        if hasattr(self._alarm_flag_offset, name):
            return self.__get_flag(hasattr(self._alarm_flag_offset, name))
        else:
            raise TypeError("Alarm %s is not exists." % name)

    def value(self):
        """Get alarm warning flag bit value

        Returns:
            string: alarm warning flag bit value by hex
        """
        return str_fill(hex(self.__flag_bit)[2:], target_len=8)


class LocAdditionalInfoConfig(object):
    """Location additional info config"""

    def __init__(self):
        self.additional_info = dict()

    def set_mileage(self, value):
        """Odometer reading

        Args:
            value(float): unit: km/h, Accurate to 0.1
        """
        self.additional_info[0x01] = str_fill(hex(int(value * 10))[2:], target_len=8)

    def get_mileage(self):
        """Get odometer reading

        Returns:
            float: mileage, no value return -1
        """
        if self.additional_info.get(0x01) is not None:
            return int(self.additional_info[0x01], 16) / 10
        return -1

    def set_oil_quantity(self, value):
        """Fuel gauge reading

        Args:
            value(float): unit: L, Accurate to 0.1
        """
        self.additional_info[0x02] = str_fill(hex(int(value * 10))[2:], target_len=4)

    def get_old_quantity(self):
        """Get Fuel gauge reading

        Returns:
            float: mileage, no value return -1
        """
        if self.additional_info.get(0x02) is not None:
            return int(self.additional_info[0x02], 16)
        return -1

    def set_speed(self, value):
        """The speed of form record function acquisition.

        Args:
            value(float): unit: km/h, Accurate to 0.1
        """
        self.additional_info[0x03] = str_fill(hex(int(value * 10))[2:], target_len=4)

    def get_speed(self):
        """Get the speed of form record function acquisition.

        Returns:
            float: mileage, no value return -1
        """
        if self.additional_info.get(0x03) is not None:
            return int(self.additional_info[0x03], 16)
        return -1

    def set_manually_confirm_the_alarm_event_id(self, value):
        """Manually confirm the alarm event id.

        Args:
            value(int): alarm event id
        """
        self.additional_info[0x04] = str_fill(hex(value)[2:], target_len=4)

    def get_manually_confirm_the_alarm_event_id(self):
        """Get manually confirm the alarm event id.

        Returns:
            int: no value return -1
        """
        if self.additional_info.get(0x04) is not None:
            return int(self.additional_info[0x04], 16)
        return -1

    def set_tire_pressure(self, values):
        """Set tire pressure

        The order of calibrating the wheels is from left to right from the front of the car.
        e.g.:
            front left 1, front left 2, front right 1, front right 2, center left 1, center left 2, center left 3,
            center right 1, center right 2, center right 3, rear left 1, rear left 2, rear left 3...

        Args:
            values(list): item int, unit: pa, max value is 254.
        """
        self.additional_info[0x05] = "".join(list(map(lambda x: str_fill(hex(int(x))[2:], target_len=2) if x < 255 else str_fill(hex(int(254))[2:], target_len=2), values[:30])))
        self.additional_info[0x05] = str_fill(self.additional_info[0x05], rl="r", target_len=60, fill_field="f")

    def get_tire_pressure(self):
        """Get tire pressure

        Returns:
            list: tire pressure list.
        """
        data = []
        if self.additional_info.get(0x05) is not None:
            tire_pressure = self.additional_info[0x05]
            data = [int(tire_pressure[i * 2:(i + 1) * 2], 16) for i in range(int(len(tire_pressure) / 2)) if tire_pressure[i * 2:(i + 1) * 2].lower() != "ff"]
        return data

    def set_temperature(self, value):
        """Cabin temperature

        The unit is Celsius. range: [-32767:32767]

        Args:
            value(int): temperature
        """
        self.additional_info[0x06] = str_fill(bin(int(bin(value & 0xFFFF), 2))[2:], target_len=4)

    def get_temperature(self):
        """Get cabin temperature

        Returns:
            int: temperature
        """
        if self.additional_info.get(0x06) is not None:
            temp = int(self.additional_info[0x06], 16)
            if temp > 0x8000:
                return temp - (2 ** len(bin(temp)[2:]))
            else:
                return temp

    def set_over_speed_alarm(self, loc_type, area_segment_id=None):
        """Over speed alarm

        Args:
            loc_type(int):
                0 - no specific location
                1 - prototype area
                2 - rectangular area
                3 - polygon area
                4 - road section
            area_segment_id(int): no this value if loc_type is 0.
        """
        self.additional_info[0x11] = str_fill(hex(loc_type)[2:], target_len=2)
        if loc_type != 0:
            self.additional_info[0x11] += str_fill(hex(area_segment_id)[2:], target_len=8)

    def get_over_speed_alarm(self):
        """Get over speed alarm

        Returns:
            dict:
                loc_type(int)
                area_segment_id(int/None)
        """
        data = {}
        if self.additional_info.get(0x11) is not None:
            loc_type = int(self.additional_info.get(0x11)[:2], 16)
            area_segment_id = None
            if loc_type != 0:
                area_segment_id = int(self.additional_info.get(0x11)[2:], 16)
            data = {"loc_type": loc_type, "area_segment_id": area_segment_id}
        return data

    def set_in_out_area_segment_alarm(self, loc_type, area_segment_id, direction):
        """In out area or segment alarm

        Args:
            loc_type(int):
                1 - prototype area
                2 - rectangular area
                3 - polygon area
                4 - road section
            area_segment_id(int): area or segment id
            direction(int):
                0 - in
                1 - out
        """
        self.additional_info[0x12] = str_fill(hex(loc_type)[2:], target_len=2)
        self.additional_info[0x12] += str_fill(hex(area_segment_id)[2:], target_len=8)
        self.additional_info[0x12] += str_fill(hex(direction)[2:], target_len=2)

    def get_in_out_area_segment_alarm(self):
        """Get in out area or segment alarm

        Returns:
            dict:
                loc_type(int)
                area_segment_id(int)
                direction(int)
        """
        data = {}
        if self.additional_info.get(0x12) is not None:
            alarm_info = self.additional_info[0x12]
            data["loc_type"] = int(alarm_info[:2], 16)
            data["area_segment_id"] = int(alarm_info[2:10], 16)
            data["direction"] = int(alarm_info[10:], 16)
        return data

    def set_insufficient_or_too_long_driving_time(self, road_id, travel_time, result):
        """Insufficient or too long driving time

        Args:
            road_id(int): road id
            travel_time(int): unit: seconds
            result(int):
                0 - insufficient
                1 - too long
        """
        self.additional_info[0x13] = str_fill(hex(road_id)[2:], target_len=8)
        self.additional_info[0x13] += str_fill(hex(travel_time)[2:], target_len=4)
        self.additional_info[0x13] += str_fill(hex(result)[2:], target_len=2)

    def get_insufficient_or_too_long_driving_time(self):
        """Get Insufficient or too long driving time

        Returns:
            dict:
                road_id(int)
                travel_time(int)
                result(int)
        """
        data = {}
        if self.additional_info.get(0x13) is not None:
            alarm_info = self.additional_info[0x13]
            data["road_id"] = int(alarm_info[:8], 16)
            data["travel_time"] = int(alarm_info[8:12], 16)
            data["result"] = int(alarm_info[12:], 16)
        return data

    def set_vehicle_signal_status(self, low_beam_lights, high_beam, left_turn, right_turn, brake, reverse,
                                  fog_light, position, horn, air_conditioning, neutral, retarder, abs_work,
                                  heating, clutch):
        """Set vehicle signal status

        Args:
            low_beam_lights(int): 0 - off, 1 - on
            high_beam(int): 0 - off, 1 - on
            left_turn(int): 0 - off, 1 - on
            right_turn(int): 0 - off, 1 - on
            brake(int): 0 - off, 1 - on
            reverse(int): 0 - off, 1 - on
            fog_light(int): 0 - off, 1 - on
            position(int): 0 - off, 1 - on
            horn(int): 0 - off, 1 - on
            air_conditioning(int): 0 - off, 1 - on
            neutral(int): 0 - off, 1 - on
            retarder(int): 0 - off, 1 - on
            abs_work(int): 0 - off, 1 - on
            heating(int): 0 - off, 1 - on
            clutch(int): 0 - off, 1 - on
        """
        self.additional_info[0x25] = "0" * 17
        args = [
            low_beam_lights, high_beam, left_turn, right_turn, brake, reverse,
            fog_light, position, horn, air_conditioning, neutral, retarder, abs_work,
            heating, clutch
        ]
        args.reverse()
        self.additional_info[0x25] += ("{}" * 15).format(*args)
        self.additional_info[0x25] = str_fill(hex(int(self.additional_info[0x25], 2))[2:], target_len=8)

    def get_vehicle_signal_status(self):
        """Get vehicle signal status

        Returns:
            dict:
                low_beam_lights(int)
                high_beam(int)
                left_turn(int)
                right_turn(int)
                brake(int)
                reverse(int)
                fog_light(int)
                position(int)
                horn(int)
                air_conditioning(int)
                neutral(int)
                retarder(int)
                abs_work(int)
                heating(int)
                clutch(int)
        """
        data = {}
        if self.additional_info.get(0x25) is not None:
            vehicle_signal_status = str_fill(bin(int(self.additional_info[0x25], 16))[2:], target_len=15)
            vehicle_signal_status = list(vehicle_signal_status)
            vehicle_signal_status.reverse()
            vehicle_signal_status = list(map(int, vehicle_signal_status))
            data = {
                "low_beam_lights": vehicle_signal_status[0],
                "high_beam": vehicle_signal_status[1],
                "left_turn": vehicle_signal_status[2],
                "right_turn": vehicle_signal_status[3],
                "brake": vehicle_signal_status[4],
                "reverse": vehicle_signal_status[5],
                "fog_light": vehicle_signal_status[6],
                "position": vehicle_signal_status[7],
                "horn": vehicle_signal_status[8],
                "air_conditioning": vehicle_signal_status[9],
                "neutral": vehicle_signal_status[10],
                "retarder": vehicle_signal_status[11],
                "abs_work": vehicle_signal_status[12],
                "heating": vehicle_signal_status[13],
                "clutch": vehicle_signal_status[14],
            }
        return data

    def set_io_status(self, deep_sleep, sleep):
        """Set IO status

        Args:
            deep_sleep(int): 0 - off, 1 - on
            sleep(int): 0 - off, 1 - on
        """
        self.additional_info[0x2A] = "0" * 14 + "{}{}".format(sleep, deep_sleep)
        self.additional_info[0x2A] = str_fill(hex(int(self.additional_info[0x2A], 2))[2:], target_len=4)

    def get_io_status(self):
        """Get IO status

        Returns:
            dict:
                deep_sleep(int)
                sleep(int)
        """
        data = {}
        if self.additional_info.get(0x2A) is not None:
            io_status = str_fill(bin(int(self.additional_info[0x2A], 16))[2:], target_len=2)
            data = {
                "deep_sleep": int(io_status[-1]),
                "sleep": int(io_status[-2]),
            }
        return data

    def set_analog(self, ad0, ad1):
        """Set analog

        Args:
            ad0(int): AD0
            ad1(int): AD1
        """
        ad0 = str_fill(hex(ad0)[2:], target_len=2)
        ad1 = str_fill(hex(ad1)[2:], target_len=2)
        self.additional_info[0x2B] = "{}{}".format(ad1, ad0)

    def get_analog(self):
        """Get analog

        Returns:
            dict:
                ad0(int)
                ad1(int)
        """
        data = {}
        if self.additional_info.get(0x2B) is not None:
            data["ad0"] = int(self.additional_info[0x2B][:2], 16)
            data["ad1"] = int(self.additional_info[0x2B][2:], 16)
        return data

    def set_wireless_communication_network_signal_strength(self, value):
        """Set wireless communication network signal strength

        Args:
            value(int): strength
        """
        self.additional_info[0x30] = str_fill(hex(value)[2:], target_len=2)

    def get_wireless_communication_network_signal_strength(self):
        """Get wireless communication network signal strength

        Returns:
            int: strength
        """
        if self.additional_info.get(0x30) is not None:
            return int(self.additional_info[0x30], 16)
        return -1

    def set_number_of_satellites(self, value):
        """Set number of satellites

        Args:
            value(int): number of satellites
        """
        self.additional_info[0x31] = str_fill(hex(value)[2:], target_len=2)

    def get_number_of_satellites(self):
        """Get number of satellites

        Returns:
            int: number of satellites
        """
        if self.additional_info.get(0x31) is not None:
            return int(self.additional_info[0x31], 16)
        return -1

    def value(self):
        """Format all set over additional infos

        Returns:
            string: additional infos
        """
        loc_additional_info = ""
        for _id_ in self.additional_info.keys():
            _id = str_fill(hex(_id_)[2:], target_len=2)
            _val = self.additional_info[_id_]
            _len = str_fill(hex(int(len(_val) / 2))[2:], target_len=2)
            loc_additional_info += "{}{}{}".format(_id, _len, _val)
        return loc_additional_info


class JTMessage(object):
    __body_length_ = 0b0000001111111111
    __encryption_ = 0b0001110000000000
    __subpackage_ = 0b0010000000000000
    __version_ = 0b0100000000000000
    __reserved_ = 0b1000000000000000

    def __init__(self):
        global _jtt808_version
        global _protocol_version
        global _client_id
        global _version
        global _encryption

        self.__jtt808_version = _jtt808_version
        self.__protocol_version = _protocol_version
        self.__client_id = _client_id
        self.__version = _version
        self.__encryption = _encryption

        self.__properties = 0b0000000000000000
        if self.__version:
            self.__properties |= self.__version_
        else:
            self.__properties ^= (self.__properties & self.__version_)

        self.__properties = self.__properties ^ (self.__properties & self.__encryption_) | (self.__encryption << 10)

        self.__message_id = 0x0000
        self.__serial_no = 0
        self.__package_total = 0
        self.__package_no = 0

        self.__header = ""
        self.__body = ""
        self.__check_code = ""

        self.__headers = {}
        self.__bodys = {}
        self.__check_codes = {}

        self.__message = ""
        self.__body_data = {}

    def __splice_header(self, **kwargs):
        return "{message_id}{properties}{version}{client_id}{serial_no}{package_total}{package_no}".format(**kwargs)

    def __init_check_code(self, header, body):
        message = "{header}{body}".format(header=header, body=body)
        data = [int(message[i * 2:i * 2 + 2], 16) for i in range(int(len(message) / 2))]
        check_code = data[0] ^ data[1]
        for i in range(2, len(data)):
            check_code = check_code ^ data[i]
        return hex(check_code)[2:]

    def __message_to_hex(self, header, body, check_code):
        kwargs = {
            "header": header,
            "body": body,
            "check_code": check_code,
        }
        message = "{header}{body}{check_code}".format(**kwargs).lower()
        logger.debug("[__message_to_hex] message: %s" % message)
        msgs = []
        for i in range(int(len(message) / 2)):
            code = message[i * 2:i * 2 + 2]
            if code == "7d":
                msgs.extend([int("7d", 16), int("01", 16)])
            elif code == "7e":
                msgs.extend([int("7d", 16), int("02", 16)])
            else:
                msgs.append(int(code, 16))
        msgs.insert(0, int("7e", 16))
        msgs.append(int("7e", 16))
        logger.debug("[__message_to_hex] msgs: %s" % msgs)
        msg = ustruct.pack("%sB" % len(msgs), *msgs)
        logger.debug("[__message_to_hex] msg: %s" % msg)

        return msg

    def get_body_len(self):
        return self.__properties & self.__body_length_

    def set_body_len(self, body_len):
        self.__properties = self.__properties ^ (self.__properties & self.__body_length_) | body_len

    def get_encryption(self):
        return (self.__properties & self.__encryption_) >> 10

    def is_subpackage(self):
        return (self.__properties & self.__subpackage_) == self.__subpackage_

    def set_subpackage(self, subpackage=False, package_total=0):
        if subpackage:
            self.__properties |= self.__subpackage_
            self.__package_total = package_total
        else:
            self.__properties ^= (self.__properties & self.__subpackage_)

    def is_version(self):
        return (self.__properties & self.__version_) == self.__version_

    def set_serial_no(self, serial_no):
        """
        Args:
            serial_no(int): serial number
        """
        self.__serial_no = serial_no

    def header_to_hex(self):
        kwargs = {
            "message_id": str_fill(hex(self.__message_id)[2:], target_len=4),
            "version": str_fill(hex(self.__protocol_version)[2:], target_len=2),
            "client_id": self.__client_id,
            "serial_no": str_fill(hex(self.__serial_no)[2:], target_len=4),
            "package_total": "",
            "package_no": "",
        }
        logger.debug("header_to_hex: %s" % str(kwargs))
        if self.is_subpackage() and self.__bodys:
            # Init properties
            for package_no in self.__bodys.keys():
                body_len = int(self.__bodys[package_no] / 2)
                self.set_body_len(body_len)
                kwargs.update({
                    "properties": str_fill(hex(self.__properties)[2:], target_len=4),
                    "package_total": str_fill(hex(self.__package_total)[2:], target_len=4),
                    "package_no": str_fill(hex(package_no)[2:], target_len=4),
                })
                self.__headers[package_no] = self.__splice_header(**kwargs)
        else:
            self.set_body_len(int(len(self.__body) / 2))
            kwargs.update({
                "properties": str_fill(hex(self.__properties)[2:], target_len=4),
            })
            self.__header = self.__splice_header(**kwargs)

    def init_check_code(self):
        if self.is_subpackage() and self.__bodys:
            for package_no in self.__bodys.keys():
                header = self.__headers[package_no]
                body = self.__bodys[package_no]
                self.__check_codes[package_no] = self.__init_check_code(header, body)
        else:
            self.__check_code = self.__init_check_code(self.__header, self.__body)

    def message(self):
        # Init body
        self.body_to_hex()
        # subcontract body
        # self.body_subcontract()
        # encrypt body
        self.rsa_encryption()
        # Init header
        self.header_to_hex()
        # Init check code
        self.init_check_code()

        if self.is_subpackage() and self.__bodys:
            msgs = [self.__message_to_hex(self.__headers[package_no], self.__bodys[package_no], self.__check_codes[package_no]) for package_no in self.__bodys.keys()]
            return msgs
        else:
            msg = self.__message_to_hex(self.__header, self.__body, self.__check_code)
            return msg

    def set_body(self, body):
        self.__body = body
        self.rsa_decryption()
        self.body_from_hex()

    def get_body(self):
        return self.__body

    def set_header(self, header):
        self.__message_id = header["message_id"]
        self.__properties = header["properties"]
        self.__protocol_version = header["protocol_version"]
        self.__client_id = header["client_id"]
        self.__serial_no = header["serial_no"]
        self.__package_total = header["package_total"]
        self.__package_no = header["package_no"]

    def body_data(self):
        return self.__body_data

    def body_subcontract(self):
        if self.is_subpackage():
            if self.__package_total <= 0:
                raise ValueError("Packge total num must greater than 0.")
            subpkg_len = int(int(len(self.__body) / 2) / self.__package_total)
            for i in range(1, self.__package_total + 2):
                start_num = i * subpkg_len * 2
                end_num = (i + 1) * subpkg_len * 2
                if self.__body[start_num:end_num]:
                    self.__bodys[i] = self.__body[start_num:end_num]

    def body_to_hex(self):
        pass

    def body_from_hex(self):
        pass

    def rsa_encryption(self):
        if self.get_encryption():
            pass

    def rsa_decryption(self):
        if self.get_encryption():
            pass


class JTMessageParse(JTMessage):
    """This class use to get server hex message header."""

    def __init__(self):
        super().__init__()

    def __escape_message(self):
        msgs = []
        jump = 0
        for i in range(int(len(self.__message) / 2)):
            code = self.__message[i * 2:i * 2 + 2]
            if code == "7d":
                jump = 1
                next_code = self.__message[(i + 1) * 2:(i + 1) * 2 + 2]
                if next_code == "01":
                    msgs.append(code)
                elif next_code == "02":
                    msgs.append("7e")
                else:
                    raise TypeError("Escape message failed. Only 01 or 02 after 7d, not %s" % next_code)
            else:
                if jump == 1:
                    jump = 0
                else:
                    msgs.append(code)
        self.__message = "".join(msgs)

    def __parse_check_code(self):
        self.__check_code = int(self.__message[-2:], 16)

    def __check_code_check(self):
        msgs = [int(self.__message[i * 2:i * 2 + 2], 16) for i in range(int(len(self.__message[:-2]) / 2))]
        check_code = msgs[0] ^ msgs[1]
        for i in range(2, len(msgs)):
            check_code ^= msgs[i]
        if check_code != self.__check_code:
            raise TypeError("check code is not compare. message check_code[%s], calculate check_code[%s]" % (self.__check_code, check_code))

    def __parse_header(self):
        self.__message_id = int(self.__message[:4], 16)
        self.__properties = int(self.__message[4:8], 16)
        if self.is_version():
            self.__protocol_version = int(self.__message[8:10], 16)
            self.__client_id = self.__message[10:30]
            self.__serial_no = int(self.__message[30:34], 16)
            if self.is_subpackage():
                self.__package_total = int(self.__message[34:38], 16)
                self.__package_no = int(self.__message[38:42], 16)
        else:
            self.__client_id = self.__message[8:20]
            self.__serial_no = int(self.__message[20:24], 16)
            if self.is_subpackage():
                self.__package_total = int(self.__message[24:28], 16)
                self.__package_no = int(self.__message[28:32], 16)

    def __parse_body(self):
        if self.is_version():
            if self.is_subpackage():
                self.__body = self.__message[42:-2]
            else:
                self.__body = self.__message[34:-2]
        else:
            if self.is_subpackage():
                self.__body = self.__message[32:-2]
            else:
                self.__body = self.__message[24:-2]

    def set_message(self, message):
        msg = "".join(str_fill(hex(i)[2:], target_len=2) for i in list(bytearray(message)))
        logger.debug("set_message msg: %s" % msg)
        if msg.startswith("7e") and msg.endswith("7e"):
            self.__message = msg[2:-2]
            logger.debug("self.__message: %s" % self.__message)
            self.__escape_message()
            self.__parse_check_code()
            self.__check_code_check()
            self.__parse_header()
            self.__parse_body()
            return True
        return False

    def get_header(self):
        header = {
            "message_id": self.__message_id,
            "properties": self.__properties,
            "protocol_version": self.__protocol_version,
            "client_id": self.__client_id,
            "serial_no": self.__serial_no,
            "package_total": self.__package_total,
            "package_no": self.__package_no,
        }
        return header

    def get_body(self):
        return self.__body


class T0001(JTMessage):
    """Terminal general answer"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0001

    def set_params(self, response_serial_no, response_msg_id, result_code):
        """
        Args:
            response_serial_no(int): response serial no
            response_msg_id(int): response message id
            result_code(int): `ResultCode.{result_type}`
        """
        self.__response_serial_no = str_fill(hex(response_serial_no)[2:], target_len=4)
        self.__response_msg_id = str_fill(hex(response_msg_id)[2:], target_len=4)
        self.__result_code = str_fill(hex(result_code)[2:], target_len=2)

    def body_to_hex(self):
        kwargs = {
            "response_serial_no": self.__response_serial_no,
            "response_msg_id": self.__response_msg_id,
            "result_code": self.__result_code,
        }
        self.__body = "{response_serial_no}{response_msg_id}{result_code}".format(**kwargs)


class T8001(JTMessage):
    """Platform universal Response"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8001

    def body_from_hex(self):
        self.__body_data = {
            "serial_no": int(self.__body[:4], 16),
            "message_id": int(self.__body[4:8], 16),
            "result_code": int(self.__body[8:10], 16),
        }


class T0002(JTMessage):
    """Terminal heartbeat"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0002


class T0004(JTMessage):
    """Search server time request"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0004


class T8004(JTMessage):
    """Search server time response"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8004

    def body_from_hex(self):
        time_item = [self.__body[i * 2:(i + 1) * 2] for i in range(int(len(self.__body) / 2))]
        self.__body_data = {
            "utc_time": "20%s-%s-%s %s:%s:%s" % tuple(time_item)
        }


class T8003(JTMessage):
    """Server supplementary subcontracting request"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8003

    def body_from_hex(self):
        source_serial_no = int(self.__body[:4], 16)
        if self.is_version():
            total_number = int(self.__body[4:8], 16)
            pkids = self.__body[8:]
        else:
            total_number = int(self.__body[4:6], 16)
            pkids = self.__body[6:]
        package_ids = [int(pkids[i * 2:(i + 1) * 2]) for i in range(int(len(pkids) / 2))]

        self.__body_data = {
            "serial_no": source_serial_no,
            "total_number": total_number,
            "package_ids": package_ids
        }


class T0005(JTMessage):
    """Terminal supplementary subcontracting request"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0005

    def set_params(self, source_serial_no, package_ids):
        """
        Args:
            source_serial_no(int): source message serial number
            package_ids(list): package id list
        """
        self.__source_serial_no = source_serial_no
        self.__package_ids = package_ids

    def body_to_hex(self):
        kwargs = {
            "source_serial_no": str_fill(hex(self.__source_serial_no)[2:], target_len=4),
            "retransmission_num": str_fill(hex(len(self.__package_ids))[2:], target_len=4),
            "package_ids": "".join([str_fill(hex(pkg_id)[2:], target_len=4) for pkg_id in self.__package_ids]),
        }
        self.__body = "{source_serial_no}{retransmission_num}{package_ids}".format(**kwargs)


class T0100(JTMessage):
    """Terminal registration request"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0100

    def set_params(self, province_id, city_id, manufacturer_id, terminal_model, terminal_id, license_plate_color, license_plate):
        """
        Args:
            province_id(int): province id from GT/T 2260 document
            city_id(int): city id from GT/T 2260 document
            manufacturer_id(str): It consists of the administrative division code of the vehicle terminal manufacturer's location and the manufacturer's id
            terminal_model(str): Manufacturer's own definition
            terminal_id(str): Manufacturer's own definition
            license_plate_color(int): Specified by JT/T 697.7-2014, 0 for no license plate
            license_plate(str): Motor vehicle license plate. If the vehicle is licensed, fill in the frame number
        """
        self.__manufacturer_id_len = 22
        self.__terminal_model_len = 60
        self.__terminal_id_len = 60
        if self.__jtt808_version == "2013":
            self.__manufacturer_id_len = 10
            self.__terminal_model_len = 40
            self.__terminal_id_len = 14
        elif self.__jtt808_version == "2011":
            self.__manufacturer_id_len = 10
            self.__terminal_model_len = 16
            self.__terminal_id_len = 14

        self.__province_id = province_id
        self.__city_id = city_id
        self.__manufacturer_id = manufacturer_id
        self.__terminal_model = terminal_model
        self.__terminal_id = terminal_id
        self.__license_plate_color = license_plate_color
        self.__license_plate = license_plate

    def body_to_hex(self):
        kwargs = {
            "province_id": str_fill(hex(self.__province_id)[2:], target_len=4),
            "city_id": str_fill(hex(self.__city_id)[2:], target_len=4),
            "manufacturer_id": str_fill(ubinascii.hexlify(str(self.__manufacturer_id).encode('gbk')).decode('gbk'), target_len=self.__manufacturer_id_len),
            "terminal_model": str_fill(ubinascii.hexlify(str(self.__terminal_model).encode('gbk')).decode('gbk'), target_len=self.__terminal_model_len),
            "terminal_id": str_fill(ubinascii.hexlify(str(self.__terminal_id).encode('gbk')).decode('gbk'), target_len=self.__terminal_id_len),
            "license_plate_color": str_fill(hex(self.__license_plate_color)[2:], target_len=2),
            "license_plate": str_fill(ubinascii.hexlify(self.__license_plate.encode('gbk')).decode('gbk'), target_len=self.__terminal_id_len),
        }
        self.__body = "{province_id}{city_id}{manufacturer_id}{terminal_model}{terminal_id}{license_plate_color}{license_plate}".format(**kwargs)


class T8100(JTMessage):
    """Terminal registration response"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8100

    def body_from_hex(self):
        self.__body_data = {
            "serial_no": int(self.__body[:4], 16),
            "registration_result": int(self.__body[4:6], 16),
            "auth_code": ubinascii.unhexlify(self.__body[6:].encode("gbk")).decode("gbk"),
        }


class T0003(JTMessage):
    """Terminal log out"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0003


class T0102(JTMessage):
    """Terminal authentication"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0102

    def set_params(self, auth_code, imei, app_version):
        """
        Args:
            auth_code(str): authentication code
            imei(str): terminal imei
            app_version(str): Manufacturer-defined software version number
        """
        self.__auth_code = ubinascii.hexlify(auth_code.encode("gbk")).decode("gbk")
        self.__auth_len = ""
        self.__imei = ""
        self.__app_version = ""
        if self.is_version():
            self.__auth_len = str_fill(hex(int(len(self.__auth_code) / 2))[2:], target_len=2)
            self.__imei = str_fill(ubinascii.hexlify(imei.encode("gbk")).decode("gbk"), target_len=30)
            self.__app_version = str_fill(ubinascii.hexlify(app_version.encode("gbk")).decode("gbk"), rl="r", target_len=40)

    def body_to_hex(self):
        kwargs = {
            "auth_len": self.__auth_len,
            "auth_code": self.__auth_code,
            "imei": self.__imei,
            "app_version": self.__app_version,
        }
        self.__body = "{auth_len}{auth_code}{imei}{app_version}".format(**kwargs)


class T8103(JTMessage):
    """Set terminal parameters"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8103

    def body_from_hex(self):
        param_count = int(self.__body[:2], 16)
        param_body = self.__body[2:]
        params = []
        for i in range(param_count):
            param_id = int(param_body[:8], 16)
            param_len = int(param_body[8:10], 16)
            param_value = param_body[10:param_len * 2]
            real_value = TerminalParams(param_id, parse=True).convert(param_value)
            params.append((param_id, real_value))
            param_body = param_body[param_len * 2:]
        self.__body_data = {
            "params": params
        }


class T8104(JTMessage):
    """Query terminal params"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8104


class T8106(JTMessage):
    """Query the specified terminal parameters"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8106

    def body_from_hex(self):
        param_count = int(self.__body[:2], 16)
        param_ids_body = self.__body[2:]
        param_ids = []
        for i in range(param_count):
            param_id = int(param_ids_body[i * 8:(i + 1) * 8], 16)
            param_ids.append(param_id)
        self.__body_data = {
            "param_ids": param_ids
        }


class T0104(JTMessage):
    """Query terminal params response"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0104
        self.__params = []

    def set_params(self, response_serial_no):
        self.__response_serial_no = str_fill(hex(response_serial_no)[2:], target_len=4)

    def set_terminal_params(self, param_id, param_value):
        """Set terminal parameter

        Args:
            param_id(int): param id
            param_value(str): `TerminalParams(param_id).value(*arg, **kwargs)`
        """
        kwargs = {
            "param_id": str_fill(hex(param_id)[2:], target_len=4),
            "param_len": str_fill(hex(int(len(param_value) / 2))[2:], target_len=2),
            "param_value": param_value,
        }
        param = "{param_id}{param_len}{param_value}".format(**kwargs)
        self.__params.append(param)

    def body_to_hex(self):
        kwargs = {
            "serial_no": self.__response_serial_no,
            "param_count": str_fill(hex(len(self.__params))[2:], target_len=2),
            "params": "".join(self.__params)
        }
        self.__body = "{serial_no}{param_count}{params}".format(**kwargs)


class T8105(JTMessage):
    """Terminal control"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8105

    def body_from_hex(self):
        """
        body data:
            cmd_word(int): command word
                1 - Wireless upgrade
                2 - Control terminal to connect to the specified server
                3 - terminal power down
                4 - terminal reset
                5 - Terminal reset to factory settings
                6 - Turn off data communication
                7 - Turn off all wireless communications

            cmd_word -- 1:
                url(str): url address (default: "")
                dial_point_name(str): dial point name (default: "")
                dial_user_name(str): dial user name (default: "")
                dial_password(str): dial password (default: "")
                addr: ip or domain (default: "")
                tcp_port: TCP port (default: "")
                udp_port: UDP port (default: "")
                manufacturer_id: manufacturer id (default: "")
                hardware_version: hardware version (default: "")
                firmware_version: firmware version (default: "")
                conn_timeout: Time limit for connecting to the server, unit: minutes (default: "")

            cmd_word -- 2:
                conn_ctrl(int): connection control (default: "")
                    0 - Switch to the designated supervision platform server
                    1 - Switch back to the original default supervision platform server
                auth_code(str): Regulatory platform authentication code (default: "")
                dial_point_name(str): dial point name (default: "")
                dial_user_name(str): dial user name (default: "")
                dial_password(str): dial password (default: "")
                addr: ip or domain (default: "")
                tcp_port: TCP port (default: "")
                udp_port: UDP port (default: "")
                conn_timeout: Time limit for connecting to the server, unit: minutes (default: "")
        """
        cmd_word = int(self.__body[:2], 16)
        cmd_param = ""
        cmd_params = {}
        if cmd_word == 1:
            cmd_param = ubinascii.unhexlify(self.__body[2:].encode("gbk")).decode("gbk")
            cmd_param_list = cmd_param.split(";")
            url, dial_point_name, dial_user_name, dial_password, addr, tcp_port, udp_port, manufacturer_id, \
                hardware_version, firmware_version, conn_timeout = cmd_param_list
            cmd_params["url"] = url
            cmd_params["dial_point_name"] = dial_point_name
            cmd_params["dial_user_name"] = dial_user_name
            cmd_params["dial_password"] = dial_password
            cmd_params["addr"] = addr
            cmd_params["tcp_port"] = tcp_port
            cmd_params["udp_port"] = udp_port
            cmd_params["manufacturer_id"] = manufacturer_id
            cmd_params["hardware_version"] = hardware_version
            cmd_params["firmware_version"] = firmware_version
            cmd_params["conn_timeout"] = conn_timeout
        if cmd_word == 2:
            cmd_param = ubinascii.unhexlify(self.__body[2:].encode("gbk")).decode("gbk")
            cmd_param_list = cmd_param.split(";")
            cmd_params["conn_ctrl"] = cmd_param_list[0]
            if cmd_param_list[0] == 0:
                auth_code, dial_point_name, dial_user_name, dial_password, addr, tcp_port, udp_port, conn_timeout = cmd_param_list[1:]
                cmd_params["auth_code"] = auth_code
                cmd_params["dial_point_name"] = dial_point_name
                cmd_params["dial_user_name"] = dial_user_name
                cmd_params["dial_password"] = dial_password
                cmd_params["addr"] = addr
                cmd_params["tcp_port"] = tcp_port
                cmd_params["udp_port"] = udp_port
                cmd_params["conn_timeout"] = conn_timeout
        self.__body_data = {
            "cmd_word": cmd_word,
            "cmd_params": cmd_params
        }


class T8107(JTMessage):
    """Query terminal attribute request"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8107


class T0107(JTMessage):
    """Query terminal attribute response"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0107

    def set_params(self, applicable_passenger_vehicles, applicable_to_dangerous_goods_vehicles,
                   applicable_to_ordinary_freight_vehicles, applicable_to_taxi, support_hard_disk_video,
                   machine_type, applicable_to_trailer, manufacturer_id, terminal_model, terminal_id,
                   iccid, hardware_version, firmware_version, support_gps, support_bds, support_glonass,
                   support_galileo, support_gprs, support_cdma, support_td_scdma, support_wcdma,
                   support_cdma2000, support_td_lte, support_other_communication):
        """
        Args:
            applicable_passenger_vehicles(int): Whether it is suitable for passenger vehicles. 0 - No, 1 - Yes
            applicable_to_dangerous_goods_vehicles(int): Whether it is suitable for dangerous goods vehicles. 0 - No, 1 - Yes
            applicable_to_ordinary_freight_vehicles(int): Whether it is suitable for ordinary freight vehicles. 0 - No, 1 - Yes
            applicable_to_taxi(int): Whether it is suitable for taxi. 0 - No, 1 - Yes
            support_hard_disk_video(int): Whether to support hard disk video recording. 0 - No, 1 - Yes
            machine_type(int): 0 - one machine, 1 - Split machine
            applicable_to_trailer(int): Whether it is suitable for trailer. 0 - No, 1 - Yes
            manufacturer_id(str): Defined by the manufacturer
            terminal_model(str): Defined by the manufacturer
            terminal_id(str): Defined by the manufacturer
            iccid(str): terminal sim' iccid
            hardware_version(str): hardware version
            firmware_version(str): firmware version
            support_gps(int): Whether to support GPS. 0 - No, 1 - Yes
            support_bds(int): Whether to support BDS. 0 - No, 1 - Yes
            support_glonass(int): Whether to support GLONASS. 0 - No, 1 - Yes
            support_galileo(int): Whether to support GALILEO. 0 - No, 1 - Yes
            support_gprs(int): Whether to support GPRS. 0 - No, 1 - Yes
            support_cdma(int): Whether to support CDMA. 0 - No, 1 - Yes
            support_td_scdma(int): Whether to support TD-SCDMA. 0 - No, 1 - Yes
            support_wcdma(int): Whether to support WCDMA. 0 - No, 1 - Yes
            support_cdma2000(int): Whether to support CDMA2000. 0 - No, 1 - Yes
            support_td_lte(int): Whether to support TD-LTE. 0 - No, 1 - Yes
            support_other_communication(int): Whether to support other communication. 0 - No, 1 - Yes
        """
        terminal_type_kw = {
            "applicable_passenger_vehicles": applicable_passenger_vehicles,
            "applicable_to_dangerous_goods_vehicles": applicable_to_dangerous_goods_vehicles,
            "applicable_to_ordinary_freight_vehicles": applicable_to_ordinary_freight_vehicles,
            "applicable_to_taxi": applicable_to_taxi,
            "support_hard_disk_video": support_hard_disk_video,
            "machine_type": machine_type,
            "applicable_to_trailer": applicable_to_trailer,
        }
        self.__terminal_type = "0b{applicable_to_trailer}{machine_type}{support_hard_disk_video}" \
                               "00{applicable_to_taxi}{applicable_to_ordinary_freight_vehicles}" \
                               "{applicable_to_dangerous_goods_vehicles}{applicable_passenger_vehicles}".format(**terminal_type_kw)
        self.__terminal_type = str_fill(hex(int(self.__terminal_type, 2))[2:], target_len=4)
        self.__manufacturer_id = str_fill(ubinascii.hexlify(str(manufacturer_id[:5]).encode("gbk")).decode("gbk"), target_len=10)
        if self.__protocol_version == 1:
            __terminal_model_len = 60
            __terminal_id_len = 60
        else:
            __terminal_model_len = 40
            __terminal_id_len = 14
        self.__terminal_model = str_fill(ubinascii.hexlify(str(terminal_model[:__terminal_model_len / 2]).encode("gbk")).decode("gbk"), rl="r", target_len=__terminal_model_len)
        self.__terminal_id = str_fill(ubinascii.hexlify(str(terminal_id[:__terminal_id_len / 2]).encode("gbk")).decode("gbk"), rl="r", target_len=__terminal_id_len)
        self.__iccid = iccid
        self.__hardware_version = ubinascii.hexlify(str(hardware_version).encode("gbk")).decode("gbk") if hardware_version else ""
        self.__hardware_version_len = str_fill(hex(int(len(self.__hardware_version) / 2))[2:], target_len=2)
        self.__firmware_version = ubinascii.hexlify(str(firmware_version).encode("gbk")).decode("gbk") if firmware_version else ""
        self.__firmware_version_len = str_fill(hex(int(len(self.__firmware_version) / 2))[2:], target_len=2)
        gnss_properties_kw = {
            "support_galileo": support_galileo,
            "support_glonass": support_glonass,
            "support_gps": support_gps,
            "support_bds": support_bds,
        }
        self.__gnss_properties = "0b{support_galileo}{support_glonass}{support_bds}{support_gps}".format(**gnss_properties_kw)
        self.__gnss_properties = str_fill(hex(int(self.__gnss_properties, 2))[2:], target_len=2)
        communication_module_properties_kw = {
            "support_gprs": support_gprs,
            "support_cdma": support_cdma,
            "support_td_scdma": support_td_scdma,
            "support_wcdma": support_wcdma,
            "support_cdma2000": support_cdma2000,
            "support_td_lte": support_td_lte,
            "support_other_communication": support_other_communication,
        }
        self.__communication_module_properties = "0b{support_other_communication}0{support_td_lte}{support_cdma2000}" \
                                                 "{support_wcdma}{support_td_scdma}{support_cdma}{support_gprs}".format(**communication_module_properties_kw)
        self.__communication_module_properties = str_fill(hex(int(self.__communication_module_properties, 2))[2:], target_len=2)

    def body_to_hex(self):
        kwargs = {
            "terminal_type": self.__terminal_type,
            "manufacturer_id": self.__manufacturer_id,
            "terminal_model": self.__terminal_model,
            "terminal_id": self.__terminal_id,
            "iccid": self.__iccid,
            "hardware_version_len": self.__hardware_version_len,
            "hardware_version": self.__hardware_version,
            "firmware_version_len": self.__firmware_version_len,
            "firmware_version": self.__firmware_version,
            "gnss_properties": self.__gnss_properties,
            "communication_module_properties": self.__communication_module_properties,
        }
        self.__body = "{terminal_type}{manufacturer_id}{terminal_model}{terminal_id}{iccid}" \
                      "{hardware_version_len}{hardware_version}{firmware_version_len}{firmware_version}" \
                      "{gnss_properties}{communication_module_properties}".format(**kwargs)


class T8108(JTMessage):
    """Issue the terminal upgrade package"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8108

    def body_from_hex(self):
        """
        body data:
            upgrade_type(str): upgrade type
                 0 - terminal
                12 - road transport permit ic card reader
                52 - satellite positioning module
            manufacturer_id(str): manufacturer id
            terminal_firmware_verion(str): terminal firmware verion
            upgrade_package(str): upgrade package file with full path.
        """
        upgrade_type = int(self.__body[:2], 16)
        manufacturer_id = ubinascii.unhexlify(self.__body[2:12].encode("gbk")).decode("gbk")
        terminal_firmware_verion_len = int(self.__body[12:14], 16)
        terminal_firmware_verion = ubinascii.unhexlify(self.__body[14:(terminal_firmware_verion_len * 2 + 14)].encode("gbk")).decode("gbk")
        upgrade_package_len = int(self.__body[(terminal_firmware_verion_len * 2 + 14):(terminal_firmware_verion_len * 2 + 22)], 16)
        upgrade_package = ubinascii.unhexlify(self.__body[(terminal_firmware_verion_len * 2 + 22):(terminal_firmware_verion_len * 2 + 22 + upgrade_package_len * 2)].encode("gbk")).decode("gbk")
        self.__body_data = {
            "upgrade_type": upgrade_type,
            "manufacturer_id": manufacturer_id,
            "terminal_firmware_verion": terminal_firmware_verion,
            "upgrade_package": upgrade_package,
        }


class T0108(JTMessage):
    """Terminal upgrade result response"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0108

    def set_params(self, upgrade_type, result_code):
        """
        Args:
            upgrade_type(str): upgrade type
                 0 - terminal
                12 - road transport permit ic card reader
                52 - satellite positioning module
            result_code(int): upgrade result
                0 - success
                1 - failed
                2 - cancel
        """
        self.__upgrade_type = str_fill(hex(upgrade_type)[2:], target_len=2)
        self.__result_code = str_fill(hex(result_code)[2:], target_len=2)

    def body_to_hex(self):
        kwargs = {
            "upgrade_type": self.__upgrade_type,
            "result_code": self.__result_code,
        }
        self.__body = "{upgrade_type}{result_code}".format(**kwargs)


class T0200(JTMessage):
    """Location information report

    When an alarm occurs, the vehicle should report a piece of location information immediately,
    and add the alarm status to the location information.
    """
    def __init__(self):
        super().__init__()
        self.__message_id = 0x0200

    def set_params(self, alarm_flag, loc_status, latitude, longitude, altitude, speed, direction, time, loc_additional_info):
        """
        Args:
            alarm_flag(str): LocAlarmWarningConfig().value()
            loc_status(str): LocStatusConfig().value()
            latitude(float): latitude
            longitude(float): longitude
            altitude(int): unit: meter
            speed(float): unit: km/h, Accurate to 0.1
            direction(int): range: 0~359, 0 is true North, Clockwise.
            time(str): GMT+8, format: YYMMDDhhmmss
            loc_additional_info(str): LocAdditonalInfoConfig().value()
        """
        self.__alarm_flag = alarm_flag
        self.__loc_status = loc_status
        self.__latitude = str_fill(hex(int(latitude * (10 ** 6)))[2:], target_len=8)
        self.__longitude = str_fill(hex(int(longitude * (10 ** 6)))[2:], target_len=8)
        self.__altitude = str_fill(hex(int(altitude))[2:], target_len=4)
        self.__speed = str_fill(hex(int(speed * 10))[2:], target_len=4)
        self.__direction = str_fill(hex(int(direction))[2:], target_len=4)
        self.__time = time
        self.__loc_additional_info = loc_additional_info

    def body_to_hex(self):
        kwargs = {
            "alarm_flag": self.__alarm_flag,
            "loc_status": self.__loc_status,
            "latitude": self.__latitude,
            "longitude": self.__longitude,
            "altitude": self.__altitude,
            "speed": self.__speed,
            "direction": self.__direction,
            "time": self.__time,
            "loc_additional_info": self.__loc_additional_info,
        }
        logger.debug("kwargs: %s" % str(kwargs))
        self.__body = "{alarm_flag}{loc_status}{latitude}{longitude}{altitude}{speed}{direction}{time}{loc_additional_info}".format(**kwargs)


class T8201(JTMessage):
    """Location information query message body"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8201


class T0201(JTMessage):
    """Location information query response"""
    def __init__(self):
        super().__init__()
        self.__message_id = 0x0201

    def set_params(self, response_serial_no, alarm_flag, loc_status, latitude, longitude, altitude, speed, direction, time, loc_additional_info):
        """
        Args:
            response_serial_no(int): 0x8201 serial no.
            alarm_flag(str): LocAlarmWarningConfig().value()
            loc_status(str): LocStatusConfig().value()
            latitude(float): latitude
            longitude(float): longitude
            altitude(int): unit: meter
            speed(float): unit: km/h, Accurate to 0.1
            direction(int): range: 0~359, 0 is true North, Clockwise.
            time(str): GMT+8, format: YYMMDDhhmmss
            loc_additional_info(str): LocAdditonalInfoConfig().value()
        """
        self.__response_serial_no = str_fill(hex(response_serial_no)[2:], target_len=4)
        self.__alarm_flag = alarm_flag
        self.__loc_status = loc_status
        self.__latitude = str_fill(hex(int(latitude * (10 ** 6)))[2:], target_len=8)
        self.__longitude = str_fill(hex(int(longitude * (10 ** 6)))[2:], target_len=8)
        self.__altitude = str_fill(hex(int(altitude))[2:], target_len=4)
        self.__speed = str_fill(hex(int(speed * 10))[2:], target_len=4)
        self.__direction = str_fill(hex(int(direction))[2:], target_len=4)
        self.__time = time
        self.__loc_additional_info = loc_additional_info

    def body_to_hex(self):
        kwargs = {
            "response_serial_no": self.__response_serial_no,
            "alarm_flag": self.__alarm_flag,
            "loc_status": self.__loc_status,
            "latitude": self.__latitude,
            "longitude": self.__longitude,
            "altitude": self.__altitude,
            "speed": self.__speed,
            "direction": self.__direction,
            "time": self.__time,
            "loc_additional_info": self.__loc_additional_info,
        }
        logger.debug("kwargs: %s" % str(kwargs))
        self.__body = "{response_serial_no}{alarm_flag}{loc_status}{latitude}{longitude}{altitude}{speed}{direction}{time}{loc_additional_info}".format(**kwargs)


class T8202(JTMessage):
    """Temporary position tracking control"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8202

    def body_from_hex(self):
        """
        body data:
            time_interval(int): unit: seconds
            location_tracking_validity_period(int): unit: seconds
        """
        time_interval = int(self.__body[:4], 16)
        location_tracking_validity_period = -1
        if time_interval != 0:
            location_tracking_validity_period = int(self.__body[4:], 16)
        self.__body_data = {
            "time_interval": time_interval,
            "location_tracking_validity_period": location_tracking_validity_period,
        }


class T8203(JTMessage):
    """Manual confirmation alarm message data format"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8203

    def body_from_hex(self):
        """
        body data:
            alarm_msg_serial_no: 1 - confirm
            alarm_type: 1 - confirm
            emergency_alarm: 1 - confirm
            hazard_alarm: 1 - confirm
            in_out_area_alarm: 1 - confirm
            in_out_road_alarm: 1 - confirm
            insufficient_or_too_long_travel_time_on_the_road_alarm: 1 - confirm
            vehicle_illegal_ignition_alarm: 1 - confirm
            vehicle_illegal_displacement_alarm: 1 - confirm
        """
        alarm_msg_serial_no = int(self.__body[:4], 16)
        alarm_type = str_fill(bin(int(self.__body[4:], 16))[2:], target_len=32)
        emergency_alarm = int(alarm_type[-1])
        hazard_alarm = int(alarm_type[-4])
        in_out_area_alarm = int(alarm_type[-21])
        in_out_road_alarm = int(alarm_type[-22])
        insufficient_or_too_long_travel_time_on_the_road_alarm = int(alarm_type[-23])
        vehicle_illegal_ignition_alarm = int(alarm_type[-28])
        vehicle_illegal_displacement_alarm = int(alarm_type[-29])
        self.__body_data = {
            "alarm_msg_serial_no": alarm_msg_serial_no,
            "alarm_type": alarm_type,
            "emergency_alarm": emergency_alarm,
            "hazard_alarm": hazard_alarm,
            "in_out_area_alarm": in_out_area_alarm,
            "in_out_road_alarm": in_out_road_alarm,
            "insufficient_or_too_long_travel_time_on_the_road_alarm": insufficient_or_too_long_travel_time_on_the_road_alarm,
            "vehicle_illegal_ignition_alarm": vehicle_illegal_ignition_alarm,
            "vehicle_illegal_displacement_alarm": vehicle_illegal_displacement_alarm,
        }


class T8204(JTMessage):
    """Link detection"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8204


class T8300(JTMessage):
    """Text message delivery"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8300

    def body_from_hex(self):
        """
        body_data:
            flag_type(int): 1 - service, 2 - emergency, 3 - notice
            terminal_display(int): 1 - terminal display
            terminal_tts_broadcast_and_read(int): 1 - terminal tts broadcast and read
            flag_msg_type(int): 0 - Center Navigation Information, 1 - CAN fault code information
            msg_type(int): 1 - notice, 2 - service
            message(str): message infomation
        """
        flag = str_fill(bin(int(self.__body[:2], 16))[2:], target_len=8)
        flag_type = int(flag[-2:], 2) if self.is_version() else int(flag[-1], 2)
        terminal_display = int(flag[-3])
        terminal_tts_broadcast_and_read = int(flag[-4])
        flag_msg_type = int(flag[-6])
        msg_type = int(self.__body[2:4], 16) if self.is_version() else 0
        message = ubinascii.unhexlify(self.__body[4 if self.is_version() else 2:]).decode("gbk")
        self.__body_data = {
            "flag": flag,
            "flag_type": flag_type,
            "terminal_display": terminal_display,
            "terminal_tts_broadcast_and_read": terminal_tts_broadcast_and_read,
            "flag_msg_type": flag_msg_type,
            "msg_type": msg_type,
            "message": message,
        }


class T8301(JTMessage):
    """Set event"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8301

    def body_from_hex(self):
        """
        body_data:
            set_type(int):
                0 - delete terminal all events
                1 - update events
                2 - add events
                3 - change events
                4 - delete the specified event
            events(list):
                item(dict):
                    id(int): event id
                    data(str): event infomation
        """
        set_type = int(self.__body[:2], 16)
        total_num = int(self.__body[2:4], 16)
        event_body = self.__body[4:]
        events = []
        for i in range(total_num):
            event = {}
            event["id"] = int(event_body[:2], 16)
            event_info_len = int(event_body[2:4], 16)
            event["data"] = ubinascii.unhexlify(event_body[4:4 + event_info_len * 2]).decode("gbk")
            event_body = event_body[4 + event_info_len * 2:]
            events.append(event)
        self.__body_data = {
            "set_type": set_type,
            "events": events,
        }


class T0301(JTMessage):
    """Event report"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0301

    def set_params(self, event_id):
        """
        Args:
            event_id(int): event id.
        """
        self.__event_id = str_fill(hex(event_id)[2:], target_len=2)

    def body_to_hex(self):
        kwargs = {
            "event_id": self.__event_id,
        }
        self.__body = "{event_id}".format(**kwargs)


class T8302(JTMessage):
    """Issue a question"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8302

    def body_from_hex(self):
        """
        body_data:
            flag(dict):
                emergency(int): 0 - off, 1 - on
                terminal_tts_broadcast_and_read(int): 0 - off, 1 - on
                Advertising_screen_display(int): 0 - off, 1 - on
            question_info(str): question infomation
            answers(list):
                item(dict):
                    id(int): answer id
                    data(str): answer infomation
        """
        flag = str_fill(bin(int(self.__body[:2], 16))[2:], target_len=8)
        emergency = int(flag[-1])
        terminal_tts_broadcast_and_read = int(flag[-4])
        Advertising_screen_display = int(flag[-5])
        question_info_len = int(self.__body[2:4], 16)
        question_info = ubinascii.unhexlify(self.__body[4: 4 + question_info_len * 2]).decode("gbk")
        answers = []
        answer_body = self.__body[4 + question_info_len * 2:]
        while answer_body:
            answer = {}
            answer["id"] = int(answer_body[:2], 16)
            answer_len = int(answer_body[2:6], 16)
            answer["data"] = ubinascii.unhexlify(answer_body[6:6 + answer_len * 2]).decode("gbk")
            answer_body = answer_body[6 + answer_len * 2:]
            answers.append(answer)
        self.__body_data = {
            "flag": {
                "emergency": emergency,
                "terminal_tts_broadcast_and_read": terminal_tts_broadcast_and_read,
                "Advertising_screen_display": Advertising_screen_display,
            },
            "question_info": question_info,
            "answers": answers,
        }


class T0302(JTMessage):
    """Issue a question response"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0302

    def set_params(self, response_serial_no, answer_id):
        """
        Args:
            response_serial_no(int): response serial no.
            answer_id(int): event id.
        """
        self.__response_serial_no = str_fill(hex(response_serial_no)[2:], target_len=4)
        self.__answer_id = str_fill(hex(answer_id)[2:], target_len=2)

    def body_to_hex(self):
        kwargs = {
            "response_serial_no": self.__response_serial_no,
            "answer_id": self.__answer_id,
        }
        self.__body = "{response_serial_no}{answer_id}".format(**kwargs)


class T8303(JTMessage):
    """Information on demand menu settings"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8303

    def body_from_hex(self):
        """
        body_data:
            set_type(int):
                0 - delete terminal all events
                1 - update events
                2 - add events
                3 - change events
            infos(list):
                item(dict):
                    type(int): info type
                    name(str): info name
        """
        set_type = int(self.__body[:2], 16)
        total_num = int(self.__body[2:4], 16)
        info_body = self.__body[4:]
        infos = []
        for i in range(total_num):
            info = {}
            info["type"] = int(info_body[:2], 16)
            info_name_len = int(info_body[2:6], 16)
            info["name"] = ubinascii.unhexlify(info_body[6:6 + info_name_len * 2]).decode("gbk")
            info_body = info_body[6 + info_name_len * 2:]
            infos.append(info)
        self.__body_data = {
            "set_type": set_type,
            "infos": infos,
        }


class T0303(JTMessage):
    """Information on demand/cancellation"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0303

    def set_params(self, info_type, onoff):
        """
        Args:
            info_type(int): info type.
            onoff(int):
                0 - cancel
                1 - demand
        """
        self.__info_type = str_fill(hex(info_type)[2:], target_len=2)
        self.__onoff = str_fill(hex(onoff)[2:], target_len=2)

    def body_to_hex(self):
        kwargs = {
            "info_type": self.__info_type,
            "onoff": self.__onoff,
        }
        self.__body = "{info_type}{onoff}".format(**kwargs)


class T8304(JTMessage):
    """Information service"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8304

    def body_from_hex(self):
        """
        body_data:
            info_type(int): info type
            info_data(str): info data
        """
        info_type = int(self.__body[:2], 16)
        info_len = int(self.__body[2:6], 16)
        info_data = ubinascii.unhexlify(self.__body[6:6 + info_len * 2]).decode("gbk")
        self.__body_data = {
            "info_type": info_type,
            "info_data": info_data,
        }


class T8400(JTMessage):
    """Call back"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8400

    def body_from_hex(self):
        flag = int(self.__body[:2], 16)
        phone_number = ubinascii.unhexlify(self.__body[2:]).decode("gbk")
        self.__body_data = {
            "flag": flag,
            "phone_number": phone_number,
        }


class T8401(JTMessage):
    """Set up phonebook"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8401

    def body_from_hex(self):
        """
        body_data:
            set_type(int):
                0 - delete all concat user
                1 - delete all concat user and add concat usr
                2 - add concat usr
                4 - edit concat usr by user name
            phonebook(list):
                item(dict):
                    call_type(int):
                        1 - call in
                        2 - call out
                        3 - call in/out
                    phone(str): phone number
                    concat_user(str): concat user name
        """
        set_type = int(self.__body[:2], 16)
        total_concat = int(self.__body[2:4], 16)
        concat_infos = self.__body[4:]
        phonebook = []
        for i in range(total_concat):
            item = {}
            item["call_type"] = int(concat_infos[:2], 16)
            phone_len = int(concat_infos[2:4], 16)
            item["phone"] = ubinascii.unhexlify(concat_infos[4:(4 + phone_len * 2)]).decode("gbk")
            concat_user_len = int(concat_infos[(4 + phone_len * 2):(6 + phone_len * 2)], 16)
            item["concat_user"] = ubinascii.unhexlify(concat_infos[(6 + phone_len * 2):(6 + phone_len * 2 + concat_user_len * 2)]).decode("gbk")
            concat_infos = concat_infos[6 + phone_len * 2 + concat_user_len * 2:]
            phonebook.append(item)
        self.__body_data = {
            "set_type": set_type,
            "phonebook": phonebook,
        }


class T8500(JTMessage):
    """Vehicle control

    The message depends on the specific control information data defined by the server
    """

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8500

    def body_from_hex(self):
        """
        control type data:
            0x0001: 0 - door lock, 1 - door open

        body_data:
            data(list):
                item(dict):
                    id(int): control type id.
                    param(int): control param.
        """
        control_infos = []
        if self.is_version():
            control_num = int(self.__body[:4], 16)
            control_data = self.__body[4:]
            for i in range(control_num):
                _id = int(control_data[:4], 16)
                # TODO: This param length depends on server, default 2.
                _param = int(control_data[4:6], 16)
                control_infos.append(({"id": _id, "param": _param}))
        else:
            control_flag = bin(int(self.__body[:2], 16))[2:]
            control_infos.append({"id": 0x0001, "param": int(control_flag[-1])})
        self.__body_data = {
            "data": control_infos
        }


class T0500(T0201):
    """Vehicle control response"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0500


class T8600(JTMessage):
    """Set up the prototype area

    NOTE: This message's source body need to save for 0x8608 message query.
    """

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8600

    def body_from_hex(self):
        """
        body_data:
            set_attr(int): 0 - delete & add, 1 - add, 2 - update
            area_data(list):
                item(dict):
                    area_id(int): area id
                    attributes(dict):
                        time_limit_enable(int): 0 - off, 1 - on
                        speed_limit_enable(int): 0 - off, 1 - on
                        alert_driver_when_entering_area(int): 0 - off, 1 - on
                        alert_platform_when_entering_area(int): 0 - off, 1 - on
                        alert_driver_when_leaving_area(int): 0 - off, 1 - on
                        alert_platform_when_leaving_area(int): 0 - off, 1 - on
                        latitude_direction(int): 0 - north, 1 - south
                        longitude_direction(int): 0 - east, 1 - western
                        open_the_door_enable(int): 0 - allow open the door, 1 - not allow open the door
                        communication_module_enable_when_entering_area(int): 0 - on, 1 - off
                        gnss_enable_when_entering_area(int): 0 - off, 1 - on
                    center_latitude(float): center latitude
                    center_longitude(float): center longitude
                    radius(int): radius, unit: meter
                    start_time(str): YYMMDDhhmmss if time_limit_enable is not 0 else empty string
                    end_time(str): YYMMDDhhmmss if time_limit_enable is not 0 else empty string
                    speed_limit(int): Top speed, unit: km/h. value is -1 if speed_limit_enable is 0
                    over_speed_time(int): Overspeed Continues Practical, unit: seconds. value is -1 if speed_limit_enable is 0
                    night_speed_limit(int): Top speed at night, unit: km/h. value is -1 if speed_limit_enable is 0
                    area_name(str): area name
        """
        set_attr = int(self.__body[:2], 16)
        total_area = int(self.__body[2:4], 16)
        area_info = self.__body[4:]
        area_data = []
        for i in range(total_area):
            area_item = {}
            area_item["area_id"] = int(area_info[:8], 16)
            area_attr = str_fill(bin(int(area_info[8:12], 16))[2:], target_len=16)
            area_item["attributes"] = {}
            area_item["attributes"]["time_limit_enable"] = int(area_attr[-1])
            area_item["attributes"]["speed_limit_enable"] = int(area_attr[-2])
            area_item["attributes"]["alert_driver_when_entering_area"] = int(area_attr[-3])
            area_item["attributes"]["alert_platform_when_entering_area"] = int(area_attr[-4])
            area_item["attributes"]["alert_driver_when_leaving_area"] = int(area_attr[-5])
            area_item["attributes"]["alert_platform_when_leaving_area"] = int(area_attr[-6])
            area_item["attributes"]["latitude_direction"] = int(area_attr[-7])
            area_item["attributes"]["longitude_direction"] = int(area_attr[-8])
            area_item["attributes"]["open_the_door_enable"] = int(area_attr[-9])
            area_item["attributes"]["communication_module_enable_when_entering_area"] = int(area_attr[-15])
            area_item["attributes"]["gnss_enable_when_entering_area"] = int(area_attr[-16])
            area_item["center_latitude"] = int(area_info[12:20], 16) / (10 ** 6)
            area_item["center_longitude"] = int(area_info[20:28], 16) / (10 ** 6)
            area_item["radius"] = int(area_info[28:36], 16)
            area_info = area_info[36:]
            area_item["start_time"] = ""
            area_item["end_time"] = ""
            if area_item["attributes"]["time_limit_enable"] == 1:
                area_item["start_time"] = area_info[:12]
                area_item["end_time"] = area_info[12:24]
                area_info = area_info[24:]
            area_item["speed_limit"] = 0
            area_item["over_speed_time"] = 0
            area_item["night_speed_limit"] = 0
            area_item["area_name"] = ""
            if area_item["attributes"]["speed_limit_enable"] == 1:
                area_item["speed_limit"] = int(area_info[:4], 16)
                area_item["over_speed_time"] = int(area_info[4:6], 16)
                if self.is_version() is True:
                    area_item["night_speed_limit"] = int(area_info[6:10], 16) if area_info[6:10] else 0
                    area_info = area_info[10:]
                else:
                    area_info = area_info[6:]
            if self.is_version() is True:
                area_name_len = int(area_info[:4], 16) if area_info[:4] else 0
                area_item["area_name"] = ubinascii.unhexlify(area_info[4:4 + area_name_len * 2]).decode("gbk")
                area_info = area_info[4 + area_name_len * 2:]
            area_data.append(area_item)
        self.__body_data = {
            "set_attr": set_attr,
            "area_data": area_data,
            "source_body": self.__body,
        }


class T8601(JTMessage):
    """Delete the prototype area"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8601

    def body_from_hex(self):
        """
        body_data:
            all(int): 1 - delete all, 0 - delete specified area id
            area_ids(list): empty list if all is 1
                item(int): area id
        """
        area_num = int(self.__body[:2], 16)
        area_id_data = self.__body[2:]
        area_ids = [int(area_id_data[i * 8:(i + 1) * 8], 16) for i in range(area_num)]
        self.__body_data = {
            "all": 1 if area_num == 0 else 0,
            "area_ids": area_ids,
        }


class T8602(JTMessage):
    """Set up the rectangular area

    NOTE: This message's source body need to save for 0x8608 message query.
    """

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8602

    def body_from_hex(self):
        """
        body_data:
            set_attr(int): 0 - delete & add, 1 - add, 2 - update
            area_data(list):
                item(dict):
                    area_id(int): area id
                    attributes(dict):
                        time_limit_enable(int): 0 - off, 1 - on
                        speed_limit_enable(int): 0 - off, 1 - on
                        alert_driver_when_entering_area(int): 0 - off, 1 - on
                        alert_platform_when_entering_area(int): 0 - off, 1 - on
                        alert_driver_when_leaving_area(int): 0 - off, 1 - on
                        alert_platform_when_leaving_area(int): 0 - off, 1 - on
                        latitude_direction(int): 0 - north, 1 - south
                        longitude_direction(int): 0 - east, 1 - western
                        open_the_door_enable(int): 0 - allow open the door, 1 - not allow open the door
                        communication_module_enable_when_entering_area(int): 0 - on, 1 - off
                        gnss_enable_when_entering_area(int): 0 - off, 1 - on
                    upper_left_latitude(float): upper left latitude
                    upper_left_longitude(float): upper left longitude
                    lower_right_latitude(float): lower right latitude
                    lower_right_longitude(float): lower right longitude
                    start_time(str): YYMMDDhhmmss if time_limit_enable is not 0 else empty string
                    end_time(str): YYMMDDhhmmss if time_limit_enable is not 0 else empty string
                    speed_limit(int): Top speed, unit: km/h. value is -1 if speed_limit_enable is 0
                    over_speed_time(int): Overspeed Continues Practical, unit: seconds. value is -1 if speed_limit_enable is 0
                    night_speed_limit(int): Top speed at night, unit: km/h. value is -1 if speed_limit_enable is 0
                    area_name(str): area name
        """
        set_attr = int(self.__body[:2], 16)
        total_area = int(self.__body[2:4], 16)
        area_info = self.__body[4:]
        area_data = []
        for i in range(total_area):
            area_item = {}
            area_item["area_id"] = int(area_info[:8], 16)
            area_attr = str_fill(bin(int(area_info[8:12], 16))[2:], target_len=16)
            area_item["attributes"] = {}
            area_item["attributes"]["time_limit_enable"] = int(area_attr[-1])
            area_item["attributes"]["speed_limit_enable"] = int(area_attr[-2])
            area_item["attributes"]["alert_driver_when_entering_area"] = int(area_attr[-3])
            area_item["attributes"]["alert_platform_when_entering_area"] = int(area_attr[-4])
            area_item["attributes"]["alert_driver_when_leaving_area"] = int(area_attr[-5])
            area_item["attributes"]["alert_platform_when_leaving_area"] = int(area_attr[-6])
            area_item["attributes"]["latitude_direction"] = int(area_attr[-7])
            area_item["attributes"]["longitude_direction"] = int(area_attr[-8])
            area_item["attributes"]["open_the_door_enable"] = int(area_attr[-9])
            area_item["attributes"]["communication_module_enable_when_entering_area"] = int(area_attr[-15])
            area_item["attributes"]["gnss_enable_when_entering_area"] = int(area_attr[-16])
            area_item["upper_left_latitude"] = int(area_info[12:20], 16) / (10 ** 6)
            area_item["upper_left_longitude"] = int(area_info[20:28], 16) / (10 ** 6)
            area_item["lower_right_latitude"] = int(area_info[28:36], 16) / (10 ** 6)
            area_item["lower_right_longitude"] = int(area_info[36:44], 16) / (10 ** 6)
            area_info = area_info[44:]
            area_item["start_time"] = ""
            area_item["end_time"] = ""
            if area_item["attributes"]["time_limit_enable"] == 1:
                area_item["start_time"] = area_info[:12]
                area_item["end_time"] = area_info[12:24]
                area_info = area_info[24:]
            area_item["speed_limit"] = 0
            area_item["over_speed_time"] = 0
            area_item["night_speed_limit"] = 0
            area_item["area_name"] = ""
            if area_item["attributes"]["speed_limit_enable"] == 1:
                area_item["speed_limit"] = int(area_info[:4], 16)
                area_item["over_speed_time"] = int(area_info[4:6], 16)
                if self.is_version() is True:
                    area_item["night_speed_limit"] = int(area_info[6:10], 16) if area_info[6:10] else 0
                    area_info = area_info[10:]
                else:
                    area_info = area_info[6:]
            if self.is_version() is True:
                area_name_len = int(area_info[:4], 16) if area_info[:4] else 0
                area_item["area_name"] = ubinascii.unhexlify(area_info[4:4 + area_name_len * 2]).decode("gbk")
                area_info = area_info[4 + area_name_len * 2:]
            area_data.append(area_item)
        self.__body_data = {
            "set_attr": set_attr,
            "area_data": area_data,
            "source_body": self.__body,
        }


class T8603(T8601):
    """Delete the rectangular area"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8603


class T8604(JTMessage):
    """Set up the polygon area

    NOTE: This message's source body need to save for 0x8608 message query.
    """

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8604

    def body_from_hex(self):
        """
        body_data:
            area_data(dict):
                area_id(int): area id
                attributes(dict):
                    time_limit_enable(int): 0 - off, 1 - on
                    speed_limit_enable(int): 0 - off, 1 - on
                    alert_driver_when_entering_area(int): 0 - off, 1 - on
                    alert_platform_when_entering_area(int): 0 - off, 1 - on
                    alert_driver_when_leaving_area(int): 0 - off, 1 - on
                    alert_platform_when_leaving_area(int): 0 - off, 1 - on
                    latitude_direction(int): 0 - north, 1 - south
                    longitude_direction(int): 0 - east, 1 - western
                    open_the_door_enable(int): 0 - allow open the door, 1 - not allow open the door
                    communication_module_enable_when_entering_area(int): 0 - on, 1 - off
                    gnss_enable_when_entering_area(int): 0 - off, 1 - on
                start_time(str): YYMMDDhhmmss if time_limit_enable is not 0 else empty string
                end_time(str): YYMMDDhhmmss if time_limit_enable is not 0 else empty string
                speed_limit(int): Top speed, unit: km/h. value is -1 if speed_limit_enable is 0
                over_speed_time(int): Overspeed Continues Practical, unit: seconds. value is -1 if speed_limit_enable is 0
                point_loction(list):
                    item(dict):
                        latitude(float)
                        longitude(float)
                night_speed_limit(int): Top speed at night, unit: km/h. value is -1 if speed_limit_enable is 0
                area_name(str): area name
        """
        area_info = self.__body
        area_data = {}
        area_data["area_id"] = int(area_info[:8], 16)
        area_attr = str_fill(bin(int(area_info[8:12], 16))[2:], target_len=16)
        area_data["attributes"] = {}
        area_data["attributes"]["time_limit_enable"] = int(area_attr[-1])
        area_data["attributes"]["speed_limit_enable"] = int(area_attr[-2])
        area_data["attributes"]["alert_driver_when_entering_area"] = int(area_attr[-3])
        area_data["attributes"]["alert_platform_when_entering_area"] = int(area_attr[-4])
        area_data["attributes"]["alert_driver_when_leaving_area"] = int(area_attr[-5])
        area_data["attributes"]["alert_platform_when_leaving_area"] = int(area_attr[-6])
        area_data["attributes"]["latitude_direction"] = int(area_attr[-7])
        area_data["attributes"]["longitude_direction"] = int(area_attr[-8])
        area_data["attributes"]["open_the_door_enable"] = int(area_attr[-9])
        area_data["attributes"]["communication_module_enable_when_entering_area"] = int(area_attr[-15])
        area_data["attributes"]["gnss_enable_when_entering_area"] = int(area_attr[-16])
        area_info = area_info[12:]
        area_data["start_time"] = ""
        area_data["end_time"] = ""
        if area_data["attributes"]["time_limit_enable"] == 1:
            area_data["start_time"] = area_info[:12]
            area_data["end_time"] = area_info[12:24]
            area_info = area_info[24:]
        area_data["speed_limit"] = 0
        area_data["over_speed_time"] = 0
        if area_data["attributes"]["speed_limit_enable"] == 1:
            area_data["speed_limit"] = int(area_info[:4], 16)
            area_data["over_speed_time"] = int(area_info[4:6], 16)
            area_info = area_info[6:]

        area_point_num = int(area_info[:4], 16)
        area_info = area_info[4:]
        area_data["point_loction"] = []
        for i in range(area_point_num):
            latitude = int(area_info[:8], 16) / (10 ** 6)
            longitude = int(area_info[8:16], 16) / (10 ** 6)
            area_data["point_loction"].append({"latitude": latitude, "longitude": longitude})
            area_info = area_info[16:]

        area_data["night_speed_limit"] = 0
        area_data["area_name"] = ""
        if area_data["attributes"]["speed_limit_enable"] == 1:
            if self.is_version() is True:
                area_data["night_speed_limit"] = int(area_info[:4], 16)
                area_info = area_info[4:]

        if self.is_version() is True:
            area_name_len = int(area_info[:4], 16) if area_info[:4] else 0
            area_data["area_name"] = ubinascii.unhexlify(area_info[4:4 + area_name_len * 2]).decode("gbk")

        self.__body_data = {
            "area_data": area_data,
            "source_body": self.__body,
        }


class T8605(T8601):
    """Delete the polygon area"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8605


class T8606(JTMessage):
    """Set up the route

    NOTE: This message's source body need to save for 0x8608 message query.
    """

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8606

    def body_from_hex(self):
        """
        body_data:
            route_data(dict):
                route_id(int): route id
                attributes(dict):
                    time_limit_enable(int): 0 - off, 1 - on
                    alert_driver_when_entering_area(int): 0 - off, 1 - on
                    alert_platform_when_entering_area(int): 0 - off, 1 - on
                    alert_driver_when_leaving_area(int): 0 - off, 1 - on
                    alert_platform_when_leaving_area(int): 0 - off, 1 - on
                start_time(str): YYMMDDhhmmss if time_limit_enable is not 0 else empty string
                end_time(str): YYMMDDhhmmss if time_limit_enable is not 0 else empty string
                turning_points(list):
                    item(dict):
                        turning_point_id(int): turning point id
                        road_section_id(int): road section id
                        turning_point_latitude(float): turning point latitude
                        turning_point_longitude(float): turning point longitude
                        road_section_width(int): road section width, unit: meter
                        attributes(dict): road section attributes
                            driving_time_limit_enable(int): 0 - off, 1 - on
                            speed_limit_enable(int): 0 - off, 1 - on
                            latitude_direction(int): 0 - north, 1 - south
                            longitude_direction(int): 0 - east, 1 - western
                        driving_too_long_time_limit(int): unit seconds, value is -1 if driving_time_limit_enable is 0
                        insufficient_travel_time_limit(int): unit seconds, value is -1 if driving_time_limit_enable is 0
                        speed_limit(int): unit: km/h, , value is -1 if speed_limit_enable is 0
                        over_speed_time(int): unit: seconds, , value is -1 if speed_limit_enable is 0
                        night_speed_limit(int): unit: km/h, , value is -1 if speed_limit_enable is 0
                route_name(str): area name
        """
        route_info = self.__body
        route_data = {}
        route_data["route_id"] = int(route_info[:8], 16)
        area_attr = str_fill(bin(int(route_info[8:12], 16))[2:], target_len=16)
        route_data["attributes"] = {}
        route_data["attributes"]["time_limit_enable"] = int(area_attr[-1])
        route_data["attributes"]["alert_driver_when_entering_route"] = int(area_attr[-3])
        route_data["attributes"]["alert_platform_when_entering_route"] = int(area_attr[-4])
        route_data["attributes"]["alert_driver_when_leaving_route"] = int(area_attr[-5])
        route_data["attributes"]["alert_platform_when_leaving_route"] = int(area_attr[-6])
        route_info = route_info[12:]
        route_data["start_time"] = ""
        route_data["end_time"] = ""
        if route_data["attributes"]["time_limit_enable"] == 1:
            route_data["start_time"] = route_info[:12]
            route_data["end_time"] = route_info[12:24]
            route_info = route_info[24:]

        route_turning_points = int(route_info[:4], 16)
        route_info = route_info[4:]
        route_data["turning_points"] = []
        for i in range(route_turning_points):
            item = {}
            item["turning_point_id"] = int(route_info[:8], 16)
            item["road_section_id"] = int(route_info[8:16], 16)
            item["turning_point_latitude"] = int(route_info[16:24], 16) / (10 ** 6)
            item["turning_point_longitude"] = int(route_info[24:32], 16) / (10 ** 6)
            item["road_section_width"] = int(route_info[32:34], 16)
            road_section_attr = str_fill(bin(int(route_info[34:36], 16))[2:], target_len=8)
            item["attributes"] = {}
            item["attributes"]["driving_time_limit_enable"] = int(road_section_attr[-1])
            item["attributes"]["speed_limit_enable"] = int(road_section_attr[-2])
            item["attributes"]["latitude_direction"] = int(road_section_attr[-3])
            item["attributes"]["longitude_direction"] = int(road_section_attr[-4])
            route_info = route_info[36:]
            item["driving_too_long_time_limit"] = -1
            item["insufficient_travel_time_limit"] = -1
            if item["attributes"]["driving_time_limit_enable"] == 1:
                item["driving_too_long_time_limit"] = int(route_info[:4], 16)
                item["insufficient_travel_time_limit"] = int(route_info[4:8], 16)
                route_info = route_info[8:]
            item["speed_limit"] = 0
            item["over_speed_time"] = 0
            item["night_speed_limit"] = 0
            if item["attributes"]["speed_limit_enable"] == 1:
                item["speed_limit"] = int(route_info[:4], 16)
                item["over_speed_time"] = int(route_info[4:6], 16)
                if self.is_version() is True:
                    item["night_speed_limit"] = int(route_info[6:10], 16)
                    route_info = route_info[10:]
                else:
                    route_info = route_info[6:]
            route_data["turning_points"].append(item)

        route_data["route_name"] = ""
        if self.is_version() is True:
            area_name_len = int(route_info[:4], 16) if route_info[:4] else 0
            route_data["route_name"] = ubinascii.unhexlify(route_info[4:4 + area_name_len * 2]).decode("gbk")
        self.__body_data = {
            "route_data": route_data,
            "source_body": self.__body,
        }


class T8607(JTMessage):
    """Delete the route"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8607

    def body_from_hex(self):
        """
        body_data:
            all(int): 1 - delete all, 0 - delete specified route id
            route_ids(list): empty list if all is 1
                item(int): route id
        """
        route_num = int(self.__body[:2], 16)
        route_id_data = self.__body[2:]
        route_ids = [int(route_id_data[i * 8:(i + 1) * 8], 16) for i in range(route_num)]
        self.__body_data = {
            "all": 1 if route_num == 0 else 0,
            "route_ids": route_ids,
        }


class T8608(JTMessage):
    """Query area or route data"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8608

    def body_from_hex(self):
        """
        body_data:
            query_type(int):
                1 - prototype area
                2 - rectangular area
                3 - polygon area
                4 - route
            ids(list):
                item(int): area or route id
        """
        query_type = int(self.__body[:2], 16)
        query_num = int(self.__body[2:10], 16)
        query_id_info = self.__body[10:]
        ids = [int(query_id_info[i * 8:(i + 1) * 8], 16) for i in range(query_num)]
        self.__body_data = {
            "query_type": query_type,
            "ids": ids,
        }


class T0608(JTMessage):
    """Query area or route data response"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0608

    def set_params(self, query_type, data):
        """
        Args:
            query_type(int):
                1 - prototype area
                2 - rectangular area
                3 - polygon area
                4 - route
            data(list):
                item(str):
                    query_type is 1, item is T8600().__body
                    query_type is 2, item is T8602().__body
                    query_type is 3, item is T8604().__body
                    query_type is 4, item is T8606().__body
        """
        self.__query_type = str_fill(hex(query_type)[2:], target_len=2)
        self.__data_len = str_fill(hex(len(data))[2:], target_len=8)
        self.__data = "".join(data)

    def body_to_hex(self):
        kwargs = {
            "query_type": self.__query_type,
            "data_len": self.__data_len,
            "data": self.__data,
        }
        self.__body = "{query_type}{data_len}{data}".format(**kwargs)


class T8700(JTMessage):
    """Driving record data collection"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8700

    def body_from_hex(self):
        """
        body_data:
            cmd_word(int):
                33: driving status record
                34: accident record
                35: overtime driving record
                36: driver record
                37: logging record
            cmd_data(bytes): record file bytes data
        """
        cmd_word = int(self.__body[:2], 16) if self.__body[:2] else 0
        cmd_data = ""
        if self.__body[2:]:
            cmd_data = ubinascii.unhexlify(self.__body[2:])
        self.__body_data = {
            "cmd_word": cmd_word,
            "cmd_data": cmd_data,
        }


class T0700(JTMessage):
    """Driving record data upload"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0700

    def set_params(self, response_serial_no, cmd_word, cmd_data):
        """
        Args:
            response_serial_no(int): 0x8700 serial no.
            cmd_word(int):
                33: driving status record
                34: accident record
                35: overtime driving record
                36: driver record
                37: logging record
            cmd_data(bytes): read record file bytes data
        """
        self.__response_serial_no = str_fill(hex(response_serial_no)[2:], target_len=4)
        self.__cmd_word = str_fill(hex(cmd_word)[2:], target_len=2)
        self.__cmd_data = ubinascii.hexlify(cmd_data).decode("gbk")

    def body_to_hex(self):
        kwargs = {
            "response_serial_no": self.__response_serial_no,
            "cmd_word": self.__cmd_word,
            "cmd_data": self.__cmd_data,
        }
        self.__body = "{response_serial_no}{cmd_word}{cmd_data}".format(**kwargs)


class T8701(JTMessage):
    """Form record parameter download"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8701

    def body_from_hex(self):
        """
        body_data:
            cmd_word(int):
                33: driving status record
                34: accident record
                35: overtime driving record
                36: driver record
                37: logging record
            cmd_data(bytes): record file bytes data
        """
        cmd_word = int(self.__body[:2], 16)
        cmd_data = ""
        if self.__body[2:]:
            cmd_data = ubinascii.unhexlify(self.__body[2:])
        self.__body_data = {
            "cmd_word": cmd_word,
            "cmd_data": cmd_data,
        }


class T0701(JTMessage):
    """Electronic Waybill Reporting"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0701

    def set_params(self, data):
        """
        Args:
            data(bytes): Electronic Waybill data.
        """
        self.__data = ubinascii.hexlify(data).decode("gbk")
        self.__data_len = str_fill(hex(int(len(self.__data) / 2))[2:], target_len=8)

    def body_to_hex(self):
        kwargs = {
            "data_len": self.__data_len,
            "data": self.__data,
        }
        self.__body = "{data_len}{data}".format(**kwargs)


class T8702(JTMessage):
    """Report driver identification information request"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8702


class T0702(JTMessage):
    """Collect and report driver identity information"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0702

    def set_params(self, status, time, ic_read_result, driver_name, qualification_certificate_code,
                   issuing_agency_name, certificate_validity, driver_id_number):
        """
        Args:
            status(int):
                0x01 - Practicing qualification certificate IC card insertion(driver goes to work)
                0x02 - Practicing qualification certificate IC card pulled out(driver off duty)
            time(str): YYMMDDhhmmss, IC card in/out time.
            ic_read_result(int):
                0x00 - IC card read success.
                0x01 - Card reading failed, key authentication failed.
                0x02 - Card reading failed, Card is locked.
                0x03 - Card reading failed, card is pulled.
                0x04 - Card reading failed, Data check error.
            driver_name(str): driver name
            qualification_certificate_code(str): qualification certificate code
            issuing_agency_name(str): issuing agency name
            certificate_validity(str): YYYYMMDD, certificate validity date
            driver_id_number(str): driver ID number.
        """
        self.__status = str_fill(hex(status)[2:], target_len=2)
        self.__time = time
        self.__ic_read_result = ""
        self.__driver_name = ""
        self.__driver_name_len = ""
        self.__qualification_certificate_code = ""
        self.__issuing_agency_name = ""
        self.__issuing_agency_name_len = ""
        self.__certificate_validity = ""
        self.__driver_id_number = ""
        if status == 1:
            self.__ic_read_result = str_fill(hex(ic_read_result)[2:], target_len=2)
            if ic_read_result == 0:
                self.__driver_name = ubinascii.hexlify(driver_name.encode("gbk")).decode("gbk")
                self.__driver_name_len = str_fill(hex(int(len(self.__driver_name) / 2))[2:], target_len=2)
                self.__qualification_certificate_code = str_fill(ubinascii.hexlify(qualification_certificate_code.encode("gbk")).decode("gbk"), target_len=40)
                self.__issuing_agency_name = str_fill(ubinascii.hexlify(issuing_agency_name.encode("gbk")).decode("gbk"), target_len=40)
                self.__issuing_agency_name_len = str_fill(hex(int(len(self.__issuing_agency_name) / 2))[2:], target_len=2)
                self.__certificate_validity = certificate_validity
                if self.is_version():
                    self.__driver_id_number = str_fill(ubinascii.hexlify(driver_id_number.encode("gbk")).decode("gbk"), target_len=40)

    def body_to_hex(self):
        kwargs = {
            "status": self.__status,
            "time": self.__time,
            "ic_read_result": self.__ic_read_result,
            "driver_name_len": self.__driver_name_len,
            "driver_name": self.__driver_name,
            "qualification_certificate_code": self.__qualification_certificate_code,
            "issuing_agency_name_len": self.__issuing_agency_name_len,
            "issuing_agency_name": self.__issuing_agency_name,
            "certificate_validity": self.__certificate_validity,
            "driver_id_number": self.__driver_id_number,
        }
        self.__body = "{status}{time}{ic_read_result}{driver_name_len}{driver_name}{qualification_certificate_code}" \
                      "{issuing_agency_name_len}{issuing_agency_name}{certificate_validity}{driver_id_number}".format(**kwargs)


class T0704(JTMessage):
    """Bulk upload of positioning data"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0704
        self.__datas = []

    def set_params(self, data_type):
        """
        Args:
            data_type(int):
                0 - Batch report of normal position
                1 - Blind spot supplementary report
        """
        self.__data_type = str_fill(hex(data_type)[2:], target_len=2)

    def set_loc_data(self, alarm_flag, loc_status, latitude, longitude, altitude, speed, direction, time, loc_additional_info):
        """
        Args:
            alarm_flag(str): LocAlarmWarningConfig().value()
            loc_status(str): LocStatusConfig().value()
            latitude(float): latitude
            longitude(float): longitude
            altitude(int): unit: meter
            speed(float): unit: km/h, Accurate to 0.1
            direction(int): range: 0~359, 0 is true North, Clockwise.
            time(str): GMT+8, format: YYMMDDhhmmss
            loc_additional_info(str): LocAdditonalInfoConfig().value()
        """
        self.__alarm_flag = alarm_flag
        self.__loc_status = loc_status
        self.__latitude = str_fill(hex(int(latitude * (10 ** 6)))[2:], target_len=8)
        self.__longitude = str_fill(hex(int(longitude * (10 ** 6)))[2:], target_len=8)
        self.__altitude = str_fill(hex(int(altitude))[2:], target_len=4)
        self.__speed = str_fill(hex(int(speed * 10))[2:], target_len=4)
        self.__direction = str_fill(hex(int(direction))[2:], target_len=4)
        self.__time = time
        self.__loc_additional_info = loc_additional_info

        kwargs = {
            "alarm_flag": self.__alarm_flag,
            "loc_status": self.__loc_status,
            "latitude": self.__latitude,
            "longitude": self.__longitude,
            "altitude": self.__altitude,
            "speed": self.__speed,
            "direction": self.__direction,
            "time": self.__time,
            "loc_additional_info": self.__loc_additional_info,
        }
        logger.debug("kwargs: %s" % str(kwargs))
        loc_data = "{alarm_flag}{loc_status}{latitude}{longitude}{altitude}{speed}{direction}{time}{loc_additional_info}".format(**kwargs)
        self.__datas.append("{}{}".format(str_fill(hex(int(len(loc_data) / 2))[2:], target_len=4), loc_data))

    def body_to_hex(self):
        kwargs = {
            "data_len": str_fill(hex(len(self.__datas))[2:], target_len=4),
            "data_type": self.__data_type,
            "data": "".join(self.__datas),
        }
        self.__body = "{data_len}{data_type}{data}".format(**kwargs)


class T0705(JTMessage):
    """CAN bus data upload"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0705
        self.__datas = []

    def set_params(self, recive_time):
        """
        Args:
            recive_time(str): hhmmssmsms
        """
        self.__recive_time = recive_time

    def set_can_data(self, can_channel_no, frame_type, collection_method, can_id, can_data):
        """
        Args:
            can_channel_no(int):
                0 - CAN1
                1 - CAN2
            frame_type(int):
                0 - standard frame
                1 - extended frame
            collection_method(int):
                0 - raw data
                1 - the average of the collection interval
            can_id(int): CAN ID
            can_data(str): CAN data
        """
        _can_id_kw = {
            "can_channel_no": can_channel_no,
            "frame_type": frame_type,
            "collection_method": collection_method,
            "can_id": str_fill(bin(can_id)[2:], target_len=29),
        }
        _can_id = "{can_channel_no}{frame_type}{collection_method}{can_id}".format(**_can_id_kw)
        _can_info_kw = {
            "_can_id": str_fill(hex(int(_can_id, 2))[2:], target_len=8),
            "_can_data": str_fill(ubinascii.hexlify(str(can_data).encode("gbk")).decode("gbk"), target_len=16),
        }
        _can_info = "{_can_id}{_can_data}".format(**_can_info_kw)
        self.__datas.append(_can_info)

    def body_to_hex(self):
        kwargs = {
            "data_len": str_fill(hex(len(self.__datas))[2:], target_len=4),
            "recive_time": self.__recive_time,
            "data": "".join(self.__datas),
        }
        self.__body = "{data_len}{recive_time}{data}".format(**kwargs)


class T0800(JTMessage):
    """Multimedia event information upload"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0800

    def set_params(self, media_id, media_type, media_encoding, event_id, channel_id):
        """
        Args:
            media_id(int): media id
            media_type(int):
                0 - picture
                1 - audio
                2 - video
            media_encoding(int):
                0 - JPEG
                1 - TIF
                2 - MP3
                3 - WAV
                4 - WMV
            event_id(int):
                0 - Platform issues instructions
                1 - timed action
                2 - Robbery alarm triggered
                3 - Collision Rollover Alarm Triggered
                4 - Open the door and take a photo
                5 - Close the door and take a photo
                6 - Door from open to closed, Speed ​​from 20km to over 20km
                7 - Take pictures at a fixed distance
            channel_id(int): channel id
        """
        self.__media_id = str_fill(hex(media_id)[2:], target_len=8)
        self.__media_type = str_fill(hex(media_type)[2:], target_len=2)
        self.__media_encoding = str_fill(hex(media_encoding)[2:], target_len=2)
        self.__event_id = str_fill(hex(event_id)[2:], target_len=2)
        self.__channel_id = str_fill(hex(channel_id)[2:], target_len=2)

    def body_to_hex(self):
        kwargs = {
            "media_id": self.__media_id,
            "media_type": self.__media_type,
            "media_encoding": self.__media_encoding,
            "event_id": self.__event_id,
            "channel_id": self.__channel_id,
        }

        self.__body = "{media_id}{media_type}{media_encoding}{event_id}{channel_id}".format(**kwargs)


class T0801(JTMessage):
    """Multimedia data upload"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0801
        self.__loc_data = ""

    def set_params(self, media_id, media_type, media_encoding, event_id, channel_id, media_data):
        """
        Args:
            media_id(int): media id
            media_type(int):
                0 - picture
                1 - audio
                2 - video
            media_encoding(int):
                0 - JPEG
                1 - TIF
                2 - MP3
                3 - WAV
                4 - WMV
            event_id(int):
                0 - Platform issues instructions
                1 - timed action
                2 - Robbery alarm triggered
                3 - Collision Rollover Alarm Triggered
                4 - Open the door and take a photo
                5 - Close the door and take a photo
                6 - Door from open to closed, Speed ​​from 20km to over 20km
                7 - Take pictures at a fixed distance
            channel_id(int): channel id
            media_data(bytes): media data bytes
        """
        self.__media_id = str_fill(hex(media_id)[2:], target_len=8)
        self.__media_type = str_fill(hex(media_type)[2:], target_len=2)
        self.__media_encoding = str_fill(hex(media_encoding)[2:], target_len=2)
        self.__event_id = str_fill(hex(event_id)[2:], target_len=2)
        self.__channel_id = str_fill(hex(channel_id)[2:], target_len=2)
        self.__media_data = ubinascii.hexlify(media_data).decode("gbk")

    def set_loc_data(self, alarm_flag, loc_status, latitude, longitude, altitude, speed, direction, time):
        """
        Args:
            alarm_flag(str): LocAlarmWarningConfig().value()
            loc_status(str): LocStatusConfig().value()
            latitude(float): latitude
            longitude(float): longitude
            altitude(int): unit: meter
            speed(float): unit: km/h, Accurate to 0.1
            direction(int): range: 0~359, 0 is true North, Clockwise.
            time(str): GMT+8, format: YYMMDDhhmmss
        """
        self.__alarm_flag = alarm_flag
        self.__loc_status = loc_status
        self.__latitude = str_fill(hex(int(latitude * (10 ** 6)))[2:], target_len=8)
        self.__longitude = str_fill(hex(int(longitude * (10 ** 6)))[2:], target_len=8)
        self.__altitude = str_fill(hex(int(altitude))[2:], target_len=4)
        self.__speed = str_fill(hex(int(speed * 10))[2:], target_len=4)
        self.__direction = str_fill(hex(int(direction))[2:], target_len=4)
        self.__time = time

        kwargs = {
            "alarm_flag": self.__alarm_flag,
            "loc_status": self.__loc_status,
            "latitude": self.__latitude,
            "longitude": self.__longitude,
            "altitude": self.__altitude,
            "speed": self.__speed,
            "direction": self.__direction,
            "time": self.__time,
        }
        self.__loc_data = "{alarm_flag}{loc_status}{latitude}{longitude}{altitude}{speed}{direction}{time}".format(**kwargs)
        self.__loc_data = str_fill(self.__loc_data, target_len=56)

    def body_to_hex(self):
        kwargs = {
            "media_id": self.__media_id,
            "media_type": self.__media_type,
            "media_encoding": self.__media_encoding,
            "event_id": self.__event_id,
            "channel_id": self.__channel_id,
            "loc_data": self.__loc_data,
            "media_data": self.__media_data,
        }

        self.__body = "{media_id}{media_type}{media_encoding}{event_id}{channel_id}{loc_data}{media_data}".format(**kwargs)


class T8800(JTMessage):
    """Multimedia data upload response"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8800

    def body_from_hex(self):
        """
        body_data:
            media_id(int): media id
            package_ids(list):
                item(int): package id
        """
        media_id = int(self.__body[:8], 16)
        retransmission_num = int(self.__body[8:10], 16)
        ids_data = self.__body[10:]
        package_ids = [ids_data[i * 4:(i + 1) * 4] for i in range(retransmission_num)]
        self.__body_data = {
            "media_id": media_id,
            "package_ids": package_ids,
        }


class T8801(JTMessage):
    """The camera shoots the command immediately"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8801

    def body_from_hex(self):
        """
        body_data:
            channel_id(int): channel id
            shooting_order(int):
                0 - stop shooting
                0xFFFF - start record vedio
                1 ~ 0xEFFF - shoot phone number
            working_time(int): unit: seconds, shooting time interval or recording time
            save_flag(int):
                1 - save
                0 - live upload
            resolution(int):
                0x00 - minimum resolution
                0x01 - 320 × 240
                0x02 - 640 × 480
                0x03 - 800 × 600
                0x04 - 1024 × 768
                0x05 - 176 × 144;[Qcif];
                0x06 - 352 × 288;[Cif];
                0x07 - 704 × 288;[HALF D1];
                0x08 - 704 × 576;[D1]
                0xFF - highest resolution
            quality(int): range: [1:10], 1 - Minimal quality loss, 10 - maximum compression ratio
            brightness(int): range: [0:255]
            contrast(int): range: [0:127]
            saturation(int): range: [0:127]
            chroma(int): range: [0:255]
        """
        channel_id = int(self.__body[:2], 16)
        shooting_order = int(self.__body[2:6], 16)
        working_time = int(self.__body[6:10], 16)
        save_flag = int(self.__body[10:12], 16)
        resolution = int(self.__body[12:14], 16)
        quality = int(self.__body[14:16], 16)
        brightness = int(self.__body[16:18], 16)
        contrast = int(self.__body[18:20], 16)
        saturation = int(self.__body[20:22], 16)
        chroma = int(self.__body[22:24], 16)
        self.__body_data = {
            "channel_id": channel_id,
            "shooting_order": shooting_order,
            "working_time": working_time,
            "save_flag": save_flag,
            "resolution": resolution,
            "quality": quality,
            "brightness": brightness,
            "contrast": contrast,
            "saturation": saturation,
            "chroma": chroma,
        }


class T0805(JTMessage):
    """The camera shoots the command immediately response"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0805

    def set_params(self, response_serial_no, result, ids):
        """
        Args:
            response_serial_no(int): response serial no
            result(int):
                0 - success
                1 - failed
                2 - channel not supported
            ids(list):
                item(int): media id
        """
        self.__response_serial_no = str_fill(hex(response_serial_no)[2:], target_len=4)
        self.__result = str_fill(hex(result)[2:], target_len=2)
        self.__ids_num = ""
        self.__ids = ""
        if result == 0:
            self.__ids_num = str_fill(hex(int(len(ids) / 2))[2:], target_len=4)
            self.__ids = "".join([str_fill(hex(i)[2:], target_len=4) for i in ids])

    def body_to_hex(self):
        kwargs = {
            "response_serial_no": self.__response_serial_no,
            "result": self.__result,
            "ids_num": self.__ids_num,
            "ids": self.__ids,
        }

        self.__body = "{response_serial_no}{result}{ids_num}{ids}".format(**kwargs)


class T8802(JTMessage):
    """Stored multimedia data retrieval"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8802

    def body_from_hex(self):
        """
        body_data:
            media_type(int):
                0 - picture
                1 - audio
                2 - video
            channel_id(int): 0 - retrieve all channels of this media type
            event_id(int):
                0 - Platform issues instructions
                1 - timed action
                2 - Robbery alarm triggered
                3 - Collision Rollover Alarm Triggered
            start_time(str): YYMMDDhhmmss
            end_time(str): YYMMDDhhmmss
        """
        media_type = int(self.__body[:2], 16)
        channel_id = int(self.__body[2:4], 16)
        event_id = int(self.__body[4:6], 16)
        start_time = self.__body[6:18]
        end_time = self.__body[18:30]
        self.__body_data = {
            "media_type": media_type,
            "channel_id": channel_id,
            "event_id": event_id,
            "start_time": start_time,
            "end_time": end_time,
        }


class T0802(JTMessage):
    """Stored multimedia data retrieval response"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0802
        self.__media_datas = []

    def set_params(self, response_serial_no):
        """
        Args:
            response_serial_no(int): response serial no
        """
        self.__response_serial_no = str_fill(hex(response_serial_no)[2:], target_len=4)

    def __format_loc_data(self, alarm_flag, loc_status, latitude, longitude, altitude, speed, direction, time):
        """
        Args:
            alarm_flag(str): LocAlarmWarningConfig().value()
            loc_status(str): LocStatusConfig().value()
            latitude(float): latitude
            longitude(float): longitude
            altitude(int): unit: meter
            speed(float): unit: km/h, Accurate to 0.1
            direction(int): range: 0~359, 0 is true North, Clockwise.
            time(str): GMT+8, format: YYMMDDhhmmss
        """
        self.__alarm_flag = alarm_flag
        self.__loc_status = loc_status
        self.__latitude = str_fill(hex(int(latitude * (10 ** 6)))[2:], target_len=8)
        self.__longitude = str_fill(hex(int(longitude * (10 ** 6)))[2:], target_len=8)
        self.__altitude = str_fill(hex(int(altitude))[2:], target_len=4)
        self.__speed = str_fill(hex(int(speed * 10))[2:], target_len=4)
        self.__direction = str_fill(hex(int(direction))[2:], target_len=4)
        self.__time = time

        kwargs = {
            "alarm_flag": self.__alarm_flag,
            "loc_status": self.__loc_status,
            "latitude": self.__latitude,
            "longitude": self.__longitude,
            "altitude": self.__altitude,
            "speed": self.__speed,
            "direction": self.__direction,
            "time": self.__time,
        }
        logger.debug("kwargs: %s" % str(kwargs))
        loc_data = "{alarm_flag}{loc_status}{latitude}{longitude}{altitude}{speed}{direction}{time}".format(**kwargs)
        loc_data = str_fill(loc_data, target_len=56)
        return loc_data

    def set_media(self, media_id, media_type, channel_id, event_id, loc_data):
        """
        Args:
            media_id(int): media id
            media_type(int):
                0 - picture
                1 - audio
                2 - video
            channel_id(int): channel id
            event_id(int):
                0 - Platform issues instructions
                1 - timed action
                2 - Robbery alarm triggered
                3 - Collision Rollover Alarm Triggered
                4 - Open the door and take a photo
                5 - Close the door and take a photo
                6 - Door from open to closed, Speed ​​from 20km to over 20km
                7 - Take pictures at a fixed distance
            loc_data(str): T0200.__body
        """
        _media_id = str_fill(hex(media_id)[2:], target_len=8)
        _media_type = str_fill(hex(media_type)[2:], target_len=2)
        _channel_id = str_fill(hex(channel_id)[2:], target_len=2)
        _event_id = str_fill(hex(event_id)[2:], target_len=2)
        _loc_data = self.__format_loc_data(*loc_data)
        args = (_media_id, _media_type, _channel_id, _event_id, _loc_data)
        _media_info = "{}{}{}{}{}".format(*args)
        self.__media_datas.append(_media_info)

    def body_to_hex(self):
        kwargs = {
            "response_serial_no": self.__response_serial_no,
            "media_data_len": str_fill(hex(len(self.__media_datas))[2:], target_len=4),
            "media_data": "".join(self.__media_datas)
        }
        self.__body = "{response_serial_no}{media_data_len}{media_data}".format(**kwargs)


class T8803(JTMessage):
    """Store multimedia upload commands"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8803

    def body_from_hex(self):
        """
        body_data:
            media_type(int):
                0 - picture
                1 - audio
                2 - video
            channel_id(int): channel id
            event_id(int):
                0 - Platform issues instructions
                1 - timed action
                2 - Robbery alarm triggered
                3 - Collision Rollover Alarm Triggered
                4 - Open the door and take a photo
                5 - Close the door and take a photo
                6 - Door from open to closed, Speed ​​from 20km to over 20km
                7 - Take pictures at a fixed distance
            starttime(str): YYMMDDhhmmss
            end_time(str): YYMMDDhhmmss
            delete_flag(int):
                0 - hold, 1 - delete
        """
        media_type = int(self.__body[:2], 16)
        channel_id = int(self.__body[2:4], 16)
        event_id = int(self.__body[4:6], 16)
        start_time = self.__body[6:18]
        end_time = self.__body[18:30]
        delete_flag = int(self.__body[30:32], 16)
        self.__body_data = {
            "media_type": media_type,
            "channel_id": channel_id,
            "event_id": event_id,
            "start_time": start_time,
            "end_time": end_time,
            "delete_flag": delete_flag,
        }


class T8804(JTMessage):
    """Recording start command"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8804

    def body_from_hex(self):
        """
        body_data:
            recording_cmd(int):
                0 - stop recording
                1 - start recording
            recording_time(int): unit: seconds, 0 is keep recording.
            save_flag(int):
                0 - live upload
                1 - save locally
            audio_sample_rate(int):
                0 - 8K
                1 - 11K
                2 - 23K
                3 - 32K
        """
        recording_cmd = int(self.__body[:2], 16)
        recording_time = int(self.__body[2:6], 16)
        save_flag = int(self.__body[6:8], 16)
        audio_sample_rate = int(self.__body[8:10], 16)
        self.__body_data = {
            "recording_cmd": recording_cmd,
            "recording_time": recording_time,
            "save_flag": save_flag,
            "audio_sample_rate": audio_sample_rate,
        }


class T8805(JTMessage):
    """One-on-one storage multimedia data retrieval upload command"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8805

    def body_from_hex(self):
        """
        body_data:
            media_id(int): media id
            delete_flag(int):
                0 - hold, 1 - delete
        """
        media_id = int(self.__body[:8], 16)
        delete_flag = int(self.__body[8:10], 16)
        self.__body_data = {
            "media_id": media_id,
            "delete_flag": delete_flag,
        }


class T8900(JTMessage):
    """Data downlink transparent transmission"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8900

    def body_from_hex(self):
        """
        body_data:
            data_type(int):
                0x00 - GNSS module detailed positioning data
                0x0B - Road transport IC card information
                0x41 - Serial port 1 transparently transmits messages
                0x42 - Serial port 2 transparently transmits messages
                0xF0~0xFF - User-defined transparent message
            data(str):
                Transparent transmission of message content
        """
        data_type = int(self.__body[:2], 16)
        data = ubinascii.hexlify(self.__body[2:]).decode("gbk")
        self.__body_data = {
            "data_type": data_type,
            "data": data,
        }


class T0900(JTMessage):
    """Data uplink transparent transmission"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0900

    def set_params(self, data_type, data):
        """
        Args:
            data_type(int):
                0x00 - GNSS module detailed positioning data
                0x0B - Road transport IC card information
                0x41 - Serial port 1 transparently transmits messages
                0x42 - Serial port 2 transparently transmits messages
                0xF0~0xFF - User-defined transparent message
            data(str): Transparent transmission of message content
        """
        self.__data_type = str_fill(hex(data_type)[2:], target_len=2)
        self.__data = ubinascii.hexlify(str(data).encode("gbk")).decode("gbk")

    def body_to_hex(self):
        kwargs = {
            "data_type": self.__data_type,
            "data": self.__data,
        }
        self.__body = "{data_type}{data}".format(**kwargs)


class T0901(JTMessage):
    """data compression report"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0901

    def set_params(self, data):
        """
        Args:
            data(str): data compression
        """
        self.__data = ubinascii.hexlify(data).decode("gbk")
        self.__data_len = str_fill(hex(int(len(self.__data) / 2))[2:], target_len=8)

    def body_to_hex(self):
        kwargs = {
            "data_len": self.__data_len,
            "data": self.__data,
        }
        self.__body = "{data_len}{data}".format(**kwargs)


class T8A00(JTMessage):
    """Platform RSA public key"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x8A00

    def body_from_hex(self):
        """
        body_data:
            e(int): e of Platform RSA public key {e, n}
            n(str): n of Platform RSA public key {e, n}
        """
        e = int(self.__body[:8], 16)
        n = int(self.__body[8:], 16)
        self.__body_data = {
            "e": e,
            "n": n,
        }


class T0A00(JTMessage):
    """Terminal RSA public key"""

    def __init__(self):
        super().__init__()
        self.__message_id = 0x0A00

    def set_params(self, e, n):
        """
        Args:
            e(int): e of terminal RAS public key {e, n}
            n(str): n of terminal RAS public key {e, n}
        """
        self.__e = str_fill(hex(e)[2:], target_len=8)
        self.__n = str_fill(hex(n)[2:], target_len=256)

    def body_to_hex(self):
        kwargs = {
            "e": self.__e,
            "n": self.__n,
        }
        self.__body = "{e}{n}".format(**kwargs)


DOWNLINK_MESSAGE = {
    0x8001: T8001,
    0x8004: T8004,
    0x8003: T8003,
    0x8100: T8100,
    0x8103: T8103,
    0x8104: T8104,
    0x8106: T8106,
    0x8105: T8105,
    0x8107: T8107,
    0x8108: T8108,
    0x8201: T8201,
    0x8202: T8202,
    0x8203: T8203,
    0x8204: T8204,
    0x8300: T8300,
    0x8301: T8301,
    0x8302: T8302,
    0x8303: T8303,
    0x8304: T8304,
    0x8400: T8400,
    0x8401: T8401,
    0x8500: T8500,
    0x8600: T8600,
    0x8601: T8601,
    0x8602: T8602,
    0x8603: T8603,
    0x8604: T8604,
    0x8605: T8605,
    0x8606: T8606,
    0x8607: T8607,
    0x8608: T8608,
    0x8700: T8700,
    0x8701: T8701,
    0x8702: T8702,
    0x8800: T8800,
    0x8801: T8801,
    0x8802: T8802,
    0x8803: T8803,
    0x8804: T8804,
    0x8805: T8805,
    0x8900: T8900,
    0x8A00: T8A00,
}

UPLINK_MESSAGE = {
    0x0001: T0001,
    0x0002: T0002,
    0x0004: T0004,
    0x0005: T0005,
    0x0100: T0100,
    0x0003: T0003,
    0x0102: T0102,
    0x0104: T0104,
    0x0107: T0107,
    0x0108: T0108,
    0x0200: T0200,
    0x0201: T0201,
    0x0301: T0301,
    0x0302: T0302,
    0x0303: T0303,
    0x0500: T0500,
    0x0608: T0608,
    0x0700: T0700,
    0x0701: T0701,
    0x0702: T0702,
    0x0704: T0704,
    0x0705: T0705,
    0x0800: T0800,
    0x0801: T0801,
    0x0805: T0805,
    0x0802: T0802,
    0x0900: T0900,
    0x0901: T0901,
    0x0A00: T0A00,
}
