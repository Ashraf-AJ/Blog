from graphene.relay.node import from_global_id
from api.database import utils as db_utils


def get_object_by_global_id(model, global_id):
    _, obj_id = from_global_id(global_id)
    return db_utils.get_object_by_id(model, obj_id)
