import pandas as pd
import numpy as np
from typing import Dict, Any, List

def gini_coefficient(values: List[float]) -> float:
    values = np.array(values, dtype=float)
    if len(values) == 0 or np.all(values == 0):
        return 0.0
    values = np.sort(values)
    n = len(values)
    index = np.arange(1, n + 1)
    return float((2 * np.sum(index * values) - (n + 1) * np.sum(values)) / (n * np.sum(values)))

def min_max_normalize(series: pd.Series) -> pd.Series:
    if series.max() == series.min():
        return pd.Series([1.0] * len(series), index=series.index)
    return (series - series.min()) / (series.max() - series.min())

def calculate_fairness(git_result: Dict, text_result: Dict, members: List[str]) -> Dict[str, Any]:
    git_df = git_result.get("dataframe", pd.DataFrame()) if git_result else pd.DataFrame()
    text_df = text_result.get("dataframe", pd.DataFrame()) if text_result else pd.DataFrame()

    results = []

    for member in members:
        member = member.strip()
        if not member:
            continue

        # Git 資料
        if not git_df.empty:
            mask = git_df["author"].str.contains(member, case=False, na=False)
            git_row = git_df[mask]
            commits = int(git_row["commits"].sum()) if not git_row.empty else 0
            lines = int(git_row["lines_changed"].sum()) if not git_row.empty else 0
            files = int(git_row["files_touched"].sum()) if not git_row.empty else 0
        else:
            commits = lines = files = 0

        # 文字資料
        if not text_df.empty:
            mask = text_df["speaker"].str.contains(member, case=False, na=False)
            text_row = text_df[mask]
            messages = int(text_row["messages"].sum()) if not text_row.empty else 0
            task_mentions = int(text_row["task_mentions"].sum()) if not text_row.empty else 0
        else:
            messages = task_mentions = 0

        results.append({
            "member": member,
            "commits": commits,
            "lines_changed": lines,
            "files_touched": files,
            "messages": messages,
            "task_mentions": task_mentions
        })

    df = pd.DataFrame(results)
    if df.empty:
        return {"summary": df, "gini": 0.0, "details": []}

    # 正規化
    df["code_norm"] = min_max_normalize(df["lines_changed"])
    df["commit_norm"] = min_max_normalize(df["commits"])
    df["comm_norm"] = min_max_normalize(df["messages"])
    df["task_norm"] = min_max_normalize(df["task_mentions"])

    # 權重設定
    W_CODE = 0.45
    W_COMMIT = 0.15
    W_COMM = 0.25
    W_TASK = 0.15

    df["total_score"] = (
        df["code_norm"] * W_CODE +
        df["commit_norm"] * W_COMMIT +
        df["comm_norm"] * W_COMM +
        df["task_norm"] * W_TASK
    ) * 100

    df["total_score"] = df["total_score"].round(1)

    gini = gini_coefficient(df["total_score"].tolist())

    summary = df[["member", "commits", "lines_changed", "messages", "task_mentions", "total_score"]].copy()
    summary = summary.sort_values("total_score", ascending=False).reset_index(drop=True)

    return {
        "summary": summary,
        "gini": round(gini, 3),
        "details": df.to_dict(orient="records")
    }
