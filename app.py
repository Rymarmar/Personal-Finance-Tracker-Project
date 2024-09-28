'''
Main Flask app
Web-App portion of Project
'''

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from data_entry import get_date, get_amount, get_category, get_description
from main import CSV

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods = ['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        date = request.form['date']
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form.get('description', '')
        
        CSV.add_entry(date, amount, category, description)
        return redirect(url_for('index'))
    
    return render_template('add_transaction.html')

@app.route('/view')
def view_transactions():
    df = pd.read_csv(CSV.CSV_FILE)
    return render_template('view_transactions.html', tables = [df.to_html()], titles = df.columns.values)
                           
if __name__ == "__main__":
    app.run(debug = True)