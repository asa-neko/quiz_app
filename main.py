import streamlit as st
import numpy as np
import random
import os
import pandas as pd

def main():
    st.title("クイズアプリ")
    mode = ["4択クイズ","一問一答"]
    choice = st.sidebar.selectbox("Select an Mode", mode)

    value = st.slider("出題問題数を選択してね",1,100,10)
    upload_file = st.file_uploader("ファイルを選択してね")
    if upload_file is not None:
        st.write(upload_file)

    if st.button("Start"):
        if choice == "4択クイズ":
            if upload_file is not None:
                try:
                    st.session_state.q_data=make_data_choice(upload_file,value)
                    st.session_state.choice_quiz_session = True
                    st.session_state.main_session = False
                    st.rerun()
                except Exception as e:
                    st.write(e)
        elif choice == "一問一答":
            if upload_file is not None:
                try:
                    st.session_state.q_data=make_data_QAA(upload_file,value)
                    st.session_state.QAA_session = True
                    st.session_state.main_session = False
                    st.rerun()
                except Exception as e:
                    st.write(e)
                    
def make_data_choice(upload_file,value):
    df = pd.read_csv(upload_file)
    num_questions_in_csv = len(df) # CSVファイルの総問題数
    quiz_list = []
    # 10問出題するための問題リストを作成
    # 同じ問題が重複して出題されないように、一度選んだ問題のインデックスを記録する
    selected_indices = set()
    while len(quiz_list) < value:
        if len(selected_indices) >= num_questions_in_csv:
            st.write("エラー: CSVファイルの問題数が不足しています。")
            break
        q_num = random.randint(0, num_questions_in_csv - 1) # CSVの範囲内でランダムな問題番号を選択
        if q_num not in selected_indices:
            selected_indices.add(q_num)
            # .ilocでDataFrameから直接スカラー値を取得するように修正
            # df.iloc[行インデックス, 列インデックス] で特定のセルの値を取得
            quiz_list.append({
                "問題": df.iloc[q_num, 0],
                "答え": df.iloc[q_num, 1],
                "選択肢1": df.iloc[q_num, 2],
                "選択肢2": df.iloc[q_num, 3],
                "選択肢3": df.iloc[q_num, 4],
                "選択肢4": df.iloc[q_num, 5]})
    if quiz_list: # 問題リストが正常に作成された場合のみクイズを開始
        return quiz_list

def make_data_QAA(upload_file,value):
    df = pd.read_csv(upload_file)
    num_questions_in_csv = len(df) # CSVファイルの総問題数
    quiz_list = []
    # 10問出題するための問題リストを作成
    # 同じ問題が重複して出題されないように、一度選んだ問題のインデックスを記録する
    selected_indices = set()
    while len(quiz_list) < value:
        if len(selected_indices) >= num_questions_in_csv:
            st.write("エラー: CSVファイルの問題数が不足しています。")
            break
        q_num = random.randint(0, num_questions_in_csv - 1) # CSVの範囲内でランダムな問題番号を選択
        if q_num not in selected_indices:
            selected_indices.add(q_num)
            # .ilocでDataFrameから直接スカラー値を取得するように修正
            # df.iloc[行インデックス, 列インデックス] で特定のセルの値を取得
            quiz_list.append({
                "問題": df.iloc[q_num, 0],
                "答え": df.iloc[q_num, 1]})
    if quiz_list: # 問題リストが正常に作成された場合のみクイズを開始
        return quiz_list

def choice_quiz():        
    correct = 0
    st.title("4択クイズ")

    q_list = st.session_state.q_data
    if not q_list or st.session_state.num == len(q_list):
        st.write("クイズが終了しました")
        st.write(f"{st.session_state.correct}問正解しました")
        if st.button("メイン画面に戻る"):
            reset_session_state()
            st.rerun()
        return
    q_list_n = q_list[st.session_state.num]
    q = q_list_n["問題"]
    a = q_list_n["答え"]
    if f"q_{st.session_state.num}" not in st.session_state:
        c = [q_list_n["選択肢1"],
             q_list_n["選択肢2"],
             q_list_n["選択肢3"],
             q_list_n["選択肢4"]]
        random.shuffle(c)
        st.session_state[f"q_{st.session_state.num}"] = c
        st.session_state.select_answer = None
    
    c2 = st.session_state[f"q_{st.session_state.num}"]

    answer = st.radio(q,c2,key=f"radio_{st.session_state.num}")

    if st.button("解答"):
        if answer == a:
            st.session_state.correct += 1
            st.session_state.num += 1
            st.session_state.q = None
            st.write("正解!")
        else:
            st.session_state.num += 1
            st.session_state.q = None
            st.write(f"不正解!　正解は「{a}」でした!")
    if st.button("次の問題へ"):
        st.rerun()
        
def QAA():
    st.title("一問一答")

    q_list = st.session_state.q_data
    if not q_list or st.session_state.num == len(q_list):
        st.write("クイズが終了しました")
        st.write(f"{st.session_state.correct}問正解しました")
        if st.button("メイン画面に戻る"):
            reset_session_state()
            st.rerun()
        return
    q_list_n = q_list[st.session_state.num]
    q = q_list_n["問題"]
    a = q_list_n["答え"]
    
    st.write(q)
    answer = st.text_input("ここに解答を入力","Write answer here.")

    if st.button("解答"):
        if answer == a:
            st.session_state.correct += 1
            st.session_state.num += 1
            st.write("正解!")
        else:
            st.session_state.num += 1
            st.write(f"不正解!　正解は「{a}」でした!")
    if st.button("次の問題へ"):
        st.rerun()

def reset_session_state():
    st.session_state.main_session = True
    st.session_state.choice_quiz_session = False
    st.session_state.QAA_session = False
    st.session_state.q_data = None
    st.session_state.num = 0
    st.session_state.correct = 0

if "main_session" not in st.session_state:
    st.session_state.main_session = True
if "choice_quiz_session" not in st.session_state:
    st.session_state.choice_quiz_session = False
if "QAA_session" not in st.session_state:
    st.session_state.QAA_session = False
if "q_data" not in st.session_state:
    st.session_state.q_data = None
if "RESULT_session" not in st.session_state:
    RESULT_session = False
if "num" not in st.session_state:
    st.session_state.num = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0


if st.session_state.main_session:
    main()
elif st.session_state.choice_quiz_session:
    choice_quiz()
elif st.session_state.QAA_session:
    QAA()
else:
    main()
