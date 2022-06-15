from app import app, db
from app.models import User, Word, Role

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Word': Word, 'Role': Role}
