from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import tWorkout, Base

db_uri = 'sqlite:///workout.db'
engine = create_engine(db_uri, echo=False)

# Create tables
Base.metadata.create_all(engine)
    
# Start session
Session = sessionmaker(bind=engine)
session = Session()

import csv
from decimal import Decimal


# Import workout csv
reader = csv.DictReader(open('workout.csv'))

workouts = []
for row in reader:
    workouts.append(
        tWorkout(date=datetime.strptime(row['Date'], "%Y-%m-%d"),
             workout_name=row['Workout'],
             exercise=row['Exercise'],
             weight=Decimal(row['Weight']),
             sets=int(row['Sets']),
             reps=int(row['Reps']))
          )

session.add_all(workouts)
session.commit()



"""

# One example
nov7 = tWorkout(date=datetime.strptime("2017-11-07", "%Y-%m-%d"),
                workout_name="Power Upper",
                exercise="Bench Press",
                weight=45,
                sets=4,
                reps=5)

# Add a workout row
session.add(nov7)
session.commit()

# Add multiple rows
session.add_all([
    tWorkout(date=datetime.strptime("2017-11-07", "%Y-%m-%d"),
               workout_name="Power Lower",
               exercise="Squats",
               weight=70,
               sets=4,
               reps=5),
    tWorkout(date=datetime.strptime("2017-11-07", "%Y-%m-%d"),
               workout_name="Power Lower",
               exercise="Deadlift",
               weight=95,
               sets=3,
               reps=5),
    tWorkout(date=datetime.strptime("2017-11-07", "%Y-%m-%d"),
               workout_name="Power Lower",
               exercise="Leg Press",
               weight=115,
               sets=4,
               reps=10),
    tWorkout(date=datetime.strptime("2017-11-07", "%Y-%m-%d"),
               workout_name="Power Lower",
               exercise="Leg Curl",
               weight=105,
               sets=4,
               reps=10),
    tWorkout(date=datetime.strptime("2017-11-07", "%Y-%m-%d"),
               workout_name="Power Lower",
               exercise="Calf Raise",
               weight=130,
               sets=4,
               reps=10)
    ])
session.commit()

"""
