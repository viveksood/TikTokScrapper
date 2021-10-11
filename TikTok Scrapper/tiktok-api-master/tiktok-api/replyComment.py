import requests
import json
import psycopg2
import datetime
from config import newConn

class ReplyComment:
  def __init__(self, reply_comment, post, user, comment):
    self.post = post
    self.comment = comment
    self.cid = reply_comment.get('cid')
    self.unique_id = reply_comment.get('user',{}).get('unique_id')
    self.text = reply_comment.get('text')
    self.digg_count = reply_comment.get('digg_count')

    self.create_time = reply_comment.get('create_time')
    if user.uniqueId == reply_comment.get('user',{}).get('unique_id'):
      user.add_social(reply_comment.get('user',{}).get('ins_id'), reply_comment.get('user',{}).get('youtube_channel_id'))
    self.save()

  def datePosted(self):
    return datetime.datetime.fromtimestamp(self.createTime)

  def save(self):
    try:
      conn = newConn()
      cur = conn.cursor()
      cur.execute("""
        INSERT INTO reply_comments (comment_id, post_url, commenter_username, comment_text, num_likes)
        values (%s, %s, %s, %s, %s)
        ON CONFLICT (comment_id, post_url, commenter_username, comment_text) DO UPDATE
        SET num_likes = %s;
        """, (self.comment.id, self.post.url(), self.unique_id, self.text, self.digg_count, self.digg_count)
      )
      cur.close()
      print(".", end = '', flush=True)
      # conn.close()
    except ValueError as v:
      print("Something is empty")
      print(v)
    except psycopg2.Error as e:
      print("Unable to connect!")
      print(e.pgerror)
      print(e.diag.message_detail)
      sys.exit(1)
