import json
import parse_data
import matplotlib.pyplot as plt
import numpy as np

import src.utils.utils

prediction_results = []
for fileno in range(100):
    file_name = "scenario_week_example_{}.csv".format(fileno)
    arr = parse_data.fromFile("unsupervised_dataset/{}".format(file_name))

    # print(parse_data.getMaxLoadCurrent(arr))
    # print(parse_data.getMaxPressure(arr))
    # print(parse_data.getMaxTurbineCurrent(arr))
    # print(parse_data.getMaxTurbineSpeed(arr))
    # print(parse_data.getMaxTurbineVoltage(arr))

    # print(parse_data.getMinPressure(arr))
    # print(parse_data.getMinPressure(arr))
    # print(parse_data.getMinPressure(arr))
    # print(parse_data.getMinPressure(arr))
    # print(parse_data.getMinPressure(arr))

    # print(parse_data.getAvgPressure(arr))

    x = []

    loadC = []
    tlak = []
    tlakPovprecje = []
    turbinaC = []
    turbinaS = []
    turbinaV = []

    for d in arr:
        x.append(src.utils.utils.convert_date_to_seconds(d.dateTime))
        loadC.append(d.loadCurrent)
        p = d.pressure
        tlak.append(p)
        turbinaC.append(d.turbineCurrent)
        turbinaS.append(d.turbineSpeed)
        turbinaV.append(d.turbineVoltage)

        # vals = []
        # for i in range(max(0, len(tlak) - 100), len(tlak)):
        #     if i == max(0, len(tlak) - 100):
        #         vals.append(tlak[i])
        #     else:
        #         spMeja = max(0, i-100)
        #         t = sum(tlak[:i-1]) / (len)
        #         #print(t)
        #         vals.append(t)

        # tlakPovprecje.append(sum(vals) / len(vals))

    anomalijeX = []
    anomalijeY = []

    sredinskaVrednost = (parse_data.getMaxPressure(arr).pressure + parse_data.getMinPressure(arr).pressure) / 2

    sredinaCrtaX = [0, (len(arr) - 1) * 10]
    sredinaCrtaY = [sredinskaVrednost] * 2  # sredinska vrednost

    n = 3500
    # razdelimo na odseke po n meritev
    for i in range(0, len(arr) - n, n):
        # maxTlak je povprecje prvih 5
        maxTlak = arr[i].pressure
        #minTlak nastavimo na povprecje oz maxTlak
        minTlak = maxTlak
        maxTlakX = src.utils.utils.convert_date_to_seconds(arr[i].dateTime)
        minTlakX = maxTlakX
        maxAbsDev = 0  # maksimalna absolutna vrednost odstopanja trenutne maksimalne vrednosti od prejšnje zabeležene
        maxAbsDevX = 0  # čas maksimalne absolutne vrednosti deviacije

        for d in range(i, i+n):
            odstopanje = 0
            if (arr[d].pressure < minTlak) or (arr[d].pressure > maxTlak):
                t = src.utils.utils.convert_date_to_seconds(arr[d].dateTime)
                if arr[d].pressure > maxTlak: 
                    odstopanje = arr[d].pressure - maxTlak
                    maxTlak = arr[d].pressure
                    maxTlakX = t
                elif arr[d].pressure < minTlak:
                    odstopanje = minTlak - arr[d].pressure
                    minTlak = arr[d].pressure
                    minTlakX = t
                
                #print("odstopanje: {}".format(odstopanje))
                if odstopanje > maxAbsDev:
                    maxAbsDev = odstopanje
                    maxAbsDevX = t

                #print("{} ({}) - razlika {}".format(arr[d].dateTime, t, odstopanje))
        
        # print("maxDev: {}, maxDevX: {}".format(maxAbsDev, maxAbsDevX))
        anomalijeX.append(maxAbsDevX)
        anomalijeY.append(arr[maxAbsDevX // 10].pressure)

    # dodamo še zadnjo meritev kot "anomalijo" oz. mejo intervala
    # EDIT: ni res, ker bi bilo povprečje meritev od zadnje meritve (nevlkjučno) naprej nedefinirano

    # anomalijeX.append(utils.utils.convert_date_to_seconds(arr[len(arr) - 1].dateTime))
    # anomalijeY.append(arr[len(arr) - 1].pressure)

    # povprecna vrednost vseh meritev do i-tega intervala od prejšnjega
    povprecja = []
    povprecjaX = []

    spMeja = 0
    for anomalijaX in anomalijeX:
        zgMeja = anomalijaX // 10
        vsota = 0
        for j in range(spMeja, zgMeja):  # trenutni indeks
            vsota += arr[j].pressure
        povprecje = vsota / ((zgMeja  - spMeja))
        povprecja.append(povprecje)
        # print("povprecje {} <--> {}: {}".format(spMeja, zgMeja, povprecje))
        # print("spodnja meja: {} --> {}".format(spMeja, zgMeja))
        spMeja = zgMeja

    # print(povprecja)
    prejsnji = 0
    for anomalijaX in anomalijeX:
        povprecjaX.append((anomalijaX + prejsnji) / 2)
        prejsnji = anomalijaX

    # Dodamo še povprečje vrednosti med zadnjo "anomalijo" in koncem meritev
    povprecjaX.append((anomalijeX[-1] + (len(arr) - 1) * 10) / 2)

    # ...in izračunamo povprečje na tem intervalu
    spMeja = anomalijeX[len(anomalijeX) - 1] // 10
    zgMeja = (len(arr) -1)
    # print(len(arr))
    # print(spMeja, zgMeja)
    vsota = 0
    for j in range(spMeja, zgMeja):  # trenutni indeks
        vsota += arr[j].pressure
    povprecje = vsota / ((zgMeja  - spMeja))
    # print(povprecje)
    povprecja.append(povprecje)

    # print(anomalijeX)
    # print(povprecja)

    # 
    # fig, axes = plt.subplots(1, 2)

    # axes[0].plot(x, tlak, color="blue")
    # axes[0].plot(anomalijeX, anomalijeY, color="orange", marker="o")
    # axes[0].plot(sredinaCrtaX, sredinaCrtaY, color="red")
    # axes[0].plot(povprecjaX, povprecja, color="lime", marker="o")

    # gremo čez vse intervale okrog točk, kjer smo našli anomalije
    # če so pod sredino, jih nastavimo na 0
    # če so nad sredino, jih nastavimo na 1
    intervali = anomalijeX + [(len(arr)) * 10]
    # print(intervali)
    spMeja = 0
    for interval in range(0, len(intervali)):
        zgMeja = intervali[interval] // 10
        for j in range(spMeja, zgMeja):
            if povprecja[interval] >= sredinskaVrednost:
                tlak[j] = 0
            else:
                tlak[j] = 1
        spMeja = zgMeja

    # zdaj imamo popravljne vrednosti [0, 1] na grafu
    # preverimo, kje se nahajajo "fronte"
    end_periods = []
    leakages = []

    trenutnaVrednost = tlak[0]
    leakages.append(trenutnaVrednost)
    for i in range(1, len(tlak)):
        if tlak[i] != trenutnaVrednost:
            end_periods.append(i * 10)
            trenutnaVrednost = tlak[i]
            leakages.append(trenutnaVrednost)
    end_periods.append((len(tlak) - 1) * 10)

    # epic hack
    if len(leakages) > 4:
        leakages = [0]
        end_periods = [len(arr)]

    slovarchek = {}  # karbonchek tribute
    slovarchek["file_name"] = file_name
    slovarchek["end_periods"] = end_periods
    slovarchek["leakages"] = leakages

    prediction_results.append(slovarchek)
    # print(fileno)
     
    # print(end_periods)
    # print(leakages)

    # axes[1].plot(x, tlak, color="blue")
    # axes[1].plot(anomalijeX, anomalijeY, color="orange", marker="o")
    # axes[1].plot(sredinaCrtaX, sredinaCrtaY, color="red")
    # axes[1].plot(povprecjaX, povprecja, color="lime", marker="o")

    # plt.show()
    #print(len(parse_data.getAnomalies(arr, 3)))

    rez = json.dumps({"prediction_results": prediction_results})
    print(rez)
f = open("results.json", "w")
f.write(rez)
f.close()
### PRI ODDAJI PODATKOV ENA VREDNOST NE SME BITI VEČJA OD PREJŠNJE