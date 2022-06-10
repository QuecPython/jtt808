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
@file      :jtt808.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :JTT808 client
@version   :1.0.0
@date      :2022-05-18 11:46:43
@copyright :Copyright (c) 2022
"""

import ure
import usys
import utime
import usocket
import osTimer
import _thread
from usr.logging import getLogger
from usr.common import option_lock, Singleton
from usr.jt_message import DOWNLINK_MESSAGE, UPLINK_MESSAGE, JTMessageParse, set_jtmsg_config

logger = getLogger(__name__)

_socket_lock = _thread.allocate_lock()
_serial_no_lock = _thread.allocate_lock()

GENERAL_ANSWER_MSG_ID = (
    0x8103, 0x8105, 0x8108, 0x8202, 0x8203, 0x8204, 0x8300, 0x8301, 0x8303,
    0x8304, 0x8400, 0x8401, 0x8600, 0x8601, 0x8602, 0x8603, 0x8604, 0x8605,
    0x8606, 0x8607, 0x8701, 0x8803, 0x8804, 0x8805, 0x8900, 0x8A00
)


class BaseSocket(Singleton):

    def __init__(self, ip=None, port=None, domain=None, method="TCP"):
        self.__ip = ip
        self.__port = port
        self.__domain = domain
        self.__addr = None
        self.__method = method
        self.__socket = None
        self.__socket_args = []
        self.__timeout = 30
        self.__init_addr()
        self.__init_socket()

    def __init_addr(self):
        if self.__domain is not None:
            if self.__port is None:
                self.__port == 8883 if self.__domain.startswith("https://") else 1883
            try:
                addr_info = usocket.getaddrinfo(self.__domain, self.__port)
                self.__ip = addr_info[0][-1][0]
            except Exception as e:
                usys.print_exception(e)
                raise ValueError("Domain %s DNS parsing error. %s" % (self.__domain, str(e)))
        self.__addr = (self.__ip, self.__port)

    def __init_socket(self):
        if self.__check_ipv4():
            socket_af = usocket.AF_INET
        elif self.__check_ipv6():
            socket_af = usocket.AF_INET6
        else:
            raise TypeError("Args ip %s if illegal!" % self.__ip)

        if self.__method == 'TCP':
            socket_type = usocket.SOCK_STREAM
            socket_proto = usocket.IPPROTO_TCP
        elif self.__method == 'UDP':
            socket_type = usocket.SOCK_DGRAM
            socket_proto = usocket.IPPROTO_UDP
        else:
            raise TypeError("Args method is TCP or UDP, not %s" % self.__method)
        self.__socket_args = (socket_af, socket_type, socket_proto)

    def __check_ipv4(self):
        self.__ipv4_item = r"(25[0-5]|2[0-4]\d|[01]?\d\d?)"
        self.__ipv4_regex = r"^{item}\.{item}\.{item}\.{item}$".format(item=self.__ipv4_item)
        if self.__ip.find(":") == -1:
            ipv4_re = ure.search(self.__ipv4_regex, self.__ip)
            if ipv4_re:
                if ipv4_re.group(0) == self.__ip:
                    return True
        return False

    def __check_ipv6(self):
        # self.__ipv6_item = r"[0-9a-fA-F]{1:4}"
        self.__ipv6_code = r"[0-9a-fA-F]"
        ipv6_item_format = [self.__ipv6_code * i for i in range(1, 5)]
        self.__ipv6_item = r"{}|{}|{}|{}".format(*ipv6_item_format)

        # TODO: check ip is ipv6 by regex when ure support `{n,m}`
        # ipv4_regex = r"({item}\.{item}\.{item}\.{item})".format(item=self.__ipv4_item)
        # regex = r"""
        #     ^({ipv6}:){6}{ipv4}$|
        #     ^::({ipv6}:){0,4}{ipv4}$|
        #     ^({ipv6}:):({ipv6}:){0,3}{ipv4}$|
        #     ^({ipv6}:){2}:({ipv6}:){0,2}{ipv4}$|
        #     ^({ipv6}:){3}:({ipv6}:){0,1}{ipv4}$|
        #     ^({ipv6}:){4}:{ipv4}$|
        #     ^({ipv6}:){7}{ipv6}$|^:((:{ipv6}){1,6}|:)$|
        #     ^{ipv6}:((:{ipv6}){1,5}|:)$|
        #     ^({ipv6}:){2}((:{ipv6}){1,4}|:)$|
        #     ^({ipv6}:){3}((:{ipv6}){1,3}|:)$|
        #     ^({ipv6}:){4}((:{ipv6}){1,2}|:)$|
        #     ^({ipv6}:){5}:({ipv6})?$|
        #     ^({ipv6}:){6}:$
        # """.format(ipv4=ipv4_regex, ipv6=self.__ipv6_item)

        if self.ip.startswith("::") or ure.search(self.__ipv6_item + ":", self.__ip):
            return True
        else:
            return False

    @option_lock(_socket_lock)
    def __connect(self):
        if self.__socket_args:
            try:
                self.__socket = usocket.socket(*self.__socket_args)
                if self.__method == 'TCP':
                    self.__socket.connect(self.__addr)
                return True
            except Exception as e:
                usys.print_exception(e)

        return False

    @option_lock(_socket_lock)
    def __disconnect(self):
        if self.__socket is not None:
            try:
                self.__socket.close()
                self.__socket = None
                return True
            except Exception as e:
                usys.print_exception(e)
                return False
        else:
            return True

    @option_lock(_socket_lock)
    def __send(self, data):
        if self.__socket is not None:
            try:
                if self.__method == "TCP":
                    write_data_num = self.__socket.write(data)
                    if write_data_num == len(data):
                        return True
                elif self.__method == "UDP":
                    send_data_num = self.__socket.sendto(data, self.__addr)
                    if send_data_num == len(data):
                        return True
            except Exception as e:
                usys.print_exception(e)

        return False

    def __read(self, bufsize=1024):
        logger.debug("start read")
        data = b""
        if self.__socket is not None:
            try:
                while True:
                    if data:
                        self.__socket.settimeout(0.5)
                    else:
                        self.__socket.settimeout(self.__timeout)
                    read_data = self.__socket.recv(bufsize)
                    logger.debug("read_data: %s" % read_data)
                    if read_data:
                        data += read_data
                    else:
                        break
            except Exception as e:
                if e.args[0] != 110:
                    usys.print_exception(e)
                    logger.error("%s read falied. error: %s" % (self.__method, str(e)))

        return data

    def _downlink_thread_start(self):
        pass

    def _downlink_thread_stop(self):
        pass

    def _heart_beat_timer_start(self):
        pass

    def _heart_beat_timer_stop(self):
        pass

    def status(self):
        """Get Socket connection status

        Returns:
            [int]:
                -1: Error
                 0: Connected
                 1: Connecting
                 2: Disconnect
        """
        _status = -1
        if self.__socket is not None:
            try:
                if self.__method == "TCP":
                    socket_sta = self.__socket.getsocketsta()
                    if socket_sta in range(4):
                        # Connecting
                        _status = 1
                    elif socket_sta == 4:
                        # Connected
                        _status = 0
                    elif socket_sta in range(5, 11):
                        # Disconnect
                        _status = 2
                elif self.__method == "UDP":
                    _status = 0
            except Exception as e:
                usys.print_exception(e)

        return _status

    def connect(self):
        if self.__connect():
            self._downlink_thread_start()
            return True

        return False

    def disconnect(self):
        if self.__disconnect():
            self._downlink_thread_stop()
            self._heart_beat_timer_stop()
            return True

        return False


