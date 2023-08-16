import config
import csv

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
                      "VS_DT_speedErrors_Demos /19",
                      "VS_DT_speedErrors_TestTrials /42",
                      "VS_DT_accuracyErrors_Demos /19",
                      "VS_DT_accuracyErrors_TestTrials /42",
                      "VS_DT_maxRT_Demos",
                      "VS_DT_maxRT_TestTrials",
                      "VS_DT_totalCorrect_Demos /19",
                      "VS_DT_totalCorrect(%)_Demos",
                      "VS_DT_totalCorrect_TestTrials /42",
                      "VS_DT_totalCorrect(%)_TestTrials",

                      "VS_BL_perfectScore_total_Demos /25",
                      "VS_BL_perfectScore_TestTrials /42",
                      "VS_BL_total_Demos /25",
                      "VS_BL_total_TestTrials /42",
                      "VS_BL_partialCredit_Demos /1",
                      "VS_BL_partialCredit_TestTrials /1",
                      "VS_RT_totalRecall_Demos (ms)",
                      "VS_RT_totalRecall_TestTrials (ms)",

                      "N_2B_hitRate_Demos /12",
                      "N_3B_hitRate_Demos /12",
                      "N_2B_hitRate_Test /24",
                      "N_3B_hitRate_Test /24",

                      "N_2B_falseAlarm_Demo",
                      "N_3B_falseAlarm_Demo",
                      "N_2B_falseAlarm_Test",
                      "N_3B_falseAlarm_Test",

                      "N_2B_accuracy_Demo",
                      "N_3B_accuracy_Demo",
                      "N_2B_accuracy_Test",
                      "N_3B_accuracy_Test",

                      "N_2B_omission_Demo",
                      "N_3B_omission_Demo",
                      "N_2B_omission_Test",
                      "N_3B_omission_Test",

                      "N_2B_sensitivity_Demo",
                      "N_3B_sensitivity_Demo",
                      "N_2B_sensitivity_Test",
                      "N_3B_sensitivity_Test",

                      "N_2B_bias_Demo?",
                      "N_3B_bias_Demo?",
                      
                      "N_2B_bias_Test?",
                      "N_3B_bias_Test?",

                      "N_2B_correct_NR_Demo",
                      "N_3B_correct_NR_Demo",
                      "N_2B_correct_NR_Test",
                      "N_3B_correct_NR_Test"

                      ]
        csvwriter.writerow(header_row)

        for i in config.items:
            csvwriter.writerow(i)