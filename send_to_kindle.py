#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# created_on: 2023-10-23 18:29

"""Send To Kindle."""

import json
from dataclasses import dataclass, field
from re import A
from typing import Optional
import requests

__author__ = 'Toran Sahu <toran.sahu@yahoo.com>'
__license__ = 'Distributed under terms of the MIT license'


def url_to_html(url: str) -> str:
    res = requests.get(url)
    res.raise_for_status()
    return res.text


def url_to_xhtml(url: str):
    html = url_to_html(url)
    html_to_xhtml(html)


def html_to_xhtml(html: str):
    from html.parser import HTMLParser

    p = HTMLParser()
    p.feed(html)
    breakpoint()
    print()


def url_to_epub(url: str):
    # html = url_to_html(url)
    # pr = PostRequest(html, "Some Title", url)
    # dot = DOTePubAPI()
    # dot.post(pr)

    converter_base = "https://dotepub.com/converter/"
    cqp = ConverterQueryParam(url)
    res = requests.get(converter_base, params=cqp.to_dict(), allow_redirects=True)
    # res = requests.get("https://dotepub.com/converter/?url=https%3A%2F%2Ftheconversation.com%2Fwhat-you-should-and-shouldnt-do-with-all-of-your-old-phone-chargers-and-other-e-waste-213946%3Futm_source%3Dpocket-newtab-en-intl&fmt=epub&imm=1&lang=en", allow_redirects=True)
    res.raise_for_status()

    with open(f"Title2.{cqp.fmt}", "wb") as fp:
        fp.write(res.content)

    breakpoint()
    print()


class DataclassBase:
    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())


@dataclass
class ConverterQueryParam(DataclassBase):
    url: str
    fmt: Optional[str] = field(default="epub")
    imm: Optional[int] = field(default=1)
    lang: Optional[str] = field(default="en")


@dataclass
class PostRequest(DataclassBase):
    html: str
    title: str
    url: str
    lang: Optional[str] = field(default="en")
    author: Optional[str] = field(default=None)
    copy: Optional[str] = field(default=None)
    format: Optional[str] = field(default="epub")


class DOTePubAPI:
    BASE_URL = "https://dotepub.com"
    API_V1 = "v1"
    POST = "post"
    URL = f"{BASE_URL}/api/{API_V1}/{POST}"

    def post(self, pr: PostRequest):
        res = requests.post(self.URL, data=pr.to_dict())
        res.raise_for_status()
        with open(f"{pr.title}.{pr.format}", "wb") as fp:
            fp.write(res.content)


if __name__ == "__main__":
    url = "https://theconversation.com/what-you-should-and-shouldnt-do-with-all-of-your-old-phone-chargers-and-other-e-waste-213946"
    # url_to_epub(url)
    url_to_xhtml(url)
