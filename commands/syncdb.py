import pkgutil

from common.lib import with_transaction
from model import DBMODELS


def load_all_modules_from_dir(dirname):
    for _, file_name, _ in pkgutil.iter_modules([dirname]):
        __import__(f"{dirname}.{file_name}")


def main(*args):
    load_all_modules_from_dir("model")
    for k, v in DBMODELS.items():
        v.objects.create_table()
