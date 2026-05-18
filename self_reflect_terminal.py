import sys
sys.stdout.reconfigure(encoding='utf-8')
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3
)

class ReflectState(TypedDict):
    query: str
    raw_answer: str
    reflect_opinion: str
    final_answer: str

def first_answer(state: ReflectState):
    res = llm.invoke(f"认真回答问题：{state['query']}")
    return {"raw_answer": res.content}

def self_reflect(state: ReflectState):
    prompt = f"""
检查下面回答是否有错、逻辑漏洞、常识错误、回答不完整，直接指出问题：
问题：{state['query']}
回答：{state['raw_answer']}
"""
    res = llm.invoke(prompt)
    return {"reflect_opinion": res.content}

def revise_answer(state: ReflectState):
    prompt = f"""
结合反思意见，修正优化答案，输出精准完整最终回答：
用户问题：{state['query']}
原始回答：{state['raw_answer']}
反思问题：{state['reflect_opinion']}
"""
    res = llm.invoke(prompt)
    return {"final_answer": res.content}

builder = StateGraph(ReflectState)
builder.add_node("初次作答", first_answer)
builder.add_node("自我反思", self_reflect)
builder.add_node("修正答案", revise_answer)

builder.add_edge(START, "初次作答")
builder.add_edge("初次作答", "自我反思")
builder.add_edge("自我反思", "修正答案")
builder.add_edge("修正答案", END)

reflect_agent = builder.compile()

def main():
    print("="*60)
    print("🧠 自我反思纠错 Agent")
    print("先作答 → 自查错误 → 自主修正 → 输出精准答案")
    print("="*60)
    
    while True:
        user_q = input("\n请输入问题（输入 'q' 退出）：")
        if user_q.lower() in ['q', 'quit', '退出']:
            print("👋 再见！")
            break
        
        if not user_q.strip():
            print("❌ 请输入有效的问题！")
            continue
        
        print("\n⏳ 智能体正在思考+自查修正...")
        result = reflect_agent.invoke({"query": user_q})
        
        print("\n" + "="*60)
        print("1. 初次原始回答")
        print("-"*60)
        print(result["raw_answer"])
        
        print("\n" + "="*60)
        print("2. 智能体自我反思纠错")
        print("-"*60)
        print(result["reflect_opinion"])
        
        print("\n" + "="*60)
        print("3. 修正后最终标准答案")
        print("-"*60)
        print(result["final_answer"])
        print("="*60)

if __name__ == "__main__":
    main()