from app.controllers.user_controller import (create_user, delete_user, get_user, login,
                                             update_user)
from flask import Blueprint

bp_user = Blueprint('bp_user', __name__, url_prefix='/api')

bp_user.post("/signup")(create_user)
bp_user.post("/signin")(login)
bp_user.get('')(get_user)
bp_user.put('')(update_user)
bp_user.delete('')(delete_user)