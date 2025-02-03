from app.api import bp
from flask import jsonify,request,abort,url_for
from app.models import Post
from app import db
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.api.chat import Chat_ai
import json
@bp.route('/posts', methods=['GET'])
@token_auth.login_required
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Post.to_collection_dict(Post.query, page, per_page, 'api.get_posts')
    return jsonify(data)


@bp.route('/posts/<string:post_id>', methods=['GET'])
@token_auth.login_required
def get_post(post_id):
    id = Post.query.filter_by(post_id=post_id).first().user_id
    if token_auth.current_user().id != id:
        abort(403)
    data = Post.query.filter_by(post_id=post_id).first().to_dict()
    return jsonify(data)

@bp.route('/posts', methods=['POST'])
@token_auth.login_required
def create_post():
    user_id = token_auth.current_user().id
    data = request.get_json() or {}
    if 'original_post' not in data:
        return bad_request('must include original post fields')
    data['user_id'] = user_id
    post = Post()
    chat = Chat_ai()
    chat.start_model()
    chat.send_text(data['original_post'])
    chats = chat.chat_conversation()
    session = chat.chat_conversation(chatbot=False)
    chat.start_format_model()
    description_model = json.loads(chat.generate_description(data['original_post']))['description']
    data['description'] =json.dumps(description_model)
    data['conversation'] = json.dumps(chats)
    data['chat_session'] = json.dumps(session)
    post.from_dict(data, new_post=True)
    db.session.add(post)
    db.session.commit()
    response = jsonify(post.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_post', post_id=post.post_id)
    return response


#requires great formatting because i don't know what i'm doing

@bp.route('/post/<string:post_id>', methods=['PUT'])
@token_auth.login_required
def update_post(post_id):
    media_dict = {'facebook':'facebook_post','linkedin':'linkedin_post','X':'twitter_thread'}
    id = Post.query.filter_by(post_id=post_id).first().user_id
    status = Post.query.filter_by(post_id=post_id).first().status
    print(id)
    print(token_auth.current_user().id)
    data = request.get_json() or {}
    if token_auth.current_user().id != id:
        abort(403)
    if 'media' in data:
        if status:
            chat = Chat_ai()    
            post = Post.query.filter_by(post_id=post_id).first().to_dict()
            chat.start_format_model(data['media'])
            # print(post['conversation'][:-1])
            response = chat.generate(json.dumps(post['conversation'][:-1]))
            print(response)
            data[media_dict[data['media']]] = response
            post = Post.query.filter_by(post_id=post_id).first()
            post.from_dict(data)
            db.session.add(post)
            db.session.commit()
            response = jsonify(post.to_dict())
            response.status_code = 201
            response.headers['Location'] = url_for('api.get_post', post_id=post.post_id)
            return response
        else:
            return bad_request('must complete conversation')
    if 'text' not in data:
        return bad_request('must include text fields')
    chat = Chat_ai()
    chat_session = Post.query.filter_by(post_id=post_id).first().chat_session
    chat.continue_model(json.loads(chat_session))
    chat.send_text(data['text'])
    chats = chat.chat_conversation(new_chat=False)
    data['status'] = chats[-1]['text'] == 'done'
    session = chat.chat_conversation(new_chat=False,chatbot=False)
    data['conversation'] = json.dumps(chats)
    data['chat_session'] = json.dumps(session)
    post = Post.query.filter_by(post_id=post_id).first()
    post.from_dict(data)
    db.session.add(post)
    db.session.commit()
    response = jsonify(post.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_post', post_id=post.post_id)
    return response
    # post.from_dict(data, new_post=False)
    # db.session.commit()
    # return jsonify(data.to_dict())