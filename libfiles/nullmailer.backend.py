from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
import threading
import os
import time
import sys
if sys.version_info[0] >= 3:
    unicode = str

NULLMAILER_SPOOLDIR = getattr(settings, 'NULLMAILER_SPOOLDIR', '/var/spool/nullmailer')

__nullmailer_threads_dict__ = {}

def to_utf8(addr):
    # RFC 6531 says that unicode email addresses must be encoded as utf8.
    # Also, according to this stackoverflow answer, if we have an unicode
    # email address, the only reasonable thing to do is to encode in utf8 and
    # hope that the target SMTP supports RFC 6531:
    #
    #  https://tools.ietf.org/html/rfc6531
    #  http://stackoverflow.com/a/14778640
    if isinstance(str(addr),unicode ):
        return str(addr).encode('utf-8')
    return str(addr)

class EmailBackend(BaseEmailBackend):

    __queue__ = "%s/queue" % NULLMAILER_SPOOLDIR
    __tmp__ = "%s/tmp" % NULLMAILER_SPOOLDIR
    __trigger__ = "%s/trigger" % NULLMAILER_SPOOLDIR

    def send_messages(self, email_messages):
        pid = os.getpid()
        tid = threading.current_thread().ident
        num_sent = 0
        if not email_messages:
            return
        for email_message in email_messages:
            from_email = to_utf8(email_message.from_email)
            to_lines = '\n'.join([str(to_utf8(addr)) for addr in email_message.to])
            msg = "%s\n%s\n\n%s" % ( from_email, to_lines, email_message.message().as_string())
            if self._send(msg, pid, tid):
                num_sent += 1
        return num_sent

    def fsyncspool(self):
        """
        Call fsync() on the queue directory
        """
        fd = -1
        try:
            fd = os.open(self.__queue__, os.O_RDONLY)
            os.fsync(fd)
        finally:
            if fd > -1: os.close(fd)

    def trigger(self):
        """
        Wakeup nullmailer writing to its trigger fifo
        """
        fd = -1
        try:
            fd = os.open(self.__trigger__, os.O_WRONLY|os.O_NONBLOCK)
            os.write(fd, b"\0")
        finally:
            if fd > -1: os.close(fd)


    def _send(self, data, pid, tid):
        global __nullmailer_threads_dict__
        if not tid in __nullmailer_threads_dict__:
            __nullmailer_threads_dict__[tid] = 0
        __nullmailer_threads_dict__[tid] += 1
        filename = "%f_%s_%d_%d_%d" % (time.time(), time.strftime("%Y.%m.%d.%H.%M.%S"), pid, tid, __nullmailer_threads_dict__[tid])
        tmp = "%s/%s" % (self.__tmp__, filename)
        spool = "%s/%s" % (self.__queue__, filename)

        with open(tmp, 'w') as f:
            f.write(data)

        try:
            os.link(tmp, spool)
            self.fsyncspool()
            self.trigger()
        finally:
            os.unlink(tmp)

        return True
