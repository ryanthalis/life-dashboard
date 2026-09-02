import life_core

def test_workout_parsing():

    failures = 0
    good_cases = [
                ("WORKOUT,2025-11-23, Push Day, 3", {"date": "2025-11-23", "exercise": "Push Day", "sets": 3}),
                ("WORKOUT , 2025-03-11  ,  Shoulders,  4", {"date": "2025-03-11", "exercise": "Shoulders", "sets": 4}),
                ("WORKOUT,2025-11-04,Arms,5", {"date": "2025-11-04", "exercise": "Arms", "sets": 5}),
                  ]
    
    bad_cases = [
        "STUDY,2025-11-02,File I/O,50",          
        "WORKOUT,only,three,fields",            
        "WORKOUT,2025-11-02,Arms,three",        
        "WORKOUT,2025-11-02,Arms,0",            
    ]


    for line, output in good_cases:
        try:
            result = life_core.parse_workout_line(line)
            assert isinstance(result, dict), ("parse_workout_line" + repr(line) + "should return dict, got " + type(result).__name__)
        except Exception: 
            failures += 1
        
        try: 
            result = life_core.parse_workout_line(line)
            assert result == output, ("parse_workout_line" + repr(line) + "should return dict" + repr(output) + "instead returned" + repr(result))
        except Exception:
            failures += 1
    
    for line in bad_cases:

        try:
            result = life_core.parse_workout_line(line)

            assert False,("This line(" + repr(line) + ") should not pass")
        
        except ValueError:
            pass

        except Exception:
            failures += 1                         
    
    return failures



def main():
    print(test_workout_parsing())

if __name__ == "__main__":
    main()