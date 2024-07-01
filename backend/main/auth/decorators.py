from .. import jwt
from flask_jwt_extended import verify_jwt_in_request,get_jwt


def role_required(roles):
    def decorator(function):
        def wrapper(*args, **kwargs):
            #verificar que el jwt es correcto
            verify_jwt_in_request()
            
            claims = get_jwt()

            if claims["sub"]["role"] in roles:
                return function(*args, **kwargs)
            else:
                return "Roll not allowed", 404
        return wrapper
    return decorator

@jwt.user_identity_loader
def user_identity_lookup(usuario):
    return{
        "usuarioId": usuario.id,
        "role": usuario.role
    }     

@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
    claims = {
        "id": usuario.id,
        "role": usuario.role,
        'email': usuario.email
    }