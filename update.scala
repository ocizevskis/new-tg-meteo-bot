import java.sql.*
import org.sqlite.SQLiteDataSource
import simplesql as sq

case class Task(id: Int, task: String) derives sq.Reader

@main def SQLiteTest3 =

    val ds = SQLiteDataSource()
    ds.setUrl("jdbc:sqlite:./ToDoList.sqlite")

    sq.transaction(ds) {
        val tasks: List[Task] = sq.read[Task](sql"select id, task from tasks")
        for t <- tasks do
            println(s"ID: ${t.id}, TASK: ${t.task}")
    }


    