import streamlit as st

st.set_page_config(page_title="AI Agent 作品集", page_icon="🤖", layout="wide")

st.title("🤖 我的 AI 智能体作品集")
st.subheader("基于 LangGraph + DeepSeek 构建")

st.markdown("""
## 📌 项目列表

1. **基础对话 Agent** — 基础智能对话，支持多轮对话和思维链模式
2. **任务规划执行智能体** — 自动拆解复杂任务，分步执行并整合结果
3. **自我反思纠错 Agent** — 先回答 → 自查错误 → 修正优化输出
4. **全能一体式终极 Agent** — 意图识别 + 规划 + 工具调用 + 反思修正全流程
5. **多角色 Agent 团队** — 项目经理、研究员、分析师、文案撰写者协作系统
""")

st.success("✅ 所有 Agent 均支持网页在线运行")
st.markdown("---")
st.caption("GitHub: `https://github.com/omj2006/langgraph-demo`")