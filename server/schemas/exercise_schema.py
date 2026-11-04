from marshmallow import Schema, fields, validate, validates, ValidationError


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)

    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    category = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    equipment_needed = fields.Boolean(required=True)

    @validates('name')
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError('Exercise name cannot be empty.')

    @validates('category')
    def validate_category(self, value):
        if not value.strip():
            raise ValidationError('Exercise category cannot be empty.')


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
