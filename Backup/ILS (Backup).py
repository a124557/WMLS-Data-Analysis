import csv
import math
import os
import pandas as pd
from datetime import datetime
# Using libraries below to parse the Testable URL and quickly retireve the token
from urllib.parse import urlparse, parse_qs

output_file = "output.csv"
items = []


def analyzeLimeSurvey(filename):
    with open(filename, "r") as csvfile, open("output.csv", "a", newline="") as outfile:
        csvreader = csv.reader(csvfile)

        next(csvreader)  # skip header row

        for row in csvreader:

            if len(row) > 0:
                token = row[4]
                date = row[1]
                gender = row[55]
                age = row[54]
                if row[1] and row[5]:
                    start_time = datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')
                    submit_time = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                    time_taken = submit_time - start_time
                else:
                    time_taken = "Not submitted"

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

                output_row = [date, token, time_taken, gender, age]
                output_row.extend(scores)
                items.append(output_row)


def analyzeSymmSpan(filename):
    with open(filename, "r") as csvfile, open("output.csv", "a", newline="") as outfile:
        csvwriter = csv.writer(outfile)
        csvreader = csv.reader(csvfile)

        next(csvreader)  # skip header row
        for a in items:
            # Array which contains data to write
            token = a[1]
            # symmMeanDemo and symmMean refer to the mean reaction time for demo and test trials
            symmMeanDemo = symmTotalDemo = symmCountDemo = 0
            symmMean = symmTotal = symmCount = 0
            incorrectDemoSymmMean = incorrectDemoSymmRtTotal = incorrectDemoSymmCount = 0
            incorrectSymmMean = incorrectSymmRtTotal = incorrectSymmCount = 0
            correctDemoSymmMean = correctDemoSymmRtTotal = correctDemoSymmCount = 0
            correctSymmMean = correctSymmTotal = correctSymmCount = 0
            partialCreditDemo = spatialTotalDemo = spatialCountDemo = 0
            partialCredit = spatialTotal = spatialCount = 0
            processingTime_demo = 0
            processingTime = 0
            recallTime = 0
            recallTime_demo = 0
            speedError_demo = 0
            speedError = 0
            processingError_demo = 0
            processingError = 0
            maxDTRtDemo = 0
            maxDTRt = 0
            # We are locating the symm span file with the same token in the current row
            filename = f"Symm_Span/Symmetry_Span_{token}.csv"
            if os.path.isfile(filename):
                data = pd.read_csv(filename)
                if "browser" in data.columns:
                    browser_value = data.loc[0, "browser"]
                else:
                    browser_value = "Not detected"
                symspan_demo_score = 0
                symmspan_score = 0
                total_demo_correct = str(int(data["spatial_demo_accuracy"].sum()))
                total_correct = str(int(data["spatial_accuracy"].sum()))
                # Iterating through each row in the csv file to extract data
                for index, row in data.iterrows():
                    # Calculating absolute block recall accuracy for demo and test trials
                    if row[data.columns.get_loc("trial_type")] == "spatial-span-recall-demo" and \
                            row[data.columns.get_loc("spatial_demo_accuracy")] == row[data.columns.get_loc("set_size")]:
                        symspan_demo_score += row[data.columns.get_loc("spatial_demo_accuracy")]
                    if row[data.columns.get_loc("trial_type")] == "spatial-span-recall" and \
                            row[data.columns.get_loc("spatial_accuracy")] == row[data.columns.get_loc("set_size")]:
                        symmspan_score += row[data.columns.get_loc("spatial_accuracy")]
                    # RT mean on demo distractor tasks
                    try:
                        if row[data.columns.get_loc("symm_demo_accuracy")] in [0, 1] or row[
                            data.columns.get_loc("symm_fulldemo_accuracy")] in [0, 1]:
                            symmCountDemo += 1
                            symmTotalDemo += row[0]
                    except KeyError:
                        print("Column not found. Skipping")
                    # RT mean on test distractor tasks
                    try:
                        if row[data.columns.get_loc("symm_accuracy")] in [0, 1]:
                            symmCount += 1
                            symmTotal += row[0]
                    except KeyError:
                        print("Column not found. Skipping")
                    # RT incorrect on demo distractor tasks
                    try:
                        if row[data.columns.get_loc("symm_demo_accuracy")] == 0 or \
                                row[data.columns.get_loc("symm_fuulldemo_accuracy")] == 0:
                            incorrectDemoSymmCount += 1
                            incorrectDemoSymmRtTotal += row[0]
                    except KeyError:
                        print("Column not found. Skipping")
                    # RT incorrect on test distractor tasks
                    try:
                        if row[data.columns.get_loc("symm_accuracy")] == 0:
                            incorrectSymmCount += 1
                            incorrectSymmRtTotal += row[0]
                    except KeyError:
                        print("Column not found. Skipping")
                    # RT correct on demo distractor tasks
                    try:
                        if row[data.columns.get_loc("symm_demo_accuracy")] == 1 or \
                                row[data.columns.get_loc("symm_fuulldemo_accuracy")] == 1:
                            correctDemoSymmCount += 1
                            correctDemoSymmRtTotal += row[0]
                    except KeyError:
                        print("Column not found. Skipping")
                    # RT correct on test distractor tasks
                    try:
                        if row[data.columns.get_loc("symm_accuracy")] == 1:
                            correctSymmCount += 1
                            correctSymmTotal += row[0]
                    except KeyError:
                        print("Column not found. Skipping")
                    # Calculating demo partial-credit scores
                    if not pd.isna(row[data.columns.get_loc("spatial_demo_accuracy")]):
                        spatialCountDemo += 1
                        spatialTotalDemo += row[data.columns.get_loc("spatial_demo_accuracy")] / row[
                            data.columns.get_loc("set_size")]
                    # Calculating partial-credit scores
                    if not pd.isna(row[data.columns.get_loc("spatial_accuracy")]):
                        spatialCount += 1
                        spatialTotal += row[data.columns.get_loc("spatial_accuracy")] / row[
                            data.columns.get_loc("set_size")]
                    # Processing time response (time taken on symmetry judgements both practice)
                    try:
                        if row[data.columns.get_loc("trial_type")] in ["symmetry-judgement-task-demo",
                                                                       "symmetry-judgement-task-fulldemo"] \
                                and not pd.isna(row[0]):
                            processingTime_demo += row[0]
                    except KeyError:
                        print("Column not found. Skipping")
                    # Processing response time for test trials (time taken on symmetry judgement test trials)
                    try:
                        if row[data.columns.get_loc("trial_type")] in ["symmetry-judgement-task"] \
                                and not pd.isna(row[0]):
                            processingTime += row[0]
                    except KeyError:
                        print("Column not found. Skipping")
                    # Maximum response time on demo distractor tasks
                    try:
                        if row[data.columns.get_loc("trial_type")] in ["symmetry-judgement-task-demo"] or \
                                row[data.columns.get_loc("trial_type")] in ["symmetry-judgement-task-fulldemo"]:
                            maxDTRtDemo = max(row[0], maxDTRtDemo)
                    except KeyError:
                        print("Column not found. Skipping")
                    # Maximum response time on test distractor tasks
                    try:
                        if row[data.columns.get_loc("trial_type")] in ["symmetry-judgement-task"]:
                            maxDTRt = max(row[0], maxDTRt)
                    except KeyError:
                        print("Column not found. Skipping")
                    # Recall response times (time taken during recall component of working memory task in practice trials only)
                    try:
                        if row[data.columns.get_loc("trial_type")] in ["spatial-span-recall-demo"] \
                                and not pd.isna(row[0]):
                            recallTime_demo += row[0]
                    except KeyError:
                        print("Column not found. Skipping")
                    # Recall response times (time taken during recall commponent of working memory task in test trials only)
                    try:
                        if row[data.columns.get_loc("trial_type")] in ["spatial-span-recall"] \
                                and not pd.isna(row[0]):
                            recallTime += row[0]
                    except KeyError:
                        print("Column not found. Skipping")
                    # Total speed errors for processing component (demos only)
                    try:
                        if (row[data.columns.get_loc("trial_type")] == "symmetry-judgement-task-demo" and pd.isna(
                                row[data.columns.get_loc("symm_demo_accuracy")])) or \
                                (row[data.columns.get_loc(
                                    "trial_type")] == "symmetry-judgement-task-fulldemo" and pd.isna(
                                    row[data.columns.get_loc("symm_fulldemo_accuracy")])):
                            speedError_demo += 1
                    except KeyError:
                        print("Column not found. Skipping")
                    # Total speed errors for processing component (test trials only)
                    try:
                        if row[data.columns.get_loc("trial_type")] == "symmetry-judgement-task" and pd.isna(
                                row[data.columns.get_loc("symm_accuracy")]):
                            speedError += 1
                    except KeyError:
                        print("Column not found. Skipping")
                    # Total accuracy errors for processing component (demos only)
                    try:
                        if row[data.columns.get_loc("symm_demo_accuracy")] == 0 or \
                                row[data.columns.get_loc("symm_fulldemo_accuracy")] == 0:
                            processingError_demo += 1
                    except KeyError:
                        print("Column not found. Skipping")
                    # Total accuracy errors for processing component (test trials only)
                    try:
                        if row[data.columns.get_loc("symm_accuracy")] == 0 or row[
                            data.columns.get_loc("symm_accuracy")] == "":
                            processingError += 1
                    except KeyError:
                        print("Column not found. Skipping")
                print(symmTotalDemo, " ", symmCountDemo)
                symmMeanDemo = symmTotalDemo / symmCountDemo
                symmMean = symmTotal / symmCount
                # If/else statements checking if all demo/test distractor answers are incorrect. If so, we add -1 into the cell
                if correctDemoSymmCount == 0:
                    correctDemoSymmMean = -1
                else:
                    correctDemoSymmMean = round(correctDemoSymmRtTotal / correctDemoSymmCount)

                if correctSymmCount == 0:
                    correctSymmMean = -1
                else:
                    correctSymmMean = round(correctDemoSymmRtTotal / correctDemoSymmCount)
                # If/else statements checking if all demo/test distractor answers are correct. If so, we add -1 into the cell
                if incorrectDemoSymmCount == 0:
                    incorrectDemoSymmMean = -1
                else:
                    incorrectDemoSymmMean = round(incorrectDemoSymmRtTotal / incorrectDemoSymmCount)

                if incorrectSymmCount == 0:
                    incorrectSymmMean = -1
                else:
                    incorrectSymmMean = round(incorrectSymmRtTotal / incorrectSymmCount)
                correctSymmMean = round(correctSymmTotal / correctSymmCount)
                # Calculating demo and test partial credit scores
                partialCredit = spatialTotal / spatialCount
                partialCreditDemo = spatialTotalDemo / spatialCountDemo
                # Number and percentages of correct scores on DTs demos and test
                symmCorrectCountDemo = symmCountDemo - (speedError_demo + processingError_demo)
                symmCorrectCountPercentDemo = (symmCorrectCountDemo / symmCountDemo) * 100
                symmCorrectCount = symmCount - (speedError + processingError)
                symmCorrectCountPercent = (symmCorrectCount / symmCount) * 100
                # Adding new variables from symmspan file into our items array which contains all output data
                a.append(browser_value)

                # Symmetry
                if not math.isnan(symmMeanDemo):
                    a.append(round(symmMeanDemo))
                else:
                    a.append("Nan")
                if not math.isnan(symmMean):
                    a.append(round(symmMean))
                else:
                    a.append("Nan")
                a.append(correctDemoSymmMean)
                a.append(correctSymmMean)
                a.append(incorrectDemoSymmMean)
                a.append(incorrectSymmMean)
                a.append(round(processingTime_demo))
                a.append(round(processingTime))
                a.append(speedError_demo)
                a.append(speedError)
                a.append(processingError_demo)
                a.append(processingError)
                a.append(round(maxDTRtDemo))
                a.append(round(maxDTRt))
                a.append(symmCorrectCountDemo)
                a.append(round(symmCorrectCountPercentDemo, 1))
                a.append(symmCorrectCount)
                a.append(round(symmCorrectCountPercent, 1))

                # Blocks
                a.append(round(symspan_demo_score))
                a.append(round(symmspan_score))
                a.append(total_demo_correct)
                a.append(total_correct)
                a.append(round(partialCreditDemo, 2))
                a.append(round(partialCredit, 2))
                a.append(round(recallTime_demo))
                a.append(round(recallTime))

            else:
                print("File not found ", token)


