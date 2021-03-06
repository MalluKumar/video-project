from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(id = {self.id}, name = {self.name}, views = {self.views}, likes = {self.likes})"


# db.create_all() should be run only once to create db in the relative path.


video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video", required=True)
video_put_args.add_argument(
    "likes", type=int, help="Likes of the video", required=True)
video_put_args.add_argument(
    "views", type=int, help="Views of the video", required=True)


video_update_args = reqparse.RequestParser()
video_update_args.add_argument(
    "name", type=str, help="Name of the video")
video_update_args.add_argument(
    "likes", type=int, help="Likes of the video")
video_update_args.add_argument(
    "views", type=int, help="Views of the video")


# def abort_if_id_doesnotexist(video_id):
#     if video_id not in videos:
#         abort(404, messge="Video id does not exist!!")


# def abort_if_id_exists(video_id):
#     if video_id in videos:
#         abort(409, message="Video ID already exists!!")


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'likes': fields.Integer,
    'views': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="ID could not be found")
        return video

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        video = VideoModel.query.filter_by(id=video_id).first()
        if video:
            abort(409, message="ID already exists!!")
        video = VideoModel(
            id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        # '201' represents status code ( for 'created')
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="ID does not exists!!")

        if args['name']:
            video.name = args['name']
        if args['likes']:
            video.likes = args['likes']
        if args['views']:
            video.views = args['views']

        db.session.commit()
        return video

    def delete(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()
        try:
            db.session.delete(video)
            db.session.commit()
            return {"Message": "Successfully Deleted!!"}
        except:
            abort(404, message="Post not deleted")


api.add_resource(Video, '/<int:video_id>')


if __name__ == '__main__':
    app.run(debug=True)
