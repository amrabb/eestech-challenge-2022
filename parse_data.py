# če se load zmanjša in se hitrost zmanjša, je napaka
# če je load večji in je hitrost večja, je napaka

# razred za hranjenje podatkov
class Data:
    def __init__(self, dateTime, loadCurrent, pressure, turbineCurrent, turbineSpeed, turbineVoltage):
        self.dateTime = dateTime
        self.loadCurrent = 0 if len(loadCurrent) == 0 else float(loadCurrent)  # toliko turbina proizvede
        self.pressure = float(turbineSpeed) / 2000 if len(pressure) == 0 else float(pressure)
        self.turbineCurrent = 0 if len(turbineCurrent) == 0 else float(turbineCurrent)
        self.turbineSpeed = 0 if len(turbineSpeed) == 0 else float(turbineSpeed)
        self.turbineVoltage = 0 if len(turbineVoltage) == 0 else float(turbineVoltage)

    def __str__(self):
        s = "Data ( dateTime: {}, loadCurrent: {}, pressure: {}, turbineCurrent: {}, turbineSpeed: {}, turbineVoltage: {} )"
        return s.format(self.dateTime, self.loadCurrent, self.pressure, self.turbineCurrent, self.turbineSpeed, self.turbineVoltage)

# prebere podatke iz datoteke in vrne seznam
def fromFile(path):
    f = open(path, "r")
    vrstice = [line[:len(line)-1] for line in f.readlines()][1:]
    f.close()

    data = []
    for l in [line.split(",") for line in vrstice]:
        data.append(Data(l[0], l[1], l[2], l[3], l[4], l[5]))
        # print(l[0])

    return data

def fromFile2(path):
    f = open(path, "r")
    vrstice = [line[:len(line)-1] for line in f.readlines()][1:]
    f.close()

    data = []
    for l in [line.split(",") for line in vrstice]:
        data.append(Data(l[0], l[1], l[5], l[2], l[3], l[4]))
        # print(l[0])

    return data

# vrne vrstice, kjer sta load in hitrost turbine premo sorazmerni količini (glede na prejšnjo vrednost)
def getAnomalies(dataList, epsilon):
    anomalies = []

    prevLoad = None
    prevSpeed = None
    for d in dataList:
        if prevLoad == None and prevSpeed == None:
            prevLoad = d.loadCurrent
            prevSpeed = d.turbineSpeed
        else:
            if (d.loadCurrent > prevLoad and d.turbineSpeed > prevSpeed) or (d.loadCurrent < prevLoad and d.turbineSpeed < prevSpeed):
                anomalies.append(d)

    return anomalies

# vrne podatek z maksimalnim tokom vode
def getMaxLoadCurrent(dataList):
    maxVal = 0
    max = None

    for d in dataList:
        if d.loadCurrent > maxVal:
            max = d
            maxVal = d.loadCurrent
    
    return max

def getMaxPressure(dataList):
    maxVal = 0
    max = None

    for d in dataList:
        if d.pressure > maxVal:
            max = d
            maxVal = d.pressure
    
    return max

def getMaxTurbineCurrent(dataList):
    maxVal = 0
    max = None

    for d in dataList:
        if d.turbineCurrent > maxVal:
            max = d
            maxVal = d.turbineCurrent
    
    return max

def getMaxTurbineSpeed(dataList):
    maxVal = 0
    max = None

    for d in dataList:
        if d.loadCurrent > maxVal:
            max = d
            maxVal = d.loadCurrent
    
    return max
    
def getMaxTurbineVoltage(dataList):
    maxVal = 0
    max = None

    for d in dataList:
        if d.turbineVoltage > maxVal:
            max = d
            maxVal = d.turbineVoltage
    
    return max

###########################################
def getMinLoadCurrent(dataList):
    minVal = 99999999
    min = None

    for d in dataList:
        if d.loadCurrent < minVal:
            min = d
            minVal = d.loadCurrent
    
    return min

def getMinPressure(dataList):
    minVal = 99999999
    min = None

    for d in dataList:
        if d.pressure < minVal:
            min = d
            minVal = d.pressure
    
    return min

def getMinTurbineCurrent(dataList):
    minVal = 99999999
    min = None

    for d in dataList:
        if d.turbineCurrent < minVal:
            min = d
            minVal = d.turbineCurrent
    
    return min

def getMinTurbineSpeed(dataList):
    minVal = 99999999
    min = None

    for d in dataList:
        if d.turbineSpeed < minVal:
            min = d
            minVal = d.turbineSpeed
    
    return min

def getMinTurbineVoltage(dataList):
    minVal = 99999999
    min = None

    for d in dataList:
        if d.turbineVoltage < minVal:
            min = d
            minVal = d.turbineVoltage
    
    return min

##########################################

def getAvgLoadCurrent(dataList):
    avg = 0

    for d in dataList:
        avg += d.loadCurrent
    
    return avg / len(dataList)


def getAvgPressure(dataList):
    avg = 0

    for d in dataList:
        avg += d.pressure
    
    return avg / len(dataList)

def getAvgTurbineCurrent(dataList):
    avg = 0

    for d in dataList:
        avg += d.turbineCurrent
    
    return avg / len(dataList)

def getAvgTurbineSpeed(dataList):
    avg = 0

    for d in dataList:
        avg += d.turbineSpeed
    
    return avg / len(dataList)

def getAvgTurbineVoltage(dataList):
    avg = 0

    for d in dataList:
        avg += d.turbineVoltage
    
    return avg / len(dataList)