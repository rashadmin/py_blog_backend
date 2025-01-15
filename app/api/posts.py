from app.api import bp
from flask import jsonify,request,abort
from app.models import Post,User
from app.api.auth import token_auth

@bp.route('/posts', methods=['GET'])
@token_auth.login_required
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Post.to_collection_dict(Post.query, page, per_page, 'api.get_posts')
    return jsonify(data)


@bp.route('/users/<int:id>/posts', methods=['GET'])
@token_auth.login_required
def get_user_posts(id):
    if token_auth.current_user().id != id:
        abort(403)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 4, type=int), 100)
    posts = User.query.get_or_404(id).posts
    data = Post.to_collection_dict(posts, page, per_page, 'api.get_posts')
    return jsonify(data)


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())