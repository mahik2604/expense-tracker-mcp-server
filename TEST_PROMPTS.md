# ✅ Expense Tracker MCP — Test Prompts

Use these prompts inside **Claude Desktop** to fully test every MCP tool in the server.

---

## ✅ 1. Test Adding Expenses

**Prompt:**
- Add an expense for ₹250 on 2025-01-10 in the Food category, subcategory Lunch, note "Pizza with friends".

- Add a travel expense of ₹1200 on 2025-02-01, subcategory Uber, note "Airport ride".

- Record ₹80 spent on Tea on 2025-02-05.

- Add test transactions(expenses) to the expense tracker in month of november.

---

## ✅ 2. Test Listing Expenses (Date Range)

**Prompt:**

- Show all my expenses from 2025-01-01 to 2025-02-10.

- List expenses between 2025-02-01 and 2025-02-28.

---

## ✅ 3. Test Summaries

**Prompt:**

- Summarize my expenses by category between 2025-01-01 and 2025-03-01.

- Show my total food expenses from 2025-02-01 to 2025-02-10.

---

## ✅ 4. Test Listing All Expenses

**Prompt:**

- Show all expenses with their IDs.

---

## ✅ 5. Test Editing an Expense

### First find the ID, Then edit:

- Show all expenses.
- Edit expense with ID 3. Change the amount to 300 and update the note to "corrected amount".

### Or natural language:

- Update the last Uber expense to ₹1500.

Claude will auto-find ID → edit.

---

## ✅ 6. Test Deleting an Expense

**Prompt:**

- Delete the expense with ID 5.

### Or natural:

- Delete my last food expense.

- Claude will search → extract ID → delete.

---

## ✅ 7. Test Adding Credit (Income)

**Prompt:**

- Add credit of ₹50,000 on 2025-02-01 from Salary, note "Feb salary".

- Record ₹1500 credit received on 2025-02-10 from Freelancing.

---

## ✅ 8. Test Total Money / Balance

**Prompt:**

- Show my total expenses, total credits, and net balance.

---

## ✅ 9. List by Category

**Prompt:**

- Show all expenses in the Food category.

- List all Travel expenses.

---

## ✅ 10. Test Recent Expenses

**Prompt:**

- Show my last 5 expenses.

- List the most recent 15 expenses.

---

## ✅ 11. Test Search

**Prompt:**

- Find all expenses with the keyword "uber".

- Search for any expense related to pizza.

- Find my Amazon expenses.

---

## ✅ 12. Test Monthly Summary

**Prompt:**

- Give me a summary of my expenses for February 2025.

- Show category totals for January 2025.

---

## ✅ 13. Test Export CSV

**Prompt:**

- Export all my expenses to CSV.

Claude will return the file path.

---

## 🎉 Done!

This test script covers **all MCP tools** in your Expense Tracker server.