from pydriller import Repository
from collections import defaultdict
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, Any

def analyze_repo(repo_path: str, since: Optional[datetime] = None, to: Optional[datetime] = None) -> Dict[str, Any]:
    """
    分析 Git Repository 的貢獻情況
    """
    if not repo_path:
        return {"error": "未提供 Repo 路徑", "dataframe": pd.DataFrame(), "raw": {}}

    author_stats = defaultdict(lambda: {
        "commits": 0,
        "insertions": 0,
        "deletions": 0,
        "files": set(),
        "first_commit": None,
        "last_commit": None
    })

    try:
        repo = Repository(repo_path, since=since, to=to)
        for commit in repo.traverse_commits():
            author = commit.author.name or commit.author.email or "Unknown"
            stats = author_stats[author]

            stats["commits"] += 1
            stats["insertions"] += commit.insertions or 0
            stats["deletions"] += commit.deletions or 0

            for f in commit.modified_files:
                if f.filename:
                    stats["files"].add(f.filename)

            commit_date = commit.author_date
            if stats["first_commit"] is None or commit_date < stats["first_commit"]:
                stats["first_commit"] = commit_date
            if stats["last_commit"] is None or commit_date > stats["last_commit"]:
                stats["last_commit"] = commit_date

    except Exception as e:
        return {"error": str(e), "dataframe": pd.DataFrame(), "raw": {}}

    records = []
    for author, stats in author_stats.items():
        records.append({
            "author": author,
            "commits": stats["commits"],
            "insertions": stats["insertions"],
            "deletions": stats["deletions"],
            "lines_changed": stats["insertions"] + stats["deletions"],
            "files_touched": len(stats["files"]),
            "first_commit": stats["first_commit"],
            "last_commit": stats["last_commit"]
        })

    df = pd.DataFrame(records)
    if not df.empty:
        df = df.sort_values("lines_changed", ascending=False).reset_index(drop=True)

    return {
        "dataframe": df,
        "raw": {k: {**v, "files": list(v["files"])} for k, v in author_stats.items()},
        "error": None
    }
