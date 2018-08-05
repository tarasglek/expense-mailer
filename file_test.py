import sys

import email

seen_it=set()
def dump(msg):
    if msg in seen_it:
        return
    seen_it.add(msg)
    for part in msg.walk():
        if part.is_multipart():
            print('walking-multipart')
            dump(part)
            print('end-multipart')
        else:
            print('blehbleh',part.get_content_type())
            print(part.as_string())
def main():
    print(sys.argv)
    msg = email.message_from_file(fp=open(sys.argv[1]))
    dump(msg)

main()
