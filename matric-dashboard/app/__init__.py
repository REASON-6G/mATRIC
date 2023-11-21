from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    # configuration
    app.config.from_object(config_class)

    #initialize extensions
    from app.extensions import db, login_manager, bootstrap, moment, migrate
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    migrate.init_app(app,db)
    
    from app import models
    with app.app_context():
        db.create_all()

    with app.app_context():
    
        # register blueprints
        from app.authentication import bp as authentication_bp
        app.register_blueprint(authentication_bp, url_prefix='/auth')
        from app.main import bp as bp_main
        app.register_blueprint(bp_main)
        from app.dashboard import bp as bp_dashboard
        app.register_blueprint(bp_dashboard)

        # process dash apps
        # dash app 1
        from app.dashboard.dashboard import add_dashboard
        app = add_dashboard(app)
        app.logger.info("Flask for MATRIC dashbaord launched.") 
        return app
