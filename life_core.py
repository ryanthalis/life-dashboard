def parse_workout_line(line: str) -> dict[str, str | int]:
   
    fields = [f.strip() for f in line.strip().split(",")]

    if len(fields) != 4:
        raise ValueError("WORKOUT must have 4 fields")
    
    if fields[0].strip().upper() != "WORKOUT":
        raise ValueError("not a WORKOUT line")

    try: 
        sets = int(fields[3])
    except ValueError:
            raise ValueError("WORKOUT sets must be a positive integer")

    if sets < 1:
        raise ValueError("WORKOUT sets must be greater than 1")
    
    return {"date": fields[1], "exercise": fields[2], "sets": sets}

def parse_study_line(line: str) -> dict[str, str | int]:

    fields = [f.strip() for f in line.strip().split(",")]

    if len(fields) != 4:
        raise ValueError("STUDY must have 4 fields")
    
    if fields[0].strip().upper() != "STUDY":
        raise ValueError("not a STUDY line")
    
    try: 
        mins = int(fields[3])
    except ValueError:
            raise ValueError("STUDY mins must be a positive integer")
   
    if mins < 1:
        raise ValueError("STUDY mins must be greater than 1")
    
    return {"date": fields[1], "topic": fields[2], "minutes": mins}
