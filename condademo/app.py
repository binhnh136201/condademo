from base64 import encode
from bs4 import BeautifulSoup
import utils
import requests
import json
import xmltojson, xmltodict
# importing re module
import re

url = "https://oto360.net/thi-lai-xe?"
question_list = []



for x in range(35):
  test_position = str(x)
  payload = "ajax=loadQuestionNext&current=" + test_position + "&exam=1&selected=0"
  headers = {
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  soup = BeautifulSoup(response.content, 'html.parser')
  response = requests.request("POST", url, headers=headers, data=payload)
  soup = BeautifulSoup(response.content, 'html.parser')

  # question number
  questions = soup.find_all("p")
  question_object = {}
  question_txt = questions[0]
  question_numbers = question_txt.find_all(string=re.compile("Câu hỏi"))
  question_number = question_numbers[0]
  question_object['question_number'] = question_number

  #question content
  question_content = questions[1].string
  question_object['question_content'] = question_content


  #question answer
  answers = soup.select('a[class="answer-Y"]')
  for answer in answers:
    question_answer = answer.get_text(strip=True)

  question_object['question_answer'] = question_answer

  question_list.append(question_object)

  # print(question_list)

  json_string = json.dumps(question_list, ensure_ascii=False)
    
  with open('data.json', 'w', encode='utf-8') as f:
    json.dump(question_list, f)

  





#TEST

# with open('result.txt') as f:
#   response = f.read()
  

# soup = BeautifulSoup(response, 'html.parser')




# response = requests.request("POST", url, headers=headers, data=payload)
# soup = BeautifulSoup(response.content, 'html.parser')

# # question number
# questions = soup.find_all("p")
# question_object = {}
# question_txt = questions[0]
# question_numbers = question_txt.find_all(string=re.compile("Câu hỏi"))
# question_number = question_numbers[0]
# question_object['question_number'] = question_number

# #question content
# question_content = questions[1].string
# question_object['question_content'] = question_content


# #question answer
# answers = soup.select('a[class="answer-Y"]')
# for answer in answers:
#   question_answer = answer.get_text(strip=True)

# question_object['question_answer'] = question_answer

# question_list.append(question_object)

# # print(question_list)

# json_string = json.dumps(question_list, ensure_ascii=False)
  
# with open('data.json', 'w') as f:
#   json.dump(question_list, f)