import streamlit as st
from openai import *
import os

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_KEY)

st.set_page_config(
    page_title="Your App Title",
    layout="wide",
    initial_sidebar_state="auto",
)

import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 调用
add_bg_from_local('new_background.png')


# Initialize chat
if "chat" not in st.session_state:
    st.session_state.chat = []
    
st.title("📚 English Practice Chat")

# 🔥 Step 1: 定义 GPT 调用函数
def get_revised_sentence(user_sentence):
    client = OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model="gpt-4",  # 或 "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are an English tutor. Please revise the student's sentence into a more natural and native-like English sentence, keeping the original meaning."},
            {"role": "user", "content": f"Please revise this sentence: '{user_sentence}'"}
        ],
        temperature=0.3  # 让改写更稳定自然
    )
    revised_sentence = response.choices[0].message.content.strip()
    # revised_sentence = response['choices'][0]['message']['content'].strip()
    return revised_sentence

def get_teacher_reply(student_sentence):
    client = OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are the friend of this student."},
            {"role": "user", "content": f"The student just wrote: '{student_sentence}'"}
        ],
        temperature=0.7  # 让回复更温暖活泼
    )
    teacher_reply = response.choices[0].message.content.strip()
    
    return teacher_reply



# 🔥 Step 2: 显示历史聊天
for role, content, revised in st.session_state.chat:
    col1, col2, col3 = st.columns([4, 1, 4])

    if role == "teacher":
        with col1:
            st.markdown(
                f"""
                <div style='background-color:#fff2cc;padding:10px 15px;
                            border-radius:10px;width:fit-content;
                            max-width:100%;margin-bottom:8px'>
                    <b>Teacher:</b> {content}
                </div>
                """,
                unsafe_allow_html=True
            )
    elif role == "student":
        with col3:
            st.markdown(
                f"""
                <div style='background-color:#e6f2ff;padding:10px 15px;
                            border-radius:10px;width:fit-content;
                            max-width:100%;margin-left:auto;margin-bottom:8px'>
                    <b>You:</b> {content}<br>
                    <hr style="margin:6px 0">
                    <i>✨ {revised}</i>
                </div>
                """,
                unsafe_allow_html=True
            )

# 🔥 Step 3: 处理新输入
user_input = st.chat_input("Type your sentence here...")

if user_input:
    with st.spinner('Revising your sentence...'):
        revised = get_revised_sentence(user_input)
    with st.spinner('Teacher is replying...'):
        teacher_reply = get_teacher_reply(revised)

    # 保存到聊天记录
    st.session_state.chat.append(("student", user_input, revised))
    st.session_state.chat.append(("teacher", teacher_reply, None))

    st.rerun()
