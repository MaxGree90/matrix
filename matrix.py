from app import app, db
from app.models import Store, User, Position, Area, City, Packing

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Store': Store, 'User': User, 'Position': Position, 'Area': Area, 'City': City, 'Packing': Packing}