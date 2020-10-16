from datetime import datetime

from flask.json import JSONEncoder
import helper
import flask
import logging
import sys

from api.app import app_bp

if sys.version_info.major == 3 and sys.version_info.minor < 7:
    from backports.datetime_fromisoformat import MonkeyPatch

    MonkeyPatch.patch_fromisoformat()


class _CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


config = helper.get_config()
app = flask.Flask(__name__)
app.json_encoder = _CustomJSONEncoder


@app.route('/')
def hello():
    return 'hello world'


app.register_blueprint(app_bp, url_prefix='/api/app/')


def _main():
    port = sys.argv[1] if len(sys.argv) > 1 else config['flask']['port']
    host = config['flask']['host']
    debug = config['flask']['debug']
    logging.info('host=%r, port=%r' % (host, port))
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == '__main__':
    _main()
