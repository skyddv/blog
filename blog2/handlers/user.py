from m import Router
from ..models import db, User, Catalog
from webob.exc import HTTPBadRequest, HTTPInternalServerError, HTTPUnauthorized
import bcrypt
from sqlalchemy import or_
from m.utils import jsonify
import logging
import jwt, bcrypt
import datetime


router = Router(prefix='/user')


@router.route(r'/register', methods=['POST'])
def register(ctx, request):
    try:
        payload = request.json()
        nickname = payload['nickname']
        mail = payload['mail']
        password = payload['password']
    except KeyError as e:
        raise HTTPBadRequest('{} is required'.format(e))
    except Exception as e:
        raise HTTPBadRequest(e)

    user = User.query.filter(or_(User.nickname == nickname, User.email == mail)).first()
    if user is not None:
        return jsonify(node=400, message='user exist')
    catalog = Catalog(name='default')
    user = User(nickname=nickname, catalogs=[catalog], email=mail, password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify(code=200)
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        raise HTTPInternalServerError(e)


@router.route(r'/login', methods=['POST'])
def login(ctx, request):
    try:
        payload = request.json()
        mail = payload['email']
        password = payload['password']
    except Exception as e:
        raise HTTPBadRequest(e)

    user = User.query.filter(User.email == mail).first_or_404('user {} not exist'.format(mail))
    if bcrypt.hashpw(password.encode(), user.password.encode()) == user.password.encode():
        key = ctx.config.get_string('auth.key')
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=ctx.config.get_int('auth.exp'))
        token = jwt.encode({'user':user.id, 'exp':exp}, key, 'HS512').decode()
        return jsonify(code=200, token=token)
    raise HTTPUnauthorized()