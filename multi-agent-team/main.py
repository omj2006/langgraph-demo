from langchain_deepseek import ChatDeepSeek
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
from dotenv import load_dotenv
import os
import requests

load_dotenv()
llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

class TeamState(TypedDict):
    task: str
    project_plan: str
    research_questions: List[str]
    research_results: List[str]
    analysis_report: str
    final_report: str
    current_agent: str

def web_search(query: str) -> str:
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = []
            if "Abstract" in data and data["Abstract"]:
                results.append(data["Abstract"])
            if "RelatedTopics" in data:
                for topic in data["RelatedTopics"][:3]:
                    if "Text" in topic:
                        results.append(topic["Text"])
            return "\n".join(results[:5])
        return ""
    except Exception as e:
        print(f"搜索出错: {e}")
        return ""

def project_manager(state: TeamState) -> TeamState:
    print("🤵 项目经理: 正在分析任务并制定计划...")
    
    prompt = f"""
你是一位资深的项目经理，请根据以下任务制定详细的项目计划：

任务：{state['task']}

请输出：
1. 任务拆解：将任务分解为3-5个具体的子任务
2. 研究问题：列出需要研究的关键问题（3-5个）

输出格式：
项目计划：
[详细的项目计划]

研究问题：
1. [问题1]
2. [问题2]
3. [问题3]
"""
    res = llm.invoke(prompt)
    content = res.content.strip()
    
    plan_section = content.split("研究问题：")[0].replace("项目计划：", "").strip()
    questions_section = content.split("研究问题：")[1].strip()
    
    state["project_plan"] = plan_section
    
    questions = []
    for line in questions_section.split("\n"):
        line = line.strip()
        if line and (line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5.")):
            questions.append(line[3:].strip())
    
    state["research_questions"] = questions
    state["current_agent"] = "项目经理"
    return state

def researcher(state: TeamState) -> TeamState:
    print("🔍 研究员: 正在收集市场信息...")
    
    results = []
    for i, question in enumerate(state["research_questions"], 1):
        print(f"   正在研究问题 {i}: {question}")
        search_result = web_search(question)
        if search_result:
            results.append(f"问题 {i}: {question}\n{search_result}")
        else:
            results.append(f"问题 {i}: {question}\n暂无搜索结果")
    
    state["research_results"] = results
    state["current_agent"] = "研究员"
    return state

def analyst(state: TeamState) -> TeamState:
    print("📊 分析师: 正在分析数据并提取洞察...")
    
    research_text = "\n\n".join(state["research_results"])
    
    prompt = f"""
你是一位资深市场分析师，请根据以下研究结果进行深入分析：

任务：{state['task']}

研究结果：
{research_text}

请输出：
1. 关键发现：列出3-5个最重要的发现
2. 趋势分析：分析市场趋势和变化
3. 建议：给出具体的行动建议

输出格式：
关键发现：
1. [发现1]
2. [发现2]
3. [发现3]

趋势分析：
[详细分析]

建议：
1. [建议1]
2. [建议2]
"""
    res = llm.invoke(prompt)
    state["analysis_report"] = res.content.strip()
    state["current_agent"] = "分析师"
    return state

def writer(state: TeamState) -> TeamState:
    print("✍️ 文案撰写者: 正在撰写最终报告...")
    
    prompt = f"""
你是一位专业的报告撰写者，请根据以下信息撰写一份专业的市场调研报告：

任务：{state['task']}

项目计划：
{state['project_plan']}

研究结果：
{chr(10).join(state['research_results'])}

分析报告：
{state['analysis_report']}

要求：
1. 格式专业、结构清晰
2. 包含执行摘要、研究方法、主要发现、结论与建议
3. 语言正式但易于理解
4. 使用Markdown格式输出
"""
    res = llm.invoke(prompt)
    state["final_report"] = res.content.strip()
    state["current_agent"] = "文案撰写者"
    return state

def print_team_workflow(state: TeamState):
    print("\n" + "="*70)
    print(f"📋 当前任务: {state['task']}")
    print(f"👤 当前负责人: {state['current_agent']}")
    print("="*70 + "\n")

builder = StateGraph(TeamState)
builder.add_node("project_manager", project_manager)
builder.add_node("researcher", researcher)
builder.add_node("analyst", analyst)
builder.add_node("writer", writer)

builder.add_edge(START, "project_manager")
builder.add_edge("project_manager", "researcher")
builder.add_edge("researcher", "analyst")
builder.add_edge("analyst", "writer")
builder.add_edge("writer", END)

graph = builder.compile()

def main():
    print("🚀 多 Agent 市场调研团队")
    print("="*70)
    print("团队成员：项目经理 → 研究员 → 分析师 → 文案撰写者")
    print("="*70 + "\n")
    
    task = input("请输入调研任务（如：分析2024年AI市场趋势）：")
    
    print("\n🔄 团队开始工作...\n")
    
    result = graph.invoke({
        "task": task,
        "project_plan": "",
        "research_questions": [],
        "research_results": [],
        "analysis_report": "",
        "final_report": "",
        "current_agent": ""
    })
    
    print("\n" + "🎉"*20)
    print("📝 最终报告已完成！")
    print("🎉"*20 + "\n")
    
    print(result["final_report"])
    
    print("\n" + "="*70)
    print("✅ 任务完成！")
    print("="*70)

if __name__ == "__main__":
    main()