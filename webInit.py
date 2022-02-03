#!/usr/bin/python3

import argparse, os, json, datetime
from string import Template

pJoin = os.path.join
curr_path = os.path.dirname(os.path.realpath(__file__))

def getFnameWithoutExtension(fname_withextention: str):
    return ".".join(fname_withextention.split(".")[:-1])

def getDate():
    e = datetime.datetime.now()
    return e.strftime("%b %d, %Y")

class Config:# {{{
    TEMPLATE_DIR = "webInitTemplate"
    ASSET_DIR = "assets"
    def __init__(self):
        self.template_dir = pJoin(curr_path, self.TEMPLATE_DIR)
        self.readAuthorInfo()

        self.wd: str
        self.asset: bool
        self.author: str
        self.author_email: str

        self.include_css = True
        self.include_js = True

        self.main_fname = "index.html"
        self.main_template = pJoin(self.template_dir, "main.template.html")

        self.css_fname = "style.css"
        self.css_template = pJoin(self.template_dir, "style.template.css")

        self.js_fname = "script.js"
        self.js_template = pJoin(self.template_dir, "script.template.js")

    def setWorkingDir(self, wd: str):
        self.wd = wd

    def useAssetFolder(self, flag: bool):
        self.asset = flag

    def readAuthorInfo(self):
        with open(pJoin(self.template_dir, "config.json"), "r", encoding = "utf-8") as fp:
            data = json.load(fp)
        self.author = data["Author"]
        self.author_email = data["Email"]# }}}

class WebConstructer:# {{{
    def __init__(self, wd: str):# {{{
        self.config = Config()
        if os.path.exists(wd) and os.path.isdir(wd):
            self.config.setWorkingDir(wd)
        else:
            raise Exception("Abort, {} is not a valid directory.".format(wd))
# }}}
    def initHTML(self):# {{{
        if self.config.asset:
            css_fname = pJoin(Config.ASSET_DIR, self.config.css_fname)
            js_fname = pJoin(Config.ASSET_DIR, self.config.js_fname)
        else:
            css_fname = self.config.css_fname
            js_fname = self.config.js_fname

        with open(self.config.main_template, "r", encoding = "utf-8") as fp:
            t = fp.read()
        t = Template(t)
        d = {
            "FNAME":self.config.main_fname,
            "AUTHOR":self.config.author,
            "EMAIL":self.config.author_email,
            "DATE":getDate(),

            "TITLE": getFnameWithoutExtension(self.config.main_fname),
            "CSS_FILE": css_fname,
            "JS_FILE": js_fname
        }
        with open(pJoin(self.config.wd, self.config.main_fname), "w", encoding = "utf-8") as fp:
            fp.write(t.substitute(d))
# }}}
    def initCSS(self):# {{{
        if self.config.asset:
            css_fname = pJoin(Config.ASSET_DIR, self.config.css_fname)
        else:
            css_fname = self.config.css_fname

        with open(self.config.css_template, "r", encoding = "utf-8") as fp:
            t = fp.read()
        t = Template(t)
        d = {
            "FNAME":self.config.css_fname,
            "AUTHOR":self.config.author,
            "EMAIL":self.config.author_email,
            "DATE":getDate()
        }
        with open(pJoin(self.config.wd, css_fname), "w", encoding = "utf-8") as fp:
            fp.write(t.substitute(d))
# }}}
    def initJS(self):# {{{
        if self.config.asset:
            js_fname = pJoin(Config.ASSET_DIR, self.config.js_fname)
        else:
            js_fname = self.config.js_fname

        with open(self.config.js_template, "r", encoding = "utf-8") as fp:
            t = fp.read()
        t = Template(t)
        d = {
            "FNAME":self.config.js_fname,
            "AUTHOR":self.config.author,
            "EMAIL":self.config.author_email,
            "DATE":getDate()
        }
        with open(pJoin(self.config.wd, js_fname), "w", encoding = "utf-8") as fp:
            fp.write(t.substitute(d))
# }}}
    def run(self):# {{{
        SAFE_RUN = True
        if os.path.exists(pJoin(self.config.wd, self.config.main_fname)):
            SAFE_RUN = False
            print(f"{self.config.main_fname} exists")
        if os.path.exists(pJoin(self.config.wd, self.config.css_fname)):
            SAFE_RUN = False
            print(f"{self.config.css_fname} exists")
        if os.path.exists(pJoin(self.config.wd, self.config.js_fname)):
            SAFE_RUN = False
            print(f"{self.config.js_fname} exists")

        if not SAFE_RUN:
            while True:
                ans = input("Some file exists, run anyway? [y/n]:")
                if ans == "y":
                    break
                if ans == "n":
                    print("Abort.")
                    exit()
                else:
                    print("Answer should be either y or n.")

        if self.config.asset:
            if not os.path.exists(pJoin(self.config.wd, Config.ASSET_DIR)):
                os.mkdir(pJoin(self.config.wd, Config.ASSET_DIR))

        self.initHTML()
        if self.config.include_css:
            self.initCSS()
        if self.config.include_js:
            self.initJS()
        print("Finished.")
# }}}
# }}}

if __name__ == "__main__":# {{{
    parser = argparse.ArgumentParser(description = "Init a directory to be webpage.")
    parser.add_argument("name", help = "Name of the main html file.")
    parser.add_argument("--asset", action = "store_true", \
                        help = "Use asset directory.")
    parser.add_argument("-c", "--css_fname", action = "store", default = "style", \
                        help = "CSS file name, set to \"None\" to not creating css file.")
    parser.add_argument("-j", "--js_fname", action = "store", default = "script", \
                        help = "JavaScript file name, set to \"None\" to not creating javascript file.")

    web_con = WebConstructer(os.getcwd())

    args = parser.parse_args()
    if args.name.endswith(".html"):
        web_con.config.main_fname = args.name
    else:
        web_con.config.main_fname = args.name+".html"

    if args.asset:
        web_con.config.useAssetFolder(True)
    else:
        web_con.config.useAssetFolder(False)

    if args.css_fname == "None":
        web_con.config.include_css = False
    else:
        if not args.css_fname.endswith(".css"):
            args.css_fname += ".css"
        web_con.config.css_fname = args.css_fname

    if args.js_fname == "None":
        web_con.config.include_js = False
    else:
        if not args.js_fname.endswith(".js"):
            args.js_fname += ".js"
        web_con.config.js_fname = args.js_fname

    web_con.run()

    # }}}
