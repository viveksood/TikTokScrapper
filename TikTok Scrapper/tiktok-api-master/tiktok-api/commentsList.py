import json
import psycopg2
from comment import Comment
from statusDeCode import statusDeCode
from tiktokRequest import TiktokRequest

class CommentsList:
  def __init__(self, post, user):
    self.user = user
    self.post = post
    self.region = 'US'
    self.status_code = None
    self.cursor = None
    self.has_more = None
    self.total = None
    self.comments = []

  def retrieve_data(self, cursor):
    newCursor = cursor
    while True:
      retry = False
      while True:
        try:
          request = self.user.tiktokRequest.commentsListRequest(self.post, newCursor, retry)
          data = request.json()
          break
        except json.decoder.JSONDecodeError as e:
          print('Try again, json error.')
          retry = True
          continue
      if data['status_code'] != 0 and not statusDeCode(data['status_code']):
        print("first if on commentsList")
        return False
      if not "cursor" in data:
        print("second if on commentList")
        raise Exception("no cursor")

      self.status_code = data['status_code']
      newCursor = data['cursor']
      self.has_more = data['has_more']
      self.total = data['total']

      if "comments" in data:
        if not data['comments'] is None:
          self.set_comments(data['comments'])
          if self.has_more == 1:
            continue
          else:
            break
        else:
          break
      else:
        break

    return self.comments

  def set_comments(self, commentItems):
    for commentItem in commentItems:
      comment = Comment(commentItem, self.post, self.user)
      self.comments.append(comment)
