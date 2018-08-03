# Copyright (c) 2016-present, Facebook, Inc.
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant 
# of patent rights can be found in the PATENTS file in the same directory.

from freeswitch import consoleLog

import json

MANUAL = "/usr/share/freeswitch/scripts/sms-manual.json"

def man_lookup(code):
    with open(MANUAL, 'r+') as man:
        man_dict = json.load(man)
        lookup = code.lower()
        if lookup in man_dict: 
            entry = man_dict[lookup]
        else:
            entry = "Maling keyword."
        return str(entry)

def chat(message, args):
    code = args
    entry = man_lookup(code) 
    
    last_ix_msg = int(round(len(entry)/160))
    for i in range(last_ix_msg + 1):
        value = entry[i*160 : min((i + 1)*160, len(entry))] 
        varname = 'manmsg_' + str(i)
        consoleLog('info', "Return Chat: " + varname + "=" + value + "\n")
        message.chat_execute('set', '%s=%s' % (varname, value))


def fsapi(session, stream, env, args):
    res = man_lookup(args)
    if isinstance(session, str):
        # we're in the FS CLI, so no session object
        consoleLog('info', "No session; otherwise would set _localstr=%s" % res)
    else:
        session.execute("set", "_localstr=%s" % res)

def handler(session, args):
    res = man_lookup(args)
    session.execute("set", "_localstr=%s" % res)
    
