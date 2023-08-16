import config
import os
import csv
import math
# Using libraries below to parse the Testable URL and quickly retireve the token
from urllib.parse import urlparse, parse_qs
import pandas as pd


def analyzeNBack():
    # Replace 'input_file.csv' with the actual filename of your input CSV file
    input_file = f"N-Back/795217_230317_000401.csv"

    """# Read the input CSV file and store its contents in a list
        with open(input_file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)"""

    # Getting list of all files in the N-Back data folder
    files = os.listdir("N-Back")
    fileNames = []
    for name in files:
        if name.endswith('.csv'):
            file_path = os.path.join("N-Back", name)
        fileNames.append(file_path)

    for a in config.items:
        i = 0
        # Define the token from our global items list
        token = a[1]
        found = False
        twoBackDemoHitRate = 0
        threeBackDemoHitRate = 0
        twoBackHitRate = 0
        threeBackHitRate = 0
        twoBackDemoFalseAlarm = 0
        threeBackDemoFalseAlarm = 0
        twoBackFalseAlarm = 0
        threeBackFalseAlarm = 0
        twoBackDemoAccuracy = 0
        twoBackDemoOmission = 0
        threeBackDemoOmission = 0
        twoBackOmission = 0
        threeBackOmission = 0
        demoSensitivity = 0
        sensitivity = 0
        # Defining correct non-response variables
        twoBackDemoCNR = 0
        # Loop through each csv file until we find the one with the token in the items array
        while not found and i < len(fileNames):
            # Open the CSV file and read the token
            with open(fileNames[i], 'r') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)

                # Extract the header row and data row
                header_row = data[0]
                data_row = data[1]
                url = data_row[7]

                # Parse the URL to extract the query parameters
                parsedUrl = urlparse(url)

                # Get the value of the 'token' parameter
                csvTokenValue = parse_qs(parsedUrl.query).get('token', [None])[0]

                if csvTokenValue == token:
                    print("File with defined token found!")
                    print("Token is: ", csvTokenValue)

                    # Read the CSV file and skip the first 3 rows
                    data = pd.read_csv(fileNames[i], skiprows=3)

                    for index, row in data.iterrows():
                        """Calculating demo hit rate for 2-back (correct answers will have a '1' in the correct cell
                            and a 'C' in their label"""
                        if row[data.columns.get_loc("correct")] == 1 and \
                                '2' in str(row[data.columns.get_loc("label")]) and \
                                'p' in str(row[data.columns.get_loc("label")]) and \
                                'C' in str(row[data.columns.get_loc("label")]):
                            twoBackDemoHitRate += 1

                        """Calculating demo hit rate for 3-back (correct answers will have a '1' in the correct cell
                            and a 'C' in their label"""
                        if row[data.columns.get_loc("correct")] == 1 and \
                                '3' in str(row[data.columns.get_loc("label")]) and \
                                'p' in str(row[data.columns.get_loc("label")]) and \
                                'C' in str(row[data.columns.get_loc("label")]):
                            threeBackDemoHitRate += 1

                        """Calculating test 2-back hit rate (correct answers will have a '1' in the correct cell
                            and a 'C' in their label"""
                        if row[data.columns.get_loc("correct")] == 1 and \
                                '2' in str(row[data.columns.get_loc("label")]) and \
                                't' in str(row[data.columns.get_loc("label")]) and \
                                'C' in str(row[data.columns.get_loc("label")]):
                            twoBackHitRate += 1

                        """Calculating test 3-back hit rate (correct answers will have a '1' in the correct cell
                            and a 'C' in their label"""
                        if row[data.columns.get_loc("correct")] == 1 and \
                                '3' in str(row[data.columns.get_loc("label")]) and \
                                't' in str(row[data.columns.get_loc("label")]) and \
                                'C' in str(row[data.columns.get_loc("label")]):
                            threeBackHitRate += 1

                        # Calculating false alarm rate for 2-back demo trials
                        if row[data.columns.get_loc("correct")] == 1 and \
                                '2' in str(row[data.columns.get_loc("label")]) and \
                                'p' in str(row[data.columns.get_loc("label")]) and \
                                'C' not in str(row[data.columns.get_loc("label")]):
                            twoBackDemoFalseAlarm += 1

                        # Calculating false alarm rate for 3-back demo trials
                        if row[data.columns.get_loc("correct")] == 1 and \
                                '3' in str(row[data.columns.get_loc("label")]) and \
                                'p' in str(row[data.columns.get_loc("label")]) and \
                                'C' not in str(row[data.columns.get_loc("label")]):
                            threeBackDemoFalseAlarm += 1

                        # Calculating false alarm rate for 2-back test trials
                        if row[data.columns.get_loc("correct")] == 1 and \
                                '2' in str(row[data.columns.get_loc("label")]) and \
                                't' in str(row[data.columns.get_loc("label")]) and \
                                'C' not in str(row[data.columns.get_loc("label")]):
                            twoBackFalseAlarm += 1

                        # Calculating false alarm rate for 3-back test trials
                        if row[data.columns.get_loc("correct")] == 1 and \
                                '3' in str(row[data.columns.get_loc("label")]) and \
                                't' in str(row[data.columns.get_loc("label")]) and \
                                'C' not in str(row[data.columns.get_loc("label")]):
                            threeBackFalseAlarm += 1

                        # Calculating 2-back demo twoBackOmission errors
                        if row[data.columns.get_loc("response")] == "timeout" and \
                                '2' in str(row[data.columns.get_loc("label")]) and \
                                'p' in str(row[data.columns.get_loc("label")]) and \
                                'C' in str(row[data.columns.get_loc("label")]):
                            twoBackDemoOmission += 1

                        # Calculating 3-back demo twoBackOmission errors
                        if row[data.columns.get_loc("response")] == "timeout" and \
                                '3' in str(row[data.columns.get_loc("label")]) and \
                                'p' in str(row[data.columns.get_loc("label")]) and \
                                'C' in str(row[data.columns.get_loc("label")]):
                            threeBackDemoOmission += 1

                        # Calculating 2-back test omission errors
                        if row[data.columns.get_loc("response")] == "timeout" and \
                                '2' in str(row[data.columns.get_loc("label")]) and \
                                't' in str(row[data.columns.get_loc("label")]) and \
                                'C' in str(row[data.columns.get_loc("label")]):
                            twoBackOmission += 1

                        # Calculating 3-back test omission errors
                        if row[data.columns.get_loc("response")] == "timeout" and \
                                '3' in str(row[data.columns.get_loc("label")]) and \
                                't' in str(row[data.columns.get_loc("label")]) and \
                                'C' in str(row[data.columns.get_loc("label")]):
                            threeBackOmission += 1

                        # Calculating 2-back demo correct non-response
                        if row[data.columns.get_loc("response")] == "timeout" and \
                                '2' in str(row[data.columns.get_loc("label")]) and \
                                'p' in str(row[data.columns.get_loc("label")]):
                            twoBackDemoCNR += 1

                    print(twoBackDemoHitRate + twoBackDemoFalseAlarm)
                    """Calculating 2-back demo accuracy. If the participant provided no response during the n-back
                    task, a -1 is placed in the cell"""
                    def calculateAccuracy(hitRate, falseAlarm):
                        if hitRate == 0 and falseAlarm == 0:
                            return -1
                        else:
                            return round(100 * ((hitRate - falseAlarm) / (hitRate + falseAlarm)), 1)

                    # Calculating sensitivity
                    def sensitivity(hit, false):
                        # If both hit rate and false alarms are zero, we return -1 as the sensitivity
                        if hit == 0 and false == 0:
                            return -1
                        else:
                            hitProportion = hit / (hit + false)
                            falseProportion = false / (hit + false)

                            # If either values are 0 or 1 we add or subtract 0.01 respectively
                            def zero(value):
                                return value + 0.01

                            def one(value):
                                return value - 0.01

                            case_dict = {
                                0: zero,
                                1: one
                            }

                            if hitProportion in case_dict:
                                hitProportion = case_dict[hitProportion](hitProportion)

                            if falseProportion in case_dict:
                                falseProportion = case_dict[falseProportion](falseProportion)

                            # Calculating sensitivity
                            return round(math.log(
                                (hitProportion * (1 - falseProportion)) / ((1 - hitProportion) * falseProportion)), 1)

                    # Calculating bias
                    def bias(hit, false):
                        # If both hit rate and false alarms are zero, we return -1 as the sensitivity
                        if hit == 0 and false == 0:
                            return -1
                        else:
                            hitProportion = hit / (hit + false)
                            falseProportion = false / (hit + false)

                            """If either values are 0 or 1 we add or subtract 0.01 respectively to maintain a 0-1 
                            proportion range"""
                            def zero(value):
                                return value + 0.01

                            def one(value):
                                return value - 0.01

                            case_dict = {
                                0: zero,
                                1: one
                            }

                            if hitProportion in case_dict:
                                hitProportion = case_dict[hitProportion](hitProportion)

                            if falseProportion in case_dict:
                                falseProportion = case_dict[falseProportion](falseProportion)

                            print("hit proportion: ", hitProportion)
                            print("false proportion: ", falseProportion)
                            return round(0.5 * math.log(((1 - falseProportion) * (1 - hitProportion)) / ((hitProportion) * falseProportion)), 1)

                    # Appending values into output data file
                    a.append(twoBackDemoHitRate)
                    a.append(threeBackDemoHitRate)

                    a.append(twoBackHitRate)
                    a.append(threeBackHitRate)

                    a.append(twoBackDemoFalseAlarm)
                    a.append(threeBackDemoFalseAlarm)

                    a.append(twoBackFalseAlarm)
                    a.append(threeBackFalseAlarm)

                    # Calculating accuracy. Just need to input hit rate and false alarms into the function
                    a.append(calculateAccuracy(twoBackDemoHitRate, twoBackDemoFalseAlarm))
                    a.append(calculateAccuracy(threeBackDemoHitRate, threeBackDemoFalseAlarm))

                    a.append(calculateAccuracy(twoBackHitRate, twoBackFalseAlarm))
                    a.append(calculateAccuracy(threeBackHitRate, threeBackFalseAlarm))

                    a.append(twoBackDemoOmission)
                    a.append(threeBackDemoOmission)

                    a.append(twoBackOmission)
                    a.append(threeBackOmission)

                    a.append(sensitivity(twoBackDemoHitRate, twoBackDemoFalseAlarm))
                    a.append(sensitivity(threeBackDemoHitRate, threeBackDemoFalseAlarm))
                    a.append(sensitivity(twoBackHitRate, twoBackFalseAlarm))
                    a.append(sensitivity(threeBackHitRate, threeBackFalseAlarm))

                    a.append(bias(twoBackDemoHitRate, twoBackDemoFalseAlarm))
                    a.append(bias(threeBackHitRate, threeBackDemoFalseAlarm))
                    a.append(bias(twoBackHitRate, twoBackFalseAlarm))
                    a.append(bias(threeBackHitRate, threeBackFalseAlarm))

                    a.append(twoBackDemoCNR)

                    found = True
                    fileNames.pop(i)
                else:
                    i += 1
