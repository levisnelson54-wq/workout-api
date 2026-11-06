"""Add exercise validation constraints

Revision ID: 16db1378b436
Revises: 7bb2ddd0338d
Create Date: 2026-10-30 10:11:09.521627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16db1378b436'
down_revision = '7bb2ddd0338d'
branch_labels = None
depends_on = None


def upgrade():
    # Add validation constraints to the existing exercises table.
    with op.batch_alter_table('exercises') as batch_op:
        batch_op.create_check_constraint(
            'check_exercise_name',
            'length(trim(name)) > 0'
        )
        batch_op.create_check_constraint(
            'check_exercise_category',
            'length(trim(category)) > 0'
        )


def downgrade():
    # Remove the validation constraints.
    with op.batch_alter_table('exercises') as batch_op:
        batch_op.drop_constraint(
            'check_exercise_name',
            type_='check'
        )
        batch_op.drop_constraint(
            'check_exercise_category',
            type_='check'
        )