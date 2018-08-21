import re, urllib
import hashlib

def mangle(s):
    return re.sub(r"\s+", " ", re.sub(r"(%..|[+/])", " ",urllib.quote_plus(s))).strip()

class ParsedMessage():
    def __init__(self, email):
        self._email = email
        self._parse_body()

    """
    Parse gmail fwded messages into part-before-fwd header + header metadata + fwded msg
    """
    def _parse_body(self):
        body = self.get_body().replace("\r\n","\n")
        # print(body)
        (before, fwd) = body.split("---------- Forwarded message ---------", 1)
        ls = fwd.split('\n\n', 1)
        fwd_headers = ls[0]
        fwd_msg = ls[1] if len(ls) == 2 else ''
        fwd_headers_dict = {}
        for header in fwd_headers.split('\n'):
            m = re.match(r"^([^ :]+): (.+)", header)
            if not m:
                continue
            (key, value) = m.groups()
            fwd_headers_dict[key] = value
        self.above_fwd_text = before.strip()
        self.fwd_headers = fwd_headers_dict
        self.fwd_body = fwd_msg

    """
    Find the text/plain encoded msg body
    """
    def get_body(self):
        for part in self._email.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain" and part.get_filename() == None:
                return part.get_payload(decode=True)


    def fwd_headers2filename(self, filename):
        return '/'.join([self.fwd_headers['From'], mangle(self.fwd_headers['Subject']), self.fwd_headers['Date'], filename])

    def attachments(self):
        for part in self._email.walk():
            filename =  part.get_filename()
            if filename:
                yield (filename, part.get_payload(decode=True))

    def hash(self):
        m = hashlib.sha256()
        m.update(self.fwd_body)
        for (filename, body) in self.attachments():
            m.update(filename)
            m.update(body)
        return m.hexdigest()

