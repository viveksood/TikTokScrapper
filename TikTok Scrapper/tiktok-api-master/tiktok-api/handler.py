from user import User
from itemList import ItemList
from commentsList import CommentsList
from time import sleep
import json
import urllib3
from multiprocessing import Pool
from multiprocessing import set_start_method
from config import newConn

def start(username):
  print(f"Starting: {username}", flush=True)
  user = User(username)
  if user.retrieve_data():
    user.save()
    print(f"Finished: {username}", flush=True)
  else:
    # user.delete()
    print(f"Deleting: {username}", flush=True)
  return user

def getPosts(user):
  if user is not None:
    print(f"Starting: {user} Posts", flush=True)
    itemList = ItemList(user)
    postList = itemList.retrieve_data(0,[])
    print(f"Finished: {user} Posts", flush=True)
    return postList

def getComments(post):
  print(f"Starting: {post.user.uniqueId} Comments", flush=True)
  commentList = CommentsList(post, post.user)
  comments = commentList.retrieve_data(0)
  print(f"Finished: {post.user.uniqueId} Comments", flush=True)

def main(event, context):
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  usernames = ['charlidamelio','lorengray']
  # conn = newConn()
  # cur = conn.cursor()
  # cur.execute(f"""
  #   SELECT username
  #   FROM users
  #   ORDER BY RANDOM();
  #   """
  # )
  # pg_users = cur.fetchall()
  # for row in pg_users:
  #   usernames.append(row[0])
  # cur.close()
  # pool = Pool(1)

  # users = pool.map(start, usernames)
  for user in usernames:
    user=start(user)
    postsList = getPosts(user)
    print(len(postsList))
    if postsList:
      total = len(postsList)
      counter = 0
      print(len(postsList))
      for post in postsList:
        print(f"Estimated progress: {counter*100/total}", flush=True)
        data=getComments(post)
        print(data)
        counter += 1
        print("comments get")
    return "Done"
  # conn.close()


if __name__ == "__main__":
  main('', '')
