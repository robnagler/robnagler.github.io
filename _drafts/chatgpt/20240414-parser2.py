def parse_workout(input_data):
    workout = []
    current_exercise = {}
    collecting_reps = False
    rep_list = []

    for line in input_data.split('\n'):
        line = line.strip()

        if line.startswith("MONDAY") or line.startswith("WEDNESDAY") or line.startswith("FRIDAY"):
            if current_exercise:
                # Finalize the last exercise if there is one
                format_and_append_exercise(workout, current_exercise, rep_list)
            date = line.split()[1]  # Extract the date
            workout.append(f"* {date} 3 sets")  # Assume 3 sets if not specified
            current_exercise = {}
            rep_list = []
        elif 'REPS' in line and 'WEIGHT' in line:
            # Start collecting reps and weights
            collecting_reps = True
        elif collecting_reps and line.isdigit():
            # Collect reps when they are listed as single numbers
            rep_list.append(line)
        elif "WEIGHT" in line and line.split()[0] == "WEIGHT":
            # Last line of reps, prepare to store the exercise
            weights = line.split()[1:]
            if current_exercise.get('name'):
                current_exercise['reps'] = rep_list
                current_exercise['weights'] = weights
                format_and_append_exercise(workout, current_exercise, rep_list)
                current_exercise = {}
                rep_list = []
            collecting_reps = False
        elif line.isupper() and not line.isdigit() and 'SETS' not in line:
            # A new exercise name line
            if current_exercise:
                # Finalize the last exercise if there is one
                format_and_append_exercise(workout, current_exercise, rep_list)
            current_exercise = {'name': line}
            rep_list = []
        elif "COMPLETED" in line:
            # Finalize any exercises at the end of the input
            if current_exercise:
                format_and_append_exercise(workout, current_exercise, rep_list)
                current_exercise = {}

    return "\n".join(workout)

def format_and_append_exercise(workout, exercise, reps):
    """ Helper function to format and append an exercise to the workout list """
    name = exercise['name']
    reps = "x".join(reps) if len(set(reps)) == 1 else "/".join(reps)
    weight = "x".join(exercise['weights']) if len(set(exercise['weights'])) == 1 else "/".join(exercise['weights'])
    workout.append(f"- {name} {reps}x{weight}")

# Example input data
input_data = """
MONDAY 1.22.24
  STRENGTH/POWER
3 SETS
1
2
3
TRAP BAR DEADLIFT
TIPS HISTORY
Rep range of 8-12 for each side per set
REPS
12
12
12
WEIGHT
115
115
115
COMPLETED
"""

# Using the parser
print(parse_workout(input_data))
