from app.api.views import ns, ns_auth, ns_user
from app.extensions import api

api.add_namespace(ns)
api.add_namespace(ns_auth)
api.add_namespace(ns_user)
