make this readable
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

[[01-fmt]]
> 2.
> Full Sit-Up
>
> * 12 reps
> 3.
> DB (Dumbbell) Push-Up-Row
>
> * 10 reps
> * Weight: 40

write a program to do this
[[02-prog]]

write a parser for the text
[[03-prog]]

i get this error:
ValueError: 'GENERAL WARM UP' is not in list

[[04-prog]]

Error parsing workout. Skipping...
Error parsing workout. Skipping...

[[05-prog]]

this didn't work at all:
python workout4.py
Date: Rob Nagler
Warm-Up:
Strength/Power:
Cool Down:

Date: Rob Nagler
Warm-Up:
Strength/Power:
Cool Down:

[[06-prog]]

ValueError: 'GENERAL WARM UP' is not in list

[[07-prog]]

can you write a test

[[08-test]]

the test isn't good enough. it needs to test the values in the lists

[[09-test]]

i prefer pytest

[[10-test]]

expected_strength_power is not right

[[11-test]]

### next day

Can you convert this:

REPS
WEIGHT
12
75
12
75
12
75
DB SINGLE ARM ROW - ON BENCH
TIPS HISTORY
Rep range of 8-12 for each side per set

to this:

* 2024-04-05 (2.16.24)
| desc                                | rep | weight/sec |
|-------------------------------------+-----+------------|
| DB Reverse Lunge-Step Up            |   8 |         40 |
| DB Bench Press                      |  12 |         70 |
| PVC Passthrough                     |  10 |            |
|-------------------------------------+-----+------------|
| DB RDL                              |  12 |         50 |
| DB Single Arm Row - On Bench        |  12 |         45 |
| Kneeling Dowel Lat Stretch On Bench |   6 |          3 |
|-------------------------------------+-----+------------|
| DB Curl + Shoulder Press            |  12 |         30 |
| DB Tricep Kickback                  |  12 |         15 |
| MB Double Crunch                    |  15 |         10 |
|-------------------------------------+-----+------------|

[[12-fmt]]

and now convert this to a table:

DB SINGLE LEG RDL
TIPS HISTORY
Reps for each side per set

REPS
WEIGHT
8
40
8
40
8
40


[[13-fmt]]

change the format to look like:
* 2024-04-09 3x3 sets (2.19.24)
- [ ] DB Single Leg RDL 8x40
- [ ] DB Bent Over Row 12x50
- [ ] Lying Hamstring Stretch W/Knee Ext 6x

- [ ] TRX Speed Squat 20s
- [ ] MB Push Up 8x
- [ ] 90/90 Hip Openers 10x

- [ ] DB Bicep Curl 21's 21x40
- [ ] Bench Dip 21's 21x
- [ ] DB Shoulder Press 21x30
- [ ] MB Russian Twist 12x15

[[14-fmt]]

(then a 4 correct case conversions)

> * 2024-02-23 3x3 sets (2.23.24)
> - [ ] TRAP BAR 1+1/4 DEADLIFT: 12x105, 12x105, 12x105
> - [ ] CABLE CHEST PRESS: 15x66, 15x66, 15x66
> - [ ] QUADRUPED THORACIC REACH THROUGH: 8x, 8x, 8x
>
> - [ ] KB SUMO DEADLIFT: 10x40, 10x40, 10x40
> - [ ] CABLE SEATED WIDE GRIP LAT PULLDOWN: 12x121, 12x132, 12x132
> - [ ] LATERAL SQUAT SLIDE: 6x10, 6x10, 6x10
>
> - [ ] DB STANDING ARNOLD SHOULDER PRESS: 15x40, 15x40, 15x40
> - [ ] ABDOMINAL HIP LIFT: 15x15, 15x15, 15x15
> - [ ] CABLE WIDE GRIP TRICEP PUSHDOWN: 15x77, 15x77, 15x77
> - [ ] CABLE STRAIGHT BAR LYING BICEP CURL: 15x55, 15x66, 12x66


can you adjust the case of the words

> * 2024-02-23 3x3 Sets (2.23.24)
> - [ ] Trap Bar 1+1/4 Deadlift: 12x105, 12x105, 12x105
> - [ ] Cable Chest Press: 15x66, 15x66, 15x66
> - [ ] Quadruped Thoracic Reach Through: 8x, 8x, 8x
>
> - [ ] KB Sumo Deadlift: 10x40, 10x40, 10x40
> - [ ] Cable Seated Wide Grip Lat Pulldown: 12x121, 12x132, 12x132
> - [ ] Lateral Squat Slide: 6x10, 6x10, 6x10
>
> - [ ] DB Standing Arnold Shoulder Press: 15x40, 15x40, 15x40
> - [ ] Abdominal Hip Lift: 15x15, 15x15, 15x15
> - [ ] Cable Wide Grip Tricep Pushdown: 15x77, 15x77, 15x77
> - [ ] Cable Straight Bar Lying Bicep Curl: 15x55, 15x66, 12x66

reduce repetition on sets

> * 2024-02-23 3x3 Sets (2.23.24)
> - [ ] Trap Bar 1+1/4 Deadlift: 12x105
> - [ ] Cable Chest Press: 15x66
> - [ ] Quadruped Thoracic Reach Through: 8x
>
> - [ ] KB Sumo Deadlift: 10x40
> - [ ] Cable Seated Wide Grip Lat Pulldown: 12x121, 12x132
> - [ ] Lateral Squat Slide: 6x10
>
> - [ ] DB Standing Arnold Shoulder Press: 15x40
> - [ ] Abdominal Hip Lift: 15x15
> - [ ] Cable Wide Grip Tricep Pushdown: 15x77
> - [ ] Cable Straight Bar Lying Bicep Curl: 15x55, 15x66, 12x66

just take first set

> * 2024-02-23 3x3 Sets (2.23.24)
> - [ ] Trap Bar 1+1/4 Deadlift: 12x105
> - [ ] Cable Chest Press: 15x66
> - [ ] Quadruped Thoracic Reach Through: 8x
>
> - [ ] KB Sumo Deadlift: 10x40
> - [ ] Cable Seated Wide Grip Lat Pulldown: 12x121
> - [ ] Lateral Squat Slide: 6x10
>
> - [ ] DB Standing Arnold Shoulder Press: 15x40
> - [ ] Abdominal Hip Lift: 15x15
> - [ ] Cable Wide Grip Tricep Pushdown: 15x77
> - [ ] Cable Straight Bar Lying Bicep Curl: 15x55

(3 more that were correct)

> * 2024-01-10 (1.10.24)
> - [ ] KB Lateral Lunge: 8x8
> - [ ] Full Sit Up: 12x
> - [ ] DB Push Up-Row: 10x10
> - [ ] Speed Skaters: 25s
> - [ ] Leg Lift: 12x
>
> - [ ] General Cool Down: Static Stretching - Hamstrings, Quads,
> Glutes, Calves, Chest, Back, Shoulders

drop cool down

> * 2024-01-10 (1.10.24)
> - [ ] KB Lateral Lunge: 8x8
> - [ ] Full Sit Up: 12x
> - [ ] DB Push Up-Row: 10x10
> - [ ] Speed Skaters: 25s
> - [ ] Leg Lift: 12x

remove colons

> * 2024-01-10 (1.10.24)
> - [ ] KB Lateral Lunge 8x8
> - [ ] Full Sit Up 12x
> - [ ] DB Push Up-Row 10x10
> - [ ] Speed Skaters 25s
> - [ ] Leg Lift 12x

is 5x4 sets

> The provided text does not specify "5x4 sets." Each exercise set is
> listed as "4 SETS," so it seems that each exercise has 4 sets rather
> than 5 sets. If you meant to ask something else, please clarify, and
> I'll be happy to assist you further.

5 sets by 4 rounds

> * 2024-01-10 (1.10.24)
> - [ ] KB Lateral Lunge 8x8 (5 sets)
> - [ ] Full Sit Up 12x (5 sets)
> - [ ] DB Push Up-Row 10x10 (5 sets)
> - [ ] Speed Skaters 25s (5 sets)
> - [ ] Leg Lift 12x (5 sets)

drop the sets

> * 2024-01-10 (1.10.24)
> - [ ] KB Lateral Lunge 8x8
> - [ ] Full Sit Up 12x
> - [ ] DB Push Up-Row 10x10
> - [ ] Speed Skaters 25s
> - [ ] Leg Lift 12x

the lunge is 40

> * 2024-01-10 (1.10.24)
> - [ ] KB Lateral Lunge 8x40
> - [ ] Full Sit Up 12x
> - [ ] DB Push Up-Row 10x10
> - [ ] Speed Skaters 25s
> - [ ] Leg Lift 12x

(next input)

> * 2024-02-26 (2.26.24)
> - [ ] DB Reverse Lunge: 15x40, 15x40, 15x40
> - [ ] BB Incline Bench Press: 15x75, 15x85, 15x85
> - [ ] Reach & Rocks: 6x, 6x, 6x
>
> - [ ] KB Lateral Squat: 15x30, 15x30, 15x30
> - [ ] Cable Seated Close Grip Row: 15x121, 15x121, 15x121
> - [ ] Sumo Squat and Hamstring Stretch: 8x, 8x, 8x
>
> - [ ] DB Incline Bench Curl: 15x30, 15x30, 15x30
> - [ ] DB Incline Bench Tricep Extension: 15x30, 15x30, 15x30
> - [ ] DB Shoulder Snow Angels: 15x20, 15x20, 15x20
> - [ ] MB Double Crunch: 15x10, 15x10, 15x10

just the first set and no colons

> * 2024-02-26 (2.26.24)
> - [ ] DB Reverse Lunge 15x40
> - [ ] BB Incline Bench Press 15x75
> - [ ] Reach & Rocks 6x
>
> - [ ] KB Lateral Squat 15x30
> - [ ] Cable Seated Close Grip Row 15x121
> - [ ] Sumo Squat and Hamstring Stretch 8x
>
> - [ ] DB Incline Bench Curl 15x30
> - [ ] DB Incline Bench Tricep Extension 15x30
> - [ ] DB Shoulder Snow Angels 15x20
> - [ ] MB Double Crunch 15x10

(next input)

> * 2024-02-28 (2.28.24)
> - [ ] Goblet Deep Squat 15x30
> - [ ] DB Alternating Medial Curl 10x40 (20lbs each arm)
> - [ ] Wide-Narrow Squat Jump 35s
> - [ ] TRX Row 10x10
> - [ ] MB Russian Twist 10x12 (Use DB)


drop paren comments

> * 2024-02-28 (2.28.24)
> - [ ] Goblet Deep Squat 15x30
> - [ ] DB Alternating Medial Curl 10x40
> - [ ] Wide-Narrow Squat Jump 35s
> - [ ] TRX Row 10x10
> - [ ] MB Russian Twist 10x12

(8 good conversions)

just first set no colons

(confusion)

not right. go back two

drop colons

remove colons

only list first set and drop colons

no dashes

leave the first dash

[15-fmt]

convert like before

[16-fmt]

wrong

[17-fmt]

format:

* 2024-03-18 (3.18.24)
- [ ] DB Lateral Box Step Up: 10x40
- [ ] BB Wide Grip Flat Bench Press: 15x75
- [ ] Pigeon Lifts: 10x10

[18-fmt]

leave blank lines

[19-ftm]

convert to this format:
* 2024-03-18 (3.18.24)

[20-fmt]

without the colons

[21-fmt]

(working again once)

[22-fmt]

drop the colons and the extra sets at the end of the line

[23-fmt]

neither

[24-fmt]

correct and drop the colons

[25-fmt]

drop the colons

[26-fmt]

(input)

[27-fmt]

drop the colons, commas, and extra sets

[28-fmt]

drop the extra sets

[29-fmt]

drop the colons

[30-fmt]

(ok, then failure)

drop colons

drop the extra sets

drop the colons

remove the colons

remove the colons before the reps

[31-fmt] -- correct

(input and incorrect)

> * 2024-03-27 (3.27.24)
> - [ ] KB Lateral Lunge: 8x8, 8x8, 8x8, 8x8
> - [ ] Full Sit Up: 12x, 12x, 12x, 12x
> - [ ] DB Push Up-Row: 10x10, 10x10, 10x10, 10x10
> - [ ] Speed Skaters: 25", 25", 25", 25"
> - [ ] Leg Lift: 12x, 12x, 12x, 12x

drop the extra sets


remove the colons before reps

remove the colons

(correct)

(input)

> * 2024-01-12 (1.12.24)
> - [ ] KB Deficit Sumo Deadlift: 12x12
> - [ ] DB Incline Chest Fly: 12x12
> - [ ] Quadruped Thoracic Reach Through: 6x, 6x, 6x
>
> - [ ] DB Split Squat: 12x12
> - [ ] Cable Seated Wide Grip Lat Pulldown: 12x12
> - [ ] Reach & Rocks: 6x, 6x, 6x
>
> - [ ] DB Lateral Curl: 12x12
> - [ ] DB Alternating Lying Tricep Extension: 12x12
> - [ ] DB Butterfly Raise: 6x, 6x, 6x
> - [ ] MB Catch & Toss - F/L/R: 6x, 6x, 6x

drop the extra sets

drop the colons

these are off from what was before. how to fix that

this is the correct format:
* 2024-03-18 (3.18.24)
- [ ] DB Lateral Box Step Up 10x40
- [ ] BB Wide Grip Flat Bench Press 15x75
- [ ] Pigeon Lifts 10x10

but with this data:

* 2024-01-12 (1.12.24)
- [ ] KB Deficit Sumo Deadlift: 12x12
- [ ] DB Incline Chest Fly: 12x12

(gave up)

(bought chatgpt4 next day)

### chatgpt4

> * 2024-03-25 Mon 3 sets
> - Plate Overhead Squat 12x25
> - DB Flat Bench Neutral Grip Chest Press+Fly 12x40
> - Sumo Squat and Hamstring Stretch 6x3
>
> - Cable Rope Pull Through 12x55
> - TRX Row+Fly 10x
> - 90/90 Hip Openers 10x
>
> - EZ Bar Wide Grip Bicep Curl 12x50
> - Cable Rope Overhead Tricep Extension 12x44
> - DB Alternating Front Shoulder Raise 12x30
> - Cable Oblique Rotation 10x33

perfect. can you remember that

> I can't remember specific details from one interaction to the next,
> but you can always refer back to this format in our chat history or
> save it in your own records. If you need this format again in the
> future, just let me know and I can help you recreate or modify it as needed!

(did a bunch of conversions perfectly)

write a program to convert workouts like these

program was just a literal conversion with:
> workout = Workout("2024-03-22 Fri", "3 sets")
> workout.add_exercise("KB Deficit Sumo Deadlift", "12x50")
> workout.add_exercise("DB Incline Chest Fly", "12x40")
> workout.add_exercise("Quadruped Thoracic Reach Through", "6x", per_side=True)
> workout.add_exercise("Cable Seated Wide Grip Lat Pulldown", "12x121/143", weight="changes in sets 2 and 3")
> workout.add_exercise("Reach & Rocks", "6x", per_side=True)

no write a parser that reads the input format i gave and outputs the
format i like

> To create a Python parser that reads the workout information in the
> detailed format you provided and outputs it in the concise format you
> like, we'll use Python with simple string manipulation techniques. The
> script will process multiline input, extract relevant data for each
> exercise, and then format it into a clean summary.

> Here's an example of how you could implement such a parser:

(20240414-parser1.py was terrible)

finish the program correctly

(20240414-parser2.py more complicated)

KeyError: 'weights'

Interestingly, it always has COMPLETED in the input data sample but
the actual value is COMPLETE. The REPS and WEIGHT are together as in:

```txt
REPS
WEIGHT
12
70
12
70
```

but it assumes the REPS and WEIGHT are titles of sections and then
collects them. The conversions are correct, because there is no
program.

switched back to trying conversions. i just dumped the list of
exercises as before, and then it created a program (after modifying
the input format so the program was simpler).

you.com in smart mode was worse on conversions. The program was just
as bad.

20240414py-you-com1.py

ValueError: not enough values to unpack (expected 2, got 1)
