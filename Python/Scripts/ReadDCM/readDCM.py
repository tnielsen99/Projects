from itertools import islice
import re
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

path = 'C:\\Users\\timo.nielsen\\OneDrive - McLaren Technology Group\\MPO_Calibration\\Programme\\P16\\Calibration\\1. Dyno\\DCM\\1. forDyno\\SW1152_ETM_Update\\ExhMod_TExhVlvMdl-1.14.0-Jcs-25%-190608-All.dcm'
file = open(path, 'r')
dcm = file.readlines()

testDict = {}
copy = False
# Read in codewords
for line in dcm:
    value = []
    if 'FESTWERT' in line:
        valName = (line.split('FESTWERT ', 1)[1]).strip('\n')
        testDict[valName] = {}
        copy = True
        continue
    elif "END" in line:
        copy = False
        continue
    elif copy:
        if 'WERT' in line:
            value = (line.split('   WERT ', 1)[-1].strip('\n'))
            testDict[valName]['V'] = value
        if 'EINHEIT_W' in line:
            unitName = (line.split('   EINHEIT_W ', 1)[-1].strip('\n'))
            testDict[valName]['Unit'] = unitName
        if 'LANGNAME' in line:
            longName = line.split('   LANGNAME ', 1)[-1].strip('"\n')
            testDict[valName]['Description'] = longName


# Read in curves
for line in dcm:
    v_value_c = []
    x_value_c = []
    y_value_c = []
    print('in first loop')
    if 'KENNLINIE' in line:
        print('in second loop')
        valName = (line.split('KENNLINIE ', 1)[1]).split("_T ", 1)[0]
        testDict[valName] = {}
        print(valName)
        copy = True
        continue
    elif "END" in line:
        copy = False
        continue
    elif copy:
        print('last loop')
        print(line)
        if 'WERT' in line:
            v_value_c = (line.split('   WERT ', 1)[-1].strip('\n'))
            testDict[valName]['V'] = v_value_c.join(v_value_c)
            print('in wert')
        if 'ST/X' in line:
            x_value_c = (line.split('   ST/X ', 1)[-1].strip('\n'))

        if 'EINHEIT_W' in line:
            unitName = (line.split('   EINHEIT_W ', 1)[-1].strip('\n'))
            testDict[valName]['Unit'] = unitName
            print('in einheit_w')
        if 'EINHEIT_X' in line:
            xunitName = (line.split('   EINHEIT_X ', 1)[-1].strip('\n'))
            testDict[valName]['Unit_X'] = xunitName
        if 'LANGNAME' in line:
            longName = line.split('   LANGNAME ', 1)[-1].strip('"\n')
            testDict[valName]['Description'] = longName
    #x_value_c = x_value_c.append(x_value_c)
    #testDict[valName]['X'] = x_value_c
    print('in st/x')
    print(x_value_c)


# Read in Maps
for line in dcm:
    if 'KENNFELD' in line:
        valName = (line.split('KENNFELD ', 1)[1]).split("_M ", 1)[0]
        testDict[valName] = {}
        copy = True
        continue
    elif "END" in line:
        copy = False
        continue
    elif copy:
        v_value_m = []
        x_value_m = []
        y_value_m = []
        if 'WERT' in line:
            v_value_m = (line.split('   WERT ', 1)[-1].strip('\n'))
            testDict[valName]['V'] = v_value_m.join(v_value_m)
        if 'ST/X' in line:
            x_value_m = (line.split('   ST/X ', 1)[-1].strip('\n'))
            testDict[valName]['X'] = x_value_m.join(x_value_m)
        if 'ST/Y' in line:
            y_value_m = (line.split('   ST/Y ', 1)[-1].strip('\n'))
            testDict[valName]['Y'] = y_value_m.join(y_value_m)
        if 'EINHEIT_W' in line:
            vunitName = (line.split('   EINHEIT_W ', 1)[-1].strip('\n'))
            testDict[valName]['Unit_V'] = vunitName
        if 'EINHEIT_X' in line:
            xunitName = (line.split('   EINHEIT_X ', 1)[-1].strip('\n'))
            testDict[valName]['Unit_X'] = xunitName
        if 'EINHEIT_Y' in line:
            yunitName = (line.split('   EINHEIT_Y ', 1)[-1].strip('\n'))
            testDict[valName]['Unit_Y'] = yunitName
        if 'LANGNAME' in line:
            longName = line.split('   LANGNAME ', 1)[-1].strip('"\n')
            testDict[valName]['Description'] = longName

print(testDict)
x = testDict.get('ExhMod_tiConTExhVlvFcoB1').get('X')
y = testDict.get('ExhMod_tiConTExhVlvFcoB1').get('Y')
# z = testDict.get('ExhMod_tExhVlvHomB1', {}).get('V', {})

print(x, y)

# fig = plt.figure()
# ax = fig.gca(projection='3d')
# print(x)
# X, Y = np.meshgrid(x, y)
# Z = np.array(z).reshape(len(x), len(y))
# surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.winter, linewidth=0, antialiased=True)
