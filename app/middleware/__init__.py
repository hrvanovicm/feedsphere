# noinspection PyUnresolvedReferences
import falcon

from . import *


# noinspection PyUnusedLocal
def admin_privileges(req, res, resource, params):
    user = req.context['user']

    if user.is_admin is False:
        raise falcon.HTTPForbidden(description='Admin permission required!')
