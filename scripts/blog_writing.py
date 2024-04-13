# -*- coding: utf-8 -*-
"""tyri blog writing

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IvuB1c7y2G63VeKweuR_7UCkY5kQHqNq

# Tyri Blog Writing

위 이미지 생성용 프롬프트를 기반으로 SNS 용으로 아래 가이드에 따라 작성해

- 너무 자랑스럽게 얘기하지말고, 겸손하나 친근하고 즐기듯이 작성해.
- 장면을 묘사하기 보다는 자기 상황을 이야기하거나 공감대를 형성하면 응원의 메시지를 전달해
위는 이미지 생성용 프롬프트이지만 SNS 인스타그램 용으로 작성해. 그리기 위한 묘사 내용을 적는 것이 아니라 자기 이야기를 작성해야 한다.
- "금발" 등의 자신의 우월함을 묘사하는 것을 작성하지마.
- 인스타그램이나 페이스북용으로 작성하는 것이라 5문장 정도만 작성해.
- 직접적으로 "응원"의 단어를 사용하지 않는다. 자기계발에 대한 직접적인 단어를 사용하지 않는다.
- 사람들간의 공감대를 형성하기 위해서 자기를 낮추고, 상대방을 바꾸려고 하지 않는다.
- 이모지와 인터넷 최신 용어도 적절하게 많이 사용한다.
- 캐주얼함과 생기있게 친근하게 작성한다.

응답형식
한국어 :
영어 :
"""

import os, sys
from google.colab import drive
drive.mount('/content/drive')

venv_path = '/content/venv'
os.symlink('/content/drive/My Drive/tykimos/venv', venv_path)
sys.path.insert(0, venv_path)

# Commented out IPython magic to ensure Python compatibility.
# """
# %%shell
# 
# pip install --target=$venv_path --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# pip install --target=$venv_path gspread
# pip install --target=$venv_path tqdm
# pip install --target=$venv_path langchain-core
# pip install --target=$venv_path langchain
# pip install --target=$venv_path langchain_openai
# pip install --target=$venv_path langchain-community
# """

"""## 키 할당 받는 법

1. Google Cloud Console에 접속
1. 사용자 인증 정보 메뉴 클릭
1. 사용자 인증 정보 만들기 클릭
1. 서비스 계정 클릭
1. 키 탭에서 키 추가 > 새 키 만들기 > JSON
1. 관리하고자 하는 시트 공유에서 client_email 계정을 편집자로 추가

## 구글 클라우드 서비스 사용

1. Google Drive API 사용
1. Google Sheets API 사용

## 설정

1. 구글 양식 작성
1. 구글 양식 연동 시트 - 서비스 계정 편집자 공유
1. 구글 양식 연동 폴더 - 서비스 계정 편집자 공유
""" 
 
SHEET_NAME = "tyri sns(응답)"

KEY_JSON = os.getenv("GOOGLE_KEY_JSON")

#GITHUB_REPO_NAME = "tykimos/tykimos.github.io"
GITHUB_REPO_NAME = "tyritarot/tyritarot.github.io"
GITHUB_USER = "tyritarot"

GT_TOKEN_KEY = os.getenv("GT_TOKEN_KEY")

PROCESS_FLOW = ["blog_content_generation", "github_upload"]
STATUS_FLOW = ["fetching", "running", "done"]

"""# 초기 셋팅"""

import time

start_time = time.time()  # Get the current time before execution
prev_time = start_time

import json
'''
# JSON 파일로 저장
with open('assi-google-credentials.json', 'w') as json_file:
  json.dump(KEY_JSON, json_file)
'''

# 문자열 데이터를 파일에 쓰기
with open('assi-google-credentials.json', 'w') as file:
    file.write(KEY_JSON)
    
print("JSON 파일이 저장되었습니다.")

from oauth2client.service_account import ServiceAccountCredentials
# 구글 인증 초기화
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('assi-google-credentials.json', scope)

import os
from google.colab import userdata

os.environ['OPENAI_API_KEY'] = userdata.get('OPENAI_API_KEY')

from langchain_openai import ChatOpenAI

chat_model = ChatOpenAI(model="gpt-4")

curr_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print(f"{curr_time - prev_time} / {curr_time - start_time}")
prev_time = curr_time

"""# 처리 함수 정의

- 타임스탬프
- 한글 제목
- 영문 제목
- 카테고리
- 기초 내용
- 유튜브 링크
- 타이틀 이미지
- blog_content_generation fetching
- blog_content_generation running
- blog_content_generation done
- github_upload fetching
- github_upload running
- github_upload done
"""

