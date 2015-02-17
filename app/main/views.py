from flask import render_template, flash, redirect, url_for, request, g, current_app
from datetime import date
from . import main
from .forms import ContactForm
from ..email import send_email
import humanize

@main.route('/', methods=['GET'])
def index():

    years_working = humanize.apnumber(date.today().year - 2007)

    return render_template("index.html", years_working=years_working)

@main.route('/contact', methods=['GET','POST'])
def contact():

    form = ContactForm()

    if form.validate_on_submit():

        email = form.email.data        
        subject = form.subject.data        
        name = form.name.data        
        message = form.message.data        

        send_email(current_app.config['HEALY_ADMIN_EMAIL'], subject,'mail/contact', email=email, name=name, message=message)

        flash('Thank you for your enquiry. I will endeavour to respond to you as soon as possible.')
        return redirect(url_for('main.contact'))

    return render_template("contact.html", form=form)
