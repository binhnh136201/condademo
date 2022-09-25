from base64 import encode
from bs4 import BeautifulSoup
import utils
import requests
import json
import xmltojson, xmltodict
from pymongo import MongoClient
import pymongo
import re
import dns

url = "https://oto360.net/thi-lai-xe?"

myclient = MongoClient("mongodb://localhost:27017/")

db = myclient["GFG"]

Collection = db["data"]

question_list = []

question_object = {}


client = pymongo.MongoClient("mongodb+srv://binhnh136201:Hoangbinh136@cluster0.btiv9as.mongodb.net/?retryWrites=true&w=majority")
db = client.test


for y in range(1,61):
  id_pos = str(y)
  for x in range(35):
    test_pos = str(x)
    payload = "ajax=loadQuestionNext&current=" + test_pos + "&exam=" + id_pos +"&selected=0"
    headers = {
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.content, 'html.parser')


    question_exam = {}

    # question id
    question_id = y
    question_exam['question_id']  = question_id
    

    # question number
    questions = soup.find_all("p")
    question_exam['question_number'] = x + 1


    # question content
    question_content = questions[1].string
    question_exam['question_content'] = question_content


    # question answers
    for answers in soup.select('blockquote'):


      all_answer = []
      all_answer.append(answers.a.get_text(strip=True))
      for answer in answers.a.find_next_siblings('a'):
        all_answer.append(answer.get_text(strip=True))

    question_exam['question_answer'] = all_answer
    
    # question final
    for final in soup.select('a[class="answer-Y"]'):
        question_exam['final_answer'] = final.b.get_text(strip=True).replace('.', '') 

    question_list.append(question_exam)






with open('data.json', 'w', encoding='utf8') as file:
  json.dump(question_list, file, indent = 4, ensure_ascii=False)

  # Inserting the loaded data in the Collection
  # if JSON contains data more than one entry
  # insert_many is used else insert_one is used

with open('data.json') as file:
    file_data = json.load(file)

if isinstance(file_data, list):
    Collection.insert_many(file_data) 
else:
    Collection.insert_one(file_data)