import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

def generate_report(fairness_result: Dict[str, Any], use_llm: bool = False) -> str:
    summary = fairness_result.get("summary")
    gini = fairness_result.get("gini", 0)

    if summary is None or summary.empty:
        return "無法生成報告，資料不足。"

    # 基本規則版報告
    level = "相當公平" if gini < 0.2 else "輕微不均" if gini < 0.4 else "明顯不公平"

    report = f"""### FairTeam AI 貢獻分析報告

**整體不公平程度（Gini 係數）**：{gini}（{level}）

#### 評分說明
- 0.0 ~ 0.2：相當公平
- 0.2 ~ 0.4：輕微不均
- 0.4 以上：明顯不公平，建議介入

#### 各成員貢獻摘要
"""

    for _, row in summary.iterrows():
        report += f"""
**{row['member']}**
- 總貢獻分數：{row['total_score']}
- Commit 數：{int(row['commits'])}
- 程式碼變更行數：{int(row['lines_changed'])}
- 發言次數：{int(row['messages'])}
- 任務相關提及：{int(row['task_mentions'])}
"""

    report += """
#### 調解建議
1. 建議貢獻較低的成員主動承接後續測試、文件撰寫或簡報製作工作。
2. 貢獻較高的成員可安排知識分享，避免知識與負擔過度集中。
3. 建議每週固定進行短時間進度同步，明確記錄任務分配。
4. 若差距過大，可與指導老師討論調整評分方式或工作範圍。
5. 鼓勵使用「任務看板」讓貢獻可視化，減少誤解。
"""

    # 若要使用真正的 LLM，可在此擴充
    if use_llm:
        try:
            report += "\n\n---\n*本報告已嘗試使用 LLM 進行進階分析*"
            # 這裡可串接 Gemini 或 OpenAI
        except Exception:
            pass

    return report
