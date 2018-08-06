import sys
import email
from msg_util import ParsedMessage
import invoice_parser

def main(filename):
    raw_msg = open(filename).read()
    email_msg = email.message_from_string(raw_msg)
    msg = ParsedMessage(email_msg)
    # print(msg.get_body())
    print(invoice_parser.parse_msg(msg.above_fwd_text))
    for (filename, body) in msg.attachments():
        print(msg.fwd_headers2filename(filename), len(body))
    print([msg.hash()])

if __name__ == "__main__":
    main(sys.argv[1])
