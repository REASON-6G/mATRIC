from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate



#all the extensions are initiated in __init__.py create_app function

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager() #used by flask_login
login_manager.login_view = 'authentication.login'
login_manager.login_message = 'Please log in to access this page.'
bootstrap = Bootstrap5()
moment = Moment()
#currently not using csrf in case there is conflict with Dash, will test later
#csrf = CSRFProtect()