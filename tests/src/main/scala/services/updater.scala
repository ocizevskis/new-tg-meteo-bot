package services

import org.json4s.DefaultFormats
import org.json4s.jackson.JsonMethods
import org.json4s.jackson.Serialization
import org.json4s.jvalue2extractable
import java.sql.*


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


object updater {
    def parse_hymer(): List[Station] = 
    val url = "https://videscentrs.lvgmc.lv/data/hymer_overview"
    val json_string = requests.get(url).text().replace("null","0.00")

    implicit val json4sFormats = DefaultFormats
    JsonMethods.parse(json_string).extract[List[Station]]


  def update(): Unit = 
    val data = parse_hymer()
    
    val keep_only_wl = (station: Station): Station =>{ 
      val obs =  station.ts.filter(_.name == "Ūdens līmenis")
      Station(ts = obs)}

    val update_db = (s: Station) => {
      val query = s"update data set level = ${s.ts(0).value} where station = ${s.name}"
      val conn = DriverManager.getConnection(url)
      val statement = conn.createStatement
      val _ = statement.executeUpdate(query)
      conn.commit()
      conn.close()
    }
    
    val wl_data = data.map(keep_only_wl(_)).filter(_.ts.length != 0)
    wl_data.foreach(update_db(_))
  }

