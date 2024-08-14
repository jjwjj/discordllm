###############################################################################
###############################################################################

#    #### ##     ## ########   #######  ########  ########  ######  
#     ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ## 
#     ##  #### #### ##     ## ##     ## ##     ##    ##    ##       
#     ##  ## ### ## ########  ##     ## ########     ##     ######  
#     ##  ##     ## ##        ##     ## ##   ##      ##          ## 
#     ##  ##     ## ##        ##     ## ##    ##     ##    ##    ## 
#    #### ##     ## ##         #######  ##     ##    ##     ######    

import openai
import credentials
import json
import langchat

###############################################################################
###############################################################################

#     ######   ##        #######  ########     ###    ##        ######  
#    ##    ##  ##       ##     ## ##     ##   ## ##   ##       ##    ## 
#    ##        ##       ##     ## ##     ##  ##   ##  ##       ##       
#    ##   #### ##       ##     ## ########  ##     ## ##        ######  
#    ##    ##  ##       ##     ## ##     ## ######### ##             ## 
#    ##    ##  ##       ##     ## ##     ## ##     ## ##       ##    ## 
#     ######   ########  #######  ########  ##     ## ########  ######      


###############################################################################
###############################################################################

#   ######## ##    ##       ########  ########  ######   ######  ########  #### ########  ######## 
#   ##       ###   ##       ##     ## ##       ##    ## ##    ## ##     ##  ##  ##     ##    ##    
#   ##       ####  ##       ##     ## ##       ##       ##       ##     ##  ##  ##     ##    ##    
#   ######   ## ## ##       ##     ## ######    ######  ##       ########   ##  ########     ##    
#   ##       ##  ####       ##     ## ##             ## ##       ##   ##    ##  ##           ##    
#   ##       ##   ###       ##     ## ##       ##    ## ##    ## ##    ##   ##  ##           ##    
#   ##       ##    ##       ########  ########  ######   ######  ##     ## #### ##           ##    


import sqlite3
import numpy as np
import time
import json

self = __import__(__name__)   # this is a placeholder as I intend to convert to class 
oai = None
embedmodel = None
gtotaltokens = 0

###############################################################################
def cosineSimilarity(vec1, vec2):
    dotProduct = np.dot(vec1, vec2)
    normVec1 = np.linalg.norm(vec1)
    normVec2 = np.linalg.norm(vec2)
    return dotProduct / (normVec1 * normVec2)


###############################################################################
def embed(inputtxt):
    global gtotaltokens
    try:
        response = oai.embeddings.create(input=inputtxt, model=embedmodel)
        embedding = response.data[0].embedding
        print(inputtxt, '=', response.usage.total_tokens, 'tokens')
        return embedding
    except Exception as e:
        print(f"Error embedding text: {e}")
        return None

###############################################################################
def setOpenAi():
    global oai
    global embedmodel
    global gtotaltokens

    oai = openai.OpenAI()
    embedmodel = credentials.embedmodel
    gtotaltokens = 0

    return oai


###############################################################################
def registerCustomFunctions(conn):
    def dotProduct(vecBlob1, vecBlob2):
        vec1 = np.frombuffer(vecBlob1, dtype=np.float32)
        vec2 = np.frombuffer(vecBlob2, dtype=np.float32)
        return float(np.dot(vec1, vec2))
    
    def vectorNorm(vecBlob):
        vec = np.frombuffer(vecBlob, dtype=np.float32)
        return float(np.linalg.norm(vec))
    
    conn.create_function("dot_product", 2, dotProduct)
    conn.create_function("vector_norm", 1, vectorNorm)

