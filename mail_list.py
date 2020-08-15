import poplib
import email
import telnetlib
import datetime
import time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import json


class DownMail:

    def __init__(self, username, pwd, server):
        self.pop3_server = server
        # 连接到POP3服务器,有些邮箱服务器需要ssl加密，可以使用poplib.POP3_SSL
        try:
            telnetlib.Telnet(self.pop3_server, 995)
            self.server = poplib.POP3_SSL(self.pop3_server, 995, timeout=10)
        except:
            time.sleep(5)
            self.server = poplib.POP3(self.pop3_server, 110, timeout=10)
        self.server.user(username)
        self.server.pass_(pwd)

    def my_charset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def my_content(self, msg):
        content = ''
        for part in msg.walk():
            content_type = part.get_content_type()
            charset = self.my_charset(part)
            # 如果有附件，则直接跳过
            if part.get_filename() is not None:
                continue
            email_content_type = ''
            if content_type == 'text/plain':
                email_content_type = 'text'
            elif content_type == 'text/html':
                print('html 格式 跳过')
                continue
            if charset:
                try:
                    content += part.get_payload(decode=True).decode(charset)
                # 这里遇到了几种由广告等不满足需求的邮件遇到的错误，直接跳过了
                except AttributeError:
                    print('type error')
                except LookupError:
                    print("unknown encoding: utf-8")
            if email_content_type == '':
                continue
        return content

    # 字符编码转换
    # @staticmethod
    def decode_str(self, str_in):
        value, charset = decode_header(str_in)[0]
        if charset:
            value = value.decode(charset)
        return value

    # 解析邮件,获取附件
    def get_att(self, msg_in, str_day):
        attachment_files = []
        for part in msg_in.walk():
            # 获取附件名称类型
            file_name = part.get_param("name")  # 如果是附件，这里就会取出附件的文件名
            # file_name = part.get_filename() #获取file_name的第2中方法
            # contType = part.get_content_type()
            if file_name:
                h = email.header.Header(file_name)
                # 对附件名称进行解码
                dh = email.header.decode_header(h)
                filename = dh[0][0]
                if dh[0][1]:
                    # 将附件名称可读化
                    filename = self.decode_str(str(filename, dh[0][1]))
                    # print(filename)
                    # filename = filename.encode("utf-8")
                # 下载附件
                data = part.get_payload(decode=True)
                # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
                att_file = open('./test/' + filename, 'wb')
                att_file.write(data)  # 保存附件
                att_file.close()
                attachment_files.append(filename)
            # else:
                # 不是附件，是文本内容
                # print(self.get_content(part))
                # # 如果ture的话内容是没用的
                # if not part.is_multipart():
                #     # 解码出文本内容，直接输出来就可以了。
                #     print(part.get_payload(decode=True).decode('utf-8'))

        return attachment_files

    def get_mails(self):
        print('Messages: %s. Size: %s' % self.server.stat())
        resp, mails, octets = self.server.list()
        str_day = str(datetime.date.today())
        res = {}
        for i in range(len(mails), 0, -1):
            resp, lines, octets = self.server.retr(i)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            msg = Parser().parsestr(msg_content)
            Content = self.my_content(msg)
            From = parseaddr(msg.get('from'))[1]
            To = parseaddr(msg.get('To'))[1]
            Cc = parseaddr(msg.get_all('Cc'))[1]
            Subject = self.decode_str(msg.get('Subject'))
            print(msg.get("Date"))
            try:
                date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')
            except:
                date1 = time.strptime(msg.get("Date")[0:19], '%d %b %Y %H:%M:%S')
            date2 = time.strftime("%Y-%m-%d %H:%M:%S", date1)
            attach_file = self.get_att(msg, str_day)
            res[date2] = {
                "From": From,
                "To": To,
                "Cc": Cc,
                "Subject": Subject,
                "Content": Content,
                "Attach": attach_file
            }
            # if date2 < str_day:
            #     break

        # 可以根据邮件索引号直接从服务器删除邮件
        # self.server.dele(26)
        self.server.quit()
        return res


if __name__ == '__main__':
    user = '**@163.com'
    password = 'FJBQRTPCWRMTMRRU'
    email_server = 'pop.163.com'
    email_class = DownMail(user, password, email_server)
    mails = email_class.get_mails()
    with open("data.json", "w") as f:
        f.write(json.dumps(mails, ensure_ascii=False, indent=4))
