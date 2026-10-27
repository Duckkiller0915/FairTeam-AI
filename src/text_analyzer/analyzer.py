from collections import defaultdict
import pandas as pd
from typing import Optional, List, Dict, Any

def analyze_text(file, members: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    分析聊天或會議紀錄
    支援格式：姓名: 內容
    """
    if file is None:
        return {"dataframe": pd.DataFrame(), "raw": {}, "error": None}

    try:
        content = file.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return {"dataframe": pd.DataFrame(), "raw": {}, "error": str(e)}

    lines = content.splitlines()
    speaker_stats = defaultdict(lambda: {
        "messages": 0,
        "words": 0,
        "task_mentions": 0
    })

    task_keywords = [
        "我做", "我完成", "我負責", "已完成", "做完", "提交", "push",
        "實作", "寫好", "修好", "解決", "完成了", "弄好", "搞定"
    ]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if ":" in line:
            parts = line.split(":", 1)
            speaker = parts[0].strip()
            text = parts[1].strip()
        else:
            speaker = "Unknown"
            text = line

        stats = speaker_stats[speaker]
        stats["messages"] += 1
        stats["words"] += len(text)

        for kw in task_keywords:
            if kw in text:
                stats["task_mentions"] += 1
                break

    records = []
    for speaker, stats in speaker_stats.items():
        records.append({
            "speaker": speaker,
            "messages": stats["messages"],
            "words": stats["words"],
            "task_mentions": stats["task_mentions"]
        })

    df = pd.DataFrame(records)
    if not df.empty:
        df = df.sort_values("messages", ascending=False).reset_index(drop=True)

    return {
        "dataframe": df,
        "raw": dict(speaker_stats),
        "error": None
    }
