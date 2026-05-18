from langchain_deepseek import ChatDeepSeek
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

class AgentState(TypedDict):
    question: str
    think_result: str
    final_answer: str

def think_node(state: AgentState) -> AgentState:
    res = llm.invoke(f"请简单梳理思路：{state['question']}")
    state["think_result"] = res.content
    return state

def answer_node(state: AgentState) -> AgentState:
    prompt = f"思路：{state['think_result']}\n根据思路完整回答问题：{state['question']}"
    res = llm.invoke(prompt)
    state["final_answer"] = res.content
    return state

builder = StateGraph(AgentState)
builder.add_node("think", think_node)
builder.add_node("answer", answer_node)
builder.add_edge(START, "think")
builder.add_edge("think", "answer")
builder.add_edge("answer", END)

graph = builder.compile()

if __name__ == "__main__":
    print("🤖 LangGraph 问答助手已启动！")
    print("输入你的问题（输入 'q' 或 'quit' 退出）：\n")
    
    while True:
        user_input = input("你的问题: ").strip()
        
        if user_input.lower() in ['q', 'quit', '退出']:
            print("👋 再见！")
            break
            
        if not user_input:
            continue
            
        print("\n🔄 正在思考...")
        result = graph.invoke({"question": user_input})
        
        print("\n=== 思考过程 ===")
        print(result["think_result"])
        print("\n=== 最终答案 ===")
        print(result["final_answer"])
        print("\n" + "="*50 + "\n")