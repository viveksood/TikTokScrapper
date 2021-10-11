import os
import urllib.parse
import psycopg2

def newConn():
  # DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://localhost/tiktok'
  # DATABASE_URI="postgres://postgres:root@192.168.0.106:5432/tiktok"
  # result = urllib.parse.urlparse(DATABASE_URI)
  # conn = psycopg2.connect(
  #         database = result.path[1:],
  #         user = result.username,
  #         password = result.password,
  #         host = result.hostname
  #     )
  # conn = psycopg2.connect(
  #       database = "tiktok",
  #       user = 'datawiz',
  #       password = '$tanf0rdcodes',
  #       host = 'tiktok-testing.cxyylfgchn3l.us-east-1.rds.amazonaws.com'
  #   )
  conn = psycopg2.connect(
        database = "tiktok",
        user = 'postgres',
        password = 'root',
        host = '127.0.0.1'
    )
  conn.autocommit = True
  return conn