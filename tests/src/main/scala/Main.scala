import org.json4s._
import org.json4s.native.JsonMethods._
import java.sql.*
import org.sqlite.SQLiteDataSource
import simplesql as sq

case class UserRiver(chatid: Int, station: String, level: Float,date: String, threshold: Float, is_notified: Boolean)

def send_notif(i: UserRiver) =
  val text = s"""Pašreizējais ūdens līmenis stacijā '${i.station}': ${i.level}m. 
  Dati pēdējoreiz atjaunināti ${i.date}"""
  val message = Map("chat_id" -> i.chatid.toString, "text" -> text)

  requests.post("https://api.telegram.org/bot5637989500:AAFBu3aHNzAlifMwUrTA5zlIcQIMM670AMo/sendMessage", data = message)
  
def get_data(path: String): List[UserRiver] = 
    val ds = SQLiteDataSource()
    ds.setUrl("jdbc:sqlite:" + path)

    sq.transaction(ds) {
      val tasks: List[UserRiver] = sq.read[UserRiver](sql"select id, task from tasks")
      tasks}

        
@main def hello: Unit =
  val condition = (row:UserRiver) => {
    row.level > row.threshold && !row.is_notified
  }

  val data = List()
  val notifyable = data.filter(condition(_))
  notifyable.foreach(send_notif)

