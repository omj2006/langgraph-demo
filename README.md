# LangGraph Agent Demo Collection

一个完整的 **AI Agent 智能体项目合集**，基于 LangGraph 框架构建，包含多种主流 Agent 类型，适合学习和面试展示。

## 🎯 项目亮点

- ✅ **标准 LangGraph 架构**：行业标准的智能体工作流设计
- ✅ **多种 Agent 类型**：覆盖对话、任务规划、自我反思、多角色协作
- ✅ **工具调用能力**：支持网络搜索等外部工具
- ✅ **状态管理**：节点间有序的数据传递
- ✅ **完整可运行**：基于 DeepSeek API，开箱即用

## 📁 项目结构

```
langgraph-demo/
├── main.py                    # 基础对话 Agent
├── task_planner_agent.py      # 任务规划执行智能体（网页版）
├── self_reflect_agent.py      # 自我反思纠错 Agent（网页版）
├── self_reflect_terminal.py   # 自我反思纠错 Agent（终端版）
├── multi-agent-team/
│   └── main.py                # 多角色 Agent 团队
├── .env                       # API Key 配置（需自行填写）
└── .gitignore                 # Git 忽略配置
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install langchain-deepseek langgraph python-dotenv streamlit requests
```

### 2. 配置 API Key

在 `.env` 文件中填入你的 DeepSeek API Key：

```env
DEEPSEEK_API_KEY=your_api_key_here
```

### 3. 运行项目

| Agent 类型 | 运行命令 | 说明 |
|-----------|----------|------|
| 基础对话 | `python3 main.py` | 交互式问答助手 |
| 任务规划 | `streamlit run task_planner_agent.py` | 网页版任务分解执行 |
| 自我反思（网页） | `streamlit run self_reflect_agent.py` | 网页版自查纠错 |
| 自我反思（终端） | `python3 self_reflect_terminal.py` | 终端版自查纠错 |
| 多角色团队 | `python3 multi-agent-team/main.py` | 市场调研团队 |

## 🧠 Agent 类型详解

### 1. 基础对话 Agent (`main.py`)
- 支持多轮对话
- "先思考后回答"思维链模式
- 简单交互界面

### 2. 任务规划执行 Agent (`task_planner_agent.py`)
- 自主拆解复杂任务
- 分步执行子任务
- 整合最终结果
- 网页可视化界面

### 3. 自我反思纠错 Agent (`self_reflect_agent.py` / `self_reflect_terminal.py`)
- 初次作答 → 自我检查 → 修正答案
- 三层逻辑链架构
- 解决大模型幻觉问题

### 4. 多角色团队 Agent (`multi-agent-team/main.py`)
- 项目经理、研究员、分析师、文案撰写者
- 多 Agent 协作完成复杂任务
- 分工明确的角色定位

## 🔧 技术栈

- **框架**: LangGraph
- **LLM**: DeepSeek (deepseek-chat)
- **前端**: Streamlit
- **工具**: DuckDuckGo Search API

## 📝 面试亮点

这个项目集合展示了以下核心能力：

1. ✅ **工作流编排**：基于 StateGraph 的状态管理和节点连接
2. ✅ **工具调用**：集成外部搜索工具获取实时信息
3. ✅ **条件分支**：根据任务类型动态路由
4. ✅ **多 Agent 协作**：多个角色分工完成复杂任务
5. ✅ **自我反思**：高阶智能体的自省能力
6. ✅ **状态管理**：节点间数据共享和传递

## 📄 License

MIT License