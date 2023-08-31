from flask import Flask
from web.authentication.authentication import authentication_pages
from web.common import common_pages
from web.user.dashboard import dashboard_pages
from web.user.posts import posts_pages

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Change this for security'
app.register_blueprint(authentication_pages)
app.register_blueprint(dashboard_pages)
app.register_blueprint(common_pages)
app.register_blueprint(posts_pages)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
