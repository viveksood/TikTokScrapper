def statusDeCode(status):
  error = "Page not available"
  switcher = {
    10202: "Couldn't find this account",
    10221: "Couldn't find this account",
    10223: error,
    10225: "Couldn't find this account",
    10222: "This account is private",
    10203: "Couldn't find this sound",
    10218: error,
    10219: "Sound isn't available",
    10204: error,
    10215: error,
    10217: error,
    10220: "Couldn't find this video",
    10216: "This video is private",
    10205: error,
    10211: error,
    10212: error,
    10209: "Couldn't find this hashtag",
    10208: "Couldn't find this effect",
    10210: "Couldn't find this live"
  }
  return switcher.get(int(status))