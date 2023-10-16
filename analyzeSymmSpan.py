import config
import csv
import os
import pandas as pd
import math
import pytz
from datetime import datetime, date


def analyzeSymmSpan():
        for a in config.items:
            # Array which contains data to write
            token = a[4]
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
            maxSpanDemo = maxSpan = 0
            perfectSpanPoints_2 = perfectSpanPoints_3 = perfectSpanPoints_4 = perfectSpanPoints_5 = 0
            # We are locating the symm span file with the same token in the current row
            filename = f"{config.visualSpanFolder}/Symmetry_Span_{token}.csv"
            if os.path.isfile(filename):
                data = pd.read_csv(filename)
                if "browser" in data.columns:
                    browser_value = data.loc[0, "browser"]
                else:
                    browser_value = "Not detected"

                """ Checking for the start time by using the unix time in the first trial. Unix times in these log files
                are in milliseconds so we need to convert them to seconds"""
                unixStartTime = data.loc[0, "unix_timeStamp"]/1000
                unixEndTime = data.loc[79, "unix_timeStamp"] / 1000
                # Define the Mountain Time (MT) timezone
                mountain_timezone = pytz.timezone('US/Mountain')

                # Convert the Unix timestamp to Mountain Time
                symmSpanStartTime = datetime.fromtimestamp(unixStartTime, mountain_timezone)

                # Parse the input datetime string
                input_datetime = datetime.strptime(str(symmSpanStartTime), "%Y-%m-%d %H:%M:%S.%f%z")

                # Format the datetime to the desired output format
                symmSpanStartTime = input_datetime.strftime("%Y-%m-%d %H:%M:%S")
                config.symmSpanStartTime = symmSpanStartTime

                # Duration of the experiment in minutes and seconds
                symmDuration = unixEndTime - unixStartTime
                minutes = int(symmDuration // 60)  # Whole minutes
                remaining_seconds = int(symmDuration % 60)  # Remaining seconds as an integer
                # Create a string in the format "minutes:seconds"
                symmDuration = f"{minutes:02}:{remaining_seconds:02}"

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
                        # Calculating maximum span size for demo trials below
                        maxSpanDemo = max(maxSpanDemo, int(row[data.columns.get_loc("set_size")]))

                    if row[data.columns.get_loc("trial_type")] == "spatial-span-recall" and \
                            row[data.columns.get_loc("spatial_accuracy")] == row[data.columns.get_loc("set_size")]:
                        symmspan_score += row[data.columns.get_loc("spatial_accuracy")]
                        # Calculating maximum span size for test trials below
                        maxSpan = max(maxSpan, int(row[data.columns.get_loc("set_size")]))

                        # Calculating perfect span points
                        if row[data.columns.get_loc("set_size")] == 2:
                            perfectSpanPoints_2 += 2
                        elif row[data.columns.get_loc("set_size")] == 3:
                            perfectSpanPoints_3 += 3
                        elif row[data.columns.get_loc("set_size")] == 4:
                            perfectSpanPoints_4 += 4
                        elif row[data.columns.get_loc("set_size")] == 5:
                            perfectSpanPoints_5 += 5
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
                                row[data.columns.get_loc("trial_type")] in ["symmetry-judgement-task-fulldemo"] and \
                                not math.isnan(row[0]):
                            maxDTRtDemo = max(row[0], maxDTRtDemo)
                    except KeyError:
                        print("Column not found. Skipping")
                    # Maximum response time on test distractor tasks
                    try:
                        if row[data.columns.get_loc("trial_type")] in ["symmetry-judgement-task"] and \
                                not math.isnan(row[0]):
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

                # Appending the start time of the symmspan task into our data array
                a.insert(4, symmSpanStartTime)

                # Appending the duration of the symmspan task into the data array
                a.insert(5, symmDuration)

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
                a.append(speedError_demo + processingError_demo)
                a.append(speedError + processingError)
                a.append(round(maxDTRtDemo))
                a.append(round(maxDTRt))
                a.append(symmCorrectCountDemo)
                a.append(round(symmCorrectCountPercentDemo, 1))
                a.append(symmCorrectCount)
                a.append(round(symmCorrectCountPercent, 1))

                # Blocks
                a.append(round(symspan_demo_score))
                a.append(round(symmspan_score))
                a.append(maxSpanDemo)
                a.append(maxSpan)
                a.append(perfectSpanPoints_2)
                a.append(perfectSpanPoints_3)
                a.append(perfectSpanPoints_4)
                a.append(perfectSpanPoints_5)
                a.append(total_demo_correct)
                a.append(total_correct)
                a.append(round(partialCreditDemo, 2))
                a.append(round(partialCredit, 2))
                a.append(round(recallTime_demo))
                a.append(round(recallTime))

            else:
                """Fill array indexes that would normally contain symm-span data with None. Ensures that n-back
                data is not placed under symm-span headers"""
                """empty_items = 27
                for _ in range(empty_items):
                    a.append(None)
                print("File not found ", token)"""
                # Appending the start time of the symmspan task into our data array
                a.insert(4, " ")

                # Appending the duration of the symmspan task into the data array
                a.insert(5, " ")

                # Adding new variables from symmspan file into our items array which contains all output data
                a.append(" ")

                # The below number is the total number of variables above pertaining to the visual-span task
                empty_items = 34
                for _ in range(empty_items):
                    a.append(" ")