def analyzeNBack(filename):
    with open(filename, "a", newline="") as outfile:
        csvwriter = csv.writer(outfile)

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

        for a in items:
            i = 0
            # Define the token from our global items list
            token = a[1]
            found = False
            demoHitRate = 0
            hitRate = 0
            demoFalseAlarm = 0
            falseAlarm = 0
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
                            """Calculating demo hit rate (correct answers will have a '1' in the correct cell
                            and a 'C' in their label"""
                            if row[data.columns.get_loc("correct")] == 1 and \
                                    'p' in str(row[data.columns.get_loc("label")]) and \
                                    'C' in str(row[data.columns.get_loc("label")]):
                                demoHitRate += 1

                            """Calculating test hit rate (correct answers will have a '1' in the correct cell
                            and a 'C' in their label"""
                            if row[data.columns.get_loc("correct")] == 1 and \
                                    't' in str(row[data.columns.get_loc("label")]) and \
                                    'C' in str(row[data.columns.get_loc("label")]):
                                hitRate += 1

                            # Calculating false alarm rate for demo trials
                            if row[data.columns.get_loc("correct")] == 1 and \
                                    'p' in str(row[data.columns.get_loc("label")]) and \
                                    'C' not in str(row[data.columns.get_loc("label")]):
                                demoFalseAlarm += 1

                            # Calculating false alarm rate for test trials
                            if row[data.columns.get_loc("correct")] == 1 and \
                                    't' in str(row[data.columns.get_loc("label")]) and \
                                    'C' not in str(row[data.columns.get_loc("label")]):
                                falseAlarm += 1

                        # Appending values into output data file
                        a.append(demoHitRate)
                        a.append(hitRate)
                        a.append(demoFalseAlarm)
                        a.append(falseAlarm)
                        found = True
                        fileNames.pop(i)
                    else:
                        i += 1


