from datetime import datetime

def model_to_dict(instance):
    result = {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

    for key, value in result.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat()

    return result