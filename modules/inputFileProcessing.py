"""Module to process instrumentation file and split this file into the corresponding parts"""
import re
def inputFileProcessing(data):
    """Function splits and extracts data from intrumentation file."""
    #The string "data" is now processed and the relevant information is extracted to the specific lists
    num_proc = re.findall(r"^\sProcesses:\s*(\d+)", data, re.MULTILINE)
    user_time = re.findall(r"^\sUser\stime:\s*(\d+.\d+)", data, re.MULTILINE)
    mpi_time_with_blocking = re.findall(r"^\sMPI\stime\s:\s*(\d+.\d+)%\s*\[Overhead:(\d+.\d+)%\s*Blocking:(\d+.\d+)%\]",data, re.MULTILINE)
    #application Summary by rank tables
    #first: Rank	Proc CPU Time	User Portion	System Portion
    #second: Rank	Proc Wall Time	User	MPI
    #third:  Rank	Proc MPI Time	Overhead	Blocking
    #mpi commands:  Rank	Routine	Statistic	Calls	Overhead(ms)	Blocking(ms) aka Routine Summary by rank
    first_table = re.findall(r"\sRank\s*Proc\sCPU\sTime\s*User\sPortion\s*System\sPortion\n^\s*-+\n^((.+\n)+\s*-)+",data, re.MULTILINE)
    second_table = re.findall(r"\sRank\s*Proc\sWall\sTime\s*User\s*MPI\n^\s*-+\n^((.+\n)+\s*-)+", data, re.MULTILINE)
    third_table = re.findall(r"\sRank\s*Proc\sMPI\sTime\s*Overhead\s*Blocking\n^\s*-+\n^((.+\n)+\s*-)+", data, re.MULTILINE)
    mpi_commands = re.findall(r"^\sRank\s*Routine\s*Statistic\s*Calls\s*Overhead\(ms\)\s*Blocking\(ms\)\n((?:\s-*(?:.+\n)+\s-+)+)\s*Message",data, re.MULTILINE)
    summary_per_rank = re.findall(r"Message\sSummary\sby\sRank\sPair:\n\s*SRank\s+DRank\s+Messages\s+\(minsize,maxsize\)\/\[bin\]\s+Totalbytes\n\s*(?:((?:.*\n)+\s*-+)+)", data, re.MULTILINE)
    #values of application Summary by rank tables
    first_table_values = re.findall(r"\s*(\d+)+\s*(\d+.\d+)\s*(\d+.\d+)\(\s*(\d+.\d+)%\)\s*(\d+.\d+)\(\s*(\d+.\d+)%\)",str(first_table), re.MULTILINE)
    second_table_values = re.findall(r"\s*(\d+)+\s*(\d+.\d+)\s*(\d+.\d+)\(\s*(\d+.\d+)%\)\s*(\d+.\d+)\(\s*(\d+.\d+)%\)",str(second_table), re.MULTILINE)
    third_table_values = re.findall(r"\s*(\d+)+\s*(\d+.\d+)\s*(\d+.\d+)\(\s*(\d+.\d+)%\)\s*(\d+.\d+)\(\s*(\d+.\d+)%\)",str(third_table), re.MULTILINE)
    #routine Summary by Rank
    mpi_commands_values = re.findall(r"(?:\n\s*(\d+)([\s\S]*?)-+)", str(mpi_commands[0]), re.MULTILINE)
    #mpi_commands_values[0]- mpi_commands_values[95] tables for each rank
    #message summary per rank pair
    #snip at --------------- for each SRank
    summary_per_rank_srank_values = re.findall(r"(?:\n\s*(\d+)([\s\S]*?)-+)", str(summary_per_rank[0]), re.MULTILINE)
    #summary_per_rank_srank_values[0] - summary_per_rank_srank_values[95] tables for each srank
    usedmpicommands = [0] * int((num_proc[0])) # number of mpi processors
    for i in range(len(mpi_commands_values)):
        usedmpicommands[i] = re.findall(r"(?P<mpi_command>MPI_\w*)\s+(?P<numberOfCalls>\d+)\s+(?P<overhead_ms>\d+.\d+)\s+(?P<blocking_ms>\d+.\d+)\s*(?:min\s*(?P<overhead_min>\d+.\d+)\s*(?P<blocking_min>\d+.\d+)\s*(?:max)\s+(?P<overhead_max>\d+.\d+)\s*(?P<blocking_max>\d+.\d+)\s+(?:avg)\s*(?P<overhead_avg>\d+.\d+)\s*(?P<blocking_avg>\d+.\d+))?", str(mpi_commands_values[i][1]), re.MULTILINE)

    return num_proc, user_time, mpi_time_with_blocking, first_table_values,\
           second_table_values, third_table_values, usedmpicommands,\
           summary_per_rank_srank_values