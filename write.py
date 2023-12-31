import config
import csv

def write():
    with open("output.csv", "w", newline="") as outfile:
        csvwriter = csv.writer(outfile)

        # Write header row
        header_row = ["Submit Date",
                      "ILS Start Time",
                      "ILS Duration (All 4 Qs Groups) (MM:SS)",
                      "Time All 4 ILS Group Qs Completed",
                      "Visual-Span Start Time",
                      "Visual-Span Duration (MM:SS)",
                      "N-Back Start Time",
                      "N-Back Duration (MM:SS)",
                      "Task Order",
                      "Token",
                      "Total Elapsed Time (Start to Submit of ILS Survey)",
                      "Gender",
                      "Age",
                      "Active/Reflective",
                      "Sensing/Intuitive",
                      "Visual/Verbal",
                      "Sequential/Global",
                      "Browser",

                      "VS_DT_meanRT_Demos (ms)",
                      "VS_DT_meanRT_TestTrials (ms)",
                      "VS_DT_meanRT_correct_Demos (ms)",
                      "VS_DT_meanRT_correct_TestTrials (ms)",
                      "VS_DT_meanRT_incorrect_Demos (ms)",
                      "VS_DT_meanRT_incorrect_TestTrials (ms)",
                      "VS_DT_totalPRT_Demos (ms)",
                      "VS_DT_totalPRT_TestTrials (ms)",
                      "VS_DT_speedErrors_Demos /19",
                      "VS_DT_speedErrors_TestTrials /42",
                      "VS_DT_accuracyErrors_Demos /19",
                      "VS_DT_accuracyErrors_TestTrials /42",
                      "VS_DT_totalErrors_Demo",
                      "VS_DT_totalErrors_TestTrials",
                      "VS_DT_maxRT_Demos (ms)",
                      "VS_DT_maxRT_TestTrials (ms)",
                      "VS_DT_totalCorrect_Demos /19",
                      "VS_DT_totalCorrect(%)_Demos",
                      "VS_DT_totalCorrect_TestTrials /42",
                      "VS_DT_totalCorrect(%)_TestTrials",

                      "VS_BL_perfectScore_total_Demos /25",
                      "VS_BL_perfectScore_TestTrials /42",
                      "VS_BL_maxSpan_Demo",
                      "VS_BL_maxSpan_TestTrials",
                      "VS_BL_spanSize_2_perfect_TestTrials",
                      "VS_BL_spanSize_3_perfect_TestTrials",
                      "VS_BL_spanSize_4_perfect_TestTrials",
                      "VS_BL_spanSize_5_perfect_TestTrials",
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