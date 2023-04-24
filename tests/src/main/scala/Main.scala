import org.json4s.DefaultFormats
import org.json4s.jackson.JsonMethods
import org.json4s.jackson.Serialization
import org.json4s.jvalue2extractable


case class UserRiver(
  chatid: Int, 
  station: String, 
  level: Float,
  date: String, 
  threshold: Float, 
  is_notified: Boolean)

def send_notif(i: UserRiver) =
  val text = s"""Pašreizējais ūdens līmenis stacijā '${i.station}': ${i.level}m. 
  Dati pēdējoreiz atjaunināti ${i.date}"""
  val message = Map("chat_id" -> i.chatid.toString, "text" -> text)

  requests.post("https://api.telegram.org/<token>/sendMessage", data = message)
  
// def get_data(path: String): List[UserRiver] = 
//     val ds = SQLiteDataSource()
//     ds.setUrl("jdbc:sqlite:" + path)

//     sq.transaction(ds) {
//       val tasks: List[UserRiver] = sq.read[UserRiver](sql"select id, task from tasks")
//       tasks}

        
@main def hello: Unit =
  update()
  // val condition = (row:UserRiver) => {
  //   row.level > row.threshold && !row.is_notified
  // }

  // val data = List()
  // val notifyable = data.filter(condition(_))
  // notifyable.foreach(send_notif)
  




case class Station(
  id: Int = 0,
  name: String = "",
  code: String = "",
  lat: Float = 0,
  lon: Float = 0, 
  elevation: Float = 0,
  plots: List[Plot] = List(),
  ts: List[Observation] = List())


case class Observation(
  name: String,
  value: String,
  unit: String,
  last_date: String,
  source: String)

case class Plot(
  name: String,
  url: String,
  last_date: String,
  source: String)


def parse_hymer() = 
  val url = "https://videscentrs.lvgmc.lv/data/hymer_overview"
  val json_string = requests.get(url).text().replace("null","0.00")

  implicit val json4sFormats = DefaultFormats
  JsonMethods.parse(json_string).extract[List[Station]]


def keep_only_wl(station: Station): Station = 
  val obs =  station.ts.filter(_.name == "Ūdens līmenis")
  Station(ts = obs)


def update() = 
  val data = parse_hymer()

  val update_db = (s: Station) => {
    val query = s"update data set level = ${s.ts(0).value} where station = ${s.name}"
    // statement.executeUpdate(query)
  }
  
  val wl_data = data.map(keep_only_wl(_)).filter(_.ts.length != 0)
  wl_data.foreach(update_db(_))



