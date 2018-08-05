import re

def parse_msg(msg_text):
    m = re.match(r"\$([^ ]+) +(.*)$", msg_text)
    if not m:
        return None
    return (m.groups()[0], m.groups()[1])