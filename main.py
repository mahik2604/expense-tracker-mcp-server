import os
import sqlite3
import csv
import tempfile
from fastmcp import FastMCP

# Paths
DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

# Init MCP server
mcp = FastMCP("ExpenseTracker")

# Initialize DB
def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)

init_db()


# -------------------------
# CORE EXPENSE OPERATIONS
# -------------------------

@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    """Add a new expense entry to the database."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": cur.lastrowid}


@mcp.tool()
def list_expenses(start_date, end_date):
    """List expense entries within a date range."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


@mcp.tool()
def summarize(start_date, end_date, category=None):
    """Summarize expenses by category in a date range."""
    with sqlite3.connect(DB_PATH) as c:
        query = """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
        """
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


# -------------------------
# EDIT / DELETE
# -------------------------

@mcp.tool()
def edit_expense(id, date=None, amount=None, category=None, subcategory=None, note=None):
    """Edit an existing expense entry by ID."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("SELECT * FROM expenses WHERE id = ?", (id,))
        row = cur.fetchone()
        if not row:
            return {"status": "error", "message": "Expense not found"}

        date = date or row[1]
        amount = amount or row[2]
        category = category or row[3]
        subcategory = subcategory if subcategory is not None else row[4]
        note = note if note is not None else row[5]

        c.execute("""
            UPDATE expenses
            SET date = ?, amount = ?, category = ?, subcategory = ?, note = ?
            WHERE id = ?
        """, (date, amount, category, subcategory, note, id))

        return {"status": "ok", "message": "Expense updated"}


@mcp.tool()
def delete_expense(id):
    """Delete an expense entry by ID."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("DELETE FROM expenses WHERE id = ?", (id,))
        if cur.rowcount == 0:
            return {"status": "error", "message": "Expense not found"}
        return {"status": "ok", "message": "Expense deleted"}


# -------------------------
# CREDIT / BALANCE
# -------------------------

@mcp.tool()
def add_credit(date, amount, source="", note=""):
    """Add money received (credit) as a special category."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, "CREDIT", source, note)
        )
        return {"status": "ok", "id": cur.lastrowid}


@mcp.tool()
def total_money():
    """Compute total expenses, total credits, and net balance."""
    with sqlite3.connect(DB_PATH) as c:
        total_expense = c.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE category != 'CREDIT'"
        ).fetchone()[0]

        total_credit = c.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE category = 'CREDIT'"
        ).fetchone()[0]

        return {
            "total_expense": total_expense,
            "total_credit": total_credit,
            "net_balance": total_credit - total_expense
        }


# -------------------------
# DISCOVERY HELPERS
# -------------------------

@mcp.tool()
def list_all_expenses():
    """Return all expenses with IDs."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "SELECT id, date, amount, category, subcategory, note FROM expenses ORDER BY id ASC"
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


@mcp.tool()
def list_by_category(category):
    """List all expenses in a category."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE category = ?
            ORDER BY date ASC
            """,
            (category,)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


@mcp.tool()
def list_recent(n: int = 10):
    """Return the most recent N expenses."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            ORDER BY id DESC
            LIMIT ?
            """,
            (n,)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


@mcp.tool()
def search_expense(keyword):
    """Search expenses by keyword in category, subcategory, or note."""
    like = f"%{keyword}%"
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE category LIKE ? 
               OR subcategory LIKE ? 
               OR note LIKE ?
            ORDER BY date ASC
            """,
            (like, like, like)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


# -------------------------
# MONTHLY SUMMARY
# -------------------------

@mcp.tool()
def monthly_summary(year: int, month: int):
    """Summarize expenses for a specific month."""
    start = f"{year:04d}-{month:02d}-01"
    end_month = month + 1
    end_year = year

    if end_month == 13:
        end_month = 1
        end_year += 1

    end = f"{end_year:04d}-{end_month:02d}-01"

    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date >= ? AND date < ?
            GROUP BY category
            ORDER BY total_amount DESC
            """,
            (start, end)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


# -------------------------
# EXPORT CSV
# -------------------------

@mcp.tool()
def export_csv():
    """Export all expenses to a CSV file and return the file path."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("SELECT * FROM expenses ORDER BY date ASC")
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]

    temp_path = os.path.join(tempfile.gettempdir(), "expenses_export.csv")
    with open(temp_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(rows)

    return {"status": "ok", "path": temp_path}


# -------------------------
# RESOURCE: CATEGORIES
# -------------------------

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()


# -------------------------
# RUN SERVER
# -------------------------

if __name__ == "__main__":
    mcp.run()
