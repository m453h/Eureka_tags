from src import app
from src.web.admin.posts import manage_posts_pages
from src.web.admin.tags import manage_tags_pages
from src.web.admin.users import manage_users_pages
from src.web.authentication.authentication import authentication_pages
from src.web.common import common_pages
from src.web.user.dashboard import dashboard_pages
from src.web.user.posts import posts_pages

# Register various application blueprints
app.register_blueprint(authentication_pages)
app.register_blueprint(dashboard_pages)
app.register_blueprint(common_pages)
app.register_blueprint(posts_pages)
app.register_blueprint(manage_tags_pages)
app.register_blueprint(manage_posts_pages)
app.register_blueprint(manage_users_pages)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=False)
