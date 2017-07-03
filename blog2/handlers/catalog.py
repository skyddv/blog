import logging
from m import Router
from m.utils import jsonify
from m.security import Require
from webob import exc
from ..models import db, Catalog, Post


router = Router('/api/catalog')


@router.post('')
@Require()
def add(ctx, request):
    try:
        name = request.json()['name']
    except Exception as e:
        raise exc.HTTPBadRequest(e)
    user = request.principal
    catalog = Catalog.query.filter(Catalog.user == user.id)\
        .filter(Catalog.name == name).first()
    if catalog is None:
        catalog = Catalog(name=name, user=user.id)
        db.session.add(catalog)
        try:
            db.session.commit()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            raise exc.HTTPInternalServerError(e)
    return jsonify(code=200, catalog=catalog.dictify())


@router.get('')
@Require()
def get_all(ctx, request):
    page = request.params.get('page', 1)
    size = request.params.get('size', 50)
    catalogs = Catalog.query.filter(Catalog.user == request.principal.id)\
        .paginate(page, size)
    return jsonify(code=200, catalogs=catalogs.dictify())


@router.delete('/{id:int}')
@Require()
def delete(ctx, request):
    catalog = Catalog.query.filter(Catalog.id == request.args['id']).first_or_404()
    if catalog.user != request.principal.id:
        raise exc.HTTPForbidden()
    if Post.query.filter(Post.catalog == catalog.id).count():
        return jsonify(code=422, message='posts not empty')
    Catalog.query.filter(Catalog.id == request.args['id']).delete()
    try:
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        raise exc.HTTPInternalServerError(e)
    return jsonify(code=200)
