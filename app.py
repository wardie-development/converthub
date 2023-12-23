from decouple import config

from chalice import Chalice

from chalicelib.routes.convert import convert_bp
from chalicelib.routes.resize import resize_bp

app = Chalice(app_name="converthub")
app.experimental_feature_flags.update(["BLUEPRINTS"])

app.register_blueprint(convert_bp, url_prefix="/convert")
app.register_blueprint(resize_bp, url_prefix="/resize")


@app.route("/healthcheck")
def healthcheck():
    return {"status": "success", "data": "ok"}
