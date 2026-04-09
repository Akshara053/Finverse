# database.py  —  Finverse v6.0
# Complete SQLite persistence layer.
# One file handles ALL data for the app.

import sqlite3
from datetime import date, datetime

DB_PATH = "finverse_data.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")   # safe concurrent reads
    return conn


def init_db():
    """Create all tables. Safe to call on every startup — uses IF NOT EXISTS."""
    conn = get_conn()
    c = conn.cursor()

    # ── USER PROFILES ─────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            username        TEXT PRIMARY KEY,
            display_name    TEXT,
            persona         TEXT DEFAULT 'Working Professional',
            age             INTEGER DEFAULT 25,
            city            TEXT DEFAULT '',
            join_date       TEXT DEFAULT (date('now','localtime')),
            last_seen       TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── SCORE HISTORY ─────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS score_history (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            username        TEXT NOT NULL,
            persona         TEXT NOT NULL DEFAULT 'Working Professional',
            income          REAL NOT NULL,
            expenses        REAL NOT NULL,
            savings         REAL NOT NULL,
            score           REAL NOT NULL,
            risk_level      TEXT NOT NULL,
            savings_rate    REAL,
            survival_months REAL,
            expense_ratio   REAL,
            stress_score    REAL DEFAULT 0,
            created_at      TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── DAILY EXPENSES ────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS daily_expenses (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            username     TEXT NOT NULL,
            category     TEXT NOT NULL,
            amount       REAL NOT NULL,
            note         TEXT DEFAULT '',
            expense_date TEXT DEFAULT (date('now','localtime')),
            created_at   TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── LEND / BORROW ─────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS lend_borrow (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            username     TEXT NOT NULL,
            party_name   TEXT NOT NULL,
            amount       REAL NOT NULL,
            txn_type     TEXT NOT NULL CHECK(txn_type IN ('gave','owe')),
            description  TEXT DEFAULT '',
            status       TEXT DEFAULT 'pending' CHECK(status IN ('pending','settled')),
            due_date     TEXT DEFAULT NULL,
            created_at   TEXT DEFAULT (datetime('now','localtime')),
            settled_at   TEXT DEFAULT NULL
        )
    """)

    # ── COMMUNITY POSTS ───────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS community_posts (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            username     TEXT NOT NULL,
            display_name TEXT NOT NULL DEFAULT 'Anonymous',
            topic        TEXT NOT NULL,
            content      TEXT NOT NULL,
            is_anonymous INTEGER DEFAULT 0,
            upvotes      INTEGER DEFAULT 0,
            created_at   TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS post_upvotes (
            username TEXT NOT NULL,
            post_id  INTEGER NOT NULL,
            PRIMARY KEY (username, post_id)
        )
    """)

    # ── EDUCATION PROGRESS ────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS education_progress (
            username    TEXT NOT NULL,
            module_id   TEXT NOT NULL,
            completed   INTEGER DEFAULT 0,
            completed_at TEXT DEFAULT NULL,
            PRIMARY KEY (username, module_id)
        )
    """)

    # ── SURVEYS ───────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS survey_responses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT NOT NULL,
            question    TEXT NOT NULL,
            answer      TEXT NOT NULL,
            created_at  TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── LEADERBOARD ───────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            username   TEXT PRIMARY KEY,
            score      REAL NOT NULL,
            level_name TEXT NOT NULL,
            persona    TEXT NOT NULL DEFAULT 'Working Professional',
            updated_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── CHALLENGES ────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS challenges_done (
            username     TEXT NOT NULL,
            challenge_id TEXT NOT NULL,
            completed_at TEXT DEFAULT (datetime('now','localtime')),
            PRIMARY KEY (username, challenge_id)
        )
    """)

    # ── USER SETTINGS ─────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            username     TEXT PRIMARY KEY,
            daily_budget REAL DEFAULT 1000.0,
            streak       INTEGER DEFAULT 0,
            last_tracked TEXT DEFAULT NULL
        )
    """)

    conn.commit()
    conn.close()


# ══════════════════════════════════════════════
# USER PROFILES
# ══════════════════════════════════════════════

def upsert_user_profile(username, display_name=None, persona=None, age=None, city=None):
    conn = get_conn()
    existing = conn.execute(
        "SELECT * FROM user_profiles WHERE username=?", (username,)
    ).fetchone()
    if existing:
        conn.execute("""
            UPDATE user_profiles SET
                display_name = COALESCE(?, display_name),
                persona      = COALESCE(?, persona),
                age          = COALESCE(?, age),
                city         = COALESCE(?, city),
                last_seen    = datetime('now','localtime')
            WHERE username=?
        """, (display_name, persona, age, city, username))
    else:
        conn.execute("""
            INSERT INTO user_profiles (username, display_name, persona, age, city)
            VALUES (?,?,?,?,?)
        """, (username, display_name or username, persona or 'Working Professional',
              age or 25, city or ''))
    conn.commit()
    conn.close()


def get_user_profile(username):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM user_profiles WHERE username=?", (username,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_users():
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM user_profiles ORDER BY last_seen DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ══════════════════════════════════════════════
# SCORE HISTORY
# ══════════════════════════════════════════════

def save_score(username, persona, income, expenses, savings, result, stress_score=0):
    conn = get_conn()
    conn.execute("""
        INSERT INTO score_history
          (username, persona, income, expenses, savings, score,
           risk_level, savings_rate, survival_months, expense_ratio, stress_score)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (
        username, persona, income, expenses, savings,
        result["composite_score"], result["risk_level"],
        result["savings_rate"], result["survival_months"],
        result["expense_ratio"], stress_score,
    ))
    conn.commit()
    conn.close()


