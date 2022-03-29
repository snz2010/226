from flask import request
from flask_restx import Resource, Namespace
from views.functions import admin_required, auth_required
from models import Genre, GenreSchema
from setup_db import db

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = db.session.query(Genre).all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        ent = Genre(**req_json)

        db.session.add(ent)
        db.session.commit()
        return "", 201, {"location": f"/genres/{ent.id}"}

@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_required
    def get(self, rid):
        r = db.session.query(Genre).get(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, bid):
        user = db.session.query(Genre).get(bid)
        req_json = request.json
        user.name = req_json.get("name")
        db.session.add(user)
        db.session.commit()
        return "", 204

    @admin_required
    def delete(self, bid):
        user = db.session.query(Genre).get(bid)
        db.session.delete(user)
        db.session.commit()
        return "", 204