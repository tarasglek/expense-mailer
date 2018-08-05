# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START log_sender_handler]
import logging

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import webapp2
from google.appengine.api import mail
import msg_util

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)

# [END log_sender_handler]
# [START bodies]
        plaintext_bodies = mail_message.bodies('text/plain')
        html_bodies = mail_message.bodies('text/html')

        for content_type, body in plaintext_bodies:
            plaintext = body.decode()
            logging.info("Plain text body of length %d. '%s'", len(plaintext), plaintext)
        mail.send_mail(sender=mail_message.to,
            to=mail_message.sender,
            subject='Re: ' + mail_message.original['Subject'],
            body="""
            test body
        """,
            headers={
                "References": mail_message.original.get('References', ''),
                "In-Reply-To": mail_message.original.get('Message-ID', ''),
            },
            attachments=[("orig_msg.txt", mail_message.original.as_string())],
        )

# [START app]
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
# [END app]