class JTT808Base(BaseSocket):

    def __init__(self, ip=None, port=None, domain=None, method="TCP", encrypted=False, timeout=30, retry_count=3,
                 life_time=60, version="2019", client_id="18888888888"):
        super().__init__(ip=ip, port=port, domain=domain, method=method)
        set_jtmsg_config(jtt808_version=version, client_id=client_id, encryption=encrypted)
        self.__timeout = timeout
        self.__retry_count = retry_count
        self.__life_time = life_time
        self.__response_res = {}
        self.__response_subpkg = {}
        self.__subpkg_timer = {}
        self.__subpkg_msg_ids = []
        self.__resend_subpkg_msg_ids = []
        self.__read_thread = None
        self.__heart_beat_timer = osTimer()
        self.__heart_beat_is_running = False
        self.__iter_serial_no = iter(range(99999))
        self.__call_back = None

    def __read_response(self):
        message = b""
        while True:
            try:
                if self.status() not in (0, 1):
                    logger.error("%s connection status is %s" % (self.__method, self.status()))
                    break

                new_msg = self.__read()
                if new_msg:
                    message += new_msg
                else:
                    message = new_msg

                if message:
                    msgs = list(bytearray(message))
                    msg_indexs = [index for index, item in enumerate(msgs) if item == 0x7e]
                    if msg_indexs[1] - msg_indexs[0] == 1:
                        msg_indexs = msg_indexs[1:]
                    range_num = len(msg_indexs) if len(msg_indexs) % 2 == 0 else len(msg_indexs) - 1
                    for i in range(0, range_num, 2):
                        msg = bytearray(msgs[msg_indexs[i]:msg_indexs[i + 1] + 1]).decode().encode()
                        logger.debug("__read_response: %s" % msg)
                        jtmessageparse_obj = JTMessageParse()
                        jtmessageparse_obj.set_message(msg)
                        header = jtmessageparse_obj.get_header()
                        logger.debug("__read_response header: %s" % header)
                        if DOWNLINK_MESSAGE.get(header["message_id"]) is None:
                            logger.error("message_id [%s] is not downlink message id" % header["message_id"])
                            continue
                        msg_obj = DOWNLINK_MESSAGE.get(header["message_id"])()
                        resp_body = jtmessageparse_obj.get_body()
                        logger.debug("__read_response resp_body: %s" % resp_body)

                        # Check subpackage
                        full_body_flag = True
                        if header["package_total"] != 0:
                            if self.__subpkg_timer.get(header["message_id"]) is None:
                                self.__subpkg_timer[header["message_id"]] = osTimer()
                                self.__subpkg_timer[header["message_id"]].start(self.__timeout * 1000, 0, self.__check_subpackage)
                            if header["message_id"] not in self.__subpkg_msg_ids:
                                self.__subpkg_msg_ids.append(header["message_id"])
                            full_data = self.__splice_subpackage(header, resp_body)
                            if not full_data:
                                full_body_flag = False
                            else:
                                header = full_data["header"]
                                resp_body = full_data["body"]

                        if full_body_flag:
                            msg_obj.set_header(header)
                            msg_obj.set_body(resp_body)
                            data = msg_obj.body_data()
                            logger.debug("__read_response body_data: %s" % data)
                            if header["message_id"] in (0x8001, 0x8100, 0x8003, 0x8004):
                                self.__response_res[header["message_id"]] = {data["serial_no"] if data.get("serial_no") is not None else header["message_id"]: data}
                            elif header["message_id"] == 0x8800:
                                    if not data["package_ids"]:
                                        self.general_answer(header["serial_no"], header["message_id"])
                                    else:
                                        # TODO: When media upload set subpackage, than server may issued this message
                                        # Now media upload do not set subpackage.
                                        pass
                            else:
                                if self.__call_back:
                                    _thread.start_new_thread(self.__call_back, ({"header": header, "data": data},))
                                # TODO: Not auto answer, user to ack general_answer in callback.
                                if header["message_id"] in GENERAL_ANSWER_MSG_ID:
                                    self.general_answer(header["serial_no"], header["message_id"])

                    message = bytearray(msgs[msg_indexs[-1]:]).decode().encode() if len(msg_indexs) % 2 != 0 else b""
            except Exception as e:
                usys.print_exception(e)

    def __splice_subpackage(self, header, source_body):
        self.__response_subpkg[header["message_id"]] = {
            "header": {
                "message_id": header["message_id"],
                "properties": header["properties"],
                "protocol_version": header["protocol_version"],
                "client_id": header["client_id"],
                "package_total": 0,
                "package_no": 0,
            },
            "total_num": header["package_total"],
            "subpackage": {
                header["package_no"]: source_body
            }
        }
        if header["package_no"] == 1:
            self.__response_subpkg[header["message_id"]]["header"]["serial_no"] = header["serial_no"]
        else:
            if self.__response_subpkg[header["message_id"]]["header"].get("serial_no") is None:
                self.__response_subpkg[header["message_id"]]["header"]["serial_no"] = -1

        if header["package_total"] == len(self.__response_subpkg[header["message_id"]]["subpackage"]):
            self.__subpkg_timer[header["message_id"]].stop()
            self.__subpkg_timer.pop(header["message_id"])
            if header["message_id"] in self.__subpkg_msg_ids:
                self.__subpkg_msg_ids.pop(self.__subpkg_msg_ids.index(header["message_id"]))
            if header["message_id"] in self.__resend_subpkg_msg_ids:
                self.__resend_subpkg_msg_ids.pop(self.__resend_subpkg_msg_ids.index(header["message_id"]))

            full_body = ""
            for i in range(1, header["package_total"] + 1):
                full_body += self.__response_subpkg[header["message_id"]]["subpackage"][i]
            full_header = self.__response_subpkg[header["message_id"]]["header"]
            self.__response_subpkg.pop(header["message_id"])
            return {"body": full_body, "header": full_header}
        return {}

    def __check_subpackage(self, args):
        if self.__subpkg_msg_ids:
            msg_id = self.__subpkg_msg_ids.pop(0)
            self.__subpkg_timer.pop(msg_id)
            if msg_id in self.__resend_subpkg_msg_ids:
                self.__response_subpkg.pop(msg_id)
                self.__resend_subpkg_msg_ids.pop(self.__resend_subpkg_msg_ids.index(msg_id))
                return

            self.__resend_subpkg_msg_ids.append(msg_id)
            if self.__response_subpkg.get(msg_id):
                source_serial_no = self.__response_subpkg[msg_id]["header"]["serial_no"]
                package_ids = [i for i in range(1, self.__response_subpkg[msg_id]["total_num"]) if i not in self.__response_subpkg[msg_id]["subpackage"].keys()]
                self.__resend_subpackage(source_serial_no, package_ids)

    def __get_response(self, message_id, serial_no, timeout):
        data = {}
        count = 0
        while count < timeout * 10:
            if self.status() != 0:
                break
            if self.__response_res.get(message_id) is not None:
                if self.__response_res[message_id].get(serial_no) is not None:
                    data = self.__response_res[message_id].pop(serial_no)
                    if not self.__response_res.get(message_id):
                        self.__response_res.pop(message_id)
                    break
                elif self.__response_res[message_id].get(message_id) is not None:
                    data = self.__response_res[message_id].pop(message_id)
                    if not self.__response_res.get(message_id):
                        self.__response_res.pop(message_id)
                    break
            utime.sleep_ms(100)
            count += 1
        return data

    def __heart_beat(self, args):
        if self.status() == 0:
            up_msg_obj = UPLINK_MESSAGE[0x0002]()
            serial_no = self.get_serial_no()
            up_msg_obj.set_serial_no(serial_no)
            data = up_msg_obj.message()
            logger.debug("heart_beat data: %s" % data)
            self.send(data, 0x8001, serial_no)
        else:
            self._heart_beat_timer_stop()

    def __resend_subpackage(self, source_serial_no, package_ids):
        up_msg_obj = UPLINK_MESSAGE[0x0005]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(source_serial_no, package_ids)
        data = up_msg_obj.message()
        logger.debug("__resend_subpackage data: %s" % data)
        send_res = self.send(data, None, serial_no)
        logger.debug("__resend_subpackage send res: %s" % send_res)

    def _downlink_thread_start(self):
        self.__read_thread = _thread.start_new_thread(self.__read_response, ())

    def _downlink_thread_stop(self):
        if self.__read_thread is not None:
            _thread.stop_thread(self.__read_thread)
            self.__read_thread = None

    def _heart_beat_timer_start(self):
        self.__heart_beat_timer.start(self.__life_time * 1000, 1, self.__heart_beat)
        self.__heart_beat_is_running = True

    def _heart_beat_timer_stop(self):
        self.__heart_beat_timer.stop()
        self.__heart_beat_is_running = False

    def set_call_back(self, call_back):
        if callable(call_back):
            self.__call_back = call_back
            return True
        return False

    @option_lock(_serial_no_lock)
    def get_serial_no(self):
        try:
            return next(self.__iter_serial_no)
        except StopIteration:
            self.__iter_serial_no = iter(range(99999))
            return self.get_serial_no()

    def send(self, data, res_msg_id, serial_no):
        count = 0
        _timeout = self.__timeout * (count + 1)
        while count <= self.__retry_count:
            send_res = self.__send(data)
            logger.debug("__send res: %s" % send_res)
            if res_msg_id is not None:
                resp_res = self.__get_response(res_msg_id, serial_no, _timeout)
                logger.debug("__get_response res: %s" % resp_res)
                if not resp_res:
                    count += 1
                    _timeout += _timeout * (count + 1)
                else:
                    break
            else:
                resp_res = send_res
                break
        return resp_res


class JTT808(JTT808Base):

    def __init__(self, ip=None, port=None, domain=None, method="TCP", encrypted=False, timeout=30, retry_count=3,
                 life_time=60, version="2019", client_id="18888888888"):
        super().__init__(
            ip=ip, port=port, domain=domain, method=method, encrypted=encrypted, timeout=timeout, retry_count=retry_count,
            life_time=life_time, version=version, client_id=client_id
        )

    def general_answer(self, response_serial_no, response_msg_id, result_code=0):
        up_msg_obj = UPLINK_MESSAGE[0x0001]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(response_serial_no, response_msg_id, result_code)
        data = up_msg_obj.message()
        logger.debug("general_answer data: %s" % data)
        send_res = self.send(data, None, serial_no)
        logger.debug("general_answer send res: %s" % send_res)
        return send_res

    def query_server_time(self):
        up_msg_obj = UPLINK_MESSAGE[0x0004]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        data = up_msg_obj.message()
        logger.debug("query_server_time data: %s" % data)
        return self.send(data, 0x8004, serial_no)

    def register(self, province_id, city_id, manufacturer_id, terminal_model, terminal_id, license_plate_color, license_plate):
        up_msg_obj = UPLINK_MESSAGE[0x0100]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(province_id, city_id, manufacturer_id, terminal_model, terminal_id, license_plate_color, license_plate)
        data = up_msg_obj.message()
        logger.debug("register data: %s" % data)
        send_res = self.send(data, 0x8100, serial_no)
        return send_res

    def authentication(self, auth_code, imei, app_version):
        up_msg_obj = UPLINK_MESSAGE[0x0102]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(auth_code, imei, app_version)
        data = up_msg_obj.message()
        logger.debug("authentication data: %s" % data)
        send_res = self.send(data, 0x8001, serial_no)
        if send_res.get("result_code") == 0:
            if self.__heart_beat_is_running is False:
                self._heart_beat_timer_start()
        return send_res

    def logout(self):
        up_msg_obj = UPLINK_MESSAGE[0x0003]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        data = up_msg_obj.message()
        logger.debug("log_out data: %s" % data)
        send_res = self.send(data, None, serial_no)
        logger.debug("log_out send res: %s" % send_res)
        self._heart_beat_timer_stop()
        self._downlink_thread_stop()
        return send_res
        # TODO: Can not get response from server because server disconnect immediately after log out, not sure if there is a problem with the server
        resp_res = self.__get_response(0x8001, serial_no)
        logger.debug("log_out response res: %s" % resp_res)

    def params_report(self, response_serial_no, terminal_params):
        up_msg_obj = UPLINK_MESSAGE[0x0104]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(response_serial_no)
        for param_id, param_value in terminal_params.items():
            up_msg_obj.set_terminal_params(param_id, param_value)
        data = up_msg_obj.message()
        logger.debug("params_report data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def properties_report(self, applicable_passenger_vehicles, applicable_to_dangerous_goods_vehicles,
                          applicable_to_ordinary_freight_vehicles, applicable_to_taxi, support_hard_disk_video,
                          machine_type, applicable_to_trailer, manufacturer_id, terminal_model, terminal_id,
                          iccid, hardware_version, firmware_version, support_gps, support_bds, support_glonass,
                          support_galileo, support_gprs, support_cdma, support_td_scdma, support_wcdma,
                          support_cdma2000, support_td_lte, support_other_communication):
        up_msg_obj = UPLINK_MESSAGE[0x0107]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(applicable_passenger_vehicles, applicable_to_dangerous_goods_vehicles,
                              applicable_to_ordinary_freight_vehicles, applicable_to_taxi, support_hard_disk_video,
                              machine_type, applicable_to_trailer, manufacturer_id, terminal_model, terminal_id,
                              iccid, hardware_version, firmware_version, support_gps, support_bds, support_glonass,
                              support_galileo, support_gprs, support_cdma, support_td_scdma, support_wcdma,
                              support_cdma2000, support_td_lte, support_other_communication)
        data = up_msg_obj.message()
        logger.debug("properties_report data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def upgrade_result_report(self, upgrade_type, result_code):
        up_msg_obj = UPLINK_MESSAGE[0x0108]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(upgrade_type, result_code)
        data = up_msg_obj.message()
        logger.debug("upgrade_result_report data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def loction_report(self, response_msg_id, response_serial_no, alarm_flag, loc_status, latitude, longitude, altitude,
                       speed, direction, time, loc_additional_info):
        """This function for Location information report, Location information query response, Vehicle control response

        Args:
            response_msg_id(int):
                None - 0x0200(Location information report)
                0x8201 - 0x0201(Location information query response)
                0x8500 - 0x0500(Vehicle control response)
            response_serial_no(int): if response_msg_id is None, this value is None
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
        if response_msg_id is None:
            up_msg_obj = UPLINK_MESSAGE[0x0200]()
            params = (alarm_flag, loc_status, latitude, longitude, altitude, speed, direction, time, loc_additional_info)
        elif response_msg_id == 0x8201:
            up_msg_obj = UPLINK_MESSAGE[0x0201]()
            params = (response_serial_no, alarm_flag, loc_status, latitude, longitude, altitude, speed, direction, time, loc_additional_info)
        elif response_msg_id == 0x8500:
            up_msg_obj = UPLINK_MESSAGE[0x0500]()
            params = (response_serial_no, alarm_flag, loc_status, latitude, longitude, altitude, speed, direction, time, loc_additional_info)

        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(*params)
        data = up_msg_obj.message()
        logger.debug("loction_report data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def event_report(self, event_id):
        up_msg_obj = UPLINK_MESSAGE[0x0301]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(event_id)
        data = up_msg_obj.message()
        logger.debug("event_report data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def issue_question_response(self, response_serial_no, answer_id):
        up_msg_obj = UPLINK_MESSAGE[0x0302]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(response_serial_no, answer_id)
        data = up_msg_obj.message()
        logger.debug("issue_question_response data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def information_demand_cancellation(self, info_type, onoff):
        up_msg_obj = UPLINK_MESSAGE[0x0303]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(info_type, onoff)
        data = up_msg_obj.message()
        logger.debug("information_demand_cancellation data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def query_area_route_data_response(self, query_type, data):
        up_msg_obj = UPLINK_MESSAGE[0x0608]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(query_type, data)
        data = up_msg_obj.message()
        logger.debug("query_area_route_data_response data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def driving_record_data_upload(self, response_serial_no, cmd_word, cmd_data):
        up_msg_obj = UPLINK_MESSAGE[0x0700]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(response_serial_no, cmd_word, cmd_data)
        data = up_msg_obj.message()
        logger.debug("driving_record_data_upload data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def electronic_waybill_report(self, data):
        up_msg_obj = UPLINK_MESSAGE[0x0701]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(data)
        data = up_msg_obj.message()
        logger.debug("electronic_waybill_report data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def driver_identity_information_report(self, status, time, ic_read_result, driver_name, qualification_certificate_code,
                                           issuing_agency_name, certificate_validity, driver_id_number):
        up_msg_obj = UPLINK_MESSAGE[0x0702]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(status, time, ic_read_result, driver_name, qualification_certificate_code,
                              issuing_agency_name, certificate_validity, driver_id_number)
        data = up_msg_obj.message()
        logger.debug("driver_identity_information_report data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def location_bulk_report(self, data_type, loc_datas):
        up_msg_obj = UPLINK_MESSAGE[0x0704]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(data_type)
        for loc_data in loc_datas:
            up_msg_obj.set_loc_data(*loc_data)
        data = up_msg_obj.message()
        logger.debug("location_bulk_report data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def can_bus_data_upload(self, recive_time, can_datas):
        up_msg_obj = UPLINK_MESSAGE[0x0705]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(recive_time)
        for can_data in can_datas:
            up_msg_obj.set_can_data(*can_data)
        data = up_msg_obj.message()
        logger.debug("can_bus_data_upload data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def media_event_upload(self, media_id, media_type, media_encoding, event_id, channel_id):
        up_msg_obj = UPLINK_MESSAGE[0x0800]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(media_id, media_type, media_encoding, event_id, channel_id)
        data = up_msg_obj.message()
        logger.debug("media_event_upload data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def media_data_upload(self, media_id, media_type, media_encoding, event_id, channel_id, media_data, loc_data):
        up_msg_obj = UPLINK_MESSAGE[0x0801]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(media_id, media_type, media_encoding, event_id, channel_id, media_data)
        up_msg_obj.set_loc_data(*loc_data)
        data = up_msg_obj.message()
        logger.debug("media_data_upload data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def camera_shoots_immediately_response(self, response_serial_no, result, ids):
        up_msg_obj = UPLINK_MESSAGE[0x0805]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(response_serial_no, result, ids)
        data = up_msg_obj.message()
        logger.debug("camera_shoots_immediately_response data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def stored_media_data_retrieval_response(self, response_serial_no, medias):
        up_msg_obj = UPLINK_MESSAGE[0x0802]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(response_serial_no)
        for media in medias:
            up_msg_obj.set_media(*media)
        data = up_msg_obj.message()
        logger.debug("stored_media_data_retrieval_response data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def data_uplink_transparent_transmission(self, data_type, data):
        up_msg_obj = UPLINK_MESSAGE[0x0900]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(data_type, data)
        data = up_msg_obj.message()
        logger.debug("data_uplink_transparent_transmission data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def data_compression_report(self, data):
        up_msg_obj = UPLINK_MESSAGE[0x0901]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(data)
        data = up_msg_obj.message()
        logger.debug("data_compression_report data: %s" % data)
        return self.send(data, 0x8001, serial_no)

    def terminal_rsa_public_key(self, e, n):
        up_msg_obj = UPLINK_MESSAGE[0x0A00]()
        serial_no = self.get_serial_no()
        up_msg_obj.set_serial_no(serial_no)
        up_msg_obj.set_params(e, n)
        data = up_msg_obj.message()
        logger.debug("terminal_rsa_public_key data: %s" % data)
        return self.send(data, 0x8001, serial_no)
