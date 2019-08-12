# pmpiav
A tool which analyzes and visualizes instrumentation files of IBM Platform MPI.

With the parameter "-i" followed by a filename, IBM Platform MPI outputs a so-called instrumentation profile as an ascii text file.
These instrumentation files contain information about the performance of an application during the run.
Since these files tend to be very large, it is not possible to analyze it manually by hand.
Here pmpiav comes in handy. It parses the text file and analyzes as well as visualizes the main parts of the file.
This makes it possible to find patterns in the file, which may have never been possible to find by hand.

# Quick Start

First, let platform_mpi create the instrumentation profile ascii text file.
pmpiav is mainly controlled via config-file.
With the standard configuration a suitable output is produced.

The tool is started via shell like this:
```sh
$ ./pmpiav.py
```
If pmpiav is started without any command-line parameters, the values stored in the config file are used.

The help can be displayed by:
```sh
$ ./pmpiav.py -h
```
The three most basic config settings can be overwritten by shell paramaters.
These are the input file (-i), the output directory (-o), the name of
the created database (-d) and a comment for the output file(s) (-c).

So for example, multiple files and directories can be used:
```sh
$ ./pmpiav.py -i file1.txt -o ~/output1
$ ./pmpiav.py -i file2.txt -o ~/output2
```
and so on.
If every input file is from a different measurement, every instance can get an individual comment:
```sh
$ ./pmpiav.py -i file1.txt -o ~/output1 -c 'Measurement on cluster1'
$ ./pmpiav.py -i file2.txt -o ~/output2 -c 'Measurement on cluster2'
```
Especially with shell scripting, command-line options are a way to easily start multiple instances consecutively.

# Config file details and explaination

The config file of pmpiav currently consists of seven different sections.
The first one, [paths] lets the user change path related settings.
These are: 
- inputfile (complete path to the input file)
- outputdir (output directory)
- sqlitedbfile (name of the sqlite database file in the output directory)

The second section [comment] lets the user enable and change the comment printed in the output files.
If **commentInOutputFileEnabled**  is set to true, the comment placed in **commentInOutputFile** will be evaluated. Otherwise **commentInOutputFile** will be ignored.

The next section [generalPlotting] contains two settings regarding the created plots.
The **dpi** value (dots per inch) influences the image quality.
The higher the value, the higher the resulting image quality will be.
The standard value is **dpi = 150**.
If **saveFigsAsPDF** is set to true, all plots will additionally be saved as a vector graphic in the pdf format in the root of the specified output directory.
**useVectorGraphics** lets the user decide whether to use vector graphics (.svg and .pdf) or bitmaps (.PNG) as a file format for the plots.

The fourth section [applicationSummaryByRankPlots] gives the user the opportunity to change the colors of the plots in the **Application Summary by Rank** part.
The colors are given in the hexadecimal format without the leading #-character, since the latex package xcolor does not require it and won't work with it.
The standard values are:
- userTimeColor = 1F78B4
- systemTimeColor = 31A354
- mpiTimeColor = A1D99B
- blockingTimeColor = B30000

The fifth section [routineSummaryByRankPlots] controls, which data is processed and plotted in the second part of the input file.
With the **plotColumn** variable, the user can name the column of the representative table, which are then processed and plotted.
The x-axis of every plot are always the MPI-ranks. This switch manipulates the content on the y-axis.
**plotColumn** can have the following values:
- calls
- overhead
- blocking
- minOverhead
- minBlocking
- maxOverhead
- maxBlocking
- avgOverhead
- avgBlocking

The first two are most valueable ones in the tests we've executed.
The program we've tested used non-blocking communication.
Therefore blocking was always zero, resulting in useless plots.

The next variable is the **metric** variable.
Here, the user can change the used metric for sorting and choosing the 'most valuable' plots.
Possible metrics are:
- cov (coefficient of variance)
- median (the value that divides a sorted list of numbers)
- mean (arithmetic)
- range (maximal value - minimal value)
- min (minimal value)
- max (maximal value)

According to these metrics, the **numberOfInterest** is the number of displayed plots with the highest value according to the chosen metric.
Example: With **numberOfInterest = 10**, **metric = mean** and **plotColumn = overhead** only the first 10 mpi routines with the highest mean value in the data set are plotted.

The **barWidth** variable sets the width of the bars displayed in the corresponding plots.
The default value provided by matplotlib is 0.8.

The second last section [MessageSummaryByRankPairPlots] controls, which data is processed and plotted in the third part of the input file.

In this part, pmpiav offers two visualizations of this matrix data.
The first one is a scatter plot, the second one is a matrix visualization provided by matplotlib called pyplot.imshow.
Imshow has the possibility to filter the visualized data.

Since the data points in the third part of the input file are independent, this does not make sense.
Therefore the **imShowInterpolationFilter** variable is set to 'none' by default.

For the scatter plot the two variables **scatterPlotThresholdEnabled** and **scatterPlotDivider** influence the result.
By setting **scatterPlotThresholdEnabled** to true, the smallest value of the data array is taken out (the 'threshold') to reduce visual clutter, since every node sends small data to every other node.

The **scatterPlotDivider** variable is the denominator, by which the data values are divided.
This is because matplotlib otherwise sets the point size that large, that the whole plot only consists of blue color hiding every detail.
The value of this variable is completely empirical and may not fit for every other dataset.
It is recommended to try multiple values and later choose the 'best fitting' value.
Lastly, **dataToPlot** determines which data should be processed and plotted:
- The number of messages sent from rank A to rank B (numberOfMessages)
- The total number of bytes sent from rank A to rank B (totalMessageBytes)

The last section [files] lets the user enable different output formats.
These are **CSV**, **HTML** and **PDF**.

# Technical details

**pmpiav** is written in python 3.6 and currently uses the following libraries:

- sys (to enable command-line parameters)
- getopt (to use command-line parameters)
- re (to parse the file via regex)
- os (for file management)
- csv (to write csv files)
- datetime (to get the current time and date)
- subprocess (to call pdflatex in order to create a pdf file from the .tex-template)
- numpy (for calculations and simple array handling)
- pandas (to create html and latex tables from a DataFrame)
- matplotlib (for plotting)
- dominate (to create html code)
- configparser (for config file usage)
- sqlalchemy (to create a db and read/write data into it)


So, how does pmpiav work?

It's simple.
First, the instrumentation file is read.
It is saved as one large string, so make sure you have enough RAM to keep this string in memory.
This is done in the function **readInputFile**.
The saving of the input file as a large string makes it possible to split and regex it later.
If the file would be processed line-by-line, it would be much harder to regex it without creating a formal language.

In the second step, the input file string is regexed and saved into the corresponding lists.
This is done in the function **inputFileProcessing**.
This function splits the file into the three parts (Application Summary by Rank, Routine Summary by Rank and Message Summary by Rank Pair).
After splitting, these parts are regexed again to get the values.

Since the second part (Routine Summary by Rank) has a lot of values to be analyzed, it is saved in a database to make this step easier.
This is done in the function **insertRoutineSummaryByRankInDB**.

The function **routineSummaryByRankAnalyze** now does some database look-up in order to get a list of all used MPI commands,
which is crucial for further processing. Then, for every command specific metrics are calculated and plots are created.

The function **applicationSummaryByRankPlots** deals with the Application Summary by Rank part of the instrumentation file.
For the first two tables, the min, max and the mean of the data sets are calculated and then visualized as area plots.

The function **reorderMessageSummaryByRankPairData** deals with the last part, the Message Summary by Rank Pair part.
As name name already tells, the data is reodered to this form [source_rank, dest_rank, value], such that a matrix visualization is possible.
Remember: Since [source_rank, dest_rank, value_1] and [dest_rank, source_rank, value_2] are two distinct data values, the matrix is symmetric.

After all data is gathered and analyzed, the results are saved in a .html, .pdf or a .csv file,
depending on the config file values the user has set in advance.
This is done in the corresponding functions **writePDF**, **writeHTML** and **writeCSV**.

Since it may be confusing to have more than 1000 LOC in one file, some functions were outsorced into modules.
These can be found in the **modules** subdirectory in the project folder.