import streamlit as st
import pandas as pd

st.set_page_config(page_title="개인 시간관리 앱", page_icon="⏰")

st.title("⏰ 개인 시간관리 웹앱")

# 세션 상태 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# 할 일 입력
with st.form("task_form"):
    task = st.text_input("할 일 입력")
    priority = st.selectbox(
        "중요도 선택",
        ["낮음", "보통", "높음"]
    )

    submitted = st.form_submit_button("추가")

    if submitted and task:
        st.session_state.tasks.append({
            "할 일": task,
            "중요도": priority,
            "완료": False
        })

# 할 일 표시
st.subheader("📋 할 일 목록")

if st.session_state.tasks:

    completed_count = 0

    for i, task in enumerate(st.session_state.tasks):

        col1, col2, col3 = st.columns([5, 2, 1])

        with col1:
            done = st.checkbox(
                task["할 일"],
                value=task["완료"],
                key=f"task_{i}"
            )
            st.session_state.tasks[i]["완료"] = done

        with col2:
            st.write(f"⭐ {task['중요도']}")

        with col3:
            if st.button("삭제", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()

        if done:
            completed_count += 1

    # 진행률 표시
    progress = completed_count / len(st.session_state.tasks)
    st.subheader("📈 진행률")
    st.progress(progress)
    st.write(f"{completed_count} / {len(st.session_state.tasks)} 완료")

else:
    st.info("할 일을 추가해보세요!")
