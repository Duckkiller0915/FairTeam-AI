# FairTeam AI
學生小組專題公平貢獻分析與衝突調解助手

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 專案簡介
FairTeam AI 是一套專為學生小組專題設計的智慧工具。  
透過分析 GitHub 貢獻紀錄與聊天/會議文字，自動計算每位成員的實際貢獻，並生成可解釋的公平報告與調解建議。

## 解決痛點
- 組員貢獻難以客觀量化
- 聊天活躍 ≠ 實際做事
- 衝突發生時缺少客觀依據
- 老師評分時資訊不足

## 主要功能
- GitHub Repo 深度分析（commit、程式碼行數、檔案類型、時間分佈）
- 聊天/會議紀錄分析（發言量、任務提及）
- 多維度貢獻分數計算 + Gini 不公平係數
- AI 生成個人貢獻摘要與具體調解建議
- 支援匯出 Markdown 報告

## 快速開始

### 1. 安裝
```bash
git clone https://github.com/Duckkiller0915/FairTeam-AI.git
cd FairTeam-AI
python -m venv venv
source venv/bin/activate  # Windows 請用 venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 啟動
```bash
streamlit run src/app.py
```

## 系統架構
```
輸入 → Git 分析 + 文字分析 → 公平計算引擎 → LLM 報告生成 → 視覺化呈現
```

## 技術棧
- Frontend: Streamlit
- Git Analysis: PyDriller, GitPython
- Data Processing: Pandas, NumPy
- Visualization: Plotly
- LLM: Google Gemini / OpenAI（可選）

## 專案結構
```
FairTeam-AI/
├── src/
│   ├── git_analyzer/
│   ├── text_analyzer/
│   ├── fairness_engine/
│   ├── llm_report/
│   └── app.py
├── docs/
├── data/
├── notebooks/
├── demo/
├── requirements.txt
└── LICENSE
```

## 開發團隊
- 隊員A：專案規劃、前端、報告生成
- 隊員B：Git 分析、公平計算引擎
- 隊員C：文字分析、文件撰寫

## 授權
MIT License
