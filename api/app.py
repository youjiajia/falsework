from flask import Blueprint, request, jsonify

from common.lib import common_view
from model.business import BusinessApp

app_bp = Blueprint('app', __name__)


@app_bp.route('/test', methods=['GET'])
def test():
    BusinessApp.objects.insert(
        id=1,
        name='多推牛',
        code='dtn',
        session_token='',
        secret_key='',
    )
    return "success"
