import urllib3
import requests
import random
import os
import time
import sys
import json
from cookies import cookie_data
def parseProxy(proxyUrl):
  return "://".join(proxyUrl.split("#")[::-1])

def getProxies():
  proxies=['lum-customer-c_b6481680-zone-tiktok_api_res_zone1-gip-us_46375_ca_berkeley_0:gy6bek012jez@zproxy.lum-superproxy.io:22225','lum-customer-c_b6481680-zone-tiktok_api_res_zone1-gip-us_46375_ca_berkeley_3:gy6bek012jez@zproxy.lum-superproxy.io:22225','lum-customer-c_b6481680-zone-tiktok_api_res_zone1-gip-us_7018_ca_berkeley_2:gy6bek012jez@zproxy.lum-superproxy.io:22225','lum-customer-c_b6481680-zone-tiktok_api_res_zone1-gip-us_7922_ca_berkeley_1:gy6bek012jez@zproxy.lum-superproxy.io:22225']
  return proxies
class TiktokRequest:

  def __init__(self, uniqueId):
    self.uniqueId = uniqueId
    self.request = None
    self.enableProxies = True
    self.proxies = {}
    if self.enableProxies:
      self.proxy = random.choice(getProxies())
      self.proxies = {"http": 'http://' + self.proxy, "https": 'http://' + self.proxy}
  def userRequest(self, retry):
    url = f"https://m.tiktok.com/api/user/detail/?uniqueId={self.uniqueId}&language=en&verifyFp="
    if retry:
      self.signature = self.requestSignature(url)
    self.request = self.getRequest(url + '&_signature=' + self.signature)

    return self.request
  
  def itemListRequest(self, user, cursor, retry):
    url=f'https://m.tiktok.com/api/post/item_list/?aid=1988&count=30&cursor={cursor}&secUid={user.secUid}'
    self.signature = self.requestSignature(url)
    self.request = self.getRequest(self.signature)
    return self.request
  
  def commentsListRequest(self, post, cursor, retry):
    print(post.id)
    url=f"https://www.tiktok.com/api/comment/list/?aweme_id={post.id}&cursor={cursor}&count=20&aid=1988&app_language=en&device_platform=web_pc&current_region=NL&fromWeb=1&channel_id=3"
    self.signature = self.requestSignature(url)
    self.request = self.getRequest(self.signature, True)
    return self.request

  def resetSigner(self):
    requests.get('http://localhost:8080/reset')
    print('reset', flush=True)

  def getRequest(self, url, sendCokies=False):
    payload={}
    headers={
              'authority': 'www.tiktok.com',
              'accept': 'application/json, text/plain, /',
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
              'referer': f'https://www.tiktok.com//@{self.uniqueId}?lang=en',
              'accept-language': 'en-US,en;q=0.9',
            }
    if sendCokies:
      headers['cookie'] = cookie_data
    while True:
      try:
        request = requests.get(url, headers=headers, proxies=self.proxies, verify=(not self.enableProxies),data=payload)
      except (ConnectionResetError, requests.exceptions.ProxyError, requests.exceptions.ConnectionError) as e:
        print("Proxy Connnection error, trying new proxy", flush=True)
        self.proxy = random.choice(getProxies())
        self.proxies = {"http": 'http://' + self.proxy, "https": 'http://' + self.proxy}
        time.sleep(1)
      else:
        break
    return request

  def requestSignature(self, url):
    while True:
      try:
        """
        Here We sign our base url with the help of node server
        """
        req_sign = requests.post('http://localhost/signature', data=url).json()
        req_sign=req_sign["data"]["signed_url"]
      except (ConnectionResetError, requests.exceptions.ProxyError, requests.exceptions.ConnectionError) as e:
        print("Signer Connnection error, trying new signer", flush=True)
        self.proxy = random.choice(getProxies())
        self.proxies = {"http": 'http://' + self.proxy, "https": 'http://' + self.proxy}
        time.sleep(1)
      else:
        break
    return req_sign
