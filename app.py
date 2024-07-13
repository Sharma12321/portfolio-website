from flask import Flask, render_template, send_file, request, flash, redirect, url_for
import json
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Load data from JSON
with open('data.json', 'r') as f:
    data = json.load(f)

personal_info = data['personal_info']
skills = data['skills']
education = data['education']
projects = data['projects']

@app.route('/')
def home():
    return render_template('index.html', personal_info=personal_info, skills=skills, education=education, projects=projects)

@app.route('/download_resume')
def download_resume():
    return send_file('static/files/resume.pdf', as_attachment=True)

@app.route('/download_certificate/<certificate_name>')
def download_certificate(certificate_name):
    return send_file(f'static/files/{certificate_name}.pdf', as_attachment=True)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Send email (configure with your own SMTP settings)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"

    msg = MIMEText(f"From: {name}\nEmail: {email}\n\n{message}")
    msg['Subject'] = f"New contact from {name}"
    msg['From'] = sender_email
    msg['To'] = sender_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, sender_email, msg.as_string())
        flash('Message sent successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

