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
@file      :test_jtt808.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :<description>
@version   :1.0.0
@date      :2022-06-02 15:31:21
@copyright :Copyright (c) 2022
"""

import sim
import modem
import utime
from usr.jtt808 import JTT808
from usr.logging import getLogger
from usr.jt_message import LicensePlateColor, TerminalParams, \
    LocAlarmWarningConfig, LocStatusConfig, LocAdditionalInfoConfig

logger = getLogger(__name__)

method = "TCP"
ip = "220.180.239.212"
port = 7611

jtt808_obj = JTT808(ip=ip, port=port, method=method)


def test_loction_data():
    LocStatusConfigObj = LocStatusConfig()
    LocAlarmWarningConfigObj = LocAlarmWarningConfig()
    LocAdditionalInfoConfigObj = LocAdditionalInfoConfig()
    for key in LocStatusConfigObj._loc_cfg_offset.__dict__.keys():
        LocStatusConfigObj.set_config(key, 1)
    LocAdditionalInfoConfigObj.set_mileage(100)
    LocAdditionalInfoConfigObj.set_oil_quantity(32.5)
    LocAdditionalInfoConfigObj.set_speed(0)

    alarm_flag = LocAlarmWarningConfigObj.value()
    logger.debug("alarm_flag: %s" % alarm_flag)
    loc_status = LocStatusConfigObj.value()
    logger.debug("loc_status: %s" % loc_status)
    latitude = 31.824845156501
    longitude = 117.24091089413
    altitude = 120
    speed = 0
    direction = 0
    time = "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(*(utime.localtime()[:6]))[2:]
    loc_additional_info = LocAdditionalInfoConfigObj.value()
    logger.debug("loc_additional_info: %s" % loc_additional_info)

    return (alarm_flag, loc_status, latitude, longitude, altitude, speed, direction, time, loc_additional_info)


def test_general_answer(serial_no, message_id):
    jtt808_obj.general_answer(serial_no, message_id)


def test_params_report(response_serial_no):
    terminal_params = {
        0x0013: TerminalParams(0x0013).convert("220.180.239.212:7611"),
        0x0001: TerminalParams(0x0001).convert(60),
        0x0002: TerminalParams(0x0002).convert(30),
    }
    jtt808_obj.params_report(response_serial_no, terminal_params)


def test_properties_report():
    applicable_passenger_vehicles = 1
    applicable_to_dangerous_goods_vehicles = 1
    applicable_to_ordinary_freight_vehicles = 1
    applicable_to_taxi = 1
    support_hard_disk_video = 1
    machine_type = 0
    applicable_to_trailer = 1
    manufacturer_id = "quec"
    terminal_model = "EC200U-CNAA"
    terminal_id = "EC200UCNAA"
    iccid = sim.getIccid()
    hardware_version = modem.getDevImei()
    firmware_version = modem.getDevFwVersion()
    support_gps = 1
    support_bds = 1
    support_glonass = 1
    support_galileo = 1
    support_gprs = 1
    support_cdma = 1
    support_td_scdma = 1
    support_wcdma = 1
    support_cdma2000 = 1
    support_td_lte = 1
    support_other_communication = 0
    jtt808_obj.properties_report(
        applicable_passenger_vehicles, applicable_to_dangerous_goods_vehicles,
        applicable_to_ordinary_freight_vehicles, applicable_to_taxi, support_hard_disk_video,
        machine_type, applicable_to_trailer, manufacturer_id, terminal_model, terminal_id,
        iccid, hardware_version, firmware_version, support_gps, support_bds, support_glonass,
        support_galileo, support_gprs, support_cdma, support_td_scdma, support_wcdma,
        support_cdma2000, support_td_lte, support_other_communication
    )


def test_loction_report(response_msg_id=None, response_serial_no=None):
    loc_data = test_loction_data()
    args = [response_msg_id, response_serial_no]
    args.extend(list(loc_data))
    jtt808_obj.loction_report(*args)


def test_event_report(event_id):
    jtt808_obj.event_report(event_id)


def test_issue_question_response(response_serial_no, answer_id):
    jtt808_obj.issue_question_response(response_serial_no, answer_id)


def test_information_demand_cancellation(info_type, onoff):
    jtt808_obj.information_demand_cancellation(info_type, onoff)


def test_query_area_route_data_response(query_type):
    query_data = {
        1: ["01010000000060ff01e59bcd06fcf44e00000064220601000000220701000000000a64"],
        2: ["01010000000160ff01e5c2dd06fd1b5e01e59bcd06fcf44e220601000000220701000000000a64"],
        3: ["0000000260ff220601000000220701000000000a64000301e59bcd06fcf44e01e59bd706fcf45801e59be106fcf462"],
        4: ["00000003003d2206010000002207010000000003000000000000000001e59bcd06fcf44e0a0f0064000a000a0a000000010000000101e59bd706fcf4580a0f0064000a000a0a000000020000000201e59be106fcf4620a0f0064000a000a0a"],
    }
    jtt808_obj.query_area_route_data_response(query_type, query_data[query_type])


def test_driving_record_data_upload(response_serial_no, cmd_word):
    with open("/usr/system_config.json", "rb") as f:
        cmd_data = f.read()
    jtt808_obj.driving_record_data_upload(response_serial_no, 33, cmd_data)


def test_driver_identity_information_report():
    status = 1
    time = "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(*(utime.localtime()[:6]))[2:]
    ic_read_result = 0
    driver_name = "jack"
    qualification_certificate_code = "88888"
    issuing_agency_name = "市级道路运输管理机构"
    certificate_validity = "20220701"
    driver_id_number = "342426199309020031"
    jtt808_obj.driver_identity_information_report(
        status, time, ic_read_result, driver_name, qualification_certificate_code,
        issuing_agency_name, certificate_validity, driver_id_number
    )


def test_camera_shoots_immediately_response(response_serial_no):
    result = 0
    ids = list(range(10))
    jtt808_obj.camera_shoots_immediately_response(response_serial_no, result, ids)


def test_stored_media_data_retrieval_response(response_serial_no):
    media_id = 1
    media_type = 0
    channel_id = 2
    event_id = 5
    loc_data = test_loction_data()[:-1]
    medias = [(media_id, media_type, channel_id, event_id, loc_data)] * 10
    jtt808_obj.stored_media_data_retrieval_response(response_serial_no, medias)


def test_callback(args):
    header = args["header"]
    data = args["data"]
    logger.debug("test_callback header: %s" % str(header))
    logger.debug("test_callback data: %s" % str(data))
    if header["message_id"] in (0x8104, 0x8106):
        response_serial_no = header["serial_no"]
        test_params_report(response_serial_no)
    elif header["message_id"] == 0x8107:
        test_properties_report()
    elif header["message_id"] in (0x8201, 0x8500):
        test_loction_report(header["message_id"], header["serial_no"])
    elif header["message_id"] == 0x8302:
        # WARNING: This message need use issue_question_response to answer, but test server only get general_answer for answer.
        # answer_id = data["answers"][0]["id"]
        # test_issue_question_response(header["serial_no"], answer_id)
        test_general_answer(header["serial_no"], header["message_id"])
    elif header["message_id"] == 0x8608:
        test_query_area_route_data_response(data["query_type"])
    elif header["message_id"] == 0x8700:
        test_driving_record_data_upload(header["serial_no"], data["cmd_word"])
    elif header["message_id"] == 0x8702:
        test_driver_identity_information_report()
    elif header["message_id"] == 0x8801:
        test_camera_shoots_immediately_response(header["serial_no"])
    elif header["message_id"] == 0x8802:
        test_stored_media_data_retrieval_response(header["serial_no"])


def test_connect():
    jtt808_obj.set_callback(test_callback)
    conn_res = jtt808_obj.connect()
    assert conn_res, "%s connect failed." % method


def test_heart_beat():
    jtt808_obj.__heart_beat(None)


def test_register():
    province_id = 340000
    city_id = 340100
    manufacturer_id = "quectel"
    terminal_model = "EC200U-CNAA"
    terminal_id = modem.getDevImei()
    license_plate_color = LicensePlateColor.blue
    license_plate = "皖A88888"
    return jtt808_obj.register(province_id, city_id, manufacturer_id, terminal_model, terminal_id, license_plate_color, license_plate)


def test_authentication(auth_code):
    jtt808_obj.authentication(auth_code, modem.getDevImei(), "v1.0.0")


def test_query_server_time():
    jtt808_obj.query_server_time()


def test_logout():
    jtt808_obj.logout()


def test_upgrade_result_report():
    upgrade_type, result_code = (0, 0)
    jtt808_obj.upgrade_result_report(upgrade_type, result_code)


def test_electronic_waybill_report():
    with open("/usr/system_config.json", "rb") as f:
        data = f.read()
    jtt808_obj.electronic_waybill_report(data)


def test_location_bulk_report():
    loc_data = test_loction_data()
    loc_datas = [loc_data] * 10
    logger.debug("loc_datas: %s" % str(loc_datas))
    data_type = 0
    jtt808_obj.location_bulk_report(data_type, loc_datas)


def test_can_bus_data_upload():
    recive_time = ("{:2d}" * 3 + "0000").format(*(utime.localtime()[3:6]))
    can_channel_no = 0
    frame_type = 0
    collection_method = 0
    can_id = 0
    can_data = "123"
    can_datas = [(can_channel_no, frame_type, collection_method, can_id, can_data)] * 3
    jtt808_obj.can_bus_data_upload(recive_time, can_datas)


def test_media_event_upload():
    media_id = 12
    media_type = 0
    media_encoding = 0
    event_id = 4
    channel_id = 1
    jtt808_obj.media_event_upload(media_id, media_type, media_encoding, event_id, channel_id)


def test_media_data_upload():
    media_id = 14
    media_type = 0
    media_encoding = 0
    event_id = 4
    channel_id = 1
    with open("/usr/system_config.json", "rb") as f:
        media_data = f.read()
    loc_data = test_loction_data()[:-1]
    jtt808_obj.media_data_upload(media_id, media_type, media_encoding, event_id, channel_id, media_data, loc_data)


def test_data_uplink_transparent_transmission():
    data_type = 0
    data = "123456"
    jtt808_obj.data_uplink_transparent_transmission(data_type, data)


def test_data_compression_report():
    with open("/usr/system_config.json", "rb") as f:
        data = f.read()
    jtt808_obj.data_compression_report(data)


def test_terminal_rsa_public_key():
    e = 65537
    n = 10923252007875538132171701535639644200191641194610072563985760225688326844567094363074389543489252121216915728771174747297043916958910473388186667405361889
    jtt808_obj.terminal_rsa_public_key(e, n)


def test_jtt808():
    test_connect()

    register_res = test_register()
    auth_code = register_res.get("auth_code")

    auth_code = "A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0086530605779823"
    test_authentication(auth_code)

    test_heart_beat()

    test_query_server_time()

    test_upgrade_result_report()

    test_loction_report()

    test_event_report(0)

    test_information_demand_cancellation(12, 1)

    test_electronic_waybill_report()

    test_location_bulk_report()

    test_can_bus_data_upload()

    test_media_event_upload()

    test_media_data_upload()

    test_data_uplink_transparent_transmission()

    test_data_compression_report()

    test_terminal_rsa_public_key()

    test_logout()


def main():
    test_jtt808()


if __name__ == '__main__':
    main()
