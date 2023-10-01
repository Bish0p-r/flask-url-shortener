from flask import render_template
from celery import Celery


def register_handlers(app):

    @app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        return render_template('404.html'), 404


def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)

    # add beat tasks if you have them here
    # celery.config_from_object(celery_config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery