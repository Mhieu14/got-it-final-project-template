import bcrypt

from main.commons.exceptions import BadRequest


def hash_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())


def get_pagination_params(request_args, default_limit=20, default_offset=0):
    try:
        offset = int(request_args.get("offset", default_offset))
        limit = int(request_args.get("limit", default_limit))
        if offset < 0 or limit < 0:
            raise Exception("Limit and offset must be bigger than 0")
        if limit > 50:
            raise Exception("Limit must be smaller than 50")
        return offset, limit
    except Exception as e:
        message = str(e) or "Invalid parameters"
        raise BadRequest(error_code=400001, error_message=message)
