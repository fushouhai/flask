from flask import current_app 

def jsonable():
#    config_now = current_app.config #    pay attentin to this point! pointing to the same object!!!
    config_now = current_app.config.copy()
    config_now.pop('PERMANENT_SESSION_LIFETIME')
    return config_now
    