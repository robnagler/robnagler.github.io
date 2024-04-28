import re

class WorkoutParser:
    def __init__(self, text):
        self.text = text

    def parse(self):
        workouts = []
        workout_texts = re.split(r'REVIEW WORKOUT \(\d/\d DONE\)', self.text)
        for workout_text in workout_texts:
            if workout_text.strip():
                workout = self._parse_workout(workout_text.strip())
                if workout:
                    workouts.append(workout)
        return workouts

    def _parse_workout(self, workout_text):
        workout_info = workout_text.split('\n')
        try:
            date = workout_info[0].strip()
            warmup_index = workout_info.index('GENERAL WARM UP') + 1 if 'GENERAL WARM UP' in workout_info else None
            strength_power_index = workout_info.index('STRENGTH/POWER') + 1 if 'STRENGTH/POWER' in workout_info else None
            cool_down_index = workout_info.index('GENERAL COOL DOWN') + 1 if 'GENERAL COOL DOWN' in workout_info else None

            warmup = workout_info[warmup_index:strength_power_index-1] if warmup_index is not None else []
            strength_power = workout_info[strength_power_index:cool_down_index-1] if strength_power_index is not None else []
            cool_down = workout_info[cool_down_index:] if cool_down_index is not None else []

            return {
                'date': date,
                'warmup': self._parse_section(warmup),
                'strength_power': self._parse_strength_power(strength_power),
                'cool_down': self._parse_section(cool_down)
            }
        except (ValueError, IndexError):
            print("Error parsing workout. Skipping...")
            return None

    def _parse_section(self, section):
        exercises = []
        for line in section:
            if line.strip() and not line.startswith('COMPLETED'):
                exercises.append(line.strip())
        return exercises

    def _parse_strength_power(self, section):
        sets = []
        current_set = None
        for line in section:
            if line.strip() and not line.startswith('COMPLETED'):
                if line.startswith('SET'):
                    current_set = {}
                    sets.append(current_set)
                else:
                    exercise, details = line.split(':', 1)
                    current_set[exercise.strip()] = {d.strip(): None for d in details.split(';')}
        return sets

# Sample text
text = """
Rob Nagler
MONDAY 3.23.20
  GENERAL WARM UP
HISTORY
Perform the following exercises:
-3' movement on treadmill, bike or fast-paced walking
-Squat @BW x10 reps
-RDL @BW x10 reps
-Forward-backward lunge @BW x5ea side
-Push ups x8-10 reps
-TRX Rows x8-10 reps

COMPLETED
  STRENGTH/POWER
4 SETS
1
2
3
4
KB LATERAL LUNGE
TIPS HISTORY
Use dumbbells;
Reps for each side per set

REPS
WEIGHT
8
30
8
30
8
30
8
30
FULL SIT UP
TIPS HISTORY
REPS
12
12
12
12
DB PUSH UP-ROW
TIPS HISTORY
REPS
WEIGHT
10
40
10
40
10
40
10
40
SPEED SKATERS
TIPS HISTORY
SECONDS
WEIGHT
25
25
25
25
LEG LIFT
TIPS HISTORY
REPS
12
12
12
12
COMPLETED
  GENERAL COOL DOWN
HISTORY
Static Stretching:
Hamstrings
Quads
Glutes
Calves
Chest
Back
Shoulders

COMPLETED
Write notes about your workout...
REVIEW WORKOUT (3/3 DONE)Rob Nagler
WEDNESDAY 3.25.20
  GENERAL WARM UP
HISTORY
Perform the following exercises:
-3' movement on treadmill, bike or fast-paced walking
-Squat @BW x10 reps
-RDL @BW x10 reps
-Forward-backward lunge @BW x5ea side
-Push ups x8-10 reps
-TRX Row x8-10 reps

COMPLETED
  STRENGTH/POWER
4 SETS
1
2
3
"""

# Parse the text
parser = WorkoutParser(text)
workouts = parser.parse()

# Display the parsed workouts
for workout in workouts:
    print(f"Date: {workout['date']}")
    print("Warm-Up:")
    for exercise in workout['warmup']:
        print(f"- {exercise}")
    print("Strength/Power:")
    for set in workout['strength_power']:
        for exercise, details in set.items():
            print(f"- {exercise}:")
            for detail, value in details.items():
                print(f"  - {detail}: {value}")
    print("Cool Down:")
    for exercise in workout['cool_down']:
        print(f"- {exercise}")
    print()
