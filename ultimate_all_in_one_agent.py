import sys
sys.stdout.reconfigure(encoding='utf-8')
import streamlit as st
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import StateGraph, START, END
from langchain.agents import tool
from langchain_community.tools import DuckDuckGoSearchRun
from typing import TypedDict, Literal
from dotenv import load_dotenv
import os
import numexpr

load_dotenv()
llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.2
)

search_tool = DuckDuckGoSearchRun()

@tool
def calc_tool(expr: str) -> str:
    """数学计算工具，支持加减乘除等基本运算"""
    try:
        return str(numexpr.evaluate(expr))
    except:
        return "计算失败"

class UltimateState(TypedDict):
    user_input: str
    intent: str
    plan: str
    tool_result: str
    draft_ans: str
    reflect: str
    final_ans: str

def recognize_intent(state: UltimateState):
    res = llm.invoke(f"判断用户需求类型：{state['user_input']}，只写用途分类")
    return {"intent": res.content}

def make_plan(state: UltimateState):
    res = llm.invoke(f"根据需求写简明执行步骤：{state['user_input']}")
    return {"plan": res.content}

def auto_use_tool(state: UltimateState):
    text = state["user_input"].lower()
    if any(k in text for k in ["计算","+","-","*","/","等于"]):
        return {"tool_result": calc_tool.invoke(text)}
    elif any(k in text for k in ["最新","实时","现在","天气","新闻","数据"]):
        return {"tool_result": search_tool.run(text)[:400]}
    return {"tool_result": "无需调用外部工具"}

def gen_draft(state: UltimateState):
    prompt = f"需求：{state['user_input']}\n方案：{state['plan']}\n工具信息：{state['tool_result']}\n写出初步回答"
    return {"draft_ans": llm.invoke(prompt).content}

def self_check(state: UltimateState):
    res = llm.invoke(f"检查回答漏洞与错误：{state['draft_ans']}，简短指出问题")
    return {"reflect": res.content}

def get_final(state: UltimateState):
    prompt = f"结合自查意见优化答案：初稿{state['draft_ans']} 问题{state['reflect']}"
    return {"final_ans": llm.invoke(prompt).content}

builder = StateGraph(UltimateState)
builder.add_node("意图识别", recognize_intent)
builder.add_node("制定方案", make_plan)
builder.add_node("调用工具", auto_use_tool)
builder.add_node("生成初稿", gen_draft)
builder.add_node("自省核查", self_check)
builder.add_node("定稿输出", get_final)

builder.add_edge(START, "意图识别")
builder.add_edge("意图识别", "制定方案")
builder.add_edge("制定方案", "调用工具")
builder.add_edge("调用工具", "生成初稿")
builder.add_edge("生成初稿", "自省核查")
builder.add_edge("自省核查", "定稿输出")
builder.add_edge("定稿输出", END)

ultimate_agent = builder.compile()

st.title("🚀 全能一体式终极Agent")
st.subheader("意图识别→规划→工具调用→自查修正全流程")
user_text = st.text_area("输入任意需求","帮我算25*48，再整理一份今日热门资讯")

if st.button("启动全能智能体") and user_text:
    with st.spinner("全链路自主执行中..."):
        res = ultimate_agent.invoke({"user_input":user_text})
    st.text_area("1. 需求意图", res["intent"], height=100)
    st.text_area("2. 执行规划", res["plan"], height=150)
    st.text_area("3. 工具返回结果", res["tool_result"], height=150)
    st.text_area("4. 初次回答", res["draft_ans"], height=200)
    st.text_area("5. 自我检查意见", res["reflect"], height=150)
    st.text_area("6. 最终优化答案", res["final_ans"], height=250)