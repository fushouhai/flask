from celery import Celery
from flask import current_app, render_template
from flask_mail import Message, Mail



#def send_async_email(app, msg):
#    with app.app_context():
#        mail.send(msg)


celery = Celery('__name__', broker='redis://localhost', backend='redis://localhost')
celery.conf.update(
    result_expires = 3600,
    task_serrializer = 'pickle'
    )
    
    
@celery.task(bind=True)
def send_email(self, to, subject, template, **kwargs):
    
    app = current_app._get_current_object()
    mail = Mail()
    mail.init_app(app)
    
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    
    mail.send(msg)
#    thr = Thread(target=send_async_email, args=[app, msg])
#    thr.start()
#    return thr
    
#    with app.app_context():
#        mail.send(msg)
    
    
