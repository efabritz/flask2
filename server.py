from flask import Flask, request, jsonify
from flask.views import MethodView
from db import User, Advertisement, Session
from errors import HttpError

app = Flask('server')

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status':'error', 'description': error.message})
    http_response.status_code = error.status_code
    return http_response

def get_ad(ad_id: int, session: Session):
    ad = session.query(Advertisement).get(ad_id)
    if ad is None:
        raise HttpError(404, 'Advertisment not found')
    return ad

def get_user(user_id: int, session: Session):
    user = session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, 'User not found')
    return user

class AdView(MethodView):
    def get(self, ad_id):
        with Session() as session:
            ad = get_ad(ad_id, session)
            return jsonify({
                'id': ad.id,
                'header': ad.header,
                'description': ad.description,
                'creation_date': ad.creation_date.isoformat(),
                'author': ad.user_id
            })

    def post(self):
        json_data = request.json
        with Session() as session:
            new_ad = Advertisement(**json_data)
            session.add(new_ad)
            session.commit()

            return jsonify({
                'id': new_ad.id,
                'header': new_ad.header,
                'creation_date': int(new_ad.creation_date.timestamp())
            })

    def delete(self, ad_id):
        with Session() as session:
            ad = get_ad(ad_id, session)
            session.delete(ad)
            session.commit()
            return jsonify({"status":"success"})

    def patch(self, ad_id):
        json_data = request.json
        with Session() as session:
            ad = get_ad(ad_id, session)
            for key, value in json_data.items():
                setattr(ad, key, value)
            session.add(ad)
            session.commit()
        return jsonify({"status":"succes"})

class UserView(MethodView):
    def get(self, user_id):
        with Session() as session:
            user = get_user(user_id, session)
            return jsonify({
                'id': user.id,
                'email': user.email,
                'username': user.username
            })

    def post(self):
        json_data = request.json
        with Session() as session:
            new_user = User(**json_data)
            session.add(new_user)
            session.commit()

            return jsonify({
                'id': new_user.id,
                'username': new_user.username
            })

    def delete(self, user_id):
        with Session() as session:
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()
            return jsonify({"status":"success"})

    def patch(self, user_id):
        json_data = request.json
        with Session() as session:
            user = get_user(user_id, session)
            for key, value in json_data.items():
                setattr(user, key, value)
            session.add(user)
            session.commit()
        return jsonify({"status":"succes"})

app.add_url_rule('/ads/<int:ad_id>', view_func=AdView.as_view('ads_with_id'), methods=['PATCH', 'GET', 'DELETE'])
app.add_url_rule('/ads', view_func=AdView.as_view('ads'), methods=['POST'])

app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('users_with_id'), methods=['PATCH', 'GET', 'DELETE'])
app.add_url_rule('/users', view_func=UserView.as_view('users'), methods=['POST'])


app.run(port=5000)