###############################################################################
def findBestMatch(dbName, tableName, inputText):
    # Embed the input text
    inputVector = self.embed(inputText)
    inputVectorArray = np.array(inputVector, dtype=np.float32)
    inputVectorBlob = sqlite3.Binary(inputVectorArray.tobytes())
    
    conn = sqlite3.connect(dbName)

    # Optimize SQLite settings
    conn.execute('PRAGMA synchronous = OFF')
    conn.execute('PRAGMA journal_mode = MEMORY')
    # conn.execute('PRAGMA cache_size = 100000')
    conn.execute('PRAGMA cache_size = 128000')


    registerCustomFunctions(conn)
    cursor = conn.cursor()
    
    cursor.execute(f'''
        SELECT id,
               (dot_product(vector, ?) / (vector_norm(vector) * vector_norm(?))) AS similarity
        FROM {tableName}
        ORDER BY similarity DESC
        LIMIT 1
    ''', (inputVectorBlob, inputVectorBlob))
    
    best_match = cursor.fetchone()
    
    if best_match:
        best_match_id = best_match[0]
        
        # Secondary query to fetch the complete record
        cursor.execute(f'''
            SELECT id, vector, briefText, verboseText, action, listOfFlags
            FROM {tableName}
            WHERE id = ?
        ''', (best_match_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "vector": np.frombuffer(result[1], dtype=np.float32),
                "briefText": result[2],
                "verboseText": result[3],
                "action": result[4],
                "listOfFlags": result[5],
                "similarity": best_match[1]  # Similarity value from initial query
            }
    conn.close()
    return None


###############################################################################
def findBestMatches(dbName, tableName, inputText, limit=5, threshold=.78):
    # Embed the input text
    inputVector = self.embed(inputText)
    inputVectorArray = np.array(inputVector, dtype=np.float32)
    inputVectorBlob = sqlite3.Binary(inputVectorArray.tobytes())
    
    conn = sqlite3.connect(dbName)

    # Optimize SQLite settings
    conn.execute('PRAGMA synchronous = OFF')
    conn.execute('PRAGMA journal_mode = MEMORY')
    conn.execute('PRAGMA cache_size = 128000')

    registerCustomFunctions(conn)
    cursor = conn.cursor()
    
    cursor.execute(f'''
        SELECT id,
            (dot_product(vector, ?) / (vector_norm(vector) * vector_norm(?))) AS similarity
        FROM {tableName}
        WHERE (dot_product(vector, ?) / (vector_norm(vector) * vector_norm(?))) > ?
        ORDER BY similarity DESC 
        LIMIT ?
        ''', (inputVectorBlob, inputVectorBlob, inputVectorBlob, inputVectorBlob, threshold, limit))

    
    matches = cursor.fetchall()
    
    results = []
    for match in matches:
        match_id = match[0]
        
        # Secondary query to fetch the complete record
        cursor.execute(f'''
            SELECT id, vector, briefText, verboseText, action, listOfFlags
            FROM {tableName}
            WHERE id = ?
        ''', (match_id,))
        
        result = cursor.fetchone()
        if result:
            results.append({
                "id": result[0],
                "vector": np.frombuffer(result[1], dtype=np.float32),
                "briefText": result[2],
                "verboseText": result[3],
                "action": result[4],
                "listOfFlags": result[5],
                "similarity": match[1]  # Similarity value from initial query
            })
    conn.close()
    return results



###############################################################################
def getAllBriefTexts(dbName, tableName="vectors"):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    
    cursor.execute(f'''
        SELECT briefText
        FROM {tableName}
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    # Combine all briefText values into a single string with newline delimiters
    briefTextList = [row[0] for row in results]
    combinedBriefTexts = '\n'.join(briefTextList)
    
    return combinedBriefTexts


###############################################################################
def ragMatch(dbName,inputText):
    
    if dbName is not None:
        tablename = 'vectors'
        self.setOpenAi()


        bestmatch = findBestMatch(dbName, tablename, inputText)

        if bestmatch["similarity"] >= .77:
            return bestmatch["briefText"], bestmatch["verboseText"]

    return None,None


###############################################################################
def ragMatches(dbName,inputText):
   if dbName is not None:
        tablename = 'vectors'
        self.setOpenAi()
        
        bestmatch = 0.00
        threshold = 0.80

        brieftxt   = ""
        verbosetxt = ""

        matches = findBestMatches(dbName, tablename, inputText, 5, .79)
        
        if matches:
            for match in matches:
                if match["similarity"] > threshold:
                    brieftxt   += "\n" + match["briefText"]
                    verbosetxt += "\n" + match["verboseText"]
            
            return brieftxt, verbosetxt

   return None,None


###############################################################################
def main():
    # Example usage:
    dbName = './db/sqlvec.db'
    tableName = 'vectors'
    inputText = input("ask me a question: ")

    self.setOpenAi()

    t0 = time.time()
    bestMatch = findBestMatch(dbName, tableName, inputText)
    t1 = time.time()



    if bestMatch:
        print(f'Brief Text: {bestMatch["briefText"]}')
        print(f'Verbose Text: {bestMatch["verboseText"]}')
        print(f'Action: {bestMatch["action"]}')
        print(f'List of Flags: {bestMatch["listOfFlags"]}')
        print(f'Best Match ID: {bestMatch["id"]}')
        print(f'Cosine Similarity: {bestMatch["similarity"]}')

        if bestMatch["similarity"] < 0.77:
            print('Warning: **Low similarity score**')
    else:
        print('No match found')

    print(f'Search time taken: {t1 - t0} seconds')



###############################################################################
if __name__ == "__main__":
    main()
