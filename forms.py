from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DecimalField, IntegerField
from wtforms.validators import DataRequired


class AddWorkoutForm(FlaskForm):
    date = DateField('Date', format="%Y-%m-%d")
    workout_name = StringField('Workout')
    exercise = StringField('exercise', validators=[DataRequired()])
    weight = DecimalField('weight', validators=[DataRequired()])
    sets = IntegerField('sets', validators=[DataRequired()])
    reps = IntegerField('reps', validators=[DataRequired()])
