import db
import datetime as dt



def menu():
    print("[1] Add Workout")
    print("[2] Add Study")
    print("[3] View All Entries")
    print("[4] View Summary")
    print("[5] Update Entry")
    print("[6] Exit")

def menu2():
    print("[1] View Workouts")
    print("[2] View Study sessions")


def get_int(
    prompt: str,
    min_value: int = 1,
    max_value: int | None = None,
) -> int:
    while True:
        try:
            x = int(input(prompt).strip())
            print()

            if x < min_value:
                print(f"number has to be greater than or equal to {min_value}")
                continue

            if max_value is not None:
                if x > max_value:
                    print(f"number has to be smaller than or equal to {max_value}")
                    continue

        except ValueError:
            print("incorrect value try again")
            continue

        return x


def get_summary(workouts, studies):

    total_workouts = 0
    total_study_sessions = 0
    total_sets = 0
    total_minutes = 0 
    topics = set() 

    for number_workouts in workouts:
        total_workouts += 1
        sets = number_workouts["quantity"]
        total_sets += sets

    for number_study in studies:
        total_study_sessions += 1
        mins = number_study["quantity"]
        topic = number_study["label"]
        topics.add(topic)
        total_minutes += mins
    
    return (total_workouts, total_study_sessions, total_sets, total_minutes, topics)

def group_by_date(entries):
    grouped = {}
    for entry in entries:
        date = entry["entry_date"]
        if date not in grouped:
            grouped[date] = []
        grouped[date].append(entry)
    return grouped


def print_workouts_grouped(workouts):
    
    if len(workouts) ==  0:
        print("No Workouts Logged yet")
        return
    
    grouped = group_by_date(workouts)

    for keys in grouped:
        date = keys
        print(f"{date}")
        total_sets = 0
        for line, lifts in enumerate(grouped[date], start=1):
            exercises = lifts["label"] 
            sets = lifts["quantity"]
            total_sets += int(sets)
            entry_id = lifts["id"]
            print(f"{line}. [ID {entry_id}] {exercises} {sets} sets")
        print(f"Total: {total_sets} sets")

def print_studies_grouped(studies):
    
    if len(studies) ==  0:
        print("No study sessions Logged yet")
        return
    
    grouped = group_by_date(studies)

    for keys in grouped:
        date = keys
        print(f"{date}")
        total_mins = 0
        for line, sesh in enumerate(grouped[date], start=1):
            subjects = sesh["label"] 
            mins = sesh["quantity"] 
            total_mins += int(mins)
            entry_id = sesh["id"]

            print(f"{line}. [ID {entry_id}] {subjects} {mins} minutes")

        print(f"Total: {total_mins} minutes")

def get_nonempty(prompt: str) -> str:

    while True:
        value = input(prompt)

        if value.strip() == "":
            print("Input must not be empty ")
            continue

        return value.strip()

def get_date(prompt: str) -> str:

    while True:
        date = input(prompt).strip()

        try:
            date_val = dt.date.fromisoformat(date)
            parse_date = date_val.isoformat()
            if parse_date == date:
                return parse_date
            else:
                print("Invalid format, enter date again")
                continue

        except ValueError:
            print("Invalid format, enter date again")
            continue

def main():
    db.init_db()

    while True:
        print()
        menu()
        option = get_int("please choose an option from between 1-6: ", 1, 6)
        print()       

        if option == 1:
            print("You have chosen to log a workout")
            date_value = get_date("Please enter the date of your workout (yyyy-mm-dd): ")
            exercise_value = get_nonempty("Please enter the exercise: ")
            sets_value = get_int("Please enter the number of sets: ")
            notes = input("please enter any relevant notes: ")

            db.add_entry(date_value, "workout", exercise_value, sets_value, notes)

            print("workout added")
        
        elif option == 2:
            print("You have chosen to log a study session")
            study_date = get_date("Please enter the date of your study session (yyyy-mm-dd): ")
            study_subject = get_nonempty("Please enter the subject of study: ")
            study_minutes = get_int("Please enter how long you studied for in minutes")
            notes = input("please enter any relevant notes: ")


            db.add_entry(study_date, "study", study_subject, study_minutes, notes)

            print("study session added ")
        
        elif option == 3:
            print()
            print("You have chosen to view all entries")
            print()
            menu2()
            option_workout_study = 0
        
            while True:

                option_workout_study = get_int(
                    "please choose an option from between 1-2: ", 1, 2
                )
            
                if option_workout_study == 1:
                    workouts = db.get_entries("workout")

                    print_workouts_grouped(workouts)                
                    break
                
                elif option_workout_study == 2:
                    studies = db.get_entries("study")

                    print_studies_grouped(studies)
                    break
                

        elif option == 4:
            workouts = db.get_entries("workout")
            studies = db.get_entries("study")

            values = get_summary(workouts, studies)
            a, b, c, d ,e = values
            print(f"total number of workouts: {a}\ntotal number of study sessions: {b}\ntotal number of sets: {c}\ntotal study minutes: {d}\ntopics studied: {e}")
                
        elif option == 5:
            entry_id = get_int("Enter ID of entry to be updated: ")
            row = db.get_entry(entry_id)
            if row is None:
                print("Entry not found")
                continue
            print(
                f"Date: {row['entry_date']}, Category: {row['category']}, "
                f"label: {row['label']}, Quantity: {row['quantity']}, "
                f"Notes: {row['notes']}"
            )

            new_date = get_date("Enter the new date (yyyy-mm-dd): ")
            new_label = get_nonempty("Enter the new label: ")
            new_quantity = get_int("Enter the new quantity: ")
            new_notes = input("Enter the new notes: ").strip()

            updated = db.update_entry(
                entry_id,
                new_date,
                row["category"],
                new_label,
                new_quantity,
                new_notes,
            )

            if updated:
                print("Entry updated")
            else:
                print("Entry could not be updated")

        elif option == 6:
            print("You will now exit the program")
            break

if __name__ == "__main__":
    main()
