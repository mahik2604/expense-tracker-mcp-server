# Expense Tracker MCP Server

A lightweight **MCP (Model Context Protocol) server** built using **FastMCP + SQLite**, allowing you to manage expenses directly through **Claude Desktop** using natural language.

This project supports adding, editing, deleting, searching, summarizing, and exporting expenses — all triggered through Claude’s tool calls.

---

## 🚀 Features

- Add, list, edit, and delete expenses  
- Add credits (income tracking)  
- Category-based summaries  
- Monthly summaries  
- Search expenses by keyword  
- View recent expenses  
- Export expenses to CSV  
- SQLite-backed lightweight storage  
- Fully compatible with Claude Desktop MCP  

---

## 📦 Project Structure

expense-tracker-mcp-server/
│
├── main.py # MCP server implementation
├── categories.json # Expense categories
├── expenses.db # SQLite DB (ignored via .gitignore)
├── README.md
├── pyproject.toml
├── uv.lock
├── .gitignore
└── .venv/ # uv-managed virtual environment


---

## 🛠 Setup Instructions

### 1. Initialize the project (already done)
uv init .

### 2. Install FastMCP
uv add fastmcp

### 3. Activate virtual environment
.venv\Scripts\activate.bat

### 4. Verify installation
fastmcp version

---

## ▶ Running the Server in Dev Mode

Use `uv` to run FastMCP’s development server:

uv run fastmcp dev main.py

This starts the MCP server and watches for file changes.

---

## 🧩 Add MCP Server to Claude Desktop

Run:

uv run fastmcp install claude-desktop main.py

This auto-registers your server with Claude Desktop.  
Restart Claude Desktop to load the MCP tools.

---

## 🧪 Testing the MCP Tools (Examples)

Try these directly inside Claude Desktop:

Add an expense of ₹250 on 2025-01-10 in Food, note "Lunch".
Add a travel expense of ₹1200 on 2025-02-01 for Uber.
Edit the last Uber expense to ₹1200.
Delete my last food expense.
Show my expenses from 2025-01-01 to 2025-02-10.
Search for expenses with the keyword "pizza".
Show my February 2025 summary.
Export all my expenses to CSV.

---

## 🧰 Available Tools (API)

### Core Tools
- `add_expense`
- `list_expenses`
- `summarize`

### Edit / Delete
- `edit_expense`
- `delete_expense`

### Credits & Balance
- `add_credit`
- `total_money`

### Discovery Tools
- `list_all_expenses`
- `list_by_category`
- `list_recent`
- `search_expense`

### Analysis
- `monthly_summary`

### Export
- `export_csv`

### Resource
- `expense://categories`

---

## 📜 License

MIT License

---

## 🙌 Acknowledgements

Built using **FastMCP** and tested with **Claude Desktop MCP** integration.