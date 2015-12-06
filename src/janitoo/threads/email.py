# -*- coding: utf-8 -*-
"""The Raspberry email thread

Send notifications via email.
Check account for ne emails

"""

__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015 Sébastien GALLET aka bibi21000"

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+                                   # pragma: no cover
    from logging import NullHandler                   # pragma: no cover
except ImportError:                                   # pragma: no cover
    class NullHandler(logging.Handler):               # pragma: no cover
        """NullHandler logger for python 2.6"""       # pragma: no cover
        def emit(self, record):                       # pragma: no cover
            pass                                      # pragma: no cover
logger = logging.getLogger(__name__)

import os, sys
import threading
from pkg_resources import get_distribution, DistributionNotFound
from janitoo.thread import JNTBusThread
from janitoo.thread import JNTThread
from janitoo.options import get_option_autostart
from janitoo.utils import HADD
from janitoo.node import JNTNode
from janitoo.value import JNTValue
from janitoo.bus import JNTBus
from janitoo.classes import COMMAND_DESC

def make_thread(options):
    if get_option_autostart(options, 'email') == True:
        return EmailThread(options)
    else:
        return None

class EmailThread(JNTBusThread):
    """The email thread

    """

    def init_bus(self):
        """Build the bus
        """
        self.section = 'email'
        self.bus = JNTBus(options=self.options, oid=self.section, product_name="Email controller")
