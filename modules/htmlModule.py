"""Module to create a full html report"""
import os
import dominate
from dominate.tags import *
from dominate.util import raw
def writeHTML(df, dir, inputfile, inputfilesize, num_proc, user_time, mpi_time_with_blocking, metric,\
              plotColumn, routineSummaryFileList, time_list_first_percent, time_list_second_percent,\
              time_list_third_percent, commentInOutputFile,commentInOutputFileEnabled,dtime, htmlPath,\
              userTimeColor, systemTimeColor, mpiTimeColor, blockingTimeColor, useVectorGraphics):
    #Get dataframe (the metrics table is included here)
    html = df.to_html()
    dtitle = 'Platform MPI Performance report for file ' + inputfile + " on " + dtime.strftime("%c")
    #Initialize html document "d" with dominate library
    d = dominate.document(title=dtitle)
    #Add the first container in the html document
    with d.add(div(id='content_firstpart')):
        h2(dtitle)
        #Add the paragraphs
        p('Size of ' + inputfile +" is " + str(inputfilesize) + " bytes.")
        p('MPI processes used: ' + str(num_proc[0]))
        p('User time: ' + str(user_time[0]) + "%")
        p('MPI time: ' + str(mpi_time_with_blocking[0][0]) + "%" + "  [Overhead: " + str(mpi_time_with_blocking[0][1]) + "%, Blocking: "+ mpi_time_with_blocking[0][2] + "%]")
        if (commentInOutputFileEnabled == True):
            p('Comment: ' + commentInOutputFile)
        h3('First part: Application Summary by Rank')
        p('The following data is depicted in percent.')
        #Add the tables for application Summary by rank
        with table(border='1').add(tbody()):
            l = tr()
            l.add(th())
            l.add(th('min'))
            l.add(th('max'))
            l.add(th('mean'))
            h = tr()
            h.add(th('user time', style="background-color:#"+ userTimeColor + ";"))
            h.add(td(round(time_list_first_percent[2],2)))
            h.add(td(round(time_list_first_percent[3],2)))
            h.add(td(round(time_list_first_percent[0],2)))
            k = tr()
            k.add(th('system time', style="background-color:#"+ systemTimeColor + ";"))
            k.add(td(round(time_list_first_percent[4],2)))
            k.add(td(round(time_list_first_percent[5],2)))
            k.add(td(round(time_list_first_percent[1],2)))
        with table(border='1').add(tbody()):
            m = tr()
            m.add(th())
            m.add(th('min'))
            m.add(th('max'))
            m.add(th('mean'))
            n = tr()
            n.add(th('user time', style="background-color:#"+ userTimeColor + ";"))
            n.add(td(round(time_list_second_percent[2],2)))
            n.add(td(round(time_list_second_percent[3],2)))
            n.add(td(round(time_list_second_percent[0],2)))
            o = tr()
            o.add(th('mpi time', style="background-color:#"+ mpiTimeColor + ";"))
            o.add(td(round(time_list_second_percent[4],2)))
            o.add(td(round(time_list_second_percent[5],2)))
            o.add(td(round(time_list_second_percent[1],2)))
        br() #new line
        with table(border='1').add(tbody()):
            r = tr()
            r.add(th())
            r.add(th('min'))
            r.add(th('max'))
            r.add(th('mean'))
            s = tr()
            s.add(th('mpi time', style="background-color:#"+ mpiTimeColor + ";"))
            s.add(td(round(time_list_third_percent[2],2)))
            s.add(td(round(time_list_third_percent[3],2)))
            s.add(td(round(time_list_third_percent[0],2)))
            t = tr()
            t.add(th('blocking time', style="background-color:#"+ blockingTimeColor + ";"))
            t.add(td(round(time_list_third_percent[4],2)))
            t.add(td(round(time_list_third_percent[5],2)))
            t.add(td(round(time_list_third_percent[1],2)))
        br() #new line
        fileEnding = 'svg'
        if (useVectorGraphics == False):
            fileEnding = 'png'
        #Add the plots after the tables
        img(src='first_table_values.' + fileEnding, id='first_table_values')
        img(src='second_table_values.' + fileEnding, id='second_table_values')
        img(src='third_table_values.' + fileEnding, id='third_table_values')
        br() #new line
        
    with d.add(div(id='content_secondpart')):
        h3('Second part: Routine Summary by Rank')
        #depending on which colums of the routine Summary per rank have to be plotted, the description text is choosen
        if (plotColumn == "overhead"):
            p('The values depicted in the following plots are the overhead of the specific routine calls in ms on the y-axis and the MPI ranks on the x-axis.')
        elif (plotColumn == "calls"):
            p('The values depicted in the following plots are the number of calls of the specific routine on the y-axis and the MPI ranks on the x-axis.')
        elif (plotColumn == "blocking"):
            p('The values depicted in the following plots are the blocking of the specific routine calls in ms on the y-axis and the MPI ranks on the x-axis.')
        elif (plotColumn == "minBlocking"):
            p('The values depicted in the following plots are the minimal blocking of the specific routine calls in ms on the y-axis and the MPI ranks on the x-axis.')
        elif (plotColumn == "maxBlocking"):
            p('The values depicted in the following plots are the maximal blocking of the specific routine calls in ms on the y-axis and the MPI ranks on the x-axis.')
        elif (plotColumn == "avgBlocking"):
            p('The values depicted in the following plots are the average blocking of the specific routine calls in ms on the y-axis and the MPI ranks on the x-axis.')
        elif (plotColumn == "minOverhead"):
            p('The values depicted in the following plots are the minimal overhead of the specific routine calls in ms on the y-axis and the MPI ranks on the x-axis.')
        elif (plotColumn == "maxOverhead"):
            p('The values depicted in the following plots are the maximal overhead of the specific routine calls in ms on the y-axis and the MPI ranks on the x-axis.')
        elif (plotColumn == "avgOverhead"):
            p('The values depicted in the following plots are the average overhead of the specific routine calls in ms on the y-axis and the MPI ranks on the x-axis.')
        for filename in routineSummaryFileList:
            img(src=filename + '.' + fileEnding, id=filename)
        p('The following table is sorted by ' + metric + '.')
        if (plotColumn == "overhead"):
            p('The values are the overhead of the specific routine calls in ms.')
        elif (plotColumn == "calls"):
            p('The values are the number of calls of the specific routine.')
        elif (plotColumn == "blocking"):
            p('The values are the blocking of the specific routine calls in ms.')
        elif (plotColumn == "minBlocking"):
            p('The values are the minimal blocking of the specific routine calls in ms.')
        elif (plotColumn == "maxBlocking"):
            p('The values are the maximal blocking of the specific routine calls in ms.')
        elif (plotColumn == "avgBlocking"):
            p('The values are the average blocking of the specific routine calls in ms.')
        elif (plotColumn == "minOverhead"):
            p('The values are the minimal overhead of the specific routine calls in ms.')
        elif (plotColumn == "maxOverhead"):
            p('The values are the maximal overhead of the specific routine calls in ms.')
        elif (plotColumn == "avgOverhead"):
            p('The values are the average overhead of the specific routine calls in ms.')
    d.add(raw(html)) #Add the metrics table in raw html, because html code comes from the pandas library
    with d.add(div(id='content_thirdpart')):
       h3('Third part: Message Summary by Rank Pair')
       img(src='imshow.' + fileEnding, id='imshow')
       img(src='scatter.'+ fileEnding, id='scatter')
    d = d.render()
    f = open(os.path.join(htmlPath,'report.html'), 'wt', encoding='utf-8')
    f.write(str(d))
    f.close()
    print("HTML output finished.")