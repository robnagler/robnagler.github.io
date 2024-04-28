class Workout:
    def __init__(self, date, warmup, strength_power, cool_down):
        self.date = date
        self.warmup = warmup
        self.strength_power = strength_power
        self.cool_down = cool_down

    def display(self):
        print(f"Date: {self.date}")
        print("")

        print("General Warm-Up:")
        self.display_exercises(self.warmup)
        print("")

        print("Completed:")
        print("Strength/Power:")
        self.display_sets(self.strength_power)
        print("")

        print("General Cool Down:")
        self.display_exercises(self.cool_down)

    @staticmethod
    def display_exercises(exercises):
        for exercise in exercises:
            print(f"- {exercise}")

    @staticmethod
    def display_sets(sets):
        for i, set in enumerate(sets, 1):
            print(f"Set {i}:")
            for exercise, details in set.items():
                print(f"  {exercise}:")
                for key, value in details.items():
                    print(f"    {key}: {value}")


# Sample workout data
workout1 = Workout(
    "Monday 3.23.20",
    warmup=["3' movement on treadmill, bike, or fast-paced walking",
            "Squat @ BW x 10 reps",
            "RDL @ BW x 10 reps",
            "Forward-backward lunge @ BW x 5 each side",
            "Push-ups x 8-10 reps",
            "TRX Rows x 8-10 reps"],
    strength_power=[
        {"KB Lateral Lunge": {"Use dumbbells": None, "Reps per side": 8, "Weight": 30}},
        {"Full Sit-Up": {"Reps": 12}},
        {"DB Push-Up-Row": {"Reps": 10, "Weight": 40}},
        {"Speed Skaters": {"Seconds": 25}},
        {"Leg Lift": {"Reps": 12}}
    ],
    cool_down=["Static Stretching: Hamstrings",
               "Quads",
               "Glutes",
               "Calves",
               "Chest",
               "Back",
               "Shoulders"]
)

workout2 = Workout(
    "Wednesday 3.25.20",
    warmup=["3' movement on treadmill, bike, or fast-paced walking",
            "Squat @ BW x 10 reps",
            "RDL @ BW x 10 reps",
            "Forward-backward lunge @ BW x 5 each side",
            "Push-ups x 8-10 reps",
            "TRX Row x 8-10 reps"],
    strength_power=[],
    cool_down=[]
)

# Display the workout
workout1.display()
print("")
workout2.display()
