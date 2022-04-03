from src.leak_detection import LeakDetection
import parse_data
import os
import src.utils.utils
import json
import parse_data
import matplotlib.pyplot as plt

# def fromFile(path):
#     f = open(path, "r")
#     vrstice = [line[:len(line)-1] for line in f.readlines()][1:]
#     f.close()

#     data = []
#     for l in [line.split(",") for line in vrstice]:
#         data.append(parse_data.Data(l[0], l[1], l[2], l[3], l[4], l[5]))
#         # print(l[0])

#     return data

prediction_results = []

for i in [58, 59, 61, 62, 66, 67, 71, 72, 73, 74, 83, 84, 85]:
    file_name = "scenario_week_example_{}.csv".format(i)
    end_periods = []
    leakages = []

    fname = os.path.join(os.path.dirname(__file__), "test_data/scenario_week_example_{}.csv".format(i))

    # odpremo fajl
    f = open(fname, "r")
    vrstice = [l[:-1] for l in f.readlines()[1:]]
    f.close()

    ld = LeakDetection()

    currentPrediction = ld.predict(vrstice[0].split(","))
    currentTime = 10

    x = []
    tlaki = []

    for vrstica in vrstice[1:]:
        t = src.utils.utils.convert_date_to_seconds(vrstica.split(",")[0])
        
        tlak = vrstica.split(",")[5]
        p = 0 if len(tlak) == 0 else float(tlak)
        tlaki.append(p)
        x.append(t)
        prediction = ld.predict(vrstica.split(","))

        leakAvg = 1.658914824064667
        noLeakAvg = 1.8174741437730197
        epsilon = (noLeakAvg - leakAvg) / 30

        spMeja = leakAvg - epsilon
        zgMeja = noLeakAvg + epsilon

        if prediction == currentPrediction or (p > spMeja and p < zgMeja):
            currentTime += 10
        else:
            end_periods.append(currentTime)
            leakages.append(1 if currentPrediction else 0)
            currentPrediction = prediction
    
    end_periods.append(currentTime)
    leakages.append(1 if currentPrediction else 0)

    # print(end_periods)
    # print(leakages)

    prediction_results.append({"file_name": file_name, "end_periods": end_periods, "leakages": leakages})

    fig, axes = plt.subplots(1, 2)
    axes[0].plot(x, tlaki, color="blue")
    axes[0].plot([0, len(tlaki) * 10], [zgMeja] * 2, color="red")
    axes[0].plot([0, len(tlaki) * 10], [spMeja] * 2, color="red")

    axes[1].plot(end_periods, leakages, color="blue")
    plt.show()

f = open("result.json", "w")
f.write(json.dumps({"prediction_results": prediction_results}))
f.close()
