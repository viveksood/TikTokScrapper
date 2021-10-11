import json
import psycopg2
from config import newConn
from statusDeCode import statusDeCode
from tiktokRequest import TiktokRequest
import sys
from TikTokApi import TikTokApi
import random
api = TikTokApi()
proxies=['lum-customer-c_b6481680-zone-tiktok_api_res_zone1-gip-us_46375_ca_berkeley_0:gy6bek012jez@zproxy.lum-superproxy.io:22225','lum-customer-c_b6481680-zone-tiktok_api_res_zone1-gip-us_46375_ca_berkeley_3:gy6bek012jez@zproxy.lum-superproxy.io:22225','lum-customer-c_b6481680-zone-tiktok_api_res_zone1-gip-us_7018_ca_berkeley_2:gy6bek012jez@zproxy.lum-superproxy.io:22225','lum-customer-c_b6481680-zone-tiktok_api_res_zone1-gip-us_7922_ca_berkeley_1:gy6bek012jez@zproxy.lum-superproxy.io:22225']
class User:
  def __init__(self, uniqueId):
    self.posts = []
    self.data = None
    self.id = None
    self.uniqueId = uniqueId
    self.diggCount = None
    self.followerCount = None
    self.followingCount = None
    self.heart = None
    self.heartCount = None
    self.videoCount = None
    self.nickname = None
    self.avatarThumb = None
    self.avatarMedium = None
    self.avatarLarger = None
    self.signature = None
    self.verified = None
    self.secUid = None
    self.secret = None
    self.relation = None
    self.openFavorite = None
    self.sign = None
    self.date_collected = None
    self.tiktokRequest = None

  def retrieve_data(self):
    retry = False
    while True:
      try:
        """
        Using Python Tiktok Module to get user details with the help of residentials proxies
        """
        self.tiktokRequest = TiktokRequest(self.uniqueId)
        request=api.getUser(self.uniqueId,proxy=random.choice(proxies))
        data=request
        break
      except Exception as e:
        print(e)
        retry = True
        continue
    if data['statusCode'] != 0 and not statusDeCode(data['statusCode']):
      print("first if on user")
      print(statusDeCode(data['statusCode']))
      return False
    if not "userInfo" in data:
      print("second if on user")
      return False
    self.data = data
    self.diggCount = data.get("userInfo", {}).get("stats", {}).get("diggCount", "")
    self.followerCount = data.get("userInfo", {}).get("stats", {}).get("followerCount", "")
    self.followingCount = data.get("userInfo", {}).get("stats", {}).get("followingCount", "")
    self.heart = data.get("userInfo", {}).get("stats", {}).get("heart", "")
    self.heartCount = data.get("userInfo", {}).get("stats", {}).get("heartCount", "")
    self.videoCount = data.get("userInfo", {}).get("stats", {}).get("videoCount", "")

    self.id = data.get("userInfo", {}).get("user", {}).get("id", "")
    self.uniqueId = data.get("userInfo", {}).get("user", {}).get("uniqueId", "")
    self.nickname = data.get("userInfo", {}).get("user", {}).get("nickname", "")
    self.avatarThumb = data.get("userInfo", {}).get("user", {}).get("avatarThumb", "")
    self.avatarMedium = data.get("userInfo", {}).get("user", {}).get("avatarMedium", "")
    self.avatarLarger = data.get("userInfo", {}).get("user", {}).get("avatarLarger", "")
    self.signature = data.get("userInfo", {}).get("user", {}).get("signature", "")
    self.verified = data.get("userInfo", {}).get("user", {}).get("verified", "")
    self.secUid = data.get("userInfo", {}).get("user", {}).get("secUid", "")
    self.secret = data.get("userInfo", {}).get("user", {}).get("secret", "")
    self.relation = data.get("userInfo", {}).get("user", {}).get("relation", "")
    self.openFavorite = data.get("userInfo", {}).get("user", {}).get("openFavorite", "")
    self.save()
    return data

  def save(self):
    try:
      conn = newConn()
      cur = conn.cursor()
      cur.execute("""
        INSERT INTO user_metrics (username, num_followers, num_following, num_likes, num_posts, bio_name, bio, is_verified)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING date_collected;
        """, (self.uniqueId, self.followerCount, self.followingCount, self.heartCount, self.videoCount, self.nickname, self.signature, self.verified)
      )
      self.date_collected = cur.fetchone()[0]
      cur.close()
    except psycopg2.Error as e:
      print("Unable to connect!")
      print(e.pgerror)
      print(e.diag.message_detail)
      sys.exit(1)

  def add_social(self, ins_id, youtube_channel_id):
    try:
      conn = newConn()
      cur = conn.cursor()
      cur.execute("""
        UPDATE user_metrics
        SET instagram_handle = %s,
            youtube_handle = %s
        WHERE username = %s AND date_collected = %s
        """, (ins_id, youtube_channel_id, self.uniqueId, self.date_collected)
      )
      cur.close()
    except psycopg2.Error as e:
      print("Unable to connect!")
      print(e.pgerror)
      print(e.diag.message_detail)
      sys.exit(1)

  def delete(self):
    try:
      conn = newConn()
      cur = conn.cursor()
      cur.execute(f"""
        DELETE FROM users
        WHERE username = '{self.uniqueId}'
        """
      )
      cur.close()
      print(f"deleted {self.uniqueId}")
    except psycopg2.Error as e:
      print("Unable to connect!")
      print(e.pgerror)
      print(e.diag.message_detail)
      sys.exit(1)