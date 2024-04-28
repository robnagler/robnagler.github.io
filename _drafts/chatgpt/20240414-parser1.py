class Workout:
    def __init__(self, date, sets):
        self.date = date
        self.sets = sets
        self.exercises = []

    def add_exercise(self, name, reps, weight=None, per_side=False):
        self.exercises.append((name, reps, weight, per_side))

    def format_workout(self):
        print(f"* {self.date} - {self.sets} sets")
        for exercise in self.exercises:
            name, reps, weight, per_side = exercise
            if per_side:
                side_text = " per side"
            else:
                side_text = ""
            if weight:
                print(f"- {name} {reps}x{weight}{side_text}")
            else:
                print(f"- {name} {reps}x{side_text}")

# Example usage:
workout = Workout("2024-03-22 Fri", "3 sets")
workout.add_exercise("KB Deficit Sumo Deadlift", "12x50")
workout.add_exercise("DB Incline Chest Fly", "12x40")
workout.add_exercise("Quadruped Thoracic Reach Through", "6x", per_side=True)
workout.add_exercise("Cable Seated Wide Grip Lat Pulldown", "12x121/143", weight="changes in sets 2 and 3")
workout.add_exercise("Reach & Rocks", "6x", per_side=True)
workout.format_workout()
