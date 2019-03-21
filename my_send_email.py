import smtplib
from email.mime.multipart import MIMEMultipart
import json
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from find_file import Affiliate
import os
import time
from multiprocessing.pool import ThreadPool
from functools import partial
import asyncio

start = time.time()

with open("affiliate_email.json") as f:
    affiliates = json.load(f)

with open("client_secret.json") as f:
    secret = json.load(f)
    MY_EMAIL = secret.get("MY_EMAIL")
    PASSWORD = secret.get("PASSWORD")

with open("msg.txt") as f:
    body = f.read()

with open("title.txt") as f:
    title = f.read()

    # attachment = open("data.xlsx", 'rb')
    # xlsx = MIMEBase('application', 'vnd.ms-excel')
    # xlsx.set_payload(attachment.read())
    # attachment.close()
    # encoders.encode_base64(xlsx)
    # xlsx.add_header('Content-Disposition', 'attachment', filename='data.xlsx')
    # msg.attach(xlsx)


def attach_file(msg, file_path, filename):
    attachment = open(file_path, 'rb')
    csvfile = MIMEBase('application', 'octet-stream')
    csvfile.set_payload(attachment.read())
    attachment.close()
    encoders.encode_base64(csvfile)
    csvfile.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(csvfile)
    return msg


async def send_email(affiliate, myemail, password, Subject, body):
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(myemail, password)
    msg = MIMEMultipart()

    msg['From'] = myemail
    msg['To'] = ", ".join(affiliate.email)
    msg['Subject'] = Subject

    msg.attach(MIMEText(body, 'plain'))
    file_path = affiliate.email_attachment
    if file_path:
        for i in file_path.keys():
            name = os.path.basename(file_path[i])
            msg = attach_file(msg, file_path[i], name)
    s.send_message(msg)
    s.quit()


# pool = ThreadPool(8)
_list = []
for i in affiliates.keys():
    affiliate_ = Affiliate(i, affiliates[i])
    if affiliate_.email_attachment is None:
        pass
    else:
        _list.append(affiliate_)


# send_email_multi = partial(send_email, myemail=MY_EMAIL, password=PASSWORD, Subject=title, body=body)
# pool.map(send_email_multi, _list)


loop = asyncio.get_event_loop()
tasks = []
for i in _list:
    tasks.append(loop.create_task(send_email(i, MY_EMAIL, PASSWORD, title, body)))
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()
print(f"{end - start}")
# but no speed up
