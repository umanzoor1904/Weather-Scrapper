import sqlite3
class DBOperations:
    """Class to perform the database operations"""
    
    def __init__(self, dbname: str):
        self.dbname = dbname

    def initialize_db(self):
        """Initializes the database if it doesn't exist
            Done by Usman Manzoor"""     
        try:
            with DBCM(self.dbname) as c:
                c.execute("""create table samples
                                (id integer primary key autoincrement not null,
                                sample_date text unique on conflict fail not null,
                                location text not null,
                                min_temp real not null,
                                max_temp real not null,
                                avg_temp real not null);""")
        except Exception as e:
            print("Error creating table:", e)

    def save_data(self, weather):
        """Saves the data to the database if it doesn't exist
            Done by Usman Manzoor""" 
        try:
            with DBCM(self.dbname) as c:
                sql = """insert into samples (sample_date,location,min_temp,max_temp,avg_temp)
                        values (?,?,?,?,?)"""
                for k in weather:
                    data = (k, 'Winnipeg, MB', weather[k]['Min'], weather[k]['Max'], weather[k]['Mean'])
                    c.execute(sql, data)
        except Exception:
            pass

    def fetch_data(self):
        """Fetches the data from the database
            Done by Usman Manzoor""" 
        try:
            rows = ()
            with DBCM(self.dbname) as c:
                for row in c.execute("select sample_date, location, min_temp, max_temp, avg_temp from samples"):
                    rows += row
                return rows
        except Exception as e:
            print("Error fetching samples.", e)
    
    def purge_data(self):
        """Purges all the data in the database
            Done by Usman Manzoor""" 
        try:
            with DBCM(self.dbname) as c:
                c.execute("drop table samples;")
        except Exception as e:
            print('Error deleting data.', e)


class DBCM:
    """Context Manager for the database"""
    def __init__(self, dbname: str):
        self.dbname = dbname

    def __enter__(self) -> 'cursor':
        try:
            self.conn = sqlite3.connect(self.dbname)
            self.cursor = self.conn.cursor()
            return self.cursor
        except Exception as e:
            print("Error", e)

    def __exit__(self, exc_type, exc_value, exc_trace):
        try:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print("Error", e)

