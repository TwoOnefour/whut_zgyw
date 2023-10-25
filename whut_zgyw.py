import os.path
import time
import requests
from lxml import etree
from datetime import datetime
from sys import argv, exit


def echo(msg):
    print(f"{str(datetime.now())[:-7]}\t{msg}")


class Zgyw:
    def __init__(self):
        self.session = requests.session()
        self.url = "http://59.69.102.9/zgyw/"
        self.username = None
        self.password = None

    def save_token(self, token):
        with open("token", "w") as f:
            f.write(token)

    def login(self):
        if os.path.exists("token"):
            echo("token存在，尝试登录")
            with open("token", "r") as f:
                token = f.read()
                self.session.cookies.set("ASP.NET_SessionId", token)
            if self.get_learning_time() is not None:
                self.get_learning_time()
                echo("登录成功")
                return
            else:
                echo("token过期，将继续登录")
                self.session.cookies.clear("")

        url = "http://59.69.102.9/zgyw"
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61"
        })
        # res = session.get("https:" + view_token)
        html = self.session.get(url)
        etree.HTMLParser(encoding="utf-8")
        # tree = etree.parse(local_file_path)
        tree = etree.HTML(html._content.decode("utf-8"))
        # session.get("https://view-cache.book118.com" + json.loads(str(tree.xpath("/html/body/div[1]/input[2]")[0].attrib).replace("'", "\""))["value"])
        __VIEWSTATE = tree.xpath("//input[@id='__VIEWSTATE']")[0].attrib["value"]
        status = self.session.post(f"{url}/index.aspx", data={
            "ctl00$ContentPlaceHolder1$name": self.username,
            "ctl00$ContentPlaceHolder1$pwd": self.password,
            "ctl00$ContentPlaceHolder1$login": "登录",
            "__VIEWSTATE": __VIEWSTATE
        })
        if len(status.history) != 1:
            echo("账号错误，请修改")
            exit(0)
        self.save_token(self.session.cookies.get("ASP.NET_SessionId"))
        echo("登陆成功")
        # self.echo(f"当前学习时间为：{self.get_learning_time()}")

    def process(self):
        echo("开始学习")
        while True:
            self.session.get("http://59.69.102.9/zgyw/study/LearningContent.aspx?type=2&id=9&learningid=2500")
            result = self.get_learning_time()
            if result is not None:
                echo(f"当前学习时间为：{result}")
                time.sleep(60)  # 60秒刷一次
            else:
                echo("登录超时，重新登陆")
                self.login()
                continue
            # self.echo(f"当前学习时间为：{self.get_learning_time()}")

    def get_learning_time(self):
        html = self.session.get("http://59.69.102.9/zgyw/onlineExam/user/usercenter.aspx")
        tree = etree.HTML(html._content.decode("utf-8"))
        now_learning_time = tree.xpath("//span[@id='ctl00_ContentPlaceHolder1_lblonlineTime']")[0].text # span id="ctl00_ContentPlaceHolder1_lblonlineTime"
        if now_learning_time is None:
            os.remove("token")
        return now_learning_time

    def run(self):
        self.login()
        self.process()


if __name__ == "__main__":
    if len(argv) <= 1:
        print(f"用法：\npython whut_zgyw.py 学号")
    elif len(argv[1]) == 13:
        bot = Zgyw()
        bot.username = argv[1]  # 用户名
        bot.password = bot.username
        bot.run()
    else:
        print(f"{str(datetime.now())[:-7]}\t请输入正确的学号")
