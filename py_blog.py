from app import db,create_app
from app.models import User,Post
from app.api.chat import Chat_ai
app= create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db':db,'user':User,'post':Post,'chat':Chat_ai}