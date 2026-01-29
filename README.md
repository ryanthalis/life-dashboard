# Life Dashboard

A command-line Python application for tracking workouts and study sessions.

## Features
- Log workouts (date, exercise, sets)
- Log study sessions (date, topic, minutes)
- View all entries grouped by date
- View daily totals for workouts and study time
- Automatically saves and loads data from a local file

## How to Run

1. Clone the repository
2. Navigate to the project directory
3. Run the program using Python:

```bash
python life_tracker.py


## Example Output

2025-11-23
  1. Kelso Shrug — 2 sets
  2. Incline Press — 3 sets
  Total: 5 sets

2025-11-24
  1. Unilateral Calf Raise — 3 sets
  2. Stiff-Leg Deadlift — 1 set
  Total: 4 sets

## Design Decisions
- Data is stored in a local text file to keep the project simple and portable.
- Entries are grouped by date to improve readability and make daily activity easier to review.
- Helper functions are used to separate data processing from user interface logic.
- The program automatically creates required data files to reduce setup friction.

## Future Improvements
- Replace text file storage with SQLite for more robust data management.
- Add filtering by date range (weekly or monthly summaries).
- Add summary statistics per exercise or study topic.
