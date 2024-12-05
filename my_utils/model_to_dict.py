from datetime import datetime

def model_to_dict(instance):
    """
    Convert a SQLAlchemy model instance to a dictionary, 
    serializing datetime objects into ISO 8601 format strings.
    """
    # Convert the model instance to a dictionary
    result = {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

    # Iterate over the dictionary and convert datetime objects to strings
    for key, value in result.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat()  # Convert datetime to ISO 8601 string format

    return result