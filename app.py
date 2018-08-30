from flask import Flask, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime

from model import tWorkout
from forms import AddWorkoutForm

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)


from flask.json import jsonify
from flask import render_template

###################################################################
# HTML Pages
###################################################################


# Calendar View
@app.route("/calendar")
def calendar_test():
    return render_template('calendar.html')

# Line Graph
@app.route("/line")
def line_graph_test():
    data = db.session.query(tWorkout.exercise).distinct()
    return render_template('line2.html', data=data)


# Add
@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddWorkoutForm()

    if request.method == 'POST' and form.validate_on_submit():

        date = form.date.data
        workout_name = form.workout_name.data
        exercise = form.exercise.data
        weight = form.weight.data
        sets = form.sets.data
        reps = form.reps.data

        new_workout = tWorkout(date=date,
                               workout_name=workout_name,
                               exercise=exercise,
                               weight=weight,
                               sets=sets,
                               reps=reps)

        db.session.add(new_workout)
        db.session.commit()

        return redirect(url_for('add'))

    return render_template('add_workout.html', form=form)


###################################################################
# RESTful API
###################################################################

# Get all data
@app.route("/data/all")
def show_all():
    return jsonify([x.serialize for x in db.session.query(tWorkout).all()])

# Query by workout name
@app.route('/data/workout/<string:workout_name>')
def show_workout(workout_name):
    t1 = db.session.query(tWorkout)\
        .filter_by(workout_name=workout_name)\
        .all()
    return jsonify([x.serialize for x in t1])

# Query a single exercise
@app.route('/data/exercise/<string:exercise>')
def show_exercise(exercise):
    t1 = db.session.query(tWorkout)\
        .filter_by(exercise=exercise)\
        .order_by(tWorkout.date)\
        .all()
    return jsonify([x.serialize for x in t1])

# Query multiple exercises. Input exercises separated by a comma
@app.route('/data/multi/<string:exercises>')
def show_exercises(exercises):
    e = exercises.split(",")
    t1 = db.session.query(tWorkout)\
        .filter(tWorkout.exercise.in_(e))\
        .order_by(tWorkout.exercise, tWorkout.date)\
        .all()
    return jsonify([x.serialize for x in t1])

# Add an exercise using POST request
@app.route('/add_data', methods=["GET", "POST"])
def add_data():
    if request.method == "GET":
        return "OK"
    date = request.args.get('date', type=str)
    date = datetime.strptime(date, "%Y-%m-%d")

    workout_name = request.args.get('reps', type=str)
    exercise = request.args.get('reps', type=str)
    weight = request.args.get('weight', type=float)
    sets = request.args.get('sets', type=int)
    reps = request.args.get('reps', type=int)

    new_workout = tWorkout(date=date,
                           workout_name=workout_name,
                           exercise=exercise,
                           weight=weight,
                           sets=sets,
                           reps=reps)

    db.session.add(new_workout)
    db.session.commit()
    return "done"

# Delete an exercise
@app.route("/delete/<int:id>")
def delete_id(id):
    to_delete = db.session.query(tWorkout).filter(tWorkout.id == id).one()

    if to_delete:
        db.session.delete(to_delete)
        db.session.commit()
        return "Deleted %d" % id
    else:
        return "Nothing to delete"


if __name__ == "__main__":
    app.run(threaded=True)
