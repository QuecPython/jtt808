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
@file      :common.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :<description>
@version   :1.0.0
@date      :2022-05-19 20:12:09
@copyright :Copyright (c) 2022
"""

import _thread


def option_lock(thread_lock):
    """Function thread lock decorator"""
    def function_lock(func):
        def wrapperd_fun(*args, **kwargs):
            with thread_lock:
                return func(*args, **kwargs)
        return wrapperd_fun
    return function_lock


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


class Singleton(object):
    """Singleton base class"""
    _instance_lock = _thread.allocate_lock()

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            Singleton.instance_dict = {}

        if str(cls) not in Singleton.instance_dict.keys():
            with Singleton._instance_lock:
                _instance = super().__new__(cls)
                Singleton.instance_dict[str(cls)] = _instance

        return Singleton.instance_dict[str(cls)]
