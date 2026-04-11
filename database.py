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

    # ── MIGRATIONS ───────────────────────────────
    # Safely add new columns to existing databases.
    # If the column already exists SQLite raises an error — we ignore it.
    # This means the fix works on BOTH fresh installs AND old deployed databases.
    migrations = [
        "ALTER TABLE score_history ADD COLUMN stress_score REAL DEFAULT 0",
        "ALTER TABLE score_history ADD COLUMN savings_rate REAL DEFAULT 0",
        "ALTER TABLE score_history ADD COLUMN survival_months REAL DEFAULT 0",
        "ALTER TABLE score_history ADD COLUMN expense_ratio REAL DEFAULT 0",
        "ALTER TABLE user_profiles ADD COLUMN age INTEGER DEFAULT 25",
        "ALTER TABLE user_profiles ADD COLUMN city TEXT DEFAULT ''",
        "ALTER TABLE lend_borrow ADD COLUMN due_date TEXT DEFAULT NULL",
        "ALTER TABLE lend_borrow ADD COLUMN settled_at TEXT DEFAULT NULL",
        "ALTER TABLE user_profiles ADD COLUMN email TEXT DEFAULT ''",
        "ALTER TABLE user_profiles ADD COLUMN total_xp INTEGER DEFAULT 0",
    ]
    for migration in migrations:
        try:
            conn.execute(migration)
            conn.commit()
        except Exception:
            pass  # Column already exists — safe to skip


    # ── USER AUTH ─────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_auth (
            username     TEXT PRIMARY KEY,
            email        TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at   TEXT DEFAULT (datetime('now','localtime')),
            last_login   TEXT DEFAULT NULL,
            is_verified  INTEGER DEFAULT 1
        )
    """)

    # ── XP LOG ────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS xp_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT NOT NULL,
            action     TEXT NOT NULL,
            xp_earned  INTEGER NOT NULL,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── DAILY STREAKS ─────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS streak_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT NOT NULL,
            log_date   TEXT NOT NULL,
            action     TEXT NOT NULL DEFAULT 'expense_tracked',
            UNIQUE(username, log_date, action)
        )
    """)

    # ── BADGES EARNED ─────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS badges_earned (
            username   TEXT NOT NULL,
            badge_name TEXT NOT NULL,
            earned_at  TEXT DEFAULT (datetime('now','localtime')),
            PRIMARY KEY (username, badge_name)
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


# ══════════════════════════════════════════════
# AUTH — EMAIL + PASSWORD LOGIN
# ══════════════════════════════════════════════
import hashlib
import secrets


def _hash_password(password: str, salt: str = "") -> str:
    """SHA-256 hash with salt. Not bcrypt but sufficient for this use case."""
    combined = password + salt + "finverse_salt_2025"
    return hashlib.sha256(combined.encode()).hexdigest()


def register_user(username: str, email: str, password: str) -> dict:
    """
    Register a new user with email + password.
    Returns {"success": True} or {"success": False, "error": "..."}
    """
    if len(password) < 6:
        return {"success": False, "error": "Password must be at least 6 characters."}
    if "@" not in email or "." not in email:
        return {"success": False, "error": "Enter a valid email address."}
    if len(username.strip()) < 2:
        return {"success": False, "error": "Username must be at least 2 characters."}

    conn = get_conn()
    # Check username taken
    if conn.execute("SELECT 1 FROM user_auth WHERE username=?", (username,)).fetchone():
        conn.close()
        return {"success": False, "error": "Username already taken. Choose another."}
    # Check email taken
    if conn.execute("SELECT 1 FROM user_auth WHERE email=?", (email.lower(),)).fetchone():
        conn.close()
        return {"success": False, "error": "Email already registered. Please sign in."}

    pw_hash = _hash_password(password)
    try:
        conn.execute(
            "INSERT INTO user_auth (username, email, password_hash) VALUES (?,?,?)",
            (username.strip(), email.lower().strip(), pw_hash)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}
    conn.close()

    # Create profile
    upsert_user_profile(username.strip(), username.strip())
    return {"success": True, "username": username.strip()}


def login_user(identifier: str, password: str) -> dict:
    """
    Login with email or username + password.
    Returns {"success": True, "username": ...} or {"success": False, "error": ...}
    """
    conn = get_conn()
    # Try by email first, then username
    row = conn.execute(
        "SELECT * FROM user_auth WHERE email=? OR username=?",
        (identifier.lower().strip(), identifier.strip())
    ).fetchone()
    conn.close()

    if not row:
        return {"success": False, "error": "No account found with that email or username."}

    pw_hash = _hash_password(password)
    if row["password_hash"] != pw_hash:
        return {"success": False, "error": "Incorrect password. Please try again."}

    # Update last_login
    conn = get_conn()
    conn.execute(
        "UPDATE user_auth SET last_login=datetime('now','localtime') WHERE username=?",
        (row["username"],)
    )
    conn.commit()
    conn.close()
    return {"success": True, "username": row["username"], "email": row["email"]}


def get_auth_by_username(username: str) -> dict:
    conn = get_conn()
    row = conn.execute("SELECT * FROM user_auth WHERE username=?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else {}


def change_password(username: str, old_password: str, new_password: str) -> dict:
    if len(new_password) < 6:
        return {"success": False, "error": "New password must be at least 6 characters."}
    conn = get_conn()
    row  = conn.execute("SELECT password_hash FROM user_auth WHERE username=?", (username,)).fetchone()
    conn.close()
    if not row:
        return {"success": False, "error": "User not found."}
    if row["password_hash"] != _hash_password(old_password):
        return {"success": False, "error": "Current password is incorrect."}
    conn = get_conn()
    conn.execute("UPDATE user_auth SET password_hash=? WHERE username=?",
                 (_hash_password(new_password), username))
    conn.commit()
    conn.close()
    return {"success": True}


def get_all_registered_users() -> list:
    """Admin — all registered accounts with metadata."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT a.username, a.email, a.created_at, a.last_login,
               COUNT(DISTINCT s.id) as score_count,
               MAX(s.score) as best_score
        FROM user_auth a
        LEFT JOIN score_history s ON s.username = a.username
        GROUP BY a.username
        ORDER BY a.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ══════════════════════════════════════════════
# GAMIFICATION — XP, BADGES, LEVELS
# ══════════════════════════════════════════════

XP_ACTIONS = {
    "score_calculated":      10,
    "expense_logged":         2,
    "expense_logged_7day":   15,   # bonus for 7-day streak
    "lend_added":             5,
    "lend_settled":          10,
    "challenge_completed":   25,
    "module_completed":      30,
    "post_published":         8,
    "post_upvoted":           3,
    "survey_answered":       10,
    "profile_completed":     20,
    "first_safe_score":      50,
    "first_emergency_fund":  75,
    "score_improved_5pts":   20,
    "streak_7days":          30,
    "streak_30days":         75,
    "streak_100days":       200,
}

LEVEL_THRESHOLDS = [
    (0,    "Starter",   "🌱"),
    (100,  "Bronze",    "🥉"),
    (300,  "Silver",    "🥈"),
    (600,  "Gold",      "🥇"),
    (1000, "Platinum",  "💎"),
    (2000, "Diamond",   "💠"),
    (5000, "Legend",    "🏆"),
]

ALL_BADGES = [
    # Score badges
    {"id": "first_score",     "name": "First Steps",        "desc": "Calculated your first safety score",    "xp": 10},
    {"id": "safe_zone",       "name": "Safe Zone",          "desc": "Achieved a SAFE rating",                "xp": 50},
    {"id": "score_80",        "name": "Finance Pro",        "desc": "Scored 80+ on safety score",            "xp": 75},
    {"id": "score_90",        "name": "Money Master",       "desc": "Scored 90+ on safety score",            "xp": 100},
    {"id": "consistent_safe", "name": "Consistently Safe",  "desc": "Maintained SAFE rating 5 times",        "xp": 80},
    # Savings badges
    {"id": "saver_10",        "name": "Saver Seedling",     "desc": "Savings rate above 10%",                "xp": 20},
    {"id": "saver_20",        "name": "Good Saver",         "desc": "Savings rate above 20%",                "xp": 40},
    {"id": "saver_30",        "name": "Super Saver",        "desc": "Savings rate above 30%",                "xp": 60},
    # Emergency fund
    {"id": "ef_3month",       "name": "Safety Net",         "desc": "3 months emergency fund",               "xp": 40},
    {"id": "ef_6month",       "name": "Emergency Ready",    "desc": "6 months emergency fund",               "xp": 80},
    {"id": "ef_12month",      "name": "Financial Fortress", "desc": "12 months emergency fund",              "xp": 150},
    # Streak badges
    {"id": "streak_3",        "name": "Habit Forming",      "desc": "3-day tracking streak",                 "xp": 15},
    {"id": "streak_7",        "name": "Week Warrior",       "desc": "7-day tracking streak",                 "xp": 30},
    {"id": "streak_30",       "name": "Monthly Champion",   "desc": "30-day tracking streak",                "xp": 75},
    # Learning badges
    {"id": "first_module",    "name": "Curious Mind",       "desc": "Completed first learning module",       "xp": 20},
    {"id": "all_beginner",    "name": "Finance Student",    "desc": "Completed all Beginner modules",        "xp": 60},
    {"id": "all_modules",     "name": "Finance Scholar",    "desc": "Completed all learning modules",        "xp": 150},
    # Community
    {"id": "first_post",      "name": "Voice of Community", "desc": "Published first community post",        "xp": 15},
    {"id": "helpful_10",      "name": "Helpful Member",     "desc": "Received 10 upvotes total",             "xp": 40},
    # Lend/Borrow
    {"id": "debt_free",       "name": "Debt Free",          "desc": "Settled all pending debts",             "xp": 50},
    # Special
    {"id": "profile_done",    "name": "Fully Onboarded",    "desc": "Completed your full profile",           "xp": 20},
    {"id": "week1",           "name": "One Week Old",       "desc": "Member for 7 days",                     "xp": 25},
    {"id": "month1",          "name": "One Month Strong",   "desc": "Member for 30 days",                    "xp": 50},
]


def log_xp(username: str, action: str, custom_xp: int = None) -> int:
    """Log an XP-earning action. Returns XP earned."""
    xp = custom_xp if custom_xp is not None else XP_ACTIONS.get(action, 0)
    if xp <= 0:
        return 0
    conn = get_conn()
    conn.execute(
        "INSERT INTO xp_log (username, action, xp_earned) VALUES (?,?,?)",
        (username, action, xp)
    )
    conn.commit()
    conn.close()
    return xp


def get_total_xp_db(username: str) -> int:
    """Get total XP from database (more accurate than session state)."""
    conn = get_conn()
    row  = conn.execute(
        "SELECT COALESCE(SUM(xp_earned),0) as total FROM xp_log WHERE username=?",
        (username,)
    ).fetchone()
    conn.close()
    return int(row["total"]) if row else 0


def get_level_from_xp(xp: int) -> dict:
    """Return level info based on total XP."""
    current = LEVEL_THRESHOLDS[0]
    for threshold, name, icon in LEVEL_THRESHOLDS:
        if xp >= threshold:
            current = (threshold, name, icon)
    # Next level
    idx = [t[0] for t in LEVEL_THRESHOLDS].index(current[0])
    if idx < len(LEVEL_THRESHOLDS) - 1:
        next_thresh = LEVEL_THRESHOLDS[idx + 1]
        xp_to_next  = next_thresh[0] - xp
        next_info   = {"name": next_thresh[1], "icon": next_thresh[2], "xp_needed": xp_to_next, "threshold": next_thresh[0]}
    else:
        next_info = None
    return {
        "name":       current[1],
        "icon":       current[2],
        "threshold":  current[0],
        "xp":         xp,
        "next":       next_info,
        "progress_pct": int((xp - current[0]) / (next_info["threshold"] - current[0]) * 100) if next_info else 100,
    }


def award_badge(username: str, badge_id: str) -> bool:
    """Award a badge if not already earned. Returns True if newly awarded."""
    conn = get_conn()
    existing = conn.execute(
        "SELECT 1 FROM badges_earned WHERE username=? AND badge_name=?",
        (username, badge_id)
    ).fetchone()
    if existing:
        conn.close()
        return False
    conn.execute(
        "INSERT INTO badges_earned (username, badge_name) VALUES (?,?)",
        (username, badge_id)
    )
    conn.commit()
    conn.close()
    # Log XP for badge
    badge = next((b for b in ALL_BADGES if b["id"] == badge_id), None)
    if badge:
        log_xp(username, f"badge_{badge_id}", badge["xp"])
    return True


def get_earned_badges(username: str) -> list:
    conn = get_conn()
    rows = conn.execute(
        "SELECT badge_name, earned_at FROM badges_earned WHERE username=? ORDER BY earned_at DESC",
        (username,)
    ).fetchall()
    conn.close()
    earned_ids = {r["badge_name"] for r in rows}
    earned_at  = {r["badge_name"]: r["earned_at"] for r in rows}
    return [
        {**b, "earned": b["id"] in earned_ids, "earned_at": earned_at.get(b["id"])}
        for b in ALL_BADGES
    ]


def check_and_award_score_badges(username: str, score: float, risk_level: str, result: dict, history: list):
    """Auto-check and award all score-related badges."""
    new_badges = []
    if award_badge(username, "first_score"):
        new_badges.append("first_score")
    if risk_level == "SAFE" and award_badge(username, "safe_zone"):
        new_badges.append("safe_zone")
    if score >= 80 and award_badge(username, "score_80"):
        new_badges.append("score_80")
    if score >= 90 and award_badge(username, "score_90"):
        new_badges.append("score_90")
    safe_count = sum(1 for h in history if h.get("risk_level") == "SAFE")
    if safe_count >= 5 and award_badge(username, "consistent_safe"):
        new_badges.append("consistent_safe")
    sr = result.get("savings_rate", 0)
    if sr >= 10 and award_badge(username, "saver_10"):
        new_badges.append("saver_10")
    if sr >= 20 and award_badge(username, "saver_20"):
        new_badges.append("saver_20")
    if sr >= 30 and award_badge(username, "saver_30"):
        new_badges.append("saver_30")
    sm = result.get("survival_months", 0)
    if sm >= 3  and award_badge(username, "ef_3month"):
        new_badges.append("ef_3month")
    if sm >= 6  and award_badge(username, "ef_6month"):
        new_badges.append("ef_6month")
    if sm >= 12 and award_badge(username, "ef_12month"):
        new_badges.append("ef_12month")
    # Score improved
    if len(history) >= 2 and (score - history[1].get("score", score)) >= 5:
        log_xp(username, "score_improved_5pts")
    log_xp(username, "score_calculated")
    return new_badges


def check_streak_badges(username: str, streak: int):
    new_badges = []
    if streak >= 3  and award_badge(username, "streak_3"):
        new_badges.append("streak_3")
    if streak >= 7:
        if award_badge(username, "streak_7"):
            new_badges.append("streak_7")
        log_xp(username, "streak_7days")
    if streak >= 30:
        if award_badge(username, "streak_30"):
            new_badges.append("streak_30")
        log_xp(username, "streak_30days")
    return new_badges


def get_xp_leaderboard(limit: int = 20) -> list:
    """Leaderboard ranked by total XP (engagement, not just score)."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT username, SUM(xp_earned) as total_xp, COUNT(*) as actions
        FROM xp_log
        GROUP BY username
        ORDER BY total_xp DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


