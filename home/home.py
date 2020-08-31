from urllib import request
import re
import json


def getProjects(url):
    html = request.urlopen(url).read().decode("utf-8")
    return re.compile(r'<h3>.+?</li><li>').findall(html)


def getProjectName(proj):
    res = re.compile(r"<a name='(.*?)'>").findall(proj)
    return res[0].split(".")[0]  # delete .incubator


def getProjectMails(proj):
    res = re.compile(r"<li><a href=(.*?)</a></li>").findall(proj)
    mails = [r.split(">")[1] for r in res]
    return mails


if __name__ == '__main__':
    home = "https://mail-archives.apache.org/mod_mbox/"
    projects = getProjects(home)
    mail_lists = {}
    for project in projects:
        name = getProjectName(project)
        lists = getProjectMails(project)
        mail_lists[name] = lists

    with open("projects.json", "w") as f:
        f.write(json.dumps(mail_lists, ensure_ascii=False, indent=4))
