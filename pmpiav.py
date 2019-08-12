#!/usr/bin/python3


#The following libraries are used in this part of pmpiav
import sys
import getopt
import os
import datetime
from configparser import ConfigParser
import sqlalchemy
from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Numeric
from sqlalchemy.orm import sessionmaker

#The following libraries are only used in imported modules below

#import re
#import csv
#import pandas as pd
#import matplotlib.pyplot as plt
#import dominate
#from dominate.tags import *
#from dominate.util import raw
#from matplotlib import cm
#import numpy as np
#import subprocess


#Code outsourced into modules for better overview

#modules for output file creation
from modules import csvModule
from modules import pdfModule
from modules import htmlModule

#modules for data processing and visualization
from modules import inputFileProcessing as iFP
from modules import applicationSummaryByRank as aSBRA
from modules import routineSummaryByRankAnalyze as rSBRA
from modules import messageSummaryByRankPair as mSBRP

#function to read inpput file into a string called 'data'
def readInputFile(inputfile):
    with open(inputfile, 'r') as myfile:
      data = myfile.read()
    print("File " + str(inputfile) + " successfully read.")
    return data

#inititalize sqlite database with the respective columns
def initDB(dbfilename,outputdir, enableVerboseDBOutput):
    engine = create_engine("sqlite:///" + os.path.join(outputdir,dbfilename), echo=enableVerboseDBOutput)
    #echo=True enables verbose output on command line
    Base = declarative_base()

    class Commands(Base):
        __tablename__ = 'mpi_commands'
        indexcount = Column(Integer, primary_key=True)
        mpi_routine = Column(String)
        rank = Column(Float(precision=6, asdecimal=True))
        calls = Column(Float(precision=6, asdecimal=True))
        overhead = Column(Float(precision=6, asdecimal=True))
        blocking = Column(Float(precision=6, asdecimal=True))
        minOverhead = Column(Float(precision=6, asdecimal=True, nullable=True))
        minBlocking = Column(Float(precision=6, asdecimal=True, nullable=True))
        maxOverhead = Column(Float(precision=6, asdecimal=True, nullable=True))
        maxBlocking = Column(Float(precision=6, asdecimal=True, nullable=True))
        avgOverhead = Column(Float(precision=6, asdecimal=True, nullable=True))
        avgBlocking = Column(Float(precision=6, asdecimal=True, nullable=True))
        UniqueConstraint(mpi_routine, rank)

        def __repr__(self):
            return "<MPI-Commands(indexcount ='%d', rank='%d', mpi_routine='%s',calls='%d',\
            overhead='%f', blocking='%f', minOverhead='%f',minBlocking='%f',maxOverhead='%f',\
            maxBlocking='%f',avgOverhead='%f',avgBlocking='%f')>" % (self.indexcount, self.rank,\
            self.mpi_routine, self.calls, self.overhead, self.blocking, self.minOverhead, self.minBlocking,\
            self.maxOverhead, self.maxBlocking, self.avgOverhead, self.avgBlocking)
    
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    print("SQLite DB with file " + dbfilename + " successfully created.")
    return engine, Base, Commands, session

def insertRoutineSummaryByRankInDB(Commands,session, usedmpicommands):
    icount = 0
    for i in range(len(usedmpicommands)):
        for j in range(len(usedmpicommands[i])):
            icount+=1
            minOverheadTemp = usedmpicommands[i][j][4]
            maxOverheadTemp = usedmpicommands[i][j][6]
            minBlockingTemp = usedmpicommands[i][j][5]
            maxBlockingTemp = usedmpicommands[i][j][7]
            avgOverheadTemp = usedmpicommands[i][j][8]
            avgBlockingTemp = usedmpicommands[i][j][9]
	    # set non-existing values for MPI_Init and MPI_Finalize to zero, since there are no min-max-avg values for routines only called once.
            if (usedmpicommands[i][j][0] == 'MPI_Init' or usedmpicommands[i][j][0] == 'MPI_Finalize'):
                minOverheadTemp = 0.
                maxOverheadTemp = 0.
                minBlockingTemp = 0.
                maxBlockingTemp = 0.
                avgOverheadTemp = 0.
                avgBlockingTemp = 0.
            tmp_object = Commands(indexcount=icount,rank=i,mpi_routine=usedmpicommands[i][j][0],calls=int(usedmpicommands[i][j][1]),\
			overhead=float(usedmpicommands[i][j][2]),blocking=float(usedmpicommands[i][j][3]), minOverhead=float(minOverheadTemp),\
			minBlocking=float(minBlockingTemp),maxOverhead=float(maxOverheadTemp),maxBlocking=float(maxBlockingTemp),\
			avgOverhead=float(avgOverheadTemp),avgBlocking=float(avgBlockingTemp))
            session.add(tmp_object)

    session.commit()
    print("Routine Summary by rank inserted into DB.")

def main(argv):
    #define empty strings for important variables
    inputfile = ''
    outputdir = ''
    sqlitedbfile = ''
    commandLineComment = ''
    #get command line arguments
    try:
       opts, args = getopt.getopt(argv,"hi:o:d:c:", ['input=', 'outputdir=', 'database=', 'comment='])
       if (opts != [] and '-h' not in opts[0][0]):
           print("Overwriting config file options by command line options.")
    except getopt.GetoptError: 
       print("pmpiav.py -i <inputfile> -o <output directory> -d <db filename>")
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print("pmpiav.py -i <inputfile> -o <output directory> -d <db filename> -c 'comment for output file(s)'")
          sys.exit()
       elif opt in ('-i','--input'):
          inputfile = arg
       elif opt in ('-o','--outputdir'):
          outputdir = arg
       elif opt in ('-d','--database'):
          sqlitedbfile = arg
       elif opt in ('-c','--comment'):
          commandLineComment = arg
    #initialize configparser and read config file
    config = ConfigParser()
    config.read('config')
    #read config file variable and print status messages
    commentInOutputFileEnabled = config.getboolean('comment', 'commentInOutputFileEnabled')
    if (inputfile == ''):
        inputfile = config.get('paths', 'inputfile')
    else:
        print("Using inputfile " + inputfile)
    if (outputdir == ''):
        outputdir = config.get('paths', 'outputdir')
    else:
        print("Using output directory '" + os.path.realpath(outputdir) + "'")
    if (sqlitedbfile == ''):
        sqlitedbfile = config.get('paths', 'sqlitedbfile')
    else:
        print("Using database file " + sqlitedbfile)
    if (commandLineComment == '' and commentInOutputFileEnabled == True):
        commentInOutputFile = config.get('comment', 'commentInOutputFile')
    elif (commandLineComment != '' and commentInOutputFileEnabled == True):
         commentInOutputFile = commandLineComment
         print ("Using comment from command line: '" + commentInOutputFile + "'.")
    writecsv = config.getboolean('files','writecsv')
    writehtml = config.getboolean('files','writehtml')
    writepdf = config.getboolean('files','writepdf')
    saveFigsAsPDF = config.getboolean('generalPlotting', 'saveFigsAsPDF')
    useVectorGraphics = config.getboolean('generalPlotting', 'useVectorGraphics')
    plotColumn = config.get('routineSummaryByRankPlots', 'plotColumn')
    metric = config.get('routineSummaryByRankPlots','metric')
    dpi = int(config.get('generalPlotting','dpi'))
    n = int(config.get('routineSummaryByRankPlots', 'numberOfInterest'))
    barWidth = config.getfloat('routineSummaryByRankPlots', 'barWidth')
    userTimeColor = config.get('applicationSummaryByRankPlots','userTimeColor')
    systemTimeColor = config.get('applicationSummaryByRankPlots','systemTimeColor')
    mpiTimeColor = config.get('applicationSummaryByRankPlots','mpiTimeColor')
    blockingTimeColor = config.get('applicationSummaryByRankPlots','blockingTimeColor')
    useScatterPlot = config.getboolean('MessageSummaryByRankPairPlots','useScatterPlot')
    useImShowPlot = config.getboolean('MessageSummaryByRankPairPlots','useImShowPlot')
    imShowInterpolationFilter = config.get('MessageSummaryByRankPairPlots', 'imShowInterpolationFilter')
    scatterPlotThresholdEnabled = config.getboolean('MessageSummaryByRankPairPlots', 'scatterPlotThresholdEnabled')
    dataToPlot = config.get('MessageSummaryByRankPairPlots','dataToPlot')
    scatterPlotDivider = config.getfloat('MessageSummaryByRankPairPlots','scatterPlotDivider')
    enableVerboseDBOutput = config.getboolean('misc','enableVerboseDBOutput')
    print("------- Begin of list of config values-------")
    if (writecsv == True):
        print ("CSV output enabled.")
    else:
        print ("CSV output disabled")
    if (writehtml == True):
        print ("HTML output enabled.")
    else:
        print ("HTML output disabled")
    if (writepdf == True):
        print ("PDF output enabled.")
    else:
        print ("PDF output disabled")
    if (useVectorGraphics == True):
        print ('Plots will be saved as vector graphics.')
    else:
        print ('Plots will be saved as *.PNG files with ' + str(dpi) +' DPI.')
    if (saveFigsAsPDF == True):
        print ('Plots will be additionally saved as PDF-Files.')
    if (commentInOutputFileEnabled == True):
        print ('Comment in output file enabled.')
    elif (commentInOutputFileEnabled == False):
        print ('Comment in output file disabled.')
    if (enableVerboseDBOutput):
        print ('Verbose output of DB engine enabled')
    print ("Using the following metric for Routine Summary by rank: " + metric + ".")
    print ("Plotting the " + plotColumn + " in Routine Summary by rank.")
    print ("Creating n = " + str(n) + " plots in Routine Summary by rank.")
    if (useImShowPlot == True):
        print("Creating matrix plot (pyplot.imshow) for Message Summary by Rank Pair with interpolation filter '"\
              + imShowInterpolationFilter + "'.")
    if (useScatterPlot == True):
        print("Creating scatter plot (pyplot.scatter) for Message Summary by Rank Pair. Threshold value enabled: "\
              + str(scatterPlotThresholdEnabled) + ".")
    print("------- End of list of config values-------")
    #create output directory if it does not exist
    if not os.path.exists(outputdir):
        print("Output directory does not exist, creating directory '" + os.path.realpath(outputdir) + "'")
        os.makedirs(outputdir)
    #remove old sqlite file
    if (os.path.isfile(os.path.join(outputdir,sqlitedbfile)) == True):
        os.remove(os.path.join(outputdir,sqlitedbfile))
        print("Old sqlite database file " + sqlitedbfile + " removed.")
    else:
         print("Old DB does not exist, a new one will be created.")
    #check if inputfile exists, if yes read file
    if (os.path.isfile(inputfile)):
        inputfilesize = os.path.getsize(inputfile)
        data = readInputFile(inputfile)
    else:
        print("Input file not found")
        sys.exit(2)
    htmlPath = os.path.join(outputdir, 'HTMLfiles')
    pdfPath = os.path.join(outputdir, 'PDFfiles')
    csvPath = os.path.join(outputdir, 'CSVfiles')
    #create directories for csv, html and pdf in output directory
    if (writecsv == True):
        if not os.path.exists(csvPath):
            print("Creating directory for CSV output: '" + os.path.realpath(csvPath) + "'")
            os.makedirs(csvPath)
        else:
            print("Using existing directory for CSV output: '" + os.path.realpath(csvPath) + "'")
    if (writehtml == True):
        if not os.path.exists(htmlPath):
            print("Creating directory for HTML output: '" + os.path.realpath(htmlPath) + "'")
            os.makedirs(htmlPath)
        else:
            print("Using existing directory for HTML output: '" + os.path.realpath(htmlPath) + "'")
    if (writepdf == True):
        if not os.path.exists(pdfPath):
            print("Creating directory for PDF output: '" + os.path.realpath(pdfPath) + "'")
            os.makedirs(pdfPath)
        else:
            print("Using existing directory for PDF output: '" + os.path.realpath(pdfPath) + "'")


    #start of the program
    #initialize DB
    engine, Base, Commands, session = initDB(sqlitedbfile,outputdir, enableVerboseDBOutput)
    #extract information from inputfile
    num_proc, user_time, mpi_time_with_blocking,\
    first_table_values, second_table_values, third_table_values,\
    usedmpicommands, summary_per_rank_srank_values = iFP.inputFileProcessing(data)
    #define list with filenames in routine Summary by Rank part for report saving
    routineSummaryFileList = []
    #insert routine Summary by Rank in previously created sqlite db
    insertRoutineSummaryByRankInDB(Commands,session, usedmpicommands)
    mSBRP.reorderMessageSummaryByRankPairData(num_proc, summary_per_rank_srank_values, outputdir, dpi,\
                                        useScatterPlot, scatterPlotThresholdEnabled,useImShowPlot,imShowInterpolationFilter,\
                                        dataToPlot, scatterPlotDivider,\
                                        htmlPath, pdfPath, saveFigsAsPDF,\
                                        writehtml, writepdf, useVectorGraphics)
    df, routineSummaryFileList = rSBRA.routineSummaryByRankAnalyze(Commands,session, config, plotColumn,\
                                                             metric,dpi,outputdir, routineSummaryFileList,n,
                                                             htmlPath, pdfPath, saveFigsAsPDF,\
                                                             writehtml, writepdf, barWidth, useVectorGraphics)
    time_list_first_percent, time_list_second_percent,time_list_third_percent = aSBRA.applicationSummaryByRankPlots(first_table_values,\
                                                                                      second_table_values, third_table_values, outputdir,dpi,\
                                                                                      htmlPath, pdfPath, saveFigsAsPDF,\
                                                                                      writehtml, writepdf, userTimeColor,\
                                                                                      systemTimeColor, mpiTimeColor, blockingTimeColor,\
                                                                                      useVectorGraphics)
    #get current time and date for the reports
    dtime = datetime.datetime.now()
    #call the output functions if enabled in config file
    if (writecsv == True):
       csvModule.writeCSV(csvPath, usedmpicommands, first_table_values,second_table_values,third_table_values, df)
    if (writehtml == True):
        htmlModule.writeHTML(df, outputdir, inputfile, inputfilesize, num_proc, user_time, mpi_time_with_blocking,\
                  metric, plotColumn, routineSummaryFileList, time_list_first_percent, time_list_second_percent,\
                  time_list_third_percent, commentInOutputFile,commentInOutputFileEnabled, dtime, htmlPath,\
                  userTimeColor, systemTimeColor, mpiTimeColor, blockingTimeColor, useVectorGraphics)
    if (writepdf == True):
        pdfModule.writePDF(df, outputdir, inputfile, inputfilesize, num_proc, user_time, mpi_time_with_blocking,\
                  metric, plotColumn, routineSummaryFileList, time_list_first_percent, time_list_second_percent,\
                  time_list_third_percent,commentInOutputFile,commentInOutputFileEnabled, dtime, pdfPath,\
                  userTimeColor, systemTimeColor, mpiTimeColor, blockingTimeColor, useVectorGraphics)
#call the main function with command line arguments
if __name__ == '__main__':
    main(sys.argv[1:])
