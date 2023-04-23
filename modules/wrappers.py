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
        
        
    def commit_and_close(self) -> None:
        self.conn.commit()
        self.conn.close()