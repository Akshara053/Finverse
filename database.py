# database.py
# ─────────────────────────────────────────────
# SQLite persistence layer for Finverse.
# Stores scores, daily expenses, and leaderboard.
# All data survives page refreshes and reruns.
# ─────────────────────────────────────────────

import sqlite3
import json
from datetime import date, datetime
from pathlib import Path

DB_PATH = "finverse_data.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they don't exist. Safe to call on every startup."""
    conn = get_conn()
    c = conn.cursor()

    # Score history — every time someone calculates
    c.execute("""
        CREATE TABLE IF NOT EXISTS score_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    NOT NULL DEFAULT 'anonymous',
            persona     TEXT    NOT NULL DEFAULT 'Working Professional',
            income      REAL    NOT NULL,
            expenses    REAL    NOT NULL,
            savings     REAL    NOT NULL,
            score       REAL    NOT NULL,
            risk_level  TEXT    NOT NULL,
            savings_rate REAL,
            survival_months REAL,
            expense_ratio REAL,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
        )
    """)

    # Daily expense log
    c.execute("""
        CREATE TABLE IF NOT EXISTS daily_expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    NOT NULL DEFAULT 'anonymous',
            category    TEXT    NOT NULL,
            amount      REAL    NOT NULL,
            note        TEXT    DEFAULT '',
            expense_date TEXT   NOT NULL DEFAULT (date('now','localtime')),
            created_at  TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
        )
    """)

    # Leaderboard (one row per username, upserted on new score)
    c.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            username    TEXT PRIMARY KEY,
            score       REAL NOT NULL,
            level_name  TEXT NOT NULL,
            persona     TEXT NOT NULL DEFAULT 'Working Professional',
            updated_at  TEXT NOT NULL DEFAULT (datetime('now','localtime'))
        )
    """)

    # Challenges completed
    c.execute("""
        CREATE TABLE IF NOT EXISTS challenges_done (
            username    TEXT NOT NULL,
            challenge_id TEXT NOT NULL,
            completed_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            PRIMARY KEY (username, challenge_id)
        )
    """)

    # Daily budget settings per user
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            username    TEXT PRIMARY KEY,
            daily_budget REAL NOT NULL DEFAULT 1000.0,
            streak       INTEGER NOT NULL DEFAULT 0,
            last_tracked TEXT DEFAULT NULL
        )
    """)

    conn.commit()
    conn.close()


# ── SCORE HISTORY ─────────────────────────────

def save_score(username, persona, income, expenses, savings, result):
    conn = get_conn()
    conn.execute("""
        INSERT INTO score_history
          (username, persona, income, expenses, savings, score,
           risk_level, savings_rate, survival_months, expense_ratio)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (
        username, persona, income, expenses, savings,
        result["composite_score"], result["risk_level"],
        result["savings_rate"], result["survival_months"], result["expense_ratio"],
    ))
    conn.commit()
    conn.close()


def get_score_history(username, limit=30):
    conn = get_conn()
    rows = conn.execute("""
        SELECT * FROM score_history
        WHERE username = ?
        ORDER BY created_at DESC LIMIT ?
    """, (username, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_scores_today():
    """For the global leaderboard — all scores calculated today."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT username, MAX(score) as score, risk_level, persona
        FROM score_history
        WHERE date(created_at) = date('now','localtime')
        GROUP BY username
        ORDER BY score DESC
        LIMIT 50
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── DAILY EXPENSES ────────────────────────────

def save_expense(username, category, amount, note):
    conn = get_conn()
    conn.execute("""
        INSERT INTO daily_expenses (username, category, amount, note)
        VALUES (?,?,?,?)
    """, (username, category, amount, note))
    conn.commit()
    conn.close()


def get_today_expenses(username):
    conn = get_conn()
    rows = conn.execute("""
        SELECT * FROM daily_expenses
        WHERE username = ? AND expense_date = date('now','localtime')
        ORDER BY created_at ASC
    """, (username,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_expense(expense_id):
    conn = get_conn()
    conn.execute("DELETE FROM daily_expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


def get_monthly_expenses(username):
    """Return this month's expenses grouped by category."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT category, SUM(amount) as total, COUNT(*) as count
        FROM daily_expenses
        WHERE username = ?
          AND strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now', 'localtime')
        GROUP BY category
        ORDER BY total DESC
    """, (username,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_spending_trend(username, days=7):
    """Return daily totals for the last N days."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT expense_date, SUM(amount) as total
        FROM daily_expenses
        WHERE username = ?
          AND expense_date >= date('now', ?, 'localtime')
        GROUP BY expense_date
        ORDER BY expense_date ASC
    """, (username, f"-{days} days")).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── LEADERBOARD ───────────────────────────────

def upsert_leaderboard(username, score, level_name, persona):
    conn = get_conn()
    conn.execute("""
        INSERT INTO leaderboard (username, score, level_name, persona, updated_at)
        VALUES (?,?,?,?, datetime('now','localtime'))
        ON CONFLICT(username) DO UPDATE SET
            score      = excluded.score,
            level_name = excluded.level_name,
            persona    = excluded.persona,
            updated_at = excluded.updated_at
        WHERE excluded.score >= leaderboard.score
    """, (username, score, level_name, persona))
    conn.commit()
    conn.close()


def get_leaderboard(limit=20):
    conn = get_conn()
    rows = conn.execute("""
        SELECT username, score, level_name, persona, updated_at
        FROM leaderboard
        ORDER BY score DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── CHALLENGES ────────────────────────────────

def save_challenge(username, challenge_id):
    conn = get_conn()
    conn.execute("""
        INSERT OR IGNORE INTO challenges_done (username, challenge_id)
        VALUES (?,?)
    """, (username, challenge_id))
    conn.commit()
    conn.close()


def get_completed_challenges(username):
    conn = get_conn()
    rows = conn.execute("""
        SELECT challenge_id FROM challenges_done WHERE username = ?
    """, (username,)).fetchall()
    conn.close()
    return {r["challenge_id"] for r in rows}


# ── USER SETTINGS ─────────────────────────────

def get_user_settings(username):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM user_settings WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    if row:
        return dict(row)
    # Defaults
    return {"username": username, "daily_budget": 1000.0, "streak": 0, "last_tracked": None}


def save_user_settings(username, daily_budget, streak, last_tracked=None):
    conn = get_conn()
    conn.execute("""
        INSERT INTO user_settings (username, daily_budget, streak, last_tracked)
        VALUES (?,?,?,?)
        ON CONFLICT(username) DO UPDATE SET
            daily_budget = excluded.daily_budget,
            streak       = excluded.streak,
            last_tracked = excluded.last_tracked
    """, (username, daily_budget, streak, last_tracked))
    conn.commit()
    conn.close()


def end_day_update_streak(username):
    """Call when user ends the day — increments streak if they tracked today."""
    settings = get_user_settings(username)
    today    = str(date.today())
    streak   = settings["streak"]
    if settings["last_tracked"] != today:
        streak += 1
    save_user_settings(username, settings["daily_budget"], streak, today)
    return streak