def get_score_history(username, limit=30):
    conn = get_conn()
    rows = conn.execute("""
        SELECT * FROM score_history WHERE username=?
        ORDER BY created_at DESC LIMIT ?
    """, (username, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_score_history():
    """Aggregate data for admin insights and surveys."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT username, persona, income, expenses, savings,
               score, risk_level, savings_rate, survival_months, expense_ratio, created_at
        FROM score_history ORDER BY created_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_platform_stats():
    """High-level platform stats."""
    conn = get_conn()
    stats = {}
    stats["total_users"]   = conn.execute("SELECT COUNT(DISTINCT username) FROM score_history").fetchone()[0]
    stats["total_scores"]  = conn.execute("SELECT COUNT(*) FROM score_history").fetchone()[0]
    stats["avg_score"]     = conn.execute("SELECT AVG(score) FROM score_history").fetchone()[0] or 0
    stats["safe_count"]    = conn.execute("SELECT COUNT(*) FROM score_history WHERE risk_level='SAFE'").fetchone()[0]
    stats["risky_count"]   = conn.execute("SELECT COUNT(*) FROM score_history WHERE risk_level='RISKY'").fetchone()[0]
    stats["total_expenses"]= conn.execute("SELECT COUNT(*) FROM daily_expenses").fetchone()[0]
    stats["total_posts"]   = conn.execute("SELECT COUNT(*) FROM community_posts").fetchone()[0]
    conn.close()
    return stats


# ══════════════════════════════════════════════
# DAILY EXPENSES
# ══════════════════════════════════════════════

def save_expense(username, category, amount, note, expense_date=None):
    conn = get_conn()
    if expense_date:
        conn.execute("""
            INSERT INTO daily_expenses (username, category, amount, note, expense_date)
            VALUES (?,?,?,?,?)
        """, (username, category, amount, note, expense_date))
    else:
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
        WHERE username=? AND expense_date=date('now','localtime')
        ORDER BY created_at ASC
    """, (username,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_expense(expense_id):
    conn = get_conn()
    conn.execute("DELETE FROM daily_expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()


def get_monthly_expenses(username):
    conn = get_conn()
    rows = conn.execute("""
        SELECT category, SUM(amount) as total, COUNT(*) as count
        FROM daily_expenses
        WHERE username=?
          AND strftime('%Y-%m', expense_date)=strftime('%Y-%m','now','localtime')
        GROUP BY category ORDER BY total DESC
    """, (username,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_spending_trend(username, days=30):
    conn = get_conn()
    rows = conn.execute("""
        SELECT expense_date, SUM(amount) as total
        FROM daily_expenses
        WHERE username=? AND expense_date >= date('now', ?, 'localtime')
        GROUP BY expense_date ORDER BY expense_date ASC
    """, (username, f"-{days} days")).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_category_trend(username, months=3):
    conn = get_conn()
    rows = conn.execute("""
        SELECT strftime('%Y-%m', expense_date) as month,
               category, SUM(amount) as total
        FROM daily_expenses
        WHERE username=?
          AND expense_date >= date('now', ?, 'localtime')
        GROUP BY month, category ORDER BY month ASC
    """, (username, f"-{months*30} days")).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ══════════════════════════════════════════════
# LEND / BORROW
# ══════════════════════════════════════════════

def add_lend_borrow(username, party_name, amount, txn_type, description="", due_date=None):
    conn = get_conn()
    conn.execute("""
        INSERT INTO lend_borrow (username, party_name, amount, txn_type, description, due_date)
        VALUES (?,?,?,?,?,?)
    """, (username, party_name, amount, txn_type, description, due_date))
    conn.commit()
    conn.close()


def get_lend_borrow(username, status=None):
    conn = get_conn()
    if status:
        rows = conn.execute("""
            SELECT * FROM lend_borrow WHERE username=? AND status=?
            ORDER BY created_at DESC
        """, (username, status)).fetchall()
    else:
        rows = conn.execute("""
            SELECT * FROM lend_borrow WHERE username=?
            ORDER BY created_at DESC
        """, (username,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def settle_lend_borrow(txn_id):
    conn = get_conn()
    conn.execute("""
        UPDATE lend_borrow SET status='settled',
        settled_at=datetime('now','localtime') WHERE id=?
    """, (txn_id,))
    conn.commit()
    conn.close()


def delete_lend_borrow(txn_id):
    conn = get_conn()
    conn.execute("DELETE FROM lend_borrow WHERE id=?", (txn_id,))
    conn.commit()
    conn.close()


def get_lend_borrow_summary(username):
    conn = get_conn()
    gave = conn.execute("""
        SELECT COALESCE(SUM(amount),0) FROM lend_borrow
        WHERE username=? AND txn_type='gave' AND status='pending'
    """, (username,)).fetchone()[0]
    owe = conn.execute("""
        SELECT COALESCE(SUM(amount),0) FROM lend_borrow
        WHERE username=? AND txn_type='owe' AND status='pending'
    """, (username,)).fetchone()[0]
    conn.close()
    return {"total_gave": gave, "total_owe": owe, "net": gave - owe}


# ══════════════════════════════════════════════
# COMMUNITY
# ══════════════════════════════════════════════

def add_post(username, display_name, topic, content, is_anonymous=False):
    conn = get_conn()
    shown_name = "Anonymous" if is_anonymous else display_name
    conn.execute("""
        INSERT INTO community_posts (username, display_name, topic, content, is_anonymous)
        VALUES (?,?,?,?,?)
    """, (username, shown_name, topic, content, int(is_anonymous)))
    conn.commit()
    conn.close()


def get_posts(topic=None, limit=30):
    conn = get_conn()
    if topic and topic != "All":
        rows = conn.execute("""
            SELECT * FROM community_posts WHERE topic=?
            ORDER BY created_at DESC LIMIT ?
        """, (topic, limit)).fetchall()
    else:
        rows = conn.execute("""
            SELECT * FROM community_posts
            ORDER BY created_at DESC LIMIT ?
        """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def upvote_post(username, post_id):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO post_upvotes (username, post_id) VALUES (?,?)",
            (username, post_id)
        )
        conn.execute(
            "UPDATE community_posts SET upvotes=upvotes+1 WHERE id=?",
            (post_id,)
        )
        conn.commit()
    except Exception:
        pass  # already upvoted
    conn.close()


def delete_post(post_id, username):
    conn = get_conn()
    conn.execute(
        "DELETE FROM community_posts WHERE id=? AND username=?",
        (post_id, username)
    )
    conn.commit()
    conn.close()


# ══════════════════════════════════════════════
# EDUCATION
# ══════════════════════════════════════════════

def mark_module_complete(username, module_id):
    conn = get_conn()
    conn.execute("""
        INSERT INTO education_progress (username, module_id, completed, completed_at)
        VALUES (?,?,1,datetime('now','localtime'))
        ON CONFLICT(username, module_id) DO UPDATE SET
            completed=1, completed_at=datetime('now','localtime')
    """, (username, module_id))
    conn.commit()
    conn.close()


def get_education_progress(username):
    conn = get_conn()
    rows = conn.execute(
        "SELECT module_id, completed FROM education_progress WHERE username=?",
        (username,)
    ).fetchall()
    conn.close()
    return {r["module_id"]: r["completed"] for r in rows}


# ══════════════════════════════════════════════
# SURVEYS
# ══════════════════════════════════════════════

def save_survey_response(username, question, answer):
    conn = get_conn()
    conn.execute("""
        INSERT INTO survey_responses (username, question, answer)
        VALUES (?,?,?)
    """, (username, question, answer))
    conn.commit()
    conn.close()


def get_survey_responses(question=None):
    conn = get_conn()
    if question:
        rows = conn.execute(
            "SELECT * FROM survey_responses WHERE question=?", (question,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM survey_responses").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def has_answered_survey(username, question):
    conn = get_conn()
    row = conn.execute(
        "SELECT id FROM survey_responses WHERE username=? AND question=?",
        (username, question)
    ).fetchone()
    conn.close()
    return row is not None


# ══════════════════════════════════════════════
# LEADERBOARD
# ══════════════════════════════════════════════

def upsert_leaderboard(username, score, level_name, persona):
    conn = get_conn()
    conn.execute("""
        INSERT INTO leaderboard (username, score, level_name, persona, updated_at)
        VALUES (?,?,?,?,datetime('now','localtime'))
        ON CONFLICT(username) DO UPDATE SET
            score      = CASE WHEN excluded.score >= leaderboard.score THEN excluded.score ELSE leaderboard.score END,
            level_name = excluded.level_name,
            persona    = excluded.persona,
            updated_at = excluded.updated_at
    """, (username, score, level_name, persona))
    conn.commit()
    conn.close()


def get_leaderboard(limit=25):
    conn = get_conn()
    rows = conn.execute("""
        SELECT username, score, level_name, persona, updated_at
        FROM leaderboard ORDER BY score DESC LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ══════════════════════════════════════════════
# CHALLENGES
# ══════════════════════════════════════════════

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
    rows = conn.execute(
        "SELECT challenge_id FROM challenges_done WHERE username=?", (username,)
    ).fetchall()
    conn.close()
    return {r["challenge_id"] for r in rows}


# ══════════════════════════════════════════════
# USER SETTINGS
# ══════════════════════════════════════════════

def get_user_settings(username):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM user_settings WHERE username=?", (username,)
    ).fetchone()
    conn.close()
    return dict(row) if row else {"username": username, "daily_budget": 1000.0, "streak": 0, "last_tracked": None}


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
    settings = get_user_settings(username)
    today    = str(date.today())
    streak   = settings["streak"]
    if settings["last_tracked"] != today:
        streak += 1
    save_user_settings(username, settings["daily_budget"], streak, today)
    return streak
