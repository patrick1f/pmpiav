"""Module to create a full PDF report"""
import os
import subprocess
def readInputFile(inputfile):
    """Function to read data from a file and write it in a string"""
    with open(inputfile, 'r') as myfile:
      data = myfile.read()
    print("File " + str(inputfile) + " successfully read.")
    return data
def pdfPlotHelperFunction(filename):
    """Function to create the LaTeX code for a graphic associated with a filename parameter"""
    includeGraphicsCode = r"\begin{figure}[H]" + "\n \centering\n \includegraphics[scale=1]{" + filename + "}\n\end{figure}\n"
    return includeGraphicsCode

def writePDF(df, dir, inputfile, inputfilesize, num_proc, user_time, mpi_time_with_blocking, metric,\
              plotColumn, routineSummaryFileList, time_list_first_percent, time_list_second_percent,\
              time_list_third_percent, commentInOutputFile,commentInOutputFileEnabled, dtime, pdfPath,\
              userTimeColor, systemTimeColor, mpiTimeColor, blockingTimeColor, useVectorGraphics):
    """Function to create a PDF report file based on a template LaTeX file"""
    #In the file template.tex, there are tags in brackets, e.g., <tags>.
    #These tags have specific names like <inputfile> and are then replaced by the corresponding string.
    #No magic here!
    templateString = readInputFile('template.tex')
    pdfTable = df.to_latex()
    #Summary section
    inputfile = inputfile.replace('_','\_')
    inputfile = inputfile.replace('%','\%')
    templateString = templateString.replace('<inputfile>',r'\text{'+ inputfile + '}')
    templateString = templateString.replace('<inputfilesize>',str(inputfilesize))
    templateString = templateString.replace('<dtime>',dtime.strftime("%c"))
    templateString = templateString.replace('<mpi_procs>',str(num_proc[0]))
    templateString = templateString.replace('<user_time>',str(user_time[0]))
    templateString = templateString.replace('<mpi_time0>',str(mpi_time_with_blocking[0][0]))
    templateString = templateString.replace('<mpi_time1>',str(mpi_time_with_blocking[0][1]))
    templateString = templateString.replace('<mpi_time2>',str(mpi_time_with_blocking[0][2]))
    #first part
    templateString = templateString.replace('<usersystem1>',str(round(time_list_first_percent[2],2)))
    templateString = templateString.replace('<usersystem2>',str(round(time_list_first_percent[3],2)))
    templateString = templateString.replace('<usersystem3>',str(round(time_list_first_percent[0],2)))
    templateString = templateString.replace('<usersystem4>',str(round(time_list_first_percent[4],2)))
    templateString = templateString.replace('<usersystem5>',str(round(time_list_first_percent[5],2)))
    templateString = templateString.replace('<usersystem6>',str(round(time_list_first_percent[1],2)))
    
    templateString = templateString.replace('<usermpi1>',str(round(time_list_second_percent[2],2)))
    templateString = templateString.replace('<usermpi2>',str(round(time_list_second_percent[3],2)))
    templateString = templateString.replace('<usermpi3>',str(round(time_list_second_percent[0],2)))
    templateString = templateString.replace('<usermpi4>',str(round(time_list_second_percent[4],2)))
    templateString = templateString.replace('<usermpi5>',str(round(time_list_second_percent[5],2)))
    templateString = templateString.replace('<usermpi6>',str(round(time_list_second_percent[1],2)))

    templateString = templateString.replace('<mpiblock1>',str(round(time_list_third_percent[2],2)))
    templateString = templateString.replace('<mpiblock2>',str(round(time_list_third_percent[3],2)))
    templateString = templateString.replace('<mpiblock3>',str(round(time_list_third_percent[0],2)))
    templateString = templateString.replace('<mpiblock4>',str(round(time_list_third_percent[4],2)))
    templateString = templateString.replace('<mpiblock5>',str(round(time_list_third_percent[5],2)))
    templateString = templateString.replace('<mpiblock6>',str(round(time_list_third_percent[1],2)))
    
    templateString = templateString.replace('<userTimeColor>',userTimeColor)
    templateString = templateString.replace('<systemTimeColor>',systemTimeColor)
    templateString = templateString.replace('<mpiTimeColor>',mpiTimeColor)
    templateString = templateString.replace('<blockingTimeColor>',blockingTimeColor)
    if (commentInOutputFileEnabled == True):
        templateString = templateString.replace('<comment>', 'Comment: ' + commentInOutputFile)
    else:
        templateString = templateString.replace('<comment>', '')
    templateString = templateString.replace('<pdftable>', pdfTable)
    fileEnding = 'pdf'
    if (useVectorGraphics == False):
        fileEnding = 'png'
    templateString = templateString.replace('<firsttable>', pdfPlotHelperFunction('first_table_values.' + fileEnding))
    templateString = templateString.replace('<secondtable>', pdfPlotHelperFunction('second_table_values.' + fileEnding))
    templateString = templateString.replace('<thirdtable>', pdfPlotHelperFunction('third_table_values.' + fileEnding))

    if (plotColumn == "overhead"):
        templateString = templateString.replace('<plotColumn1>','The values depicted in the following plots are the overhead of the\
                                                 specific routine calls in ms on the y-axis and the MPI ranks on the x-axis.')
        templateString = templateString.replace('<plotColumn2>','The values are the overhead of the specific routine calls in ms.')
        templateString = templateString.replace('<pdftabledesc>', 'Showing the overhead of the specific routine calls in ms sorted by ' + metric)
    elif (plotColumn == "calls"):
        templateString = templateString.replace('<plotColumn1>','The values depicted in the following plots are the number of calls of the\
                                                 specific routine on the y-axis and the MPI ranks on the x-axis.')
        templateString = templateString.replace('<plotColumn2>','The values are the number of calls of the specific routine.')
        templateString = templateString.replace('<pdftabledesc>', 'Showing the number of calls of the specific routine sorted by ' + metric)
    elif (plotColumn == "blocking"):
        templateString = templateString.replace('<plotColumn1>','The values depicted in the following plots are the blocking in ms of the\
                                                 specific routine on the y-axis and the MPI ranks on the x-axis.')
        templateString = templateString.replace('<plotColumn2>','The values are the blocking of the specific routine calls in ms.')
        templateString = templateString.replace('<pdftabledesc>', 'Showing the blocking of the specific routine calls in ms sorted by ' + metric)
    elif (plotColumn == "minBlocking"):
        templateString = templateString.replace('<plotColumn1>','The values depicted in the following plots are the minimal blocking in ms of the\
                                                 specific routine on the y-axis and the MPI ranks on the x-axis.')
        templateString = templateString.replace('<plotColumn2>','The values are the minimal blocking of the specific routine calls in ms.')
        templateString = templateString.replace('<pdftabledesc>', 'Showing the minimal blocking of the specific routine calls in ms sorted by ' + metric)
    elif (plotColumn == "maxBlocking"):
        templateString = templateString.replace('<plotColumn1>','The values depicted in the following plots are the maximal blocking in ms of the\
                                                 specific routine on the y-axis and the MPI ranks on the x-axis.')
        templateString = templateString.replace('<plotColumn2>','The values are the maximal blocking of the specific routine calls in ms.')
        templateString = templateString.replace('<pdftabledesc>', 'Showing the maximal blocking of the specific routine calls in ms sorted by ' + metric)
    elif (plotColumn == "avgBlocking"):
        templateString = templateString.replace('<plotColumn1>','The values depicted in the following plots are the average blocking in ms of the\
                                                 specific routine on the y-axis and the MPI ranks on the x-axis.')
        templateString = templateString.replace('<plotColumn2>','The values are the average blocking of the specific routine calls in ms.')
        templateString = templateString.replace('<pdftabledesc>', 'Showing the minimal average of the specific routine calls in ms sorted by ' + metric)
    elif (plotColumn == "minOverhead"):
        templateString = templateString.replace('<plotColumn1>','The values depicted in the following plots are the minimal overhead of the\
                                                 specific routine calls in ms on the y-axis and the MPI ranks on the x-axis.')
        templateString = templateString.replace('<plotColumn2>','The values are the minimal overhead of the specific routine calls in ms.')
        templateString = templateString.replace('<pdftabledesc>', 'Showing the minimal overhead of the specific routine calls in ms sorted by ' + metric)
    elif (plotColumn == "maxOverhead"):
        templateString = templateString.replace('<plotColumn1>','The values depicted in the following plots are the maximal overhead of the\
                                                 specific routine calls in ms on the y-axis and the MPI ranks on the x-axis.')
        templateString = templateString.replace('<plotColumn2>','The values are the maximal overhead of the specific routine calls in ms.')
        templateString = templateString.replace('<pdftabledesc>', 'Showing the maximal overhead of the specific routine calls in ms sorted by ' + metric)
    elif (plotColumn == "avgOverhead"):
        templateString = templateString.replace('<plotColumn1>','The values depicted in the following plots are the average overhead of the\
                                                 specific routine calls in ms on the y-axis and the MPI ranks on the x-axis.')
        templateString = templateString.replace('<plotColumn2>','The values are the average overhead of the specific routine calls in ms.')
        templateString = templateString.replace('<pdftabledesc>', 'Showing the average overhead of the specific routine calls in ms sorted by ' + metric)
    templateRoutineSummaryByRankPlots = ''
    #Add plots
    for filename in routineSummaryFileList:
        templateRoutineSummaryByRankPlots +=(pdfPlotHelperFunction(filename + '.' + fileEnding))
    templateString = templateString.replace('<imshow>', pdfPlotHelperFunction('imshow.' + fileEnding))
    templateString = templateString.replace('<scatter>',pdfPlotHelperFunction('scatter.'+ fileEnding))
    templateString = templateString.replace('<sorting>','The following table is sorted by ' + metric + '.')
    templateString = templateString.replace('<routineSummaryByRankPlots>', templateRoutineSummaryByRankPlots)
    f = open(os.path.join(pdfPath,'report.tex'), 'wt', encoding='utf-8')
    f.write(templateString)
    f.close()
    #compile
    #starting pdflatex
    proc = subprocess.Popen(['pdflatex', 'report.tex'], cwd=pdfPath)
    proc.communicate()
    #deleting auxiliary files, not needed for later use
    os.unlink(os.path.join(pdfPath, 'report.log'))
    os.unlink(os.path.join(pdfPath, 'report.aux'))
    print('PDF output finished.')