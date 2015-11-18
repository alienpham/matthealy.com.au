from flask import render_template, flash, redirect, url_for, request, g, current_app
from . import main
from .forms import ContactForm
from ..email import send_email

@main.route('/', methods=['GET','POST'])
def index():
    form = ContactForm()
    return render_template("index.html", form=form)

@main.route('/submit_contact', methods=['GET','POST'])
def submit_contact():

    form = ContactForm()

    if form.validate_on_submit():

        name = form.name.data        
        phone = form.phone.data
        email = form.email.data        
        message = form.message.data        

        send_email(current_app.config['HEALY_ADMIN_EMAIL'], 'Website Enquiry','mail/contact', phone=phone, email=email, name=name, message=message)

        return '', 200

    else:
        return redirect(url_for('main.index'))

@main.route('/terms', methods=['GET'])
def terms():
    return render_template("terms.html")
