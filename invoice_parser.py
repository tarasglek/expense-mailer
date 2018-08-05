import re

def parse_msg(msg_text):
    m = re.match(r"\$([^ ]+) +(.*)$", msg_text)
    if not m:
        return None
    return {'price':m.groups()[0], 'description':m.groups()[1]}