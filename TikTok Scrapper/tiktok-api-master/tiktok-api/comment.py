import psycopg2
import datetime
from config import newConn
from replyComment import ReplyComment
import sys
class Comment:
  def __init__(self, comment, post, user):
    self.id = None
    self.post = post
    self.cid = comment['cid']
    if "unique_id" not in comment['user']:
      return None
    self.unique_id = comment['user']['unique_id']
    self.text = comment['text']
    self.digg_count = comment['digg_count']

    self.create_time = comment['create_time']
    if user.uniqueId == comment['user']['unique_id']:
      if comment['user'].get('ins_id',None) and  comment['user'].get('youtube_channel_id',None):
        user.add_social(comment['user']['ins_id'], comment['user']['youtube_channel_id'])
    self.save()
    if "reply_comment" in comment:
      if comment["reply_comment"] is not None:
        for replyComment in comment["reply_comment"]:
          ReplyComment(replyComment, post, user, self)

  def datePosted(self):
    return datetime.datetime.fromtimestamp(self.createTime)

  def save(self):
    try:
      conn = newConn()
      cur = conn.cursor()
      cur.execute("""
        INSERT INTO post_comments (post_url, commenter_username, comment_text, num_likes)
        values (%s, %s, %s, %s)
        ON CONFLICT (post_url, commenter_username, comment_text ) DO UPDATE
        SET num_likes = %s
        RETURNING id;;
        """, (self.post.url(), self.unique_id, self.text, self.digg_count, self.digg_count)
      )
      print(".", end = '', flush=True)
      self.id = cur.fetchone()[0]
      cur.close()
    except ValueError as v:
      print("Something is empty")
      print(v)
    except psycopg2.Error as e:
      print("Unable to connect!")
      print(e.pgerror)
      print(e.diag.message_detail)
      sys.exit(1)
