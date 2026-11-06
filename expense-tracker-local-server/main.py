from fastmcp import FastMCP
import sqlite3
import os


mcp = FastMCP(name='expense-tracker')
DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                date DATE NOT NULL,
                description TEXT
            )
        """)

init_db()

@mcp.tool()
def add_expense(category:str, amount:float, date:str, description:str|None = None) -> str:
    """
    ADD AN EXPENSE TO DATABASE
    """
    if amount<0:
        raise ValueError("Amount cannot be negative")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expenses (category, amount, date, description) VALUES (?,?,?,?)",
                (category,amount,date,description)
            )
            conn.commit()
            return f"Expense of {amount} in category {category} on {date} added successfully, id:{cursor.lastrowid}"
    except sqlite3.Error as e:
        return f"Error adding expense: {e}"

@mcp.tool()
def get_expenses(category:str|None = None, date:str|None = None) -> str:
    """
    Get expenses from the database.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            query = "SELECT * FROM expenses WHERE 1=1"
            params = []
            if category:
                query += " AND category = ?"
                params.append(category)
            if date:
                query += " AND date = ?"
                params.append(date)
            cur.execute(query, params)
            rows = cur.fetchall()
            if not rows:
                return "No expenses found."
            result = "\n".join([f"{row[3]}: {row[1]} - {row[2]}" for row in rows])
            return f"Expenses:\n{result}"
    except sqlite3.Error as e:
        return f"Error getting expenses: {e}"


if __name__ == "__main__":
    mcp.run()
    