# ========================================================================
#
# * WARNING * Changing the content of this file at will may cause a crash.
#
# ========================================================================

from configs import conf
from modules.http_server.view import PackagesExplorer

ALLOWED_URL = {
    "": PackagesExplorer.main,

}

ALLOWED_URL = {"/" + conf.ROOT_URL + t: ALLOWED_URL[t] for t in ALLOWED_URL}