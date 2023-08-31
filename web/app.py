from web import app
from web.authentication.authentication import authentication_pages
from web.common import common_pages
from web.user.dashboard import dashboard_pages
from web.user.posts import posts_pages
from models import user, post
from web import db

app.register_blueprint(authentication_pages)
app.register_blueprint(dashboard_pages)
app.register_blueprint(common_pages)
app.register_blueprint(posts_pages)
db.create_all()

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
