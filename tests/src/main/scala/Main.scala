import org.json4s.DefaultFormats
import org.json4s.jackson.JsonMethods
import org.json4s.jackson.Serialization
import org.json4s.jvalue2extractable
import java.sql.*
import scala.collection.mutable.ListBuffer
import services.*
        
@main def hello: Unit =
  updater.update()
  notifier.notify()
  