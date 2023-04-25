from dataclasses import dataclass
import requests
from dacite import from_dict
import os
from modules.wrappers import Sqlite


@dataclass
class UserRiver:
  chatid: int 
  station: str 
  level: float
  date: str 
  threshold: float 
  is_notified: int
  plot_url: str


def send_notif(i: UserRiver):
    text = f"""Pašreizējais ūdens līmenis stacijā '{i.station}': {i.level}m. Dati pēdējoreiz atjaunināti {i.date}
    https://hidro.meteo.lv/hymer/images/{i.plot_url}"""

    message  = {"chat_id": str(i.chatid),
        "text": text}

    token = os.environ["TGBOT_TOKEN"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    response = requests.post(url, data = message)
    print(response)


def notify():
    db = Sqlite("./meteo.db")
    data = db.read(
    "Select * from user_rivers join data on user_rivers.station = data.station")
    
    #real men don't need ORMs
    to_dataclass = lambda x: from_dict(data = x, data_class = UserRiver)
    data = map(to_dataclass,data)

    should_notify = lambda i: i.level > i.threshold and not i.is_notified
    should_reset_flag = lambda i: i.level < i.threshold and i.is_notified
    
    notifyable = filter(should_notify, data)
    resettable = filter(should_reset_flag, data)

    for i in notifyable:
        send_notif(i)
        db.write("update user_rivers set is_notified = 1 where chatid = ? and station = ?", (i.chatid,i.station))
        
    for i in resettable:
        db.write("update user_rivers set is_notified = 1 where chatid = ? and station = ?", (i.chatid,i.station))
        
    db.commit_and_close()
        
        
notify()