def write():
    with open("output.csv", "w", newline="") as outfile:
        csvwriter = csv.writer(outfile)

        # Write header row
        header_row = ["Submit Date",
                      "Token",
                      "Time Taken",
                      "Gender",
                      "Age",
                      "Active/Reflective",
                      "Sensing/Intuitive",
                      "Visual/Verbal",
                      "Sequential/Global",
                      "Browser",

                      "VS_DT_meanRT_Demos",
                      "VS_DT_meanRT_TestTrials",
                      "VS_DT_meanRT_correct_Demos",
                      "VS_DT_meanRT_correct_TestTrials",
                      "VS_DT_meanRT_incorrect_Demos",
                      "VS_DT_meanRT_incorrect_TestTrials",
                      "VS_DT_totalPRT_Demos",
                      "VS_DT_totalPRT_TestTrials",
                      "VS_DT_speedErrors_Demos",
                      "VS_DT_speedErrors_TestTrials",
                      "VS_DT_accuracyErrors_Demos",
                      "VS_DT_accuracyErrors_TestTrials",
                      "VS_DT_maxRT_Demos",
                      "VS_DT_maxRT_TestTrials",
                      "VS_DT_totalCorrect_Demos",
                      "VS_DT_totalCorrect(%)_Demos",
                      "VS_DT_totalCorrect_TestTrials",
                      "VS_DT_totalCorrect(%)_TestTrials",

                      "VS_BL_perfectScore_total_Demos",
                      "VS_BL_perfectScore_TestTrials",
                      "VS_BL_total_Demos",
                      "VS_BL_total_TestTrials",
                      "VS_BL_partialCredit_Demos",
                      "VS_BL_partialCredit_TestTrials",
                      "VS_RT_totalRecall_Demos",
                      "VS_RT_totalRecall_TestTrials",

                      "N_hitRate_Demos (/12)",
                      "N_hitRate_Test (/24)",
                      "N_falseAlarm_Demo",
                      "N_falseAlarm_Test"

                      ]
        csvwriter.writerow(header_row)

        for i in items:
            csvwriter.writerow(i)


analyzeLimeSurvey("test LimeSurvey results.csv")
analyzeSymmSpan(output_file)
analyzeNBack(output_file)
write()
