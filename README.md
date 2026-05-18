# 🤖 LangGraph Agent Collection

基于 LangGraph + DeepSeek 构建的完整 AI 智能体集合，包含 5 个不同类型的 Agent！

---

## 📁 项目结构

```
langgraph-demo/
├── main.py                          # 基础对话 Agent
├── task_planner_agent.py            # 任务规划执行 Agent（网页版）
├── self_reflect_agent.py            # 自我反思纠错 Agent（网页版）
├── self_reflect_terminal.py         # 自我反思纠错 Agent（终端版）
├── ultimate_all_in_one_agent.py     # 全能一体式终极 Agent（网页版）
├── ultimate_all_in_one_terminal.py  # 全能一体式终极 Agent（终端版）
├── multi-agent-team/
│   └── main.py                      # 多角色 Agent 团队（市场调研）
└── requirements.txt                 # 依赖列表
```

---

## 🎯 Agent 类型

| Agent | 功能 | 特点 |
|-------|------|------|
| 1️⃣ **基础对话 Agent** | 交互式问答 | 简单直接的对话功能 |
| 2️⃣ **任务规划 Agent** | 任务拆解执行 | 自动拆解复杂任务 |
| 3️⃣ **自我反思 Agent** | 自我检查修正 | 三层逻辑：回答→反思→优化 |
| 4️⃣ **全能终极 Agent** | 意图+工具+反思 | 完整的工作流 |
| 5️⃣ **多角色团队 Agent** | 协作分工 | 项目经理+研究员+分析师+文案 |

---

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 1. 基础对话 Agent
```bash
python3 main.py
```

### 2. 任务规划 Agent（网页版）
```bash
streamlit run task_planner_agent.py
```

### 3. 自我反思 Agent（终端版）
```bash
python3 self_reflect_terminal.py
```

### 4. 全能终极 Agent（终端版）
```bash
python3 ultimate_all_in_one_terminal.py
```

### 5. 多角色团队 Agent
```bash
cd multi-agent-team && python3 main.py
```

---

## 🏗️ 技术栈

| 技术 | 说明 |
|------|------|
| **LangGraph** | Agent 工作流编排 |
| **DeepSeek API** | LLM 调用 |
| **Streamlit** | 网页界面（可选） |
| **Python 3.9+** | 运行环境 |

---

## ✨ 核心能力

- ✅ **状态管理**：TypedDict 类型安全
- ✅ **条件分支**：动态路由逻辑
- ✅ **工具调用**：搜索、计算等
- ✅ **多Agent协作**：角色分工
- ✅ **自我反思**：自我纠错机制

---

## 📝 配置

复制 `.env.example` 为 `.env` 并填入：
```env
DEEPSEEK_API_KEY=你的API密钥
```

---

## 🌐 在线演示

- Streamlit 部署：[https://share.streamlit.io/...](https://share.streamlit.io/...)
- FastAPI 后端：[https://...](https://...)

---

## 📄 License

MIT License - 自由使用！

