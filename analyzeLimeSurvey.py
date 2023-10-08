import config
import csv
from datetime import datetime, timedelta

def analyzeLimeSurvey(filename):
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)

        next(csvreader)  # skip header row

        for row in csvreader:

            if len(row) > 0:
                token = row[4]
                date = row[1]
                gender = row[55]
                age = row[54]
                ilsDuration = float(row[58]) + float(row[70]) + float(row[82]) + float(row[94])
                # Convert to minutes and seconds
                minutes = int(ilsDuration // 60)  # Whole minutes
                remaining_seconds = int(ilsDuration % 60)  # Remaining seconds as an integer
                # Create a string in the format "minutes:seconds"
                ilsDuration = f"{minutes:02}:{remaining_seconds:02}"

                if row[1] and row[5]:
                    limeStartTime = datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')
                    submit_time = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                    time_taken = submit_time - limeStartTime
                else:
                    time_taken = "Not submitted"

                # Retrieving time participant completed 4 questions group to move on and complete tasks

                # Time duration to add
                minutes, seconds = map(int, ilsDuration.split(':'))
                duration = timedelta(minutes=minutes, seconds=seconds)

                # Add the duration to the original time
                ilsCompleteTime = limeStartTime + duration

                # Format the result as a string
                ilsCompleteTime = ilsCompleteTime.strftime('%Y-%m-%d %H:%M:%S')

                # Reset scores and set names for each row
                set_names = []
                scores = []
                for i in range(0, 4):
                    scores.append(0)

                # Analyze data for each set of questions
                """
                i starts at column 7 because that is where the first question of the ILS questionnaire is present. 50 
                corresponds to the last question on the ILS questionnaire. We are processing a set of 4 questions at a 
                time during each iteration of the for loop. 

                For example, in the first iteration we are calculating the scores for columns 7-10 in the ILS data table 
                which correspond to questions 1-4 on the ILS questionnaire

                You can subtract 6 from each column number to get the actual question number on the ILS questionnaire

                7 - Active/Reflective
                8 - Sensing/Intuitive
                9 - Visual/Verbal
                10 - Sequential/Global

                """
                for i in range(7, 50, 4):
                    # Active/Reflective
                    if row[i] == '1':
                        scores[0] += 1
                    elif row[i] == '2':
                        scores[0] -= 1

                    # Sensing/Intuitive
                    if row[i + 1] == '1':
                        scores[1] += 1
                    elif row[i + 1] == '2':
                        scores[1] -= 1

                    # Visual/Verbal
                    if row[i + 2] == '1':
                        scores[2] += 1
                    elif row[i + 2] == '2':
                        scores[2] -= 1

                    # Sequential/Global
                    if row[i + 3] == '1':
                        scores[3] += 1
                    elif row[i + 3] == '2':
                        scores[3] -= 1

                output_row = [date, limeStartTime, ilsDuration, ilsCompleteTime, token, time_taken, gender, age]
                output_row.extend(scores)
                config.items.append(output_row)