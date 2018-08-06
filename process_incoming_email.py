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
from msg_util import ParsedMessage
import expense_tracker
import invoice_parser
import re
import json
# https://github.com/olucurious/PyFCM/issues/115
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        m = re.search(r"(\S+)@", mail_message.to)
        if not m:
            return
        config = json.load(open('sheets.json'))
        if config["users"].index(mail_message.sender) == -1:
            print("Invalid user " + mail_message.sender)
            return
        expense_category = m.groups()[0]
        email = ParsedMessage(mail_message.original)
        parsed = invoice_parser.parse_msg(email.above_fwd_text)

        sheet_link = config["sheets"][expense_category]
        folder_id = config["folders"][expense_category]
        hash = email.hash()
        links = {}
        for (filename, body) in email.attachments():
            link = expense_tracker.upload_file(folder_id, hash + '.' + filename, body)
            links[filename] = link
        expense_tracker.add_entry(sheet_link, parsed['description'], parsed['price'], links, hash)
        mail.send_mail(sender=mail_message.to,
            to=mail_message.sender,
            subject='Re: ' + mail_message.original['Subject'],
            body="""
            Added {} to
            https://docs.google.com/spreadsheets/d/{}
        """.format(str(parsed), sheet_link),
            headers={
                "References": mail_message.original.get('References', ''),
                "In-Reply-To": mail_message.original.get('Message-ID', ''),
            },
        )

app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
