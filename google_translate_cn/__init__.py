import json
import urllib.parse
import urllib.request
from albert import *

# -*- coding: utf-8 -*-

"""Translate text to zh-cn using Google Translate.

Check available languages here: https://cloud.google.com/translate/docs/languages

Synopsis: <trigger> <text>"""


__title__ = "Google Translate zh-cn"
__version__ = "0.4.0"
__triggers__ = "trcn "
__authors__ = "ttyS3"

ua = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
urltmpl = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=%s&tl=%s&dt=t&q=%s"

iconPath = iconLookup("config-language") or ":python_module"


def handleQuery(query):
    if query.isTriggered:
        fields = query.string.split()
        item = Item(id=__title__, icon=iconPath)
        if len(fields) >= 1:
            src = "auto"
            dst = "zh-cn"
            txt = " ".join(fields)
            url = urltmpl % (src, dst, urllib.parse.quote_plus(txt))
            req = urllib.request.Request(url, headers={"User-Agent": ua})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode("utf-8"))
                result = data[0][0][0]
                item.text = result
                item.subtext = "%s-%s translation of %s" % (
                    src.upper(),
                    dst.upper(),
                    txt,
                )
                item.addAction(ClipAction("Copy translation to clipboard", result))
                return item
        else:
            item.text = __title__
            item.subtext = 'Enter a query in the form of "&lt;text&gt;"'
            return item
