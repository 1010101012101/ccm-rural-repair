# Copyright (c) 2016-present, Facebook, Inc.
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant 
# of patent rights can be found in the PATENTS file in the same directory.

from freeswitch import consoleLog

import subprocess

def python_get_temp():
    warning_temp = 70
    temp_loc = "/sys/class/thermal/thermal_zone0/temp"
    raw_temp = subprocess.check_output(["cat", temp_loc]).strip()
    integer_temp = int(raw_temp[:2])
    # removed decimal numbers for readability
    #decimal_temp = int(raw_temp[2:])
    if integer_temp >= warning_temp:
        warning_status = "BABALA: Mataas ang temperatura ng sistema. Maaari itong mamatay ano mang oras."
    else:
        warning_status = "Temperatura OK."
    return "%s Ang temperatura ng BTS computer ay %s degrees C." % (warning_status, integer_temp)

def chat(message, placeholder):
    res = python_get_temp() 
    temp_loc = "/sys/class/thermal/thermal_zone0/temp"
    consoleLog('info', "Checking CPU temp at %s: %s" % (temp_loc, res))
    message.chat_execute('set', '_localstr=%s' % res)

def fsapi(session, stream, env, placeholder):
    res = python_get_temp()
    if isinstance(session, str):
        # we're in the FS CLI, so no session object
        consoleLog('info', "No session; otherwise would set _localstr=%s" % res)
    else:
        session.execute("set", "_localstr=%s" % res)

def handler(session, placeholder):
    res = python_get_temp()
    session.execute("set", "_localstr=%s" % res)

