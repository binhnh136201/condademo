import pandas as pd
import pymongo
import streamlit as st

from config import mongo_uri
from database.query import get_question_info, get_number_assignment

def create_question(db, question_id, question_number):
    query_params = {
        "question_id": question_id,
        "question_number": question_number
    }
    
    question_info = get_question_info(db, query_params)
    return question_info

def connect_db(mongo_uri):
    client = pymongo.MongoClient(mongo_uri)
    db = client["GFG"]
    
    return db

def set_question_id():
    st.session_state["cur_question_id"] = st.session_state["question_id_option"]
    st.session_state["cur_question_num"] = 1
    
    # refresh state
    del st.session_state["answer_mapper"]
    del st.session_state["answer_storage"]
    if "num_answer_right" in st.session_state:
        del st.session_state["num_answer_right"]
    
def set_question_answer():
    cur_question_num = st.session_state['cur_question_num']
    st.session_state["answer_mapper"][cur_question_num] = int(st.session_state["answer_option"]) + 1
    
def set_next_button():
    if(st.session_state["cur_question_num"] < 35): # hard code
        st.session_state["cur_question_num"] += 1
        
def set_previous_button():
    if(st.session_state["cur_question_num"] > 1): # hard code
        st.session_state["cur_question_num"] -= 1
        
def get_assignment_results(): #
    user_answer = st.session_state['answer_mapper']
    assignment_answer = st.session_state['answer_storage']
    
    num_answer_right = 0
    total_answer = 35
    
    for k in user_answer.keys():
        if(user_answer[k] == assignment_answer[k]):
            num_answer_right += 1
    
    st.session_state["num_answer_right"] = num_answer_right
    # st.write(f"Số đáp án đúng: {num_answer_right}/{total_answer}")

if __name__ == "__main__":
    db = connect_db(mongo_uri)
    num_assignment = get_number_assignment(db)
    
    # Initialization state
    if 'cur_question_num' not in st.session_state:
        st.session_state['cur_question_num'] = 1
    if 'cur_question_id' not in st.session_state:
        st.session_state['cur_question_id'] = 1
    if 'answer_mapper' not in st.session_state:
        st.session_state['answer_mapper'] = {}
    if 'answer_storage' not in st.session_state: # store real data
        st.session_state['answer_storage'] = {}
    
    st.title("Demo car assignment crawl")
    
    # render sidebar
    with st.sidebar:
        st.header("Welcome")
        option = st.selectbox(
            'Chọn đề làm',
            [idx for idx in range(1, num_assignment)], on_change=set_question_id, key="question_id_option")

        st.write('Bạn đang làm đề số:', st.session_state["cur_question_id"])
    
    # render question container
    with st.container():
        question_info = create_question(db, st.session_state["cur_question_id"], 
                                        st.session_state["cur_question_num"])
        
        # get info
        question_number = question_info["question_number"]
        question_content = question_info["question_content"]
        question_answer = question_info["question_answer"]
        final_answer = question_info["final_answer"]
        
        if(question_number not in st.session_state['answer_storage']):
            st.session_state['answer_storage'][question_number] = int(final_answer)
        
        # question
        st.header(f"Câu {question_number}: {question_content}")
        
        # set radio options 
        radio_index = 0
        if(question_number in st.session_state['answer_mapper']):
            radio_index = st.session_state['answer_mapper'][question_number] - 1
            
        st.radio("Chọn đáp án", [idx for idx in range(len(question_answer))], format_func = lambda x: question_answer[x]
                                ,on_change=set_question_answer, key="answer_option", index=radio_index)
        
        if "num_answer_right" in st.session_state:
            right_answer = st.session_state['answer_storage'][question_number]
            st.success(f"Đáp án chính xác: {right_answer}")
        
        col1, col2 = st.columns(2)
        
        with col2:
            next_button = st.button("Next", on_click=set_next_button)

        with col1:
            previous_button = st.button("Previous", on_click=set_previous_button)
        
    if "num_answer_right" in st.session_state:
        num_answer_right = st.session_state["num_answer_right"]
        st.write(f"Số đáp án đúng: {num_answer_right}/35")
        
    submit_button = st.button("Submit", on_click=get_assignment_results)
    