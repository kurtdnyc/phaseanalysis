from scipy.interpolate import interp1d
from scipy.signal import savgol_filter, find_peaks
from scipy.optimize import curve_fit
from PyAstronomy import pyaC
import matplotlib.pyplot as plt
import numpy as np
import sys, time, csv

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
start=time.time()

toWrite = False
csvfilename1 = args[0]
csvfilename2 = args[1]

# Oscilliscope trigger will never deliver a consistent start time
# the data output usually starts with a negative time in relation to trigger latency
# to make the data easy to use with pyplot we zero the time domain with LevelTimeRange

DualChannel, SoloChannel = LevelTimeRange(csvfilename1, csvfilename2)
if "-w" in opts:
    toWrite = True
if "-diff" in opts:
    difference(DualChannel, SoloChannel, toWrite)
elif "-phase" in opts:
    phase(DualChannel, SoloChannel, toWrite)
else:
    raise SystemExit(f"Usage: {sys.argv[0]} (-diff | -phase | -w) <2 channel data csv file> <Solo csv data> ...")



def LevelTimeRange(csvfilename1, csvfilename2):
    x,x2,y,y2,s,s2 = ([] for i in range(6))

    with open(csvfilename1, 'r') as csvFile1:
        reader = csv.reader(csvFile1)
        for row in reader:
            y.append(float(row[1]))
        temp = list(reader)
        for i in range(1,len(temp)):
            s.append(float(temp[i][0])-float(temp[i-1][0]))
    csvFile1.close()

    with open(csvfilename2, 'r') as csvFile2:
        reader = csv.reader(csvFile2)
        for row in reader:
            y2.append(float(row[1]))
        temp = list(reader)
        for i in range(1, len(temp)):
            s2.append(float(temp[i][0]) - float(temp[i - 1][0]))
    csvFile2.close()

    samplingrate = float(sum(s) / (len(s) - 1))
    samplingrate2 = float(sum(s2) / (len(s2) - 1))

    for i in range(len(y)):
        x.append(float(i * samplingrate))
    for i in range(len(y2)):
        x2.append(float(i * samplingrate2))


    xa=np.array(x)
    ya=np.array(y)
    xa2 = np.array(x2)
    ya2 = np.array(y2)

    Dual = (xa,ya)
    Solo = (xa2,ya2)

    print('Zeroing took', int(time.time() - start), 'seconds to finish.')

    return Dual, Solo

def smooth(a,b):
    itp = interp1d(a, b, kind='cubic')
    window_size, poly_order = 181, 3
    q = savgol_filter(itp(a), window_size, poly_order)
    return q

def difference(DualChannel, SoloChannel, toWrite):
    x, y = DualChannel
    x2, y2 = SoloChannel

    ax = np.asarray(x)
    ay = np.asarray(y)
    ax2 = np.asarray(x2)
    ay2 = np.asarray(y2)

    if len(x2) > len(x):
        time = np.asarray(Diff(x, x2))
    elif len(x) > len(x2):
        time = np.asarray(Diff(x2, x))
    elif len(x) == len(x2):
        time = ax

    tp = np.array(ax)
    fp = np.array(ay)
    tp2 = np.array(ax2)
    fp2 = np.array(ay2)

    # The constant reassignment to np.arrays had some purpose when i wrote this, but I'm at a loss for what that was
    # or if this was even necessary
    combined = np.vstack((tp, fp)).T
    combined2 = np.vstack((tp2, fp2)).T



    # The following 2 loops ensure an extra y coordinate wasn't left over from zeroing, which would break pyplot
    j = []
    for i in range(len(combined)):
        if combined[i][0] <= time[0]:
            j.append(int(i))
        elif combined[i][0] >= time[-1]:
            j.append(int(i))
    new_y = np.delete(ay, j)

    k = []
    for i in range(len(combined2)):
        if combined2[i][0] <= time[0]:
            k.append(int(i))
        elif combined2[i][0] >= time[-1]:
            k.append(int(i))
    new_y2 = np.delete(ay2, k)

    matchedtime = []
    difference = []
    for i in range(len(new_y)):
        matchedtime.append(time[i])
        dy = (new_y2[i] - new_y[i])
        difference.append(dy)


    matchedtimea = np.array(matchedtime)
    differencea = np.array(difference)
    differencea = smooth(matchedtime, differencea)

    if toWrite:
        Newfilename = "inputimpedance_{}_{}".format(csvfilename1,csvfilename2)
        with open(Newfilename, mode='w') as csv_file:
            fieldnames = ['t', 'y']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            for i in range(len(matchedtimea)):
                writer.writerow({'t': matchedtimea[i], 'y': differencea[i]})
        csv_file.close()
        print('CSV wrote after', int(time.time() - start), 'seconds.')

    f, axarr = plt.subplots(3, sharex=True)
    axarr[0].plot(x, y)
    axarr[0].set_title('Dual channel')
    axarr[1].plot(x2, y2)
    axarr[1].set_title('Solo Channel')
    axarr[2].plot(matchedtimea, differencea)
    axarr[2].set_title('Difference')
    plt.axis([time[0], time[-1], -10, 10])
    plt.ylabel('Voltage measured')
    plt.xlabel('time (s)')
    plt.show()

def phase(DualChannel,SoloChannel, toWrite):
    print("find latest code")
    pass
    # x = np.array(xa)
    # y = np.array(ya)
    # x2 = np.array(x2a)
    # y2 = np.array(y2a)
    # y = clean(x, y)
    # y2 = clean(x2, y2)
    #
    # # Set the last data point to zero.
    # # It will not be counted as a zero crossing!
    # y[-1] = 0
    # y2[-1] = 0
    #
    # # Set point to zero. This will be counted as a
    # # zero crossing
    # y[0] = 0.00000
    # y2[0] = 0.00000
    # # Get coordinates and indices of zero crossings
    # xc, xi = pyaC.zerocross1d(x, y, getIndices=True)
    # x2c, x2i = pyaC.zerocross1d(x2, y2, getIndices=True)








