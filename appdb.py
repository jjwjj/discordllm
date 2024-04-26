import sqlite3
import json

dbname = 'app.db'

###############################################################################
def initializeDb(db_name=dbname):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            UserId TEXT PRIMARY KEY,
            MsgArray TEXT,
            PromptCount INTEGER
        )
    ''')
    connection.commit()
    connection.close()


###############################################################################
def readUserData(user_id, db_name=dbname):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data WHERE UserId = ?", (user_id,))
    user_data = cursor.fetchone()
    connection.close()
    if user_data:
        # Deserialize the JSON string back into a list of dictionaries
        msg_array = json.loads(user_data[1]) if user_data[1] else None
        return {
            "UserId": user_data[0],
            "MsgArray": msg_array,
            "PromptCount": user_data[2]
        }
    else:
        return None


###############################################################################
def updateUserData(user_id, msg_array, prompt_count, db_name=dbname):
    # Convert the list of dictionaries to a JSON string for storage

    # print(f'updateUserData: {msg_array}\n\n')
    msg_array_json = json.dumps(msg_array) if msg_array is not None else None

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO user_data (UserId, MsgArray, PromptCount) VALUES (?, ?, ?)
        ON CONFLICT(UserId) DO UPDATE SET MsgArray=excluded.MsgArray, PromptCount=excluded.PromptCount
    ''', (user_id, msg_array_json, prompt_count))
    connection.commit()
    connection.close()


###############################################################################
def resetUserData(user_id, db_name=dbname):
    updateUserData(user_id, None, 0, db_name)




###############################################################################
def main():
    initializeDb()  # Call this function to initialize the database



###############################################################################
if __name__ == '__main__':

    restart = True
    
    while restart:
        restart = main()