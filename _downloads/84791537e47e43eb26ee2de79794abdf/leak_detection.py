from typing import List
import datetime
import json
import os
# ne importat fajlov, ker se pri testiranju ne bodo importali

def convert_date_to_seconds(date_string, start_date_string='2022-03-01 00:00:00'):
    d = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    start = datetime.datetime.strptime(start_date_string, '%Y-%m-%d %H:%M:%S')
    return int((d - start).total_seconds())

def puscaAlNe(puscaAvg, nePuscaAvg, novPritisk):
    if abs(puscaAvg - novPritisk) > abs(nePuscaAvg - novPritisk):
        return False

    return True

def getAverage(arr):
    sum = 0

    for val in arr:
        sum += val

    return sum / len(arr)

class Data:
    def __init__(self, dateTime, loadCurrent, pressure, turbineCurrent, turbineSpeed, turbineVoltage):
        self.dateTime = dateTime
        self.loadCurrent = 0 if len(loadCurrent) == 0 else float(loadCurrent)  # toliko turbina proizvede
        self.pressure = 0 if len(pressure) == 0 else float(pressure)
        self.turbineCurrent = 0 if len(turbineCurrent) == 0 else float(turbineCurrent)
        self.turbineSpeed = 0 if len(turbineSpeed) == 0 else float(turbineSpeed)
        self.turbineVoltage = 0 if len(turbineVoltage) == 0 else float(turbineVoltage)

    def __str__(self):
        s = "Data ( dateTime: {}, loadCurrent: {}, pressure: {}, turbineCurrent: {}, turbineSpeed: {}, turbineVoltage: {} )"
        return s.format(self.dateTime, self.loadCurrent, self.pressure, self.turbineCurrent, self.turbineSpeed, self.turbineVoltage)

class LeakDetection:
    """
    For correct automatic evaluation please implement your prediction logic inside this class
    """

    def __init__(self, dirname='.'):
        self.model = self.load_model(dirname)

    def getPressureValuesByLeakingState(self):
        resultsFile = open(os.path.join(os.path.dirname(__file__), "../train_data/results.json"), "r")
        contents = resultsFile.read()
        resultsFile.close()
        results = json.loads(contents)["prediction_results"]

        leakLists = []  # seznam para seznamov - eden z meritvami pritiska ob puščanju, drugi z meritvami pritiska ob normalnem stanju

        leak = []
        noLeak = []

        for i in range(len(results)): 

            end_periods = results[i]["end_periods"]
            leakages = results[i]["leakages"]
            fname = results[i]["file_name"]

            dataFile = open(os.path.join(os.path.dirname(__file__), "../train_data/{}".format(fname)), "r")
            lines = [l[:-1] for l in dataFile.readlines()[1:]]  # odrežemo header in znak za novo vrstico vsake vrstice
            dataFile.close()

            lIndex = 0  # indeks trenutnega elementa seznama leakages, ki ga obravnavamo
            pIndex = 0  # indeks trenutnega elementa seznama end_periods, ki ga obravnavamo

            for l in [x.split(",") for x in lines]:  # gre čez vse podatke
                t = convert_date_to_seconds(l[0])
                if t <= end_periods[pIndex]:
                    if len(l[5]) > 0: 
                        p = float(l[5])
                        (leak if leakages[lIndex] == 1 else noLeak).append(p)

                if t == end_periods[pIndex]:
                    pIndex += 1
                    lIndex += 1
                    if (pIndex >= len(end_periods)):  # če smo presegli obseg seznama, prekinemo (ostati ne bi smela nobena neobdelana vrstica)
                        break

        return {"leak": leak, "noLeak": noLeak}

    def load_model(self, dirname):
        """
        Loads your pretrained model to use it for prediction.
        Please use os.path.join(location_to_dir, model_file_name)

        :param dirname: Path to directory where model is located
        :return: your pretrained model, if no model is required return None

        Example:
            import os
            import joblib
            load(os.path.join(self.dirname, 'tree.joblib'))

        """

        return None

    def predict(self, features: List) -> bool:
        """
        Your implementation for prediction. If leak is detected it should return true.

        :param features: A list of features
        :return: should return true if leak is detected. Otherwise, it should return false.

        Example:
            return self.model.predict(features) == 0

        """ 

        leakAvg = 1.658914824064667
        noLeakAvg = 1.8174741437730197
        
        # vrednosti leakAvg in noLeakAvg sta bili pridobljeni z naslednjim algoritmom 

        l = features
        p = 0 if len(l[5]) == 0 else float(l[5])

        # če ni podatkov o tlaku, predpostavimo, da ne pušča
        if p == 0:
            return False
        
        return puscaAlNe(leakAvg, noLeakAvg, p)

# funkcija, ki gre čez podatke v train data in vrne povprečni vrednosti tlaka v obdobjih, ko je cev puščala in v obdobjih, ko ni
def natreniraj():
    ld = LeakDetection()
    seznami = ld.getPressureValuesByLeakingState()
    leakAvg = sum(seznami["leak"]) / len(seznami["leak"])
    noLeakAvg = sum(seznami["noLeak"]) / len(seznami["noLeak"])
    return (leakAvg, noLeakAvg)
