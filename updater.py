from dataclasses import dataclass
import requests
import json
from dacite import from_dict
import typing as t
from modules.wrappers import Sqlite


@dataclass
class Observation:
    """used by Station dataclass"""
    name: str
    value: str
    unit: str
    last_date: str
    source: str

@dataclass
class Plot:
    """used by Station dataclass"""
    name: str
    url: str
    last_date: str
    source: str

@dataclass
class Station:
    """dataclass representing the json structure"""
    id: int = 0
    name: str = ""
    code: str = ""
    lat: float = 0
    lon: float = 0 
    elevation: float = 0
    plots: list[Plot] = 0
    ts: list[Observation] = 0

def parse_hymer():
    url = "https://videscentrs.lvgmc.lv/data/hymer_overview"
    json_string = requests.get(url=url).text.replace("null","0.00")
    
    hymer_data = json.loads(json_string)
    temp = lambda x: from_dict(data = x, data_class = Station)
    
    return list(map(temp,hymer_data))
    
    
def filter_data(data:list[Station]):
    
    def __keep_only_wl(s:Station):
        obs = [i for i in s.ts if i.name == "Ūdens līmenis"]
        
        return Station(ts=obs,name=s.name.split(",")[1][1:])
    
    wl_data = map(__keep_only_wl,data)
    is_not_empty = lambda s: len(s.ts) > 0
    return list(filter(is_not_empty,wl_data))
     

def update_data_table():
    db = Sqlite("meteo.db")
    data = parse_hymer()
    data_filtered = filter_data(data=data)
    print(data_filtered[0].name)
    
    update_tuple = lambda s: (s.ts[0].value,s.ts[0].last_date,s.name)
    data_tuples = map(update_tuple,data_filtered)
    
    for t in data_tuples:
        db.update_data(t)
        print(t)
    db.commit_and_close()
           

def create_data_table():
    pass

update_data_table()


@dataclass
class UserRiver(
  chatid: Int, 
  station: String, 
  level: Float,
  date: String, 
  threshold: Float, 
  is_notified: Boolean)


def send_notif(i: UserRiver):
  text = f"""Pašreizējais ūdens līmenis
  stacijā '{i.station}': {i.level}m. 
  Dati pēdējoreiz atjaunināti {i.date}"""
  
  message  = {"chat_id": i.chatid.toString,
      "text": text}

  token = os.environ["TGBOT_TOKEN"]

  url = f"https://api.telegram.org/{token}/sendMessage"

  requests.post(url, data = message)



def notify():
  data = get_data(
  "jdbc:sqlite:../meteo.db",
  "Select * from user_rivers join data on user_rivers.station = data.station")

  should_notify = lambda i: i.level > i.threshold and not i.is_notified

  notifyable = filter(should_notify, data)
  notifyable.foreach(send_notif)