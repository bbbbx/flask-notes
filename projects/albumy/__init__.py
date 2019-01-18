import os
import click
from flask import Flask, render_template
from albumy.extensions import db, bootstrap, login_manager, mail, moment, dropzone, csrf, avatars
from albumy.models import Role, User, Permission
from albumy.blueprints import auth, main, user, admin, ajax
from albumy.settings import config

def register_commands(app):
    @app.cli.command()
    def init():
        """初始化 Albumy。"""
        click.echo('Initializing the roles and permissions.')
        Role.init_role()
        click.echo('Done')
    
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--user', default=10, help='Quantity of users, default is 10.')
    def forge(user):
        """Generate fake data."""

        from albumy.fakes import fake_admin, fake_user

        db.drop_all()
        db.create_all()

        click.echo('Initializing the roles and permissions...')
        Role.init_role()
        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Generating %d users...' % user)
        fake_user(user)
        click.echo('Done.')


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    dropzone.init_app(app)
    csrf.init_app(app)
    avatars.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main.main_bp)
    app.register_blueprint(auth.auth_bp, url_prefix='/auth')
    app.register_blueprint(admin.admin_bp, url_prefix='/admin')
    app.register_blueprint(user.user_bp, url_prefix='/user')
    app.register_blueprint(ajax.ajax_bp, url_prefix='/ajax')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User)


def register_template_context(app):
    pass


def register_errorhandlers(app):
    pass


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('albumy')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errorhandlers(app)
    register_shell_context(app)
    register_template_context(app)

    return app