import numpy as np
import uuid

# UUID 생성 후 4자리만 추출하는 함수
def generate_4_digit_uuid():
    return str(uuid.uuid4())[:4]

def adjust_pm_hours(date_str):

    # 날짜와 시간을 분리
    date_parts = date_str.split(" ")
    time_part = date_parts[-1]  # 시간 부분은 마지막 요소에 위치
    am_pm_part = date_parts[-2]  # "오전" 또는 "오후"는 세 번째 요소에 위치

    # 시, 분, 초 분리
    hours, minutes, seconds = map(int, time_part.split(":"))

    # "오후"인 경우 시간 조정
    if am_pm_part == "오후" and hours < 12:
        hours += 12
    elif am_pm_part == "오전" and hours == 12:
        # "오전 12시"는 "00시"와 동일
        hours = 0

    # 조정된 시간을 다시 문자열로 합치기
    adjusted_time = f"{hours}:{minutes}:{seconds}"
    # 날짜 부분과 조정된 시간 부분을 합침
    return " ".join(date_parts[:-2] + [adjusted_time])

adjust_pm_hours("2024. 4. 3 오후 8:20:07")

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import os

def download_file_from_gdrive(url, topic_id, creds):
    """특정 Google Drive 파일을 다운로드합니다."""

    file_id = url.split('=')[-1]

    service = build('drive', 'v3', credentials=creds)

    # 파일 메타데이터 조회
    file_metadata = service.files().get(fileId=file_id, fields='name').execute()

    # 파일 이름과 확장자 추출
    file_name = file_metadata.get('name')
    file_extension = file_name.split('.')[-1]

    new_filename = f"{topic_id}_title." + file_extension

    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    # 파일 쓰기
    with open(new_filename, 'wb') as f:
        f.write(fh.getbuffer())

    return new_filename

import json

def parse_json(json_str):
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None

def gen_daily_life_blog_content_body(sketch, prompt):

    content_body = ""
    system_prompt = """사용자가 입력한 sketch와 dalle prompt를 기반으로 SNS 용으로 아래 가이드에 따라 작성해. 모든 응답은 JSON으로 작성한다.

- 너무 자랑스럽게 얘기하지말고, 겸손하나 친근하고 즐기듯이 작성해.
- 장면을 묘사하기 보다는 자기 상황을 이야기하거나 공감대를 형성하면 응원의 메시지를 전달해
위는 이미지 생성용 프롬프트이지만 SNS 인스타그램 용으로 작성해. 그리기 위한 묘사 내용을 적는 것이 아니라 자기 이야기를 작성해야 한다.
- "금발" 등의 자신의 우월함을 묘사하는 것을 작성하지마.
- 인스타그램이나 페이스북용으로 작성하는 것이라 5문장 정도만 작성해.
- 직접적으로 "응원"의 단어를 사용하지 않는다. 자기계발에 대한 직접적인 단어를 사용하지 않는다.
- 사람들간의 공감대를 형성하기 위해서 자기를 낮추고, 상대방을 바꾸려고 하지 않는다.
- 이모지와 인터넷 최신 용어도 적절하게 많이 사용한다.
- 캐주얼함과 생기있게 친근하게 작성한다.
- tag는 본 게시물에 가장 잘 어울리는 태그 3개를 영어로 작성한다. 태그 단어 내부에는 띄워쓰기가 없어야 한다.
- tag은 인스타그램에서 많이 사용하는 태그를 해야한다.
- 응답을 JSON으로 파싱을 해야되기 때문에 반드시 JSON만으로만 응답한다.
- subtitle은 내용에 적절한 영문 제목을 개괄식으로 작성한다. 특수기호는 사용하지 않는다.

[응답형식 JSON]
{{
    "subtitle" : "(Write in English)"
    "ko" : "",
    "en" : "",
    "tag" : ["", ""]

}}
"""

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_prompt),
        ("human", "sketch : {sketch}\n\ndalle prompt : {prompt}")]
    )

    chain = (prompt_template
            | chat_model
            | StrOutputParser())

    gen_content = chain.invoke({"sketch" : sketch, "prompt": prompt})

    # 최대 재시도 횟수 설정
    max_retries = 3
    retry_count = 0

    # 재시도를 통해 JSON 형식의 부분을 찾아 파싱
    while retry_count < max_retries:
        # 문자열에 JSON 형식의 부분을 찾기
        start_index = gen_content.find("{")
        end_index = gen_content.rfind("}")

        # JSON 형식의 부분을 추출하여 파싱
        if start_index != -1 and end_index != -1:
            json_str = gen_content[start_index:end_index+1]
            gen_content_json = parse_json(json_str)
            if gen_content_json:
                print("Parsed JSON:", gen_content_json)
                # 추가 작업 수행
                break
            else:
                retry_count += 1
        else:
            print("JSON 형식의 부분을 찾을 수 없습니다.")
            retry_count += 1

    # 최대 재시도 횟수를 초과한 경우 메시지 출력
    if retry_count == max_retries:
        print("최대 재시도 횟수를 초과하여 JSON을 파싱할 수 없습니다.")
        content_body += gen_content
        content_tag = ""
        content_subtitle = gen_content[:10]
    else:
        content_subtitle = gen_content_json['subtitle']
        content_body += gen_content_json['ko']
        content_body += '\n\n'
        content_body += gen_content_json['en']
        content_body += '\n\n'
        content_body += '### Dalle Prompt'
        content_body += '\n\n'
        content_body += prompt
        content_tag = " ".join(gen_content_json['tag'])

    return content_subtitle, content_body, content_tag

from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

gen_content_type_dict = {
    "daily life" : gen_daily_life_blog_content_body,
}

def gen_content_body(content_type, sketch, prompt):

    print("gen_content_type_dict : " + content_type)

    content_subtitle, content_body, content_tag = gen_content_type_dict[content_type](sketch, prompt)

    return content_subtitle, content_body, content_tag

def gen_topic_id(date, topic):
    date_str = date.strftime('%Y-%-m-%-d')

    topic = topic.replace(' ', '_')
    topic = topic.replace('+', '_')
    topic = topic.replace('·', '_')
    topic = topic.replace('-', '_')
    topic = topic.replace("'", '_')

    return f"{date_str}-{topic.lower()}"

def proc_content_generation(item):

    adjusted_date_string = adjust_pm_hours(item['타임스탬프'])
    datetime_object = datetime.strptime(adjusted_date_string, "%Y. %m. %d %H:%M:%S")
    datetime_str = datetime_object.strftime('%Y-%-m-%-d %H:%M:%S')
    year_str = datetime_object.strftime('%Y')

    content_subtitle, content_body, content_tag = gen_content_body(item['type'], item['sketch'], item['prompt'])

    topic_id = gen_topic_id(datetime_object, content_subtitle)

    # 파일 이름 및 메타데이터 파싱
    filename = f"{topic_id}.md"

    new_image_filename = download_file_from_gdrive(item['image'], topic_id, creds)

    image_url = f"http://{GITHUB_USER}.github.io/warehouse/{year_str}/{new_image_filename}"

    # 파일 내용 설정
    content = f"""---
layout: post
title: "{content_subtitle}"
author: tyri
date: {datetime_str}
categories: {content_tag}
comments: true
image: {image_url}
---

{content_body}
"""

   # 블로그 내용을 저장할 markdown 파일명 생성
    markdown_filename = f"{topic_id}.md"

    # markdown 파일로 내용 저장
    with open(markdown_filename, 'w', encoding='utf-8') as md_file:
        md_file.write(content)

    curr_report_filename = f"blog_content_generation_{generate_4_digit_uuid()}.json"

    # 최종 결과 저장을 위한 JSON 파일 생성
    report_data = {
        'markdown_filename': markdown_filename,
        'image_filename': new_image_filename
    }

    with open(curr_report_filename, 'w') as file:
        json.dump(report_data, file)

    return curr_report_filename

import json
import base64
import requests

def get_file_sha(token, repo, path):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("sha")
    return None

def github_file_upload(src_filepath, dst_filepath):

    # 파일 확장자 기반으로 파일 타입 판별
    _, file_extension = os.path.splitext(src_filepath)
    text_extensions = ['.txt', '.md']
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif']

    content = None  # 파일 내용을 저장할 변수 초기화

    # 텍스트 파일일 경우
    if file_extension in text_extensions:
        with open(src_filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            encoded_content = base64.b64encode(content.encode()).decode()

    # 이미지 파일일 경우
    elif file_extension in image_extensions:
        with open(src_filepath, 'rb') as file:
            encoded_content = base64.b64encode(file.read()).decode()

    # 기본 URL 및 인증 설정
    url = f"https://api.github.com/repos/{GITHUB_REPO_NAME}/contents/{dst_filepath}"
    headers = {
        "Authorization": f"token {GT_TOKEN_KEY}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 파일의 SHA 값을 가져오기
    sha = get_file_sha(GT_TOKEN_KEY, GITHUB_REPO_NAME, dst_filepath)

    # 요청 데이터 구성
    data = {
        "message": f"Add or update {dst_filepath}",
        "content": encoded_content
    }

    # 만약 sha 값이 있다면, data에 추가 (기존 파일 수정을 위함)
    if sha:
        data["sha"] = sha

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 201:
        print(f"Successfully created or updated file at {url}")
        return True
    elif response.status_code == 200:
        print(f"Successfully updated file at {url}")
        return True
    else:
        print(f"Failed to create or update file. Response: {response.text}")

    return False

def proc_github_upload(item):

    prev_report_filename = item["blog_content_generation done"]

    # JSON 파일에서 markdown 파일 이름 읽기
    with open(prev_report_filename, 'r', encoding='utf-8') as file:
        report_data = json.load(file)
        markdown_filename = report_data['markdown_filename']
        image_filename = report_data['image_filename']

    adjusted_date_string = adjust_pm_hours(item['타임스탬프'])
    datetime_object = datetime.strptime(adjusted_date_string, "%Y. %m. %d %H:%M:%S")
    year_str = datetime_object.strftime('%Y')

    github_markdown_filepath = f"_posts/{markdown_filename}"
    github_image_filepath = f"warehouse/{year_str}/{image_filename}"

    if github_file_upload(markdown_filename, github_markdown_filepath) == False:
        print(f"Failed to upload {github_markdown_filepath}")
    if github_file_upload(image_filename, github_image_filepath) == False:
        print(f"Failed to upload {github_image_filepath}")

    curr_report_filename = f"github_upload_{generate_4_digit_uuid()}.json"

    # 최종 결과 저장을 위한 JSON 파일 생성
    report_data = {
        'github_markdown_filepath': github_markdown_filepath,
        'github_image_filepath': github_image_filepath
    }

    with open(curr_report_filename, 'w') as file:
        json.dump(report_data, file)

    return curr_report_filename

tools = {
    "blog_content_generation" : proc_content_generation,
    "github_upload" : proc_github_upload
}

"""# 구글 연결

# 시트 연결
"""

import gspread

client = gspread.authorize(creds)

# 구글 시트 열기
worksheet = client.open(SHEET_NAME).sheet1

"""# 시트 모니터링"""

# 첫 번째 행에서 열 이름을 찾아 해당 열 인덱스를 얻기
def get_column_index(column_name):
    first_row = worksheet.row_values(1)  # 첫 번째 행의 값 가져오기
    return first_row.index(column_name) + 1  # 열 번호는 1부터 시작하므로 1을 더해야 합니다.

def update_sheet_status(row_index, column_name, value):
    """시트의 상태를 업데이트하는 함수"""
    column_index = get_column_index(column_name)
    worksheet.update_cell(row_index + 2, column_index, value)

from tqdm import tqdm
import pandas as pd

def proc_invoke(pf, df):

    global prev_time

    column_name = pf + " " + STATUS_FLOW[0]

    column_index = df.columns.get_loc(column_name)

    if column_index <= 0:
        return False

    # 이전 열의 이름
    previous_column_name = df.columns[column_index - 1]

    pending_workorder = df[df[previous_column_name].notna() & (df[column_name] == '')]

    # 팬딩된 비디오 생성 요청의 수 계산
    pending_workorder_count = pending_workorder.shape[0]

    # 결과 출력
    print(f"Pending {pf} requests: {pending_workorder_count}")

    for index, row in tqdm(pending_workorder.iterrows(), total=pending_workorder.shape[0], desc="Processing " + pf):

        update_sheet_status(index, pf + " " + STATUS_FLOW[0], '1')
        update_sheet_status(index, pf + " " + STATUS_FLOW[1], '1')

        try:
            report_filename = tools[pf](row)
            print(report_filename)
            update_sheet_status(index, pf + " " + STATUS_FLOW[2], report_filename)

        except Exception as e:

            print(f"오류 발생: {e}")
            update_sheet_status(index, pf + " " + STATUS_FLOW[0], '')
            update_sheet_status(index, pf + " " + STATUS_FLOW[1], '')

        curr_time = time.time()
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(f"{curr_time - prev_time} / {curr_time - start_time}")
        prev_time = curr_time

for pf in PROCESS_FLOW:

    print(pf + "...")

    # pandas로 구글 시트 데이터 불러오기
    df = pd.DataFrame(worksheet.get_all_records())

    proc_invoke(pf, df)

    print("\nDone.")
