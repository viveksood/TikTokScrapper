import json
import psycopg2
import datetime
from post import Post
from statusDeCode import statusDeCode
from tiktokRequest import TiktokRequest
class ItemList:
  def __init__(self, user):
    self.user = user
    self.region = 'US'
    self.statusCode = None
    self.hasMore = None
    self.posts = []

  def retrieve_data(self, cursor, api_items):
    retry = False
    while True:
      try:
        request = self.user.tiktokRequest.itemListRequest(self.user, cursor, retry)
        data = request.json()
        break
      except json.decoder.JSONDecodeError as e:
        print('Try again, json error.')
        retry = True
        continue
    if data['statusCode'] != 0 and not statusDeCode(data['statusCode']):
      return False
    if not "hasMore" in data:
      return False

    self.statusCode = data['statusCode']
    self.hasMore = data['hasMore']
    newCursor = data['cursor']
    flatten = lambda l: [item for sublist in l for item in sublist]

    if "itemList" in data:
      if not data['itemList'] is None:
        if self.checkDateOnLastItem(data['itemList']):
          self.set_posts(flatten(api_items))
        else:
          api_items.append(data['itemList'])
          if self.hasMore:
            self.retrieve_data(newCursor, api_items)
          else:
            self.set_posts(flatten(api_items))

    return self.posts

  def set_posts(self, flattend_items):
    for item in flattend_items:
      post = Post(item, self.user)
      self.posts.append(post)

  def checkDateOnLastItem(self, items):
    return self.moreThan3Months(items[0]['createTime'])

  def moreThan3Months(self, time):
    time_between = datetime.datetime.now() - datetime.datetime.fromtimestamp(time)
    result = time_between.days > 90
    if result:
      print("skipping older posts")
    return result