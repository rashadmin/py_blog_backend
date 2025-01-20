from app.api import bp
from flask import jsonify,request,abort,url_for
from app.models import Post
from app import db
from app.api.auth import token_auth
from app.api.errors import bad_request


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
    post.from_dict(data, new_post=True)
    db.session.add(post)
    db.session.commit()
    response = jsonify(post.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_post', post_id=post.post_id)
    return response



@bp.route('/post/<string:post_id>', methods=['PUT'])
@token_auth.login_required
def update_post(post_id):
    id = Post.query.filter_by(post_id=post_id).first().user_id
    if token_auth.current_user().id != id:
        abort(403)
    data = Post.query.filter_by(post_id=post_id).first().to_dict()
    # post.from_dict(data, new_user=False)
    db.session.commit()
    # return jsonify(user.to_dict())