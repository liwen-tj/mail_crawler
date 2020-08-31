import xml.sax


class MailListXMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.messages = []
        self.index = {}

    def startElement(self, tag, attributes):
        if tag == "index":
            self.index['page'] = attributes["page"]
            self.index['pages'] = attributes["pages"]

        elif tag == "message":
            self.messages.append({
                "linked": attributes["linked"],
                "depth": attributes["depth"],
                "id": attributes["id"]
            })


class MailXMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.currentData = ''
        self.mail = {}
        self._from = ''
        self.subject = ''
        self.date = ''
        self.details = ''

    def startElement(self, tag, attributes):
        if tag == 'from' or tag == 'subject' or tag == 'date' or tag == 'contents':
            self.currentData = tag

    def endElement(self, tag):
        if tag == 'from':
            self.mail['from'] = self._from
        elif tag == 'subject':
            self.mail['subject'] = self.subject
        elif tag == 'date':
            self.mail['date'] = self.date
        elif tag == 'contents':
            self.mail['contents'] = self.details

    def characters(self, content):
        if self.currentData == 'from':
            self._from = content
        elif self.currentData == 'subject':
            self.subject = content
        elif self.currentData == 'date':
            self.date = content
        elif self.currentData == 'contents':
            self.details = content
