from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'nitu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_desc = db.Column(db.String(800),  nullable=False)
    cost = db.Column(db.Integer,  nullable=False)
    date_exp = db.Column(db.String(10),  nullable=False)
    tag = db.Column(db.String(20),  nullable=False)

   

@app.route('/')
def home():
    return render_template ('index.html')

@app.route('/all')
def all():
     all_expenses = Expense.query.all()
  
     return render_template ('all.html', all_expenses=all_expenses)


@app.route('/add', methods=['GET','POST'])
def add_expenses():
    if request.method=='POST':
        expense_desc = request.form['expense_desc']
        cost = request.form['cost']
        date_exp = request.form['date_exp']
        tag = request.form['tag']
        expense = Expense(expense_desc=expense_desc, cost=cost, date_exp=date_exp, tag=tag)
        db.session.add(expense)
        db.session.commit()
        return redirect ('/report')
        
    all_expenses = Expense.query.all()
  
    return render_template ('adding.html', all_expenses=all_expenses)


@app.route('/report', methods=['GET','POST'])
def report_expenses():
    if request.method == 'POST':
        tags = request.form['tags']
        all_expenses = Expense.query.filter(Expense.tag.endswith(str(tags))).all()
        print(all_expenses)
        return render_template('report.html', all_expenses=all_expenses)
   

    all_expenses = Expense.query.all() 
    return render_template ('report.html' , all_expenses=all_expenses)



@app.route('/update/<int:sno>', methods=['GET','POST'])
def update_expenses(sno):
    if request.method=='POST':
        expense_desc = request.form['expense_desc']
        cost = request.form['cost']
        date_exp = request.form['date_exp']
        tag = request.form['tag']
        expense = Expense.query.filter_by(id=sno).first()
        expense = Expense(expense_desc=expense_desc, cost=cost, date_exp=date_exp, tag=tag)
        db.session.add(expense)
        db.session.commit()

        return redirect ('/report')
    
    expense = Expense.query.filter_by(id=sno).first()
    return render_template ('update.html', expense=expense)


@app.route('/delete/<int:sno>', methods=['GET','POST'])
def delete_expenses(sno):
     expense = Expense.query.filter_by(id=sno).first()
     db.session.delete(expense)
     db.session.commit()
     return redirect ('/report')

    
     expense = Expense.query.filter_by(id=sno).first()
     return render_template ('all.html')


if __name__=='__main__':
    app.run(debug= True )