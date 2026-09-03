from db.conn import open_connection
import pandas as pd
import numpy as np

def get_df(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.commit()
        columns = [column[0] for column in cursor.description]
        results = cursor.fetchall()
        df = pd.DataFrame(np.array(results), columns=columns)
        return df
    except Exception as e:
        return ValueError(f"Somithing went wrong: '{e}'")