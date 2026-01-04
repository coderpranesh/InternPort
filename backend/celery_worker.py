from celery import Celery
from app import app, db
from models import Internship, Application, User, CompanyProfile
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

@celery.task
def send_deadline_reminders():
    with app.app_context():
        tomorrow = datetime.utcnow() + timedelta(days=1)
        internships = Internship.query.filter(
            Internship.last_date <= tomorrow,
            Internship.last_date > datetime.utcnow(),
            Internship.is_active == True
        ).all()
        
        for internship in internships:
            applications = Application.query.filter_by(
                internship_id=internship.id
            ).all()
            
            for application in applications:
                student = User.query.get(application.student_id)
                if student:
                    send_email(
                        student.email,
                        f"Deadline Reminder: {internship.title}",
                        f"The application deadline for {internship.title} is approaching."
                    )

@celery.task
def send_daily_summary():
    with app.app_context():
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        companies = CompanyProfile.query.all()
        for company in companies:
            new_applications = Application.query.join(
                Internship
            ).filter(
                Internship.company_id == company.id,
                Application.applied_at >= yesterday
            ).count()
            
            if new_applications > 0:
                user = User.query.get(company.user_id)
                if user:
                    send_email(
                        user.email,
                        "Daily Applications Summary",
                        f"You received {new_applications} new applications yesterday."
                    )

def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'noreply@internport.com'
        msg['To'] = to_email
        
        with smtplib.SMTP('localhost') as server:
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        3600.0,
        send_deadline_reminders.s(),
        name='send deadline reminders every hour'
    )
    
    sender.add_periodic_task(
        86400.0,
        send_daily_summary.s(),
        name='send daily summary'
    )