from urllib import request
import re
from project.xml_handler import MailListXMLHandler
from xml import sax
import json
from datetime import datetime


class Project:
    def __init__(self, name, mail_list):
        self.name = name
        self.mail_list = mail_list
        self.base_url = "https://mail-archives.apache.org/mod_mbox/" + name + "-" + mail_list + "/"

    def getHistoryMonths(self):
        months_html = request.urlopen(self.base_url).read().decode("utf-8")
        months = re.compile(r'''<span class="links" id="(.*?)">''').findall(months_html)
        return months  # list

    def getMailData(self, month, mail_id, parent_id, depth):
        url = self.base_url + month + ".mbox/ajax/" + mail_id
        data = request.urlopen(url).read().decode("utf-8")
        mail = re.compile(r"<!\[CDATA\[(.*?)]]").findall(data)
        row = {
            "id": mail_id,
            "from": mail[0],
            "to": self.mail_list + "@" + self.name + ".apache.org",
            "date": mail[2],
            "subject": mail[1],
            "content": mail[3],
            "depth": depth,
            "reply": parent_id
        }
        return row

    def getMonthData(self, month):
        page = "0"
        original_id = ""
        mails = []
        counter = 1
        while True:
            archive_url = self.base_url + month + ".mbox/ajax/thread?" + page
            archive_xml = request.urlopen(archive_url).read().decode("utf-8")
            handler = MailListXMLHandler()
            sax.parseString(archive_xml, handler)
            messages = handler.messages
            for msg in messages:
                if int(msg['depth']) == 0:
                    original_id = msg['id']
                if msg['linked'] == "1":  # only store data with link
                    mail = self.getMailData(month, msg['id'], original_id, msg['depth'])
                    mails.append(mail)
                    print(counter, page)
                    counter += 1
            index = handler.index
            if int(index['page']) + 1 == int(index['pages']):
                break
            page = index['page']
        return mails


if __name__ == '__main__':
    pro = Project('flink', 'user-zh')
    # todo: multi process / thread
    start = datetime.now()
    res = pro.getMonthData('202007')
    end = datetime.now()
    print((end-start).seconds)
    with open("202007.json", "w") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))

