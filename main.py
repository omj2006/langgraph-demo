# 1. 导入包 (把 ChatOpenAI 换成 ChatDeepSeek)
from langchain_deepseek import ChatDeepSeek  # 关键替换
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from dotenv import load_dotenv
import os

# 2. 加载环境变量
load_dotenv()

# 3. 初始化 DeepSeek 模型 (关键部分)
llm = ChatDeepSeek(
    model="deepseek-chat",      # DeepSeek 主模型 (V3)
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7,            # 创意度
    max_tokens=2048             # 最大输出长度
)

# 4. 定义状态 (和之前一样)
class AgentState(TypedDict):
    question: str
    think_result: str
    final_answer: str

# 5. 节点1：思考
def think_node(state: AgentState) -> AgentState:
    res = llm.invoke(f"请简单梳理思路：{state['question']}")
    state["think_result"] = res.content
    return state

# 6. 节点2：回答
def answer_node(state: AgentState) -> AgentState:
    prompt = f"思路：{state['think_result']}\n根据思路完整回答问题：{state['question']}"
    res = llm.invoke(prompt)
    state["final_answer"] = res.content
    return state

# 7. 构建流程图 (和之前一样)
builder = StateGraph(AgentState)
builder.add_node("think", think_node)
builder.add_node("answer", answer_node)
builder.add_edge(START, "think")
builder.add_edge("think", "answer")
builder.add_edge("answer", END)

graph = builder.compile()

# 8. 运行测试
if __name__ == "__main__":
    user_question = "解释什么是RAG检索增强生成"
    result = graph.invoke({"question": user_question})
    
    print("=== 思考过程 ===")
    print(result["think_result"])
    print("\n=== 最终答案 ===")
    print(result["final_answer"])