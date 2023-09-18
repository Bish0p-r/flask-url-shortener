from flask import render_template


def register_handlers(app):

    @app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        return render_template('404.html'), 404
