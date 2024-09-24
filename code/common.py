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

"""
@file      :common.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :<description>
@version   :1.0.0
@date      :2022-05-19 20:12:09
@copyright :Copyright (c) 2022
"""

import ure
import sys
import utime
import usocket
import _thread
from usr.logging import getLogger

logger = getLogger(__name__)

_serial_no_lock = _thread.allocate_lock()


def str_fill(source, rl="l", target_len=0, fill_field="0"):
    if len(source) >= target_len or target_len <= 0:
        return source
    if rl not in ("r", "l"):
        return source
    if not isinstance(fill_field, str):
        return source
    if isinstance(fill_field, str) and len(fill_field) == 0:
        return source

    fill_len = target_len - len(source)
    fill_info = fill_field * fill_len
    if rl == "l":
        return fill_info + source
    else:
        return source + fill_info


class SerialNo:

    def __init__(self):
        self.__num = 0xFFFF
        self.__iter_serial_no = iter(range(self.__num))

    def get_serial_no(self):
        """Get message serial number.

        Returns:
            int: serial number
        """
        try:
            with _serial_no_lock:
                return next(self.__iter_serial_no)
        except StopIteration:
            self.__iter_serial_no = iter(range(self.__num))
            return self.get_serial_no()


class TCPUDPBase:
    """This class is TCP/UDP base module."""

    def __init__(self, ip=None, port=None, domain=None, method="TCP", timeout=600, keep_alive=0):
        """
        Args:
            ip: server ip address (default: {None})
            port: server port (default: {None})
            domain: server domain (default: {None})
            method: TCP or UDP (default: {"TCP"})
        """
        self.__ip = ip
        self.__port = port
        self.__domain = domain
        self.__addr = None
        self.__method = method
        self.__socket = None
        self.__socket_args = []
        self.__timeout = timeout
        self.__keep_alive = keep_alive
        self.__socket_lock = _thread.allocate_lock()
        self.__conn_tag = 0
        self.__tid = None
        self.__callback = print
        self.__stack_size = 0x2000

    def __init_addr(self):
        """Get ip and port from domain.

        Raises:
            ValueError: Domain DNS parsing falied.
        """
        if self.__domain is not None and self.__domain:
            if self.__port is None:
                self.__port == 8883 if self.__domain.startswith("https://") else 1883
            try:
                addr_info = usocket.getaddrinfo(self.__domain, self.__port)
                self.__ip = addr_info[0][-1][0]
            except Exception as e:
                sys.print_exception(e)
                raise ValueError("Domain %s DNS parsing error. %s" % (self.__domain, str(e)))
        self.__addr = (self.__ip, self.__port)

    def __init_socket(self):
        """Init socket by ip, port and method

        Raises:
            ValueError: ip or domain or method is illegal.
        """
        if self.__check_ipv4():
            socket_af = usocket.AF_INET
        elif self.__check_ipv6():
            socket_af = usocket.AF_INET6
        else:
            raise ValueError("Args ip %s is illegal!" % self.__ip)

        if self.__method == 'TCP':
            socket_type = usocket.SOCK_STREAM
            socket_proto = usocket.IPPROTO_TCP
        elif self.__method == 'UDP':
            socket_type = usocket.SOCK_DGRAM
            socket_proto = usocket.IPPROTO_UDP
        else:
            raise ValueError("Args method is TCP or UDP, not %s" % self.__method)
        self.__socket_args = (socket_af, socket_type, socket_proto)

    def __check_ipv4(self):
        """Check ip is ipv4.

        Returns:
            bool: True - ip is ipv4, False - ip is not ipv4
        """
        self.__ipv4_item = r"(25[0-5]|2[0-4]\d|[01]?\d\d?)"
        self.__ipv4_regex = r"^{item}\.{item}\.{item}\.{item}$".format(item=self.__ipv4_item)
        if self.__ip.find(":") == -1:
            ipv4_re = ure.search(self.__ipv4_regex, self.__ip)
            if ipv4_re:
                if ipv4_re.group(0) == self.__ip:
                    return True
        return False

    def __check_ipv6(self):
        """Check ip is ipv6.

        Returns:
            bool: True - ip is ipv6, False - ip is not ipv6
        """
        self.__ipv6_code = r"[0-9a-fA-F]"
        ipv6_item_format = [self.__ipv6_code * i for i in range(1, 5)]
        self.__ipv6_item = r"{}|{}|{}|{}".format(*ipv6_item_format)

        if self.ip.startswith("::") or ure.search(self.__ipv6_item + ":", self.__ip):
            return True
        else:
            return False

    def __connect(self):
        """Socket connect when method is TCP

        Returns:
            bool: True - success, False - falied
        """
        with self.__socket_lock:
            self.__init_addr()
            self.__init_socket()
            if self.__socket_args:
                try:
                    logger.debug("self.__socket_args %s" % str(self.__socket_args))
                    self.__socket = usocket.socket(*self.__socket_args)
                    if self.__method == 'TCP':
                        logger.debug("self.__addr %s" % str(self.__addr))
                        self.__socket.connect(self.__addr)
                        if 1 <= self.__keep_alive <= 120:
                            self.__socket.setsockopt(usocket.SOL_SOCKET, usocket.TCP_KEEPALIVE, self.__keep_alive)
                    return True
                except Exception as e:
                    sys.print_exception(e)
            return False

    def __disconnect(self):
        """Socket disconnect

        Returns:
            bool: True - success, False - falied
        """
        with self.__socket_lock:
            if self.__socket is not None:
                try:
                    self.__socket.close()
                    self.__socket = None
                    return True
                except Exception as e:
                    sys.print_exception(e)
                    return False
            else:
                return True

    def __send(self, data):
        """Send data by socket.

        Args:
            data(bytes): byte stream

        Returns:
            bool: True - success, False - falied.
        """
        with self.__socket_lock:
            if self.__socket is not None:
                try:
                    if self.__method == "TCP":
                        write_data_num = self.__socket.write(data)
                        return (write_data_num == len(data))
                    elif self.__method == "UDP":
                        send_data_num = self.__socket.sendto(data, self.__addr)
                        return (send_data_num == len(data))
                except Exception as e:
                    sys.print_exception(e)
            return False

    def __read(self, bufsize=1024):
        """Read data by socket.

        Args:
            bufsize(int): read data size.

        Returns:
            bytes: read data info
        """
        logger.debug("start read")
        data = b""
        if self.__socket is not None:
            while True:
                read_data = b""
                try:
                    self.__socket.settimeout(0.5 if data else self.__timeout)
                    read_data = self.__socket.recv(bufsize)
                    logger.debug("read_data: %s" % read_data)
                except Exception as e:
                    if e.args[0] != 110:
                        sys.print_exception(e)
                        logger.error("%s read falied. error: %s" % (self.__method, repr(e)))
                data += read_data if read_data else b""
                if not read_data or len(data) >= bufsize:
                    break

        logger.debug("__read data", repr(data))
        return data

    def __wait_msg(self):
        _msg = b""
        while self.__conn_tag:
            if self.status() != 0:
                if self.status() != 1:
                    self.__disconnect()
                    self.__connect()
                logger.error("%s connection status is %s" % (self.__method, self.status()))
                utime.sleep(1)
                continue
            logger.debug("__wait_msg _msg", repr(_msg))
            _msg += self.__read()
            if not _msg:
                continue
            _msg = self.parse(_msg)

    def __downlink_thread_start(self):
        """This function starts a thread to read the data sent by the server"""
        if self.__tid is None or (self.__tid and not _thread.threadIsRunning(self.__tid)):
            _thread.stack_size(self.__stack_size)
            self.__tid = _thread.start_new_thread(self.__wait_msg, ())

    def __downlink_thread_stop(self):
        """This function stop the thread that read the data sent by the server"""
        if self.__tid:
            _cnt = 0
            while _thread.threadIsRunning(self.__tid) and _cnt < 300:
                utime.sleep_ms(10)
                _cnt += 1
            if _thread.threadIsRunning(self.__tid):
                _thread.stop_thread(self.__tid)
            self.__tid = None

    def parse(self, msg):
        if callable(self.__callback):
            self.__callback("Receive msg %s" % repr(msg))
        else:
            logger.info("Receive msg %s" % repr(msg))

        return b""

    def status(self):
        """Get socket connection status

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
                sys.print_exception(e)

        return _status

    def set_callback(self, callback):
        if callable(callback):
            self.__callback = callback
            return True
        return False

    def connect(self):
        """Connect server and start downlink thread for server

        Returns:
            bool: True - success, False - failed
        """
        if self.__conn_tag == 0:
            if self.__connect():
                self.__conn_tag = 1
                self.__downlink_thread_start()
                return True
        return False

    def disconnect(self):
        """Disconnect server, than stop downlink thread and heart beat timer

        Returns:
            bool: True - success, False - failed
        """
        if self.__conn_tag == 1:
            self.__conn_tag = 0
            self.__socket.settimeout(0.1)
            self.__downlink_thread_stop()
            return self.__disconnect()
        return True
