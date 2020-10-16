import datetime
import traceback
import base64

from Crypto.Cipher import ARC4
from flask import request, make_response, jsonify
from common.exception import SimpleException
from .utils import *
from .const import *
import helper as _helper
_db = _helper.get_mongodb()


def common_view(func):
    @functools.wraps(func)
    def decorated_func(*args, **kwargs):
        result = {
            'code': 0,
            'msg': '',
            'success': False,
            'data': None,
        }
        try:
            result['data'] = func(*args, **kwargs)
            result['success'] = True
        except SimpleException as e:
            result['code'] = e.code
            result['msg'] = str(e)
            traceback.print_exc()
        except Exception as e:
            result['code'] = 1
            result['msg'] = str(e)
            traceback.print_exc()
        return jsonify(result)
    return decorated_func


def with_transaction(func):
    @functools.wraps(func)
    def decorated_func(*args, **kwargs):
        tx = helper.Transaction()
        try:
            result = func(*args, **kwargs)
            tx.commit()
        except Exception as ex:
            tx.rollback()
            raise ex
        return result
    return decorated_func


def login_required(func):
    @functools.wraps(func)
    def decorated_func(*args, **kwargs):
        x_token = request.cookies.get('x-token')
        if not _db.luckycat_users.find_one({'token': x_token}):
            response = make_response('need login', 401)
            return response

        return func(*args, **kwargs)

    return decorated_func


def set_regex_query(arg_list, req, query):
    for q in arg_list:
        v = req.get(q)
        if v:
            query[f"{q}__icontains"] = v


def set_eq_query(arg_list, req, query, t=str):
    for q in arg_list:
        v = req.get(q)
        if v:
            query[q] = t(v)


def set_boolean_query(arg_list, req, query):
    for q in arg_list:
        v = req.get(q)
        if v:
            query[q] = v == 'true'


def set_date_range_query(arg_list, req, query):
    for q in arg_list:
        v = req.getlist(q+"[]")
        if v:
            [start, end] = v
            query[f"{q}__range"] = [datetime.strptime(
                start, QUERY_UTC_FORMAT), datetime.strptime(end, QUERY_UTC_FORMAT)]


def set_indexes(data, begin=0):
    for x in data:
        x['index'] = begin
        begin += 1
    return data
