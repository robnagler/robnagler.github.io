def convert_workout(input_string):
    # Split the input string into lines
    lines = input_string.split('\n')

    # Extract the date from the second line
    date_line = lines[1]
    date = date_line.split()[1]

    # Initialize an empty list to store the converted exercises
    converted_exercises = []

    # Iterate over the lines starting from the third line
    for line in lines[2:]:
        # Skip empty lines
        if not line:
            continue

        # Split the line into exercise and details
        exercise, details = line.split(':', 1)

        # Extract the reps and weight from the details
        reps, weight = details.strip().split()

        # Format the converted exercise string
        converted_exercise = f"- {exercise.strip()} {reps}x{weight}"

        # Append the converted exercise to the list
        converted_exercises.append(converted_exercise)

    # Format the final output string
    output_string = f"* {date} 4 sets\n" + '\n'.join(converted_exercises)

    return output_string


# Example usage
input_string = """
WEDNESDAY 3.06.24
  GENERAL WARM UP
HISTORY
Perform the following exercises:
-3' movement on treadmill, bike or fast-paced walking
-Squat @BW x10 reps
-RDL @BW x10 reps
-Forward-backward lunge @BW x5ea side
-Push ups x8-10 reps

COMPLETED
  STRENGTH/POWER
4 SETS
1
2
3
4
DB RDL
TIPS HISTORY
REPS
WEIGHT
15
40
15
40
15
40
15
40
DB NEUTRAL GRIP SINGLE ARM FLAT BENCH PRESS
HISTORY
Palm facing inward;
Reps for each side per set

REPS
WEIGHT
12
35
12
35
12
35
12
35
ALTERNATING EXPLOSIVE BOX STEP UP
TIPS HISTORY
Use a chair or the stairs, about 12" in height

SECONDS
35
35
35
35
DB TRICEP KICKBACK
TIPS HISTORY
Reps for each side per set

REPS
WEIGHT
12
15
12
15
12
15
12
15
V-UP - ALTERNATING
TIPS HISTORY
Reps for each side per set

REPS
8
8
8
8
"""

output_string = convert_workout(input_string)
print(output_string)
