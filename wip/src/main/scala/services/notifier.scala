package services

import org.json4s.DefaultFormats
import org.json4s.jackson.JsonMethods
import org.json4s.jackson.Serialization
import org.json4s.jvalue2extractable
import java.sql.*
import scala.collection.mutable.ListBuffer


case class UserRiver(
  chatid: Int, 
  station: String, 
  level: Float,
  date: String, 
  threshold: Float, 
  is_notified: Boolean)


object notifier {

  def get_data(url: String, sql_query: String) = 
    var output = ListBuffer[UserRiver]()

    val conn = DriverManager.getConnection(url)
    val statement = conn.createStatement
    val rs = statement.executeQuery(sql_query)
    while rs.next do
        val row = UserRiver(
          rs.getInt("chatid"),
          rs.getString("station"),
          rs.getFloat("level"),
          rs.getString("date"),
          rs.getFloat("threshold"),
          rs.getBoolean("is_notified")
        )
        output += row
    end while

    conn.close()
    output.toList

  def send_notif(i: UserRiver) =
    val text = s"""Pašreizējais ūdens līmenis
    stacijā '${i.station}': ${i.level}m. 
    Dati pēdējoreiz atjaunināti ${i.date}"""
    
    val message = Map(
      "chat_id" -> i.chatid.toString,
       "text" -> text)

    val token = sys.env.get("TGBOT_TOKEN")

    val url = s"https://api.telegram.org/${token}/sendMessage"

    requests.post(url, data = message)

  def notify(): Unit = 
    val data = get_data(
    "jdbc:sqlite:../meteo.db",
    "Select * from user_rivers join data on user_rivers.station = data.station")

    val condition = (row:UserRiver) =>
      row.level > row.threshold && !row.is_notified

    val notifyable = data.filter(condition(_))
    notifyable.foreach(send_notif)
}