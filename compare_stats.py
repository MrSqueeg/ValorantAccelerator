import json

def compare_stats(user_stats, average_stats):
    print("\nComparing User Stats\n")
    try:
        with open(user_stats, 'r') as user, open(average_stats, 'r') as average:
            user_data = json.load(user)
            average_data = json.load(average)
            for field in user_data:
                if field in average_data:
                    try:
                        # Add fields and specifics here
                        #  - Maybe AI stuff later.
                        difference = user_data[field] - average_data[field]
                        print(f"user_data {user_data[field]} - average_data {average_data[field]} = difference {difference}")
                        if field == 'Legshot Rate' or 'Bodyshot Rate':
                            difference *= -1
                            
                        print(f"difference {difference}")
                        if difference <= 0:
                            print(f"work on {field}")
                        else:
                            print(f"good job {field}")
                    except (ValueError, TypeError):
                        print(f"field not a number")
                        continue
                else:
                    print(f"Field not in average")

    except Exception as e:
        print(e)