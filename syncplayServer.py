#!/usr/bin/env python3
#coding:utf8

import sys

# libpath

try:
    if (sys.version_info.major != 3) or (sys.version_info.minor < 4):
        raise Exception("You must run Syncplay with Python 3.4 or newer!")
except AttributeError:
    import warnings
    warnings.warn("You must run Syncplay with Python 3.4 or newer!")

from twisted.internet import reactor
from twisted.internet.endpoints import serverFromString
from twisted.internet.defer import Deferred
from twisted.internet.task import react

from syncplay.server import SyncFactory, ConfigurationGetter

def main(reactor, args):
    fatal = Deferred()  # Use this to signal a fatal problem with the server.
    factory = SyncFactory(
        0,
        args.password,
        args.motd_file,
        args.isolate_rooms,
        args.salt,
        args.disable_ready,
        args.disable_chat,
        args.max_chat_message_length,
        args.max_username_length,
        args.stats_db_file
    )

    for endpoint in args.endpoint:
        serverFromString(reactor, endpoint).listen(factory).addErrback(fatal.errback)

    return fatal

if __name__ == '__main__':
    argsGetter = ConfigurationGetter()
    react(main, (argsGetter.getConfiguration(),))
