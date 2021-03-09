from marshmallow import Schema, fields, pre_load
from backend_api.app.common import schema_fields

class IpListSchema(Schema):
    id = schema_fields.String()
    system_name = schema_fields.String()
    system_description = schema_fields.String()
    ip_address = schema_fields.String()
    device_model = schema_fields.String()