"""Module to output relevant data into csv files"""
import os
import csv
#
def writeCSV(csvPath, usedmpicommands, first_table_values,second_table_values,third_table_values, df):
    """Writes multiple csv files, one for every list"""

    print("Saving CSV files in directory '" + os.path.realpath(csvPath) +"'")

    #routine Summary by rank metrics table
    metric_csv_table = df.to_csv(sep=';')
    with open(os.path.join(csvPath,'routineSummaryByRank_metric_table.csv'), 'w') as outfileMetricTable:
        outfileMetricTable.write(metric_csv_table)
    outfileMetricTable.close()

    #routine Summary by rank data table (just the data from the instrumenation file in csv format)
    with open(os.path.join(csvPath,'routineSummaryByRank_summary.csv'), 'w') as outfileMPICommands:
        wr = csv.writer(outfileMPICommands, delimiter=';')
        wr.writerows(usedmpicommands)
    outfileMPICommands.close()

    #application Summary by rank data (first table)
    #Columns: "Rank","Proc CPU Time","User Portion", "User Portion in Percent", "System Portion", "System Portion in Percent"
    with open(os.path.join(csvPath,'applicationSummaryByRank_1st_table.csv'), 'w') as outfile_first_table:
        wr = csv.writer(outfile_first_table, delimiter=';')
        wr.writerow(["Rank","Proc CPU Time","User Portion", "User Portion in Percent", "System Portion", "System Portion in Percent"])
        wr.writerows(first_table_values)
    outfile_first_table.close()
    
    #application Summary by rank data (second table) 
    #Columns: "Rank","Proc Wall Time","User" , "User in Percent","MPI", "MPI in Percent"
    with open(os.path.join(csvPath,'applicationSummaryByRank_2st_table.csv'), 'w') as outfile_second_table:
        wr = csv.writer(outfile_second_table, delimiter=';')
        wr.writerow(["Rank","Proc Wall Time","User" , "User in Percent","MPI", "MPI in Percent"])
        wr.writerows(second_table_values)
    outfile_second_table.close()

    #application Summary by rank data (third table)
    #Columns: "Rank","Proc MPI Time","Overhead", "Overhead in Percent","Blocking", "Blocking in Percent"
    with open(os.path.join(csvPath,'applicationSummaryByRank_3rd_table.csv'), 'w') as outfile_third_table:
        wr = csv.writer(outfile_third_table, delimiter=';')
        wr.writerow(["Rank","Proc MPI Time","Overhead", "Overhead in Percent","Blocking", "Blocking in Percent"])
        wr.writerows(third_table_values)
    outfile_third_table.close()

    #In case, you are wondering, where the last part of the instrumentation file is (message Summary by rank),
    #it is currently not saved as a csv file. This is because:
    #
    #1st: In the platform_mpi instrumentation file, the data is somehow visualized beautifully
    #2nd: It is very hard to save the data in a 2-dimensional csv file format
    #Therefore we decided, not to export this data in a csv file format