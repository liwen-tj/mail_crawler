import smtplib
from email.mime.text import MIMEText

subject = "auto mail"
sender = "**@163.com"
content = "have a nice day"
receiver = "liwen00812@qq.com"
password = "FJBQRTPCWRMTMRRU"
message = MIMEText(content, "plain", "utf-8")

message['Subject'] = subject
message['To'] = receiver
message['From'] = sender

smtp = smtplib.SMTP_SSL("smtp.163.com", 994)
smtp.login(sender, password)
smtp.sendmail(sender, [receiver], message.as_string())
smtp.close()

