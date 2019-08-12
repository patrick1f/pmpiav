"""Module to plot and calulate metric of  the application Summary by rank part of the instrumenation file"""
import os
import matplotlib.pyplot as plt
import numpy as np
def applicationSummaryByRankPlots(first_table_values, second_table_values, third_table_values, dir,dpi, htmlPath, pdfPath, saveFigsAsPDF, writehtml, writepdf,\
                                  userTimeColor, systemTimeColor, mpiTimeColor, blockingTimeColor, useVectorGraphics):
    """Function to plot and calculate metrics for (first_table_values, second_table_values, third_table_values lists"""
    first_table_values_list = []
    #Evaluate the first list
    #Get the percentage, not the absolute values from the list an save it into first_table_values_list
    for i in range(len(first_table_values)):
        tmp_array  = np.array([i, float(first_table_values[i][3]), float(first_table_values[i][5])]) ## only the percentage values
        first_table_values_list.append(tmp_array)
    #Calculate metrics (mean, min, max)
    first_table_values_list = np.array(first_table_values_list)
    first_user_time_avg_percent = np.mean(first_table_values_list[:,1])
    first_system_time_avg_percent = np.mean(first_table_values_list[:,2])
    
    first_user_time_min_percent = np.amin(first_table_values_list[:,1])
    first_user_time_max_percent = np.amax(first_table_values_list[:,1])
    
    first_system_time_min_percent = np.amin(first_table_values_list[:,2])
    first_system_time_max_percent = np.amax(first_table_values_list[:,2])
    #Create a stackplot
    fig, ax = plt.subplots()
    plt.stackplot(first_table_values_list[:,0], first_table_values_list[:,1],first_table_values_list[:,2], colors = ["#" + userTimeColor,"#" + systemTimeColor])
    ax.set_xlabel('MPI ranks')
    ax.set_ylabel('Time in percent')
    leg = ax.legend(['User time','System time'], loc='best')
    ax.set_aspect('auto')
    plt.title('System and MPI time distribution by rank')
    if (saveFigsAsPDF == True):
        plt.savefig(os.path.join(dir,'first_table_values.pdf'), dpi=dpi)
    if (writehtml == True):
        if (useVectorGraphics == True):
            plt.savefig(os.path.join(htmlPath,'first_table_values.svg'), dpi=dpi)
        else:
            plt.savefig(os.path.join(htmlPath,'first_table_values.png'), bbox_inches='tight', dpi=dpi)
    if (writepdf == True):
        if (useVectorGraphics == True):
            plt.savefig(os.path.join(pdfPath,'first_table_values.pdf'), dpi=dpi)
        else:
            plt.savefig(os.path.join(pdfPath,'first_table_values.png'), bbox_inches='tight', dpi=dpi)
    plt.close(fig)


    second_table_values_list = []
    for i in range(len(second_table_values)):
        tmp_array  = np.array([i, float(second_table_values[i][3]), float(second_table_values[i][5])]) ## only the percentage values
        second_table_values_list.append(tmp_array)
    
    second_table_values_list = np.array(second_table_values_list)
    #print(second_table_values_list)
    second_user_time_avg_percent = np.mean(second_table_values_list[:,1])
    second_mpi_time_avg_percent = np.mean(second_table_values_list[:,2])
    
    second_user_time_min_percent = np.amin(second_table_values_list[:,1])
    second_user_time_max_percent = np.amax(second_table_values_list[:,1])
    
    second_mpi_time_min_percent = np.amin(second_table_values_list[:,2])
    second_mpi_time_max_percent = np.amax(second_table_values_list[:,2])

    time_list_first_percent = [first_user_time_avg_percent, first_system_time_avg_percent,first_user_time_min_percent,\
                 first_user_time_max_percent, first_system_time_min_percent, first_system_time_max_percent]
    time_list_second_percent = [second_user_time_avg_percent, second_mpi_time_avg_percent,second_user_time_min_percent,\
                 second_user_time_max_percent, second_mpi_time_min_percent, second_mpi_time_max_percent]
    fig, ax = plt.subplots()
    ## area plot
    ax.stackplot(second_table_values_list[:,0], second_table_values_list[:,1], second_table_values_list[:,2], colors = ["#" + userTimeColor,"#" + mpiTimeColor])
    ## line plot
    #ax.plot(second_table_values_list[:,0], second_table_values_list[:,1])
    #ax.plot(second_table_values_list[:,0], second_table_values_list[:,2])
    #plt.ylim(0, 100)
    ax.set_xlabel('MPI ranks')
    ax.set_ylabel('Time in percent')
    ax.set_aspect('auto')
    leg = ax.legend(['User time','MPI time'], loc='best')
    plt.title('User and MPI time distribution by rank')
    if (saveFigsAsPDF == True):
        plt.savefig(os.path.join(dir,'second_table_values.pdf'), dpi=dpi)
    if (writehtml == True):
        if (useVectorGraphics == True):
            plt.savefig(os.path.join(htmlPath,'second_table_values.svg'), dpi=dpi)
        else:
            plt.savefig(os.path.join(htmlPath,'second_table_values.png'), bbox_inches='tight', dpi=dpi)
    if (writepdf == True):
        if (useVectorGraphics == True):
            plt.savefig(os.path.join(pdfPath,'second_table_values.pdf'), dpi=dpi)
        else:
            plt.savefig(os.path.join(pdfPath,'second_table_values.png'), bbox_inches='tight', dpi=dpi)
    plt.close(fig)


    third_table_values_list = []
    for i in range(len(third_table_values)):
        tmp_array  = np.array([i, float(third_table_values[i][3]), float(third_table_values[i][5])]) ## only the percentage values
        third_table_values_list.append(tmp_array)

    third_table_values_list = np.array(third_table_values_list)
    third_mpi_time_avg_percent = np.mean(third_table_values_list[:,1])
    third_blocking_time_avg_percent = np.mean(third_table_values_list[:,2])
    
    third_mpi_time_min_percent = np.amin(third_table_values_list[:,1])
    third_mpi_time_max_percent = np.amax(third_table_values_list[:,1])
    
    third_blocking_time_min_percent = np.amin(third_table_values_list[:,2])
    third_blocking_time_max_percent = np.amax(third_table_values_list[:,2])
    time_list_third_percent = [third_mpi_time_avg_percent, third_blocking_time_avg_percent,third_mpi_time_min_percent,\
                 third_mpi_time_max_percent, third_blocking_time_min_percent, third_blocking_time_max_percent]
    fig, ax = plt.subplots()
    plt.stackplot(third_table_values_list[:,0], third_table_values_list[:,1],third_table_values_list[:,2], colors = ["#" + mpiTimeColor,"#" + blockingTimeColor])
    ax.set_xlabel('MPI ranks')
    ax.set_ylabel('Time in percent')
    leg = ax.legend(['MPI time','Blocking time'], loc='best')
    ax.set_aspect('auto')
    plt.title('MPI time and Blocking time distribution by rank')
    if (saveFigsAsPDF == True):
        plt.savefig(os.path.join(dir,'third_table_values.pdf'), dpi=dpi)
    if (writehtml == True):
        if (useVectorGraphics == True):
            plt.savefig(os.path.join(htmlPath,'third_table_values.svg'), dpi=dpi)
        else:
            plt.savefig(os.path.join(htmlPath,'third_table_values.png'), bbox_inches='tight', dpi=dpi)
    if (writepdf == True):
        if (useVectorGraphics == True):
            plt.savefig(os.path.join(pdfPath,'third_table_values.pdf'), dpi=dpi)
        else:
            plt.savefig(os.path.join(pdfPath,'third_table_values.png'), bbox_inches='tight', dpi=dpi)
    plt.close(fig)
    return time_list_first_percent, time_list_second_percent, time_list_third_percent
