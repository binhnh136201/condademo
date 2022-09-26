import pymongo

from config import data_col

def get_question_info(db, query_params):
    question_id = query_params['question_id']
    question_number = query_params['question_number']
    
    query = {
        "question_id": int(question_id),
        "question_number": int(question_number)
    }
    
    data = db[data_col].find(query)
    data = list(data)   
    
    if(len(data) > 0):
        return data[0]
    
    return None

def get_number_assignment(db):
    data = db[data_col].find_one(sort=[("question_id", pymongo.DESCENDING)])

    return data["question_id"]