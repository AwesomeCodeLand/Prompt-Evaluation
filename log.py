#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import hashlib
import socket
from utils.configure import getConfigPath
from utils.tools import changeLogLevel

ErrLevel = "error"
DebugLevel = "debug"


def get_local_ip():
    """
    获取本机IP地址
    :return: 本机IP地址
    """
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def md5_hash(string):
    """
    计算字符串的MD5值
    :param string: 字符串
    :return: MD5值
    """
    m = hashlib.md5()
    m.update(string.encode("utf-8"))
    return m.hexdigest()


def get_current_timestamp():
    """
    获取当前时间戳
    :return: 当前时间戳(秒级)
    """
    return int(time.time())


def error_out_log(x_msg):
    output_log(x_msg, level=ErrLevel)


def output_log(x_msg, x_trace_id="", level="info"):
    """
    生成日志
    :param x_msg: 日志内容
    :param x_trace_id: 日志ID
    :return: 日志
    """
    # 判断下面处理是否会出现异常
    if not isinstance(x_msg, str):
        # check whether str() will be exception
        try:
            x_msg = str(x_msg)
        except Exception as e:
            x_msg = f"x_msg is not a string  {x_msg}"
    if not isinstance(x_trace_id, str):
        # check whether str() will be exception
        try:
            x_trace_id = str(x_trace_id)
        except Exception as e:
            x_trace_id = f"x_trace_id is not a string  {x_trace_id}"

    x_span_id = md5_hash(x_msg)

    # print(f'x_trace_id: {type(x_trace_id)}')
    # check whether x_trace_id is None
    # or is a empty string
    if x_trace_id is None or x_trace_id == "":
        # check whether x_span_id is Str
        # if x_span_id is not a str, convert it to str
        if not isinstance(x_span_id, str):
            x_span_id = str(x_span_id)
        x_trace_id = x_span_id

    log_data = {
        "x_msg": x_msg,
        "x_name": level,
        "x_server_ip": "127.0.0.1",
        "x_span_id": x_span_id,
        "x_timestamp": get_current_timestamp(),
        "x_trace_id": x_trace_id,
        "x_version": "python-gpt-1.0.0",
    }

    # output log_data item type
    log_json = json.dumps(log_data, ensure_ascii=False, separators=(",", ":"))

    # check the level whether equal to conf.LogLevel
    c = getConfigPath()

    # print(f"x_msg: {level} {c.logLevel}")
    if changeLogLevel(level) >= changeLogLevel(c.logLevel):
        # 输出日志
        print(log_json)
