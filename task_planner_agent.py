# 任务规划执行智能体 标准Agent应用
import sys
sys.stdout.reconfigure(encoding='utf-8')
import streamlit as st
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,List
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.2
)

class AgentState(TypedDict):
    user_task:str
    task_list:List[str]
    finish_result:str
    final_answer:str

def split_task(state:AgentState):
    prompt=f"""
请把用户需求拆分成清晰可执行的分步任务，只列出任务列表：
用户需求：{state['user_task']}
"""
    res=llm.invoke(prompt)
    task_arr=[t.strip() for t in res.content.split("\n") if t.strip()]
    return {"task_list":task_arr}

def run_task(state:AgentState):
    all_res=""
    for idx,task in enumerate(state["task_list"],1):
        res=llm.invoke(f"完成任务：{task}")
        all_res+=f"步骤{idx}：{res.content}\n"
    return {"finish_result":all_res}

def summary_result(state:AgentState):
    prompt=f"""
整合下面所有执行步骤，整理成完整通顺的最终方案：
执行过程：{state['finish_result']}
"""
    ans=llm.invoke(prompt)
    return {"final_answer":ans.content}

builder=StateGraph(AgentState)
builder.add_node("拆分任务",split_task)
builder.add_node("执行任务",run_task)
builder.add_node("汇总结果",summary_result)

builder.add_edge(START,"拆分任务")
builder.add_edge("拆分任务","执行任务")
builder.add_edge("执行任务","汇总结果")
builder.add_edge("汇总结果",END)

agent=builder.compile()

st.title("📋 任务规划执行智能体 | 标准Agent")
st.subheader("自动拆解任务→分步执行→整合答案")
user_input=st.text_area("输入你的目标任务","写一份一周健身计划")
if st.button("Agent自动执行") and user_input:
    with st.spinner("智能体正在规划并执行任务..."):
        out=agent.invoke({"user_task":user_input})
    st.markdown("### 📝 拆解任务列表")
    for t in out["task_list"]:
        st.write("-",t)
    st.markdown("### ✅ 最终完成方案")
    st.write(out["final_answer"])