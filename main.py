
"""
ROTC Cadet Dashboard

This program allows ROTC cadets to manage profile information,
calculate AFT scores, view fitness recommendations, and follow
a weekly training calendar.
"""

from drafter import *
from dataclasses import dataclass, field
from aft_scoring_data_table import *
import calendar as cal

set_website_title("ROTC Cadet Dashboard")
set_site_information(
    author="Henry Samer",
    description="ROTC Student Fitness Plan.",
    sources="Thanks to the Drafter docs and my study group.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/your-username/your-repository"]
)
hide_debug_information()
set_website_framed(False)

# This uses an imported library to calculate the layout of a calendar instead of manually calculating dates and weekdays.

# -------------------------
# CALENDAR SETTINGS
# -------------------------

# Make Sunday the first day displayed in the calendar.
cal.setfirstweekday(cal.SUNDAY)


# -------------------------
# DATACLASSES
# -------------------------

@dataclass
class Profile:
    age: int = 0
    gender: str = ""
    school: str = ""
    class_year: str = "MS1"
    ranger_challenge: bool = False


@dataclass
class AFT_score:
    deadlift: int = 0
    hrp: int = 0
    sprint_drag_carry: int = 0
    plank: int = 0
    run: int = 0


@dataclass
class AFT_points:
    deadlift: int = 0
    hrp: int = 0
    sprint_drag_carry: int = 0
    plank: int = 0
    run: int = 0
    total: int = 0

# default_factory creates a new list whenever a new Fitness_plan object is created. This prevents different objects from unintentionally sharing the same list.
@dataclass
class Fitness_plan:
    best_events: list = field(default_factory=list) 
    worst_events: list = field(default_factory=list)
    workout_program: list = field(default_factory=list)


@dataclass
class Calendar:
    training_days: list = field(default_factory=list)
    month: int = 11
    year: int = 2026


@dataclass
class State:
    profile: Profile = field(default_factory=Profile)
    aft_score: AFT_score = field(default_factory=AFT_score)
    aft_points: AFT_points = field(default_factory=AFT_points)
    fitness_plan: Fitness_plan = field(default_factory=Fitness_plan)
    calendar: Calendar = field(default_factory=Calendar)


# -------------------------
# HOME PAGE
# -------------------------

@route
def index(state: State) -> Page:
    '''Goal: Display the main ROTC Cadet Dashboard.
    Parameters: state (State), containing all saved cadet information.
    Returns: The home page with navigation buttons and AFT score.'''

    return Page(state, [
        "ROTC CADET DASHBOARD",
        "--------------------------------",

        "Welcome to your ROTC Cadet Dashboard.",

        "Use the buttons below to manage your information.", "\n",

        "PROFILE",
        Button("View / Edit Profile", "profile"), "\n",

        "AFT PERFORMANCE",
        Button(
            "AFT Score: " + str(state.aft_points.total) + " / 500",
            "aft_score"
        ), "\n",

        "FITNESS",
        Button("View Fitness Plan", "fitness_plan"),"\n",

        "TRAINING",
        Button("View Training Calendar", "calendar"),"\n",
    ])


# -------------------------
# PROFILE PAGE
# -------------------------

@route
def profile(state: State) -> Page:
    '''Goal: Display the cadet profile information form.
    Parameters: state (State), containing the current profile information.
    Returns: A page with editable profile fields.'''

    return Page(state, [
        "CADET PROFILE",
        "--------------------------------",

        "Enter or update your information below.", "\n",

        "Age:",
        TextBox("age", state.profile.age, "number"),"\n",

        "Gender:",
        SelectBox(
            "gender",
            ["Male", "Female"],
            state.profile.gender
        ),"\n",

        "School:",
        TextBox("school", state.profile.school),"\n",

        "Class Year:",
        SelectBox(
            "class_year",
            ["MS1", "MS2", "MS3", "MS4"],
            state.profile.class_year
        ),"\n",

        "Ranger Challenge:",
        SelectBox(
            "ranger_challenge",
            ["Yes", "No"],
            "Yes" if state.profile.ranger_challenge else "No"
        ), "\n",

        "--------------------------------",

        Button("Save Profile", "save_profile"),
        Button("Back to Home", "index")
    ])


@route
def save_profile(
    state: State,
    age: int,
    gender: str,
    school: str,
    class_year: str,
    ranger_challenge: str
) -> Page:
    '''Goal: Save the information entered into the profile form.
    Parameters: state, age, gender, school, class_year, and ranger_challenge.
    Returns: The home page with the updated profile saved.'''

    state.profile = Profile(
        age,
        gender,
        school,
        class_year,
        ranger_challenge == "Yes"
    )

    return index(state)


# -------------------------
# AFT AGE GROUP
# -------------------------

def get_age_group(age: int) -> str:
    '''Goal: Determine the AFT scoring age group for a cadet.
    Parameters: age (int), representing the cadet's age in years.
    Returns: The age-group category used by the AFT scoring tables.'''

    if age <= 21:
        return "17-21"
    elif age <= 26:
        return "22-26"
    elif age <= 31:
        return "27-31"
    elif age <= 36:
        return "32-36"
    elif age <= 41:
        return "37-41"
    elif age <= 46:
        return "42-46"
    elif age <= 51:
        return "47-51"
    elif age <= 56:
        return "52-56"
    elif age <= 61:
        return "57-61"
    else:
        return "Over 62"


# -------------------------
# AFT SCORING FUNCTIONS
# -------------------------

def get_event_points(
    profile: Profile,
    result: int,
    scoring_table: dict,
    higher_is_better: bool
) -> int:
    '''Goal: Find the AFT points earned for one event.
    Parameters: profile, result, scoring_table, and higher_is_better.
    Returns: The number of points earned for the event.'''

    age_range = get_age_group(profile.age)
    gender = profile.gender.strip().lower()

    if age_range not in scoring_table or gender not in scoring_table[age_range]:
        raise ValueError(
            "Profile age or gender does not match the AFT scoring tables."
        )

    for points, required in scoring_table[age_range][gender]:

        if higher_is_better and result >= required:
            return points

        elif not higher_is_better and result <= required:
            return points

    return 0


def deadlift_score(profile: Profile, deadlift: int) -> int:
    '''Goal: Calculate the points earned on the deadlift event.
    Parameters: profile (Profile) and deadlift (int), the event result.
    Returns: The deadlift points earned.'''

    return get_event_points(profile, deadlift, DEADLIFT_TABLE, True)


def hrp_score(profile: Profile, hrp: int) -> int:
    '''Goal: Calculate the points earned on hand-release pushups.
    Parameters: profile (Profile) and hrp (int), the event result.
    Returns: The hand-release pushup points earned.'''

    return get_event_points(profile, hrp, HRP_TABLE, True)


def sprint_drag_carry_score(
    profile: Profile,
    sprint_drag_carry: int
) -> int:
    '''Goal: Calculate the points earned on the sprint-drag-carry.
    Parameters: profile (Profile) and sprint_drag_carry (int), in seconds.
    Returns: The sprint-drag-carry points earned.'''

    return get_event_points(
        profile,
        sprint_drag_carry,
        SDC_TABLE,
        False
    )


def plank_score(profile: Profile, plank: int) -> int:
    '''Goal: Calculate the points earned on the plank event.
    Parameters: profile (Profile) and plank (int), the time in seconds.
    Returns: The plank points earned.'''

    return get_event_points(profile, plank, PLANK_TABLE, True)


def run_score(profile: Profile, run: int) -> int:
    '''Goal: Calculate the points earned on the two-mile run.
    Parameters: profile (Profile) and run (int), the time in seconds.
    Returns: The two-mile run points earned.'''

    return get_event_points(profile, run, RUN_TABLE, False)


# -------------------------
# CALCULATE TOTAL AFT SCORE
# -------------------------

def calculate_aft_points(
    profile: Profile,
    results: AFT_score
) -> AFT_points:
    '''Goal: Calculate the points earned across all five AFT events.
    Parameters: profile (Profile) and results (AFT_score), the cadet data.
    Returns: An AFT_points object containing event points and total points.'''

    deadlift_points = deadlift_score(
        profile,
        results.deadlift
    )

    hrp_points = hrp_score(
        profile,
        results.hrp
    )

    sprint_drag_carry_points = sprint_drag_carry_score(
        profile,
        results.sprint_drag_carry
    )

    plank_points = plank_score(
        profile,
        results.plank
    )

    run_points = run_score(
        profile,
        results.run
    )

    total = (
        deadlift_points
        + hrp_points
        + sprint_drag_carry_points
        + plank_points
        + run_points
    )

    return AFT_points(
        deadlift=deadlift_points,
        hrp=hrp_points,
        sprint_drag_carry=sprint_drag_carry_points,
        plank=plank_points,
        run=run_points,
        total=total
    )


# -------------------------
# TIME CONVERSION
# -------------------------

def time_to_seconds(time: str) -> int:
    '''Goal: Convert a minutes-and-seconds time into total seconds.
    Parameters: time (str), formatted as minutes:seconds.
    Returns: The total time in seconds as an integer.'''

    minutes, seconds = time.split(":")

    minutes = int(minutes)
    seconds = int(seconds)

    if seconds < 0 or seconds >= 60 or minutes < 0:
        raise ValueError("Enter time in minutes:seconds format.")

    return minutes * 60 + seconds


# -------------------------
# CALCULATE SCORE ROUTE
# -------------------------

@route
def calculate_score(
    state: State,
    deadlift: int,
    hrp: int,
    sprint_drag_carry: str,
    plank: str,
    run: str
) -> Page:
    '''Goal: Save AFT results and calculate the cadet's total score.
    Parameters: state, deadlift, hrp, sprint_drag_carry, plank, and run.
    Returns: A page displaying the calculated AFT event and total scores.'''

    if state.profile.age <= 0 or state.profile.gender == "":
        return Page(state, [
            "PROFILE INFORMATION REQUIRED",
            "Please enter your age and gender before calculating your score.",
            Button("Go to Profile", "profile"),
            Button("Back to AFT Score", "aft_score")
        ])

    try:
        state.aft_score.deadlift = deadlift
        state.aft_score.hrp = hrp

        state.aft_score.sprint_drag_carry = time_to_seconds(
            sprint_drag_carry
        )

        state.aft_score.plank = time_to_seconds(plank)

        state.aft_score.run = time_to_seconds(run)

        state.aft_points = calculate_aft_points(
            state.profile,
            state.aft_score
        )

    except ValueError as error: #This introduces error handling, which allows the program to respond when an operation fails instead of crashing.
        return Page(state, [
            "UNABLE TO CALCULATE SCORE",
            str(error),
            "Check your profile information and time entries.",
            Button("Back to Profile", "profile"),
            Button("Back to AFT Score", "aft_score")
        ])

    return Page(state, [
        "AFT SCORE RESULTS",
        "--------------------------------",

        "Deadlift: " + str(state.aft_points.deadlift), "\n",
        "Hand Release Pushups: " + str(state.aft_points.hrp),  "\n",
        "Sprint Drag Carry: " + str(state.aft_points.sprint_drag_carry), "\n",
        "Plank: " + str(state.aft_points.plank), "\n",
        "2 Mile Run: " + str(state.aft_points.run), "\n",

        "--------------------------------",

        "TOTAL SCORE: " + str(state.aft_points.total) + " / 500", "\n",

        Button("View Fitness Plan", "fitness_plan"),
        Button("Back to AFT Score", "aft_score"),
        Button("Home", "index")
    ])


# -------------------------
# AFT SCORE PAGE
# -------------------------

@route
def aft_score(state: State) -> Page:
    '''Goal: Display the form for entering AFT event results.
    Parameters: state (State), containing the saved AFT results.
    Returns: A page with input fields for all five AFT events.'''

    return Page(state, [
        "ARMY FITNESS TEST",
        "--------------------------------",

        "Enter your event results below.", "\n",

        "3 Rep Max Deadlift (pounds)",
        TextBox(
            "deadlift",
            state.aft_score.deadlift,
            "number"
        ),"\n",

        "Hand Release Pushups (repetitions)",
        TextBox(
            "hrp",
            state.aft_score.hrp,
            "number"
        ),"\n",

        "Sprint Drag Carry (minutes:seconds)",
        TextBox(
            "sprint_drag_carry",
            "0:00",
            "text"
        ),"\n",

        "Plank (minutes:seconds)",
        TextBox(
            "plank",
            "0:00",
            "text"
        ),"\n",

        "2 Mile Run (minutes:seconds)",
        TextBox(
            "run",
            "00:00",
            "text"
        ),"\n",

        "--------------------------------",

        Button("Calculate AFT Score", "calculate_score"),
        Button("Back to Home", "index")
    ])


# -------------------------
# FITNESS PLAN PAGE
# -------------------------

@route
def fitness_plan(state: State) -> Page:
    '''Goal: Create fitness recommendations from the AFT event scores.
    Parameters: state (State), containing the cadet's AFT results.
    Returns: A page displaying strongest events and areas to improve.'''

    if (
        state.aft_score.deadlift == 0
        and state.aft_score.hrp == 0
        and state.aft_score.sprint_drag_carry == 0
        and state.aft_score.plank == 0
        and state.aft_score.run == 0
    ):
        return Page(state, [
            "FITNESS PLAN",
            "--------------------------------",

            "You must enter and calculate your AFT scores first.",

            Button("Enter AFT Scores", "aft_score"),
            Button("Back to Home", "index")
        ])

    event_scores = [
        ("Deadlift", state.aft_points.deadlift),
        ("HRP", state.aft_points.hrp),
        ("Sprint Drag Carry", state.aft_points.sprint_drag_carry),
        ("Plank", state.aft_points.plank),
        ("2 Mile Run", state.aft_points.run)
    ]
#     The program sorts the event scores using the second item in each tuple rather than sorting the entire tuple alphabetically.
    sorted_scores = sorted(
        event_scores,
        key=lambda x: x[1] #A lambda function creates a small, unnamed function inside another function call.
    )

    worst_events = sorted_scores[:2]
    best_events = sorted_scores[-2:][::-1]

    state.fitness_plan.best_events = best_events
    state.fitness_plan.worst_events = worst_events

    recommendations = {
        "Deadlift": "Practice proper lifting technique and develop strength.",
        "HRP": "Work on upper-body pushing strength and controlled technique.",
        "Sprint Drag Carry": "Develop acceleration, agility, and conditioning.",
        "Plank": "Improve core stability and maintain proper technique.",
        "2 Mile Run": "Build aerobic endurance and practice consistent pacing."
    }

    program = [
        "Workout 1: Focus on " + worst_events[0][0] +
        ". " + recommendations[worst_events[0][0]],

        "Workout 2: Focus on " + worst_events[1][0] +
        ". " + recommendations[worst_events[1][0]],

        "Workout 3: Maintain " + best_events[0][0] +
        " and " + best_events[1][0] +
        " with regular technique practice and balanced training.",

        "Recovery: Include rest days and appropriate recovery between sessions."
    ]

    state.fitness_plan.workout_program = program

    page_content = [
        "FITNESS PLAN",
        "--------------------------------",

        "YOUR TWO STRONGEST EVENTS","\n",
    ]

    for event, points in best_events:
        page_content.append(
            event + ": " + str(points) + " points"
        )

    page_content.append("--------------------------------")
    page_content.append("\n")
    page_content.append("YOUR TWO EVENTS TO IMPROVE")

    for event, points in worst_events:
        page_content.append(
            event + ": " + str(points) + " points"
        )
    page_content.append("\n")
    page_content.append("--------------------------------")
    page_content.append("\n")
    page_content.append("RECOMMENDED TRAINING FOCUS")

    for workout in program:
        page_content.append(workout)

    page_content.append("\n")
    page_content.append("--------------------------------")
    page_content.append("\n")
    page_content.append(Button("Back to Home", "index"))
    page_content.append(Button("Back to AFT Score", "aft_score"))

    return Page(state, page_content)


# -------------------------
# WEEKLY TRAINING SCHEDULE
# -------------------------

def get_calendar_activity(year: int, month: int, day: int) -> str:
    '''Goal: Determine the scheduled activity for a calendar date.
    Parameters: year, month, and day (int), identifying the date.
    Returns: The activity description scheduled for that date.'''

    weekday = cal.weekday(year, month, day)

    weekly_schedule = {
        0: "Morning PT - Short Intervals - Workout 1",
        1: "Recovery / No Scheduled PT",
        2: "PT - 4 Mile Ruck",
        3: "PT - Long Distance Intervals - Workout 2",
        4: "Rest Day",
        5: "Workout Day- Workout 3",
        6: "Rest Day"
    }

    return weekly_schedule[weekday]


# -------------------------
# NEXT MONTH
# -------------------------

@route
def next_month(state: State) -> Page:
    '''Goal: Move the training calendar forward by one month.
    Parameters: state (State), containing the current calendar month and year.
    Returns: The calendar page displaying the next month.'''

    state.calendar.month += 1

    if state.calendar.month > 12:
        state.calendar.month = 1
        state.calendar.year += 1

    return calendar(state)


# -------------------------
# PREVIOUS MONTH
# -------------------------

@route
def previous_month(state: State) -> Page:
    '''Goal: Move the training calendar backward by one month.
    Parameters: state (State), containing the current calendar month and year.
    Returns: The calendar page displaying the previous month.'''

    state.calendar.month -= 1

    if state.calendar.month < 1:
        state.calendar.month = 12
        state.calendar.year -= 1

    return calendar(state)


# -------------------------
# CALENDAR PAGE
# -------------------------

@route
def calendar(state: State) -> Page:
    '''Goal: Display the monthly ROTC training calendar and PT schedule.
    Parameters: state (State), containing the selected month and year.
    Returns: A calendar page with scheduled activities for each date.'''

    month = state.calendar.month
    year = state.calendar.year

    month_dates = cal.monthcalendar(year, month)

    calendar_rows = [
        [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
        ]
    ]

    for week in month_dates:
        calendar_row = []

        for day in week:

            if day == 0:
                calendar_row.append("")

            else:
                activity = get_calendar_activity(
                    year,
                    month,
                    day
                )

                message = (
                    str(day)
                    + "\n"
                    + activity
                )

                calendar_row.append(message)

        calendar_rows.append(calendar_row)

    weekly_schedule_rows = [
        ["Day", "Scheduled Activity"],
        ["Monday", "Morning PT - Short Intervals - Workout 1"],
        ["Tuesday", "Recovery / No Scheduled PT"],
        ["Wednesday", "PT - 4 Mile Ruck"],
        ["Thursday", "PT - Long Distance Intervals - Workout 2"],
        ["Friday", "Rest Day"],
        ["Saturday", "Workout 3"],
        ["Sunday", "Rest Day"]
    ]

    return Page(state, [
        "ROTC TRAINING CALENDAR",
        "--------------------------------",

        cal.month_name[month] + " " + str(year),

        Button("Previous Month", "previous_month"),
        Button("Next Month", "next_month"),

        "MONTHLY TRAINING CALENDAR",
        Table(calendar_rows),

        "--------------------------------",

        "WEEKLY TRAINING SCHEDULE",
        Table(weekly_schedule_rows),

        Button("Back to Home", "index")
    ])


# -------------------------
# START SERVER
# -------------------------

start_server(State())


