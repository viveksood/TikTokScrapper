import psycopg2
import datetime
from config import newConn
import sys
class Post:
  def __init__(self, item, user):
    self.user = user
    self.userId = item.get('author', {}).get('id', '')
    self.uniqueId = item.get('author', {}).get('uniqueId', '')
    self.id = item.get('id', '')
    self.desc = item.get('desc', '')
    self.createTime = item.get('createTime', '')
    self.playAddr = item.get('video', {}).get('playAddr', '')
    self.downloadAddr = item.get('video', {}).get('downloadAddr', '')
    self.diggCount = item.get('stats', {}).get('diggCount', '')
    self.shareCount = item.get('stats', {}).get('shareCount', '')
    self.commentCount = item.get('stats', {}).get('commentCount', '')
    self.playCount = item.get('stats', {}).get('playCount', '')
    self.itemCommentStatus = item.get('itemCommentStatus', '')
    self.comments = []
    self.save()

  def url(self):
    return f"https://www.tiktok.com/@{self.user.uniqueId}/video/{self.id}"
  def datePosted(self):
    return datetime.datetime.fromtimestamp(self.createTime)

  def save(self):
    try:
      conn = newConn()
      cur = conn.cursor()
      cur.execute("""
        INSERT INTO posts (post_url, date_posted, username, video_url, caption) values (%s, %s, %s, %s, %s)
        ON CONFLICT (post_url) DO UPDATE
        SET video_url = %s;
        """, (self.url(),  self.datePosted(), self.uniqueId, self.downloadAddr, self.desc, self.downloadAddr)
      )
      print(".", end = '', flush=True)
      cur.execute("""
        INSERT INTO post_metrics (post_url, date_posted, num_likes, num_views, num_comments, num_shares)
        values (%s, %s, %s, %s, %s, %s)
        """, (self.url(), self.datePosted(), self.diggCount, self.playCount, self.commentCount, self.shareCount)
      )
      print(".", end = '', flush=True)
      cur.close()
    except psycopg2.Error as e:
      print("Unable to connect!")
      print(e.pgerror)
      print(e.diag.message_detail)
      sys.exit(1)
