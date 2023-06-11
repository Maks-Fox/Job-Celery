from celery import Celery

from src.entrypoints.container import AppContainer


def create_app() -> Celery:
    container = AppContainer()
    config = container.config()

    app = Celery(config['celery_name'])
    app.conf.broker_url = config['broker_url']
    app.conf.result_backend = config['result_backend']

    app.register_task(container.task())
    # app.register_task(container.link_parse_task())
    # app.register_task(container.description_parse_task())
    # app.register_task(container.key_word_generation_task())
    return app


application = create_app()
