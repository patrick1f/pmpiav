"""Module to process the message Summary by rank data from the instrumentation file."""
import re
import matplotlib.pyplot as plt
import os
import numpy as np
def reorderMessageSummaryByRankPairData(num_proc, summary_per_rank_srank_values, dir,dpi,\
                                        useScatterPlot, scatterPlotThresholdEnabled,useImShowPlot,imShowInterpolationFilter, dataToPlot, scatterPlotDivider,
                                        htmlPath, pdfPath, saveFigsAsPDF,writehtml, writepdf, useVectorGraphics):
    """Function to process the message Summary by rank data from the instrumentation file."""
    if not (useScatterPlot == False and useImShowPlot == False): #if both plots are unwanted, why compute everything?
        #summary_per_srank_for_each_drank is a 2 dimensial arry [i][j] with i equals the srank and j the drank
        summary_per_srank_for_each_drank = [0] * int((num_proc[0]))
        #Test
        #print(type(summary_per_srank_for_each_drank))
        for i in range(len(summary_per_rank_srank_values)):
            #print ("---------------------" + str(i) + "---------------------")
            #print(summary_per_rank_srank_values[i][1]) 
            summary_per_srank_for_each_drank[i] = re.findall(r"(?:\r?\n|^)((?:\r?\n|.)+?)(?=\r?\n\r?\n|$)", str(summary_per_rank_srank_values[i][1])) # no multiline here, otherwise it wont match the content between each empty line
            #print (summary_per_srank_for_each_drank[i][j]) #source rank i, destination rank j=1
    
        #first line of message Summary by rank table (only with round brackets)
        list3 = []
        srank_drank_value_tuples_round = [[0]* int((num_proc[0]))] * int((num_proc[0]))
        if (dataToPlot == 'numberOfMessages'):
            for i in range(len(summary_per_rank_srank_values)):
                #print ("-------------------------" + "i=" + str(i) + "  ----------------------------------")
                for j in range(len(summary_per_rank_srank_values)):
                    #print ("---------------------"+ " Source Rank: " + str(i) + " Destination Rank: " + str(j) +"---------------------")
                    i_string = str(i)
                    srank_drank_value_tuples_round[i][j] =(re.findall(r"^\s*(?P<DRank>\d+)\s+(?P<Messages>\d+)\s+\((?P<minvalue>\d+),\s(?P<maxvalue>\d+)\)\s+(?P<totalbytes>\d+)", str(summary_per_srank_for_each_drank[i][j]), re.MULTILINE))
                    #srank_drank_value_tuples_round[i][j] = print(re.findall(r"^\s*(?P<DRank>\d+)\s+(?P<Messages>\d+)\s+\((?P<minvalue>\d+),\s(?P<maxvalue>\d+)\)\s+(?P<totalbytes>\d+)", str(summary_per_srank_for_each_drank[i][j]), re.MULTILINE))
                    #tmp =np.array((str((i_string,) + srank_drank_value_tuples_round[i][j][0]))) #srank i, drank j, first tuple
                    #tmp_all = np.array ([i, int(srank_drank_value_tuples_round[i][j][0][0]),int(srank_drank_value_tuples_round[i][j][0][1]), int(srank_drank_value_tuples_round[i][j][0][2]),int(srank_drank_value_tuples_round[i][j][0][3]), int(srank_drank_value_tuples_round[i][j][0][4])])
                    tmp_msg_number_only = np.array ([i, int(srank_drank_value_tuples_round[i][j][0][0]),int(srank_drank_value_tuples_round[i][j][0][1])])
                    #tmp_msg_totalbytes_only = np.array ([i, int(srank_drank_value_tuples_round[i][j][0][0]),int(srank_drank_value_tuples_round[i][j][0][4])])
                    #srank_drank_value_tuples_round[i][j] = (i,) + srank_drank_value_tuples_round[i][j][0]
                    #print(srank_drank_value_tuples_round[i][j][0]) #srank i, drank j, first tuple
                    list3.append(tmp_msg_number_only)
            np.set_printoptions(threshold=np.nan)
            list3 = np.array(list3)	
            #print (list3)
        elif (dataToPlot == 'totalMessageBytes'):
            for i in range(len(summary_per_rank_srank_values)):
                #print ("-------------------------" + "i=" + str(i) + "  ----------------------------------")
                for j in range(len(summary_per_rank_srank_values)):
                    #print ("---------------------"+ " Source Rank: " + str(i) + " Destination Rank: " + str(j) +"---------------------")
                    i_string = str(i)
                    srank_drank_value_tuples_round[i][j] =(re.findall(r"^\s*(?P<DRank>\d+)\s+(?P<Messages>\d+)\s+\((?P<minvalue>\d+),\s(?P<maxvalue>\d+)\)\s+(?P<totalbytes>\d+)", str(summary_per_srank_for_each_drank[i][j]), re.MULTILINE))
                    #srank_drank_value_tuples_round[i][j] = print(re.findall(r"^\s*(?P<DRank>\d+)\s+(?P<Messages>\d+)\s+\((?P<minvalue>\d+),\s(?P<maxvalue>\d+)\)\s+(?P<totalbytes>\d+)", str(summary_per_srank_for_each_drank[i][j]), re.MULTILINE))
                    #tmp =np.array((str((i_string,) + srank_drank_value_tuples_round[i][j][0]))) #srank i, drank j, first tuple
                    #tmp_all = np.array ([i, int(srank_drank_value_tuples_round[i][j][0][0]),int(srank_drank_value_tuples_round[i][j][0][1]), int(srank_drank_value_tuples_round[i][j][0][2]),int(srank_drank_value_tuples_round[i][j][0][3]), int(srank_drank_value_tuples_round[i][j][0][4])])
                    #tmp_msg_number_only = np.array ([i, int(srank_drank_value_tuples_round[i][j][0][0]),int(srank_drank_value_tuples_round[i][j][0][1])])
                    tmp_msg_totalbytes_only = np.array ([i, int(srank_drank_value_tuples_round[i][j][0][0]),int(srank_drank_value_tuples_round[i][j][0][4])])
                    #srank_drank_value_tuples_round[i][j] = (i,) + srank_drank_value_tuples_round[i][j][0]
                    #print(srank_drank_value_tuples_round[i][j][0]) #srank i, drank j, first tuple
                    list3.append(tmp_msg_totalbytes_only)
            np.set_printoptions(threshold=np.nan)
            list3 = np.array(list3)	
            #print (list3)
            #all lines after first line (only with square brackets), may be multiple lines aka multiple tuples. this part is not used.
            #srank_drank_value_tuples_square = [[0]* int((num_proc[0]))] * int((num_proc[0]))
            #for i in range(len(summary_per_rank_srank_values)):
            #    for j in range(len(summary_per_rank_srank_values)):
                     #print ("---------------------"+ " Source Rank: " + str(i) + " Destination Rank: " + str(j) +"---------------------")
                     #srank_drank_value_tuples_square[i][j] = re.findall(r"\s+(?P<Messages>\d+)\s+\[(?P<minvalue>\d+)..(?P<maxvalue>\d+)\]\s+(?P<totalbytes>\d+)",str(summary_per_srank_for_each_drank[i][j])) # no multiline
                     #print(srank_drank_value_tuples_square[i][j]) #srank i, drank j, [0] - first line, [1] - second line ...
        


        #Plots (imshow and individual scatter plot)
        titleString = ""
        ### with numpy reshape
        if (useImShowPlot == True):
            list4 = list3.reshape(int(np.sqrt(list3.shape[0])),int(np.sqrt(list3.shape[0])),3)
            fig, ax = plt.subplots()
            cax = ax.imshow(list4[:,:,2],interpolation=imShowInterpolationFilter, cmap='Blues')
            ax.set_xlabel('Source MPI ranks')
            ax.set_ylabel('Destination MPI ranks')
            ax.set_aspect('auto')    
            if (dataToPlot == 'numberOfMessages'):
                titleString = "Matrix plot showing the number of messages \n sent between MPI ranks filtered \n with '"\
                               + imShowInterpolationFilter + "' filter enabled."
            elif (dataToPlot == 'totalMessageBytes'):
                titleString = "Matrix plot showing the total bytes \n sent between MPI ranks filtered \n with '"\
                               + imShowInterpolationFilter + "' filter enabled."
            ax.set_title(titleString)
            cbar = fig.colorbar(cax)
            if (saveFigsAsPDF == True):
                plt.savefig(os.path.join(dir,'imshow.pdf'), dpi=dpi)
            if (writehtml == True):
                if (useVectorGraphics == True):
                    plt.savefig(os.path.join(htmlPath,'imshow.svg'), dpi=dpi)
                else:
                    plt.savefig(os.path.join(htmlPath,'imshow.png'), bbox_inches='tight', dpi=dpi)
            if (writepdf == True):
                if (useVectorGraphics == True):
                    plt.savefig(os.path.join(pdfPath,'imshow.pdf'), dpi=dpi)
                else:
                    plt.savefig(os.path.join(pdfPath,'imshow.png'), bbox_inches='tight', dpi=dpi)
            plt.close(fig)
            print("Matrix plot finished.")
        ### scatter plot with matplotlib
        if (useScatterPlot == True):
            fig, ax = plt.subplots()
            scatterThreshold = 0
            if (scatterPlotThresholdEnabled):
                scatterThreshold = np.min(list3[:,2])
                print ("Scatter plot threshold is " + str(scatterThreshold) + ".")
            ax.scatter(list3[:,0],list3[:,1],((list3[:,2])-scatterThreshold)/scatterPlotDivider,marker ='o')
            # 5600 is the minimum size of messages sent to every rank for n=96 in ls-dyna dynampitrace.txt
            ax.set_xlabel('Source MPI ranks')
            ax.set_ylabel('Destination MPI ranks')
            ax.set_aspect('auto')
            if (dataToPlot == 'numberOfMessages'):
                titleString = "Scatter plot showing the number \n of messages sent between MPI ranks (Threshold = " + str(scatterThreshold) +")"
            elif (dataToPlot == 'totalMessageBytes'):
                titleString = "Matrix plot showing the total bytes \n sent between MPI ranks (Threshold = " + str(scatterThreshold) +")"
            ax.set_title(titleString)
            if (saveFigsAsPDF == True):
                plt.savefig(os.path.join(dir,'scatter.pdf'), dpi=dpi)
            if (writehtml == True):
                if (useVectorGraphics == True):
                    plt.savefig(os.path.join(htmlPath,'scatter.svg'), dpi=dpi)
                else:
                    plt.savefig(os.path.join(htmlPath,'scatter.png'), bbox_inches='tight', dpi=dpi)
            if (writepdf == True):
                if (useVectorGraphics == True):
                    plt.savefig(os.path.join(pdfPath,'scatter.pdf'), dpi=dpi)
                else:
                    plt.savefig(os.path.join(pdfPath,'scatter.png'), bbox_inches='tight', dpi=dpi)
            plt.close(fig)
            print("Scatter plot finished.")