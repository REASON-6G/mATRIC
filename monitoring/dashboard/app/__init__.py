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
        from app.profile import bp as bp_profile
        app.register_blueprint(bp_profile)
        from app.manage_users import bp as bp_manageusers
        app.register_blueprint(bp_manageusers)
        from app.settings import bp as bp_settings
        app.register_blueprint(bp_settings)


        app.logger.info("Flask for MATRIC dashboard launched.")
        
        return app
