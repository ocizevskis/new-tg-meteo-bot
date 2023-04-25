import sqlite3

class Sqlite():
    
    """wrapper for frequently used sqlite commands"""
    
    
    
    def __init__(self,address) -> None:
        self.conn = sqlite3.connect(address)
        self.cursor = self.conn.cursor()
    
    
    def new_user_river(self,chatid:int,station:str,threshold:float) -> None:
        self.cursor.execute("insert into user_rivers values(?,?,?,?)",(chatid,station,threshold,0))
    
    def read_unique_rivers(self) -> tuple:
        self.cursor.execute("select distinct river from data")
        return self.cursor.fetchall()
    
    def read_river_stations(self,river:str) -> tuple:
        self.cursor.execute("select station from data where river = ?",(river,))
        return self.cursor.fetchall()
    
    def read_user_rivers(self,chatid:int) -> tuple:
        print(chatid,type(chatid))
        self.cursor.execute("select station, threshold from user_rivers where chatid = ?",(chatid,))
        return self.cursor.fetchall()
    
    def del_user_river(self,chatid:int,station:str) -> None:
        self.cursor.execute("delete from user_rivers where chatid = ? and station = ?", (chatid,station))
        
    def update_data(self,data:tuple):
        self.cursor.execute("update data set level = ?, date = ? where station = ?",data)
        
    def read(self,query:str):
        self.cursor.execute(query)
        names = [d[0] for d in self.cursor.description]
        tuple_list =  self.cursor.fetchall()
        return [{k:v for k,v in zip(names,i)} for i in tuple_list]
        
    def write(self,query:str,data:tuple|dict):
        self.cursor.execute(query,data)
 
        
    def commit_and_close(self) -> None:
        self.conn.commit()
        self.conn.close()