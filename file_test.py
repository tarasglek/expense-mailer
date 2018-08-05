import sys
import email
from email_reply_parser import EmailReplyParser
from msg_util import ParsedMessage

def main(filename):
    raw_msg = open(filename).read()
    email_msg = email.message_from_string(raw_msg)
    msg = ParsedMessage(email_msg)
    for (filename, body) in msg.attachments():
        print(msg.fwd_headers2filename(filename), len(body))

if __name__ == "__main__":
    main(sys.argv[1])
