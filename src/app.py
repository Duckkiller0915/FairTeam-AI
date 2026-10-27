import streamlit as st
import pandas as pd
from git_analyzer.analyzer import analyze_repo
from text_analyzer.analyzer import analyze_text
from fairness_engine.calculator import calculate_fairness
from llm_report.generator import generate_report

st.set_page_config(
    page_title="FairTeam AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚖️ FairTeam AI")
st.markdown("### 學生小組專題公平貢獻分析與衝突調解助手")
st.markdown("---")

with st.sidebar:
    st.header("資料輸入")
    repo_path = st.text_input(
        "GitHub Repo 路徑",
        placeholder="https://github.com/xxx/yyy.git 或本地路徑"
    )
    chat_file = st.file_uploader("上傳聊天/會議紀錄 (txt)", type=["txt"])
    members_input = st.text_area(
        "組員名單（每行一個）",
        height=150,
        placeholder="王小明\n陳小華\n林小美"
    )
    st.markdown("---")
    analyze_btn = st.button("開始分析", type="primary", use_container_width=True)

if analyze_btn:
    members = [m.strip() for m in members_input.splitlines() if m.strip()]

    if not members:
        st.error("請至少輸入一位組員名字")
    else:
        with st.spinner("正在分析中，請稍候..."):
            git_result = analyze_repo(repo_path) if repo_path else {"dataframe": pd.DataFrame(), "error": None}
            text_result = analyze_text(chat_file, members) if chat_file else {"dataframe": pd.DataFrame(), "error": None}
            
            if git_result.get("error"):
                st.warning(f"Git 分析警告：{git_result['error']}")
            
            fairness = calculate_fairness(git_result, text_result, members)
            report = generate_report(fairness)

        # 結果區
        st.success("分析完成！")
        
        col1, col2 = st.columns([2.2, 1])

        with col1:
            st.subheader("貢獻總覽")
            st.dataframe(
                fairness["summary"],
                use_container_width=True,
                hide_index=True
            )

        with col2:
            st.subheader("不公平指標")
            gini = fairness["gini"]
            st.metric("Gini 係數", gini)
            
            if gini < 0.2:
                st.success("相當公平")
            elif gini < 0.4:
                st.warning("輕微不均")
            else:
                st.error("明顯不公平")

        st.subheader("AI 分析報告與調解建議")
        st.markdown(report)

        st.download_button(
            label="下載報告 (Markdown)",
            data=report,
            file_name="FairTeam_Report.md",
            mime="text/markdown"
        )
else:
    st.info("請在左側欄位輸入 GitHub 路徑、上傳聊天紀錄，並填寫組員名單後點擊「開始分析」。")
    
    with st.expander("使用說明"):
        st.markdown("""
        1. **GitHub 路徑**：可填寫公開 Repo 網址或本地資料夾路徑  
        2. **聊天紀錄**：建議格式為 `姓名: 內容`，每行一則訊息  
        3. **組員名單**：每行填寫一位成員名字，需與 Git 作者名稱或聊天發言者對應  
        """)
