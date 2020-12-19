import os

from flask.cli import FlaskGroup

from src import app, db

cli = FlaskGroup(app)


def full_load():
    os.system('flask seed run')


def init_db():
    db.drop_all()
    db.configure_mappers()
    db.create_all()
    db.session.commit()


def drop_db():
    db.drop_all()
    db.session.commit()


def configure_db():
    db.configure_mappers()
    db.session.commit()


def create_db():
    db.create_all()
    db.session.commit()


def reset_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


def clear_db():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


@cli.command("init")
def init():
    init_db()


@cli.command("load")
def load():
    full_load()


@cli.command("create")
def create():
    create_db()


@cli.command("drop")
def drop():
    drop_db()


@cli.command("reset")
def reset():
    reset_db()


@cli.command("configure")
def configure():
    configure_db()


@cli.command("delete_db")
def delete_db():
    clear_db()


if __name__ == "__main__":
    cli()
