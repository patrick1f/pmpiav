"""Module to plot and process the routine Summary by rank part of the instrumentation file"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def plot_commands(Commands, session, x, plotColumn,dpi,dir, routineSummaryFileList, htmlPath,\
                  pdfPath, saveFigsAsPDF, writehtml, writepdf, barWidth, useVectorGraphics):
        """Helper function to create a plot"""
        linetmp = []
        titleString = "Default plot title"
        xAxisLabel = "MPI ranks"
        yAxisLabel = ""
        #print (plotColumn)
        #Depending on the case, different data has to be gathered from the Database
        #and the labels have to match the data.
        if (plotColumn == "overhead"):
            titleString = "The overhead in ms of routine " + str(x)
            yAxisLabel = "Overhead in ms"
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x):
                lineSend = np.array([line.rank, line.overhead, line.mpi_routine])
                linetmp.append(lineSend)
            linetmp = np.array(linetmp)
        elif (plotColumn == "calls"):
            titleString = "Number of calls of routine " + str(x)
            yAxisLabel = "Number of routine calls"
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x):
                lineSend = np.array([line.rank, line.calls, line.mpi_routine])
                linetmp.append(lineSend)
            linetmp = np.array(linetmp)
        elif (plotColumn == "blocking"):
            titleString = "The blocking in ms of routine " + str(x)
            yAxisLabel = "Blocking in ms"
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x):
                lineSend = np.array([line.rank, line.blocking, line.mpi_routine])
                linetmp.append(lineSend)
            linetmp = np.array(linetmp)
        elif (plotColumn == "minOverhead"):
            titleString = "The minimal overhead in ms of routine " + str(x)
            yAxisLabel = "Minimal overhead in ms"
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x):
                lineSend = np.array([line.rank, line.minOverhead, line.mpi_routine])
                linetmp.append(lineSend)
            linetmp = np.array(linetmp)
        elif (plotColumn == "maxOverhead"):
            titleString = "The maximal overhead in ms of routine " + str(x)
            yAxisLabel = "Maximal overhead in ms"
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x):
                lineSend = np.array([line.rank, line.maxOverhead, line.mpi_routine])
                linetmp.append(lineSend)
            linetmp = np.array(linetmp)
        elif (plotColumn == "avgOverhead"):
            titleString = "The average overhead in ms of routine " + str(x)
            yAxisLabel = "Average overhead in ms"
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x):
                lineSend = np.array([line.rank, line.avgOverhead, line.mpi_routine])
                linetmp.append(lineSend)
            linetmp = np.array(linetmp)
        elif (plotColumn == "minBlocking"):
            titleString = "The minmal blocking in ms of routine " + str(x)
            yAxisLabel = "Minimal blocking in ms"
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x):
                lineSend = np.array([line.rank, line.minBlocking, line.mpi_routine])
                linetmp.append(lineSend)
            linetmp = np.array(linetmp)
        elif (plotColumn == "maxBlocking"):
            titleString = "The maximal blocking in ms of routine " + str(x)
            yAxisLabel = "Maximal blocking in ms"
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x):
                lineSend = np.array([line.rank, line.maxBlocking, line.mpi_routine])
                linetmp.append(lineSend)
            linetmp = np.array(linetmp)
        elif (plotColumn == "avgBlocking"):
            titleString = "The average blocking in ms of routine " + str(x)
            yAxisLabel = "Average blocking in ms"
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x):
                lineSend = np.array([line.rank, line.avgBlocking, line.mpi_routine])
                linetmp.append(lineSend)
            linetmp = np.array(linetmp)
        else:
            print ("plotColumn not correctly assigned in config file.")
        #print(np.std(linetmp[:,1]))
        #print(np.mean(linetmp[:,1],dtype=np.float64))
        #print("coefficient of variance=" + str(np.std(linetmp[:,1])/np.mean(linetmp[:,1])))
        #plot of query
        fig, ax = plt.subplots()
        plt.title(titleString)
        #ax.plot(linetmp[:,0], linetmp[:,1])
        ## bar chart
        linetmp[:,0] = linetmp[:,0].astype(float)
        linetmp[:,1] = linetmp[:,1].astype(float)
        ax.bar(linetmp[:,0],linetmp[:,1], barWidth)
        #ax.plot(linetmp[:,0],linetmp[:,1])
        #ax.fill_between(linetmp[:,0].data, 0,linetmp[:,1].data)
        ax.set_xlabel(xAxisLabel)
        ax.set_ylabel(yAxisLabel)
        ax.set_aspect('auto') #correct aspect ratio, without this option some labels are cut off
        figfilename = str('routine_' + str(x))
        #print(type(figfilename))
        #print (figfilename)
        routineSummaryFileList.append(figfilename)
        if (saveFigsAsPDF == True):
            plt.savefig(os.path.join(dir,figfilename + '.pdf'), dpi=dpi)
        if (writehtml == True):
            if (useVectorGraphics == True):
                plt.savefig(os.path.join(htmlPath,figfilename + '.svg'), dpi=dpi)
            else:
                plt.savefig(os.path.join(htmlPath,figfilename + '.png'), bbox_inches='tight', dpi=dpi)
        if (writepdf == True):
            if (useVectorGraphics == True):
                plt.savefig(os.path.join(pdfPath,figfilename + '.pdf'), dpi=dpi)
            else:
                plt.savefig(os.path.join(pdfPath,figfilename + '.png'), bbox_inches='tight', dpi=dpi)
        plt.close(fig)
        #plt.show()
def routineSummaryByRankAnalyze(Commands,session,config, plotColumn, metric,dpi,dir,routineSummaryFileList,n,\
                                htmlPath, pdfPath, saveFigsAsPDF, writehtml, writepdf, barWidth, useVectorGraphics):
    """Main function to analyze routine Summary by rank"""
    #Querying the database
    listOfUsedMPICommands = []
    #Get a list of all commands which contain "mpi" in their name.
    #This has to be distinct, since we want no duplicates 
    for line in session.query(Commands.mpi_routine).distinct().filter(Commands.mpi_routine.ilike("%mpi%")):
        lineNames = np.array([line.mpi_routine])
        listOfUsedMPICommands.append(lineNames)
    listOfUsedMPICommands = np.array(listOfUsedMPICommands)
    np.set_printoptions(threshold=np.nan)
    #print ("----------listOfUsedMPICommands-------------")
    #print (listOfUsedMPICommands)
    
    #Create a dictionary to get a decent data structure
    dict ={}
    listCOV = []
    for x in listOfUsedMPICommands:
        #print (x)
        listtmp = []
        currentCommand = ""
        cov = 0.
        mean = 0.
        var = 0.
        #Depending on the variable in the config file, different data has to be gathered from the database
        if (plotColumn == "overhead"):
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x[0]):
                currentLine = np.array([line.rank, line.overhead, line.mpi_routine]) #plot of overhead in ms
                currentCommand = line.mpi_routine
                #print(currentCommand)
                listtmp.append(currentLine)
            listtmp = np.array(listtmp)
        elif (plotColumn == "calls"):
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x[0]):
                currentLine = np.array([line.rank, line.calls, line.mpi_routine]) #plot of calls
                currentCommand = line.mpi_routine
                #print(currentCommand)
                listtmp.append(currentLine)
            listtmp = np.array(listtmp)
        elif (plotColumn == "blocking"):
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x[0]):
                currentLine = np.array([line.rank, line.blocking, line.mpi_routine]) #plot of blocking
                currentCommand = line.mpi_routine
                #print(currentCommand)
                listtmp.append(currentLine)
            listtmp = np.array(listtmp)
        elif (plotColumn == "minBlocking"):
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x[0]):
                currentLine = np.array([line.rank, line.minBlocking, line.mpi_routine]) #plot of minBlocking
                currentCommand = line.mpi_routine
                #print(currentCommand)
                listtmp.append(currentLine)
            listtmp = np.array(listtmp)
        elif (plotColumn == "maxBlocking"):
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x[0]):
                currentLine = np.array([line.rank, line.maxBlocking, line.mpi_routine]) #plot of blocking
                currentCommand = line.mpi_routine
                #print(currentCommand)
                listtmp.append(currentLine)
            listtmp = np.array(listtmp)
        elif (plotColumn == "avgBlocking"):
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x[0]):
                currentLine = np.array([line.rank, line.avgBlocking, line.mpi_routine]) #plot of avgBlocking
                currentCommand = line.mpi_routine
                #print(currentCommand)
                listtmp.append(currentLine)
            listtmp = np.array(listtmp)
        elif (plotColumn == "minOverhead"):
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x[0]):
                currentLine = np.array([line.rank, line.minOverhead, line.mpi_routine]) #plot of minOverhead
                currentCommand = line.mpi_routine
                #print(currentCommand)
                listtmp.append(currentLine)
            listtmp = np.array(listtmp)
        elif (plotColumn == "maxOverhead"):
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x[0]):
                currentLine = np.array([line.rank, line.maxOverhead, line.mpi_routine]) #plot of maxOverhead
                currentCommand = line.mpi_routine
                #print(currentCommand)
                listtmp.append(currentLine)
            listtmp = np.array(listtmp)
        elif (plotColumn == "avgOverhead"):
            for line in session.query(Commands).order_by(Commands.rank).\
               filter(Commands.mpi_routine == x[0]):
                currentLine = np.array([line.rank, line.avgOverhead, line.mpi_routine]) #plot of avgOverhead
                currentCommand = line.mpi_routine
                #print(currentCommand)
                listtmp.append(currentLine)
            listtmp = np.array(listtmp)
        #Calculate metrics
        valueMin = np.amin(listtmp[:,1]) #array min
        valueMax = np.amax(listtmp[:,1]) #array max
        valueRange = np.ptp(listtmp[:,1]) #range (max-min)
        median = np.median(listtmp[:,1]) #median
        mean = np.mean(listtmp[:,1])  #mean
        var = np.std(listtmp[:,1]) #standard deviation
        if (mean == 0): #special case, e.g. if blocking is always zero, then we have division by 0
            cov = 0
        else:
            cov = var / mean #coefficient of variance
        listtmp = np.array([currentCommand, cov])
        listCOV.append(listtmp)
        dict.update({currentCommand : (cov,mean, median, valueRange, valueMin, valueMax)})
    listCOV = np.array(listCOV)    
    #print(listCOV)
    #print("---------------- dictionary print: Routine Name|COV|Mean|Range|Median --------------------")
    #print(dict)
    #Map the metric to the respective number
    metricIndex = 0
    if (metric == "mean"):
        metricIndex = 1
    elif (metric == "median"):
        metricIndex = 2
    elif (metric == "range"):
        metricIndex = 3
    elif (metric == "min"):
        metricIndex = 4
    elif (metric == "max"):
        metricIndex = 5
    # sort w.r.t to the chosen metric in the config file (1: mean, 2: median, 3: range, 4: min, 5: max)
    sorted_x = sorted(dict, key= lambda x :dict[x][metricIndex], reverse=True)
    arrayForPandas = []
    #to_html
    for w in sorted_x:
      tmparray = np.array([w,round(dict[w][0],2), round(dict[w][1],2),round(dict[w][2],2), round(dict[w][3],2), round(dict[w][4],2), round(dict[w][5],2)])
      #print (w, dict[w])
      arrayForPandas.append(tmparray)
    arrayForPandas = np.array(arrayForPandas)
    #print (arrayForPandas)
    #create a data frame to ensure easy creation of html and LaTeX tables later
    df = pd.DataFrame(arrayForPandas, columns = ['Routine Name', 'Coefficient of Variance', 'Mean',\
                                                 'Median','Range', 'Minimal value', 'Maximal value'])
    #take the first n (NumberOfInterest) items out of the dict
    #n=int(config.get('routineSummaryByRankPlots', 'numberOfInterest'))
    #print("---------------- the top n="+str(n)+ " routines by " + metric + " are --------------------")
    t = sorted (dict, key= lambda x : dict[x][metricIndex], reverse=True)[:n] # sort w.r.t to the cov (1: mean, 2: median, 3: range, 4: min, 5: max)
    #print (t) # sorted dictionary containing the routine name in specific order
    
    #plot of the n (NumberOfInterest) most interesting commands in n independent figures
    for x in t:
       plot_commands(Commands,session,x, plotColumn,dpi,dir,routineSummaryFileList,\
                     htmlPath, pdfPath, saveFigsAsPDF, writehtml, writepdf, barWidth, useVectorGraphics)
    routineSummaryFileList = np.array(routineSummaryFileList)

    #return the dataframe for writing the output
    return df, routineSummaryFileList