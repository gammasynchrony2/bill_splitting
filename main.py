from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request

app = Flask(__name__)

class HomePage(MethodView):
    def get(self):
        return render_template('index.html')

class BillFormPage(MethodView):
    def get(self):
        bill_form = BillForm()
        return render_template('bill_form_page.html', billform=bill_form)

class Bill:

    def __init__(self, amount, period):
        self.amount = amount
        self.period = period

class Flatmate:

    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house

    def pays(self, bill, flatmate2):
        weight = self.days_in_house / (self.days_in_house + flatmate2.days_in_house)
        to_pay = bill.amount * weight
        return to_pay

class ResultsPage(MethodView):

    def post(self):
        billform = BillForm(request.form)
        the_bill = Bill(
            amount=float(billform.amount.data),
            period=billform.period.data
        )
        flatmate_one = Flatmate(
            name=billform.name1.data,
            days_in_house=float(billform.days_in_house1.data)
        )
        flatmate_two = Flatmate(
            name=billform.name2.data,
            days_in_house=float(billform.days_in_house2.data)
        )
        return render_template(
            'results.html',
            name1=flatmate_one.name,
            amount1=round(flatmate_one.pays(the_bill, flatmate_two), 2),
            name2=flatmate_two.name,
            amount2=round(flatmate_two.pays(the_bill, flatmate_one), 2)
        )

class BillForm(Form):
    amount = StringField("Bill Amount: ", default="100")
    period = StringField("Bill Period: ")

    name1 = StringField("Name of Flatmate 1: ", default="Flatmate 1")
    days_in_house1 = StringField("Flatmate 1's days in house: ", default="20")

    name2 = StringField("Name of Flatmate 2: ", default="Flatmate 2")
    days_in_house2 = StringField("Flatmate 2's days in house: ", default="15")

    button = SubmitField("Calculate")


app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/bill', view_func=BillFormPage.as_view('bill_form_page'))
app.add_url_rule('/results', view_func=ResultsPage.as_view('results_page'))

app.run(debug=True)