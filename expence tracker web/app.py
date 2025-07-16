from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(_name_)
CSV_FILE = 'expenses.csv'

# ✅ Home route - show all expenses
@app.route('/')
def index():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])

    total = df["Amount"].sum()
    return render_template("index.html", expenses=df.to_dict(orient="records"), total=total)

# ✅ Add expense route
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = float(request.form['amount'])
        note = request.form['note']

        new_row = pd.DataFrame([[date, category, amount, note]], columns=["Date", "Category", "Amount", "Note"])
        new_row.to_csv(CSV_FILE, mode='a', index=False, header=not os.path.exists(CSV_FILE))

        return redirect(url_for('index'))
    
    return render_template("add.html")

# ✅ Chart route
@app.route('/chart')
def chart():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        category_data = df.groupby("Category")["Amount"].sum()

        plt.figure(figsize=(6, 6))
        category_data.plot.pie(autopct="%1.1f%%", startangle=90)
        plt.title("Expense by Category")
        plt.ylabel("")
        plt.tight_layout()

        chart_path = os.path.join("static", "chart.png")
        plt.savefig(chart_path)
        plt.close()

        return render_template("chart.html", chart_url=chart_path)
    else:
        return "No data available to plot chart."

if _name_ == '_main_':
    app.run(debug=True)