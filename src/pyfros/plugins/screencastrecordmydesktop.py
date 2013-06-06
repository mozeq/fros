## Copyright (C) 2013 ABRT team <abrt-devel-list@redhat.com>
## Copyright (C) 2013 Red Hat, Inc.

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Suite 500, Boston, MA  02110-1335  USA

from pyfros.screencastbase import ScreencastBase, ScreencastResult
import pyfros.plugins.const as const
import popen2
import fcntl
import os
import signal
#pylint: disable=E0611
from gi.repository import GLib
import re
from pyfros.froslogging import warn


def getScreencastPluginInstance():
    return ScreencastRecordMyDesktop()


class ScreencastRecordMyDesktop(ScreencastBase):
    r = re.compile(r'.(?P<num>\d+).')
    recorapp = None
    enc_completed = None
    recPid = None
    screencast_done = None

    # pylint: disable=W0613
    def enc_progress(self, source, condition):
        """
        Callback which is run when there is some data to be read from the
        child stdout
        It updates the progress bar if the data read from the child contains
        a progress information
        """
        if self.recorapp.poll() != -1:  # process died
            #Gtk.main_quit()  # encoding finished, so just close the window
            print  # print empty line to to align the progress output
            self.screencast_done()

        strstdout = ""
        try:
            c = ""
            strstdout = ""
            # read only until ']' - the string we're trying to read is:
            # "[X%]" or "[XX%]"
            while self.recorapp.poll() == -1 and c != "]":
                c = self.recorapp.fromchild.read(1)
                strstdout += c

        except IOError, ex:
            pass  # fd is non-blocking so we ignore "Resource unavailable"

        except Exception, ex:
            warn(ex)

        # child process prints some escape sequences to control the output on
        # terminal, so we need to filter it only tor ord(c) < 32, otherwise the
        # regexp matching is not reliable
        cleaned_str = ''.join(c for c in strstdout.strip() if ord(c) >= 32)
        num_regexp = self.r.match(cleaned_str)
        num = ""
        if num_regexp:
            num = num_regexp.group("num")

        if not num:
            return True

        self.enc_completed = float(num)
        percentage = self.enc_completed/100.0
        if percentage > 1.0 or (self.recorapp.poll() != -1):
            percentage = 1.0

        self.progress_update(self.enc_completed)
        return True

    def __init__(self, *args, **kwargs):
        super(ScreencastRecordMyDesktop, self).__init__(*args, **kwargs)
        self.output = os.path.join(os.getcwd(), "screencast.ogv")

    def ScreencastArea(self):
        print "ScreencastArea ScreencastRecordMyDesktop"

    def IsSuitable(self):
        return const.SUITABLE_DEFAULT  # 1 is default

    def Screencast(self):
        args = [
            "recordmydesktop",
            "-o", self.output,  # where to save the screencast
            "--fps", "5",  # 5 fps should be enough
            "--no-sound",  # we don't care about the sound
            "--v_quality", "50",  # 50 seems to be a good quality/size ratio
            "--workdir", "/tmp",
            "-x", str(self.x),  # top left corner coordinates
            "-y", str(self.y),
            "--width",  str(self.width),  # low right corner offset
            "--height", str(self.height)
        ]

        self.recorapp = popen2.Popen3(args, True, 0)
        flags = fcntl.fcntl(self.recorapp.fromchild, fcntl.F_GETFL)
        fcntl.fcntl(self.recorapp.fromchild, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        self.recPid = self.recorapp.pid
        #if self.recPid != None:
        #    stop_button.set_sensitive(True)
        #    button.set_sensitive(False)
        return ScreencastResult(self.recPid is not None, self.output)

    def StopScreencast(self, end_handler):
        """
        Callback to stop the recording process
        """
        self.screencast_done = end_handler
        os.kill(self.recPid, signal.SIGINT)

        giochannel = GLib.IOChannel(filedes=self.recorapp.fromchild.fileno())
        giochannel.add_watch(GLib.IO_IN | GLib.IO_HUP, self.enc_progress)
