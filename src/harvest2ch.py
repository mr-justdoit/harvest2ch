#!/usr/bin/python
# coding:utf-8
import urllib.request as urllib2
import html2text
import re
import sys
import getopt


def output_time(text, time):
    if time == "h":
        texts = re.findall(r"[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", text)
        for i in range(0, len(texts)):
            texts[i] = texts[i].split(":")[0]
    elif time == "m":
        texts = re.findall(r"[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]", text)
        for i in range(0, len(texts)):
            texts[i] = texts[i].split("/")[1]

    for i in range(0, len(texts)):
        print(texts[i])


def output_regex(html, regex):
    texts = re.findall(regex, html)
    for i in range(0, len(texts)):
        texts[i] = re.sub("<dd>", "", texts[i])
        texts[i] = re.sub("<br>", "\n", texts[i])
        texts[i] = re.sub(r"<a.*?>(.*?)</a>", r"\1", texts[i])
    return texts


def format_dt(metatexts):
    for i in range(0, len(metatexts)):
        metatexts[i] = re.sub(
            r"([0-9][0-9][0-9][0-9])/([0-9][0-9])/([0-9][0-9])", r"\1-\2-\3",
            metatexts[i])
    return metatexts


def feature_extraction(texts, metatexts):
    metatexts = format_dt(metatexts)
    for i in range(0, len(texts)):
        V1 = len(texts[i])
        V2 = len(re.findall('、', texts[i])) / V1
        V3 = len(re.findall(r'。', texts[i])) / V1
        V4 = len(re.findall('\u3000', texts[i])) / V1
        V5 = len(re.findall('\n', texts[i])) / V1
        V6 = len(re.findall(' ', texts[i])) / V1
        V7 = len(re.findall(
            r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?',
            texts[i]))
        texts[i] = re.sub(
            r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?',
            "", texts[i])
        V8 = len(re.findall('&gt;&gt;', texts[i]))
        V9 = len(re.findall('？', texts[i])) / V1
        V10 = len(re.findall('！', texts[i])) / V1
        V11 = len(re.findall(r'[wｗ]', texts[i])) / V1
        V12 = int("green" in metatexts[i])
        V13 = re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', metatexts[i]).pop()
        V13 += ' '
        V13 += re.findall(r'[0-9]{2}:[0-9]{2}:[0-9]{2}', metatexts[i]).pop()
        V13 += ' JST'
        print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %
              (V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13))


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:t:p:h')
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    time = "h"
    url = ""
    text = ""

    for o, a in opts:
        if o == "-u":
            url = a
            html = str(urllib2.urlopen(url).read().decode('shift-jis',
                                                          'ignore'))
            h = html2text.HTML2Text()
            text = h.handle(html)

        if o == "-t":
            time = a
            output_time(text, time)
        elif o == "-p":
            if a == "1":
                print(output_regex(html, r"<dd>.*"))
            elif a == "2":
                texts = output_regex(html, r"<dd>.*")
                metatexts = output_regex(html, r"<dt>.*?<dd>")
                feature_extraction(texts, metatexts)
            elif a == "3":
                print(output_regex(html, r"<dt>.*?<dd>"))


if __name__ == "__main__":
    main()
