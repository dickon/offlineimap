# Copyright (C) 2007-2011 John Goerzen & contributors
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
try:
    from urllib import urlencode
except ImportError: # python3
    from urllib.parse import urlencode
import email
import logging
from offlineimap.ui.UIBase import UIBase
import offlineimap
import logging
import sys
import subprocess
import time

protocol = '7.0.0'
def run(command):
    pobj = subprocess.Popen(command, stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
    pobj.communicate()
    return pobj.returncode


def index():
    run(['pkill', '-f',  'mu server'])
    while 1:
        ec = run(['pgrep', '-f', 'mu server'])
        if ec == 1:
            break
        time.sleep(0.1)
    run(['mu', 'index', '--maildir=/scratch/Mail/citrix'])
    print '[indexed]'


class Biff(UIBase):
    def syncingmessages(self, sr, srcfolder, dr, destfolder):
        pass

    def syncingfolder(self, srcrepos, srcfolder, destrepos, destfolder):
        pass

    def acctdone(self, account):
        pass

    def acct(self, account):
        pass

    def connecting(self, hostname, port):
        pass

    def copyingmessage(self, uid, num, num_to_copy, srcfolder, destfolder):
        message = srcfolder.getmessage(uid)
        pmess = email.message_from_string(message)
        author = pmess.get('from')
        if '<' in author:
            author = author[:author.find('<')-1]
        pl = pmess.get_payload()
        if type(pl) == type([]):
            pl = pl[0].get_payload()
        if type(pl) == type([]):
            pl = 'MULTIPART'
        print destfolder, author, pmess.get('subject'), 
        print ' '.join(pl[:300].split()),

    def savemessage(self, debugtype, uid, flags, folder):
        pass

    ################################################## UTILS
    def setup_consolehandler(self):
        ch = logging.StreamHandler(sys.stdout)
        # create formatter and add it to the handlers
        self.formatter = logging.Formatter("%(message)s")
        ch.setFormatter(self.formatter)
        # add the handlers to the logger
        self.logger.addHandler(ch)
        return ch

    def addingflags(self, uidlist, flags, dest):
        pass

    def madelocalmessage(self, filename):
        index()
