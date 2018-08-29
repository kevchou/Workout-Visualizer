from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, String, Integer, Numeric

Base = declarative_base()

class tWorkout(Base):
    __tablename__ = 'workouts'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    workout_name = Column(String)
    exercise = Column(String)
    weight = Column(Numeric)
    sets = Column(Integer)
    reps = Column(Integer)
    
    def __repr__(self):
        return "<Workout(date='%s', workout_name='%s')>" % (self.date, self.workout_name)

    @property
    def serialize(self):
        return {
            'date': self.date.strftime('%Y-%m-%d'),
            'workout_name': self.workout_name,
            'exercise': self.exercise,
            'weight': "%.2f" % self.weight,
            'sets': str(self.sets),
            'reps': str(self.reps)
            }
