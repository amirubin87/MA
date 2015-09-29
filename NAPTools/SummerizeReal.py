__author__ = 't-amirub'
import os


def GetMetricResultFromFile(path, isNMI):
    if not os.path.isfile(path):
        return 0.0
    if os.stat(path).st_size == 0:
        return 0.0
    file = open(path, 'r')
    lines = file.readlines()
    if isNMI:
        line = lines[2]
    else:
        line = lines[0]
    file.close()
    metricS = line.split('\t')[1].replace('OmegaIndex:', '\n').replace('\n', '')
    if 'e-' in metricS:
        return 0.0
    return float(metricS)


    def GenerateMetricSummary(metricName, outputPath):

    if metricName not in ["FScore", "NMI2", "OmegaIndex", "F1", "Qe"]:
        print  " metric name must be one of the supported"
        return
    isNMI = False
    if metricName == "NMI2":
        isNMI = True
    output = open(outputPath, 'a')
    output.write(metricName)

    SLPAMetricSum = 0
    OSLOMMetricSum = 0
    CFINDERMetricSum = 0
    COPRAMetricSum = 0
    GCEMetricSum = 0
    QeMetricSum = 0

    OLMetricSum = 0
    OL1MetricSum = 0
    OL8MetricSum = 0
    OL5MetricSum = 0

    OSCDMetricSum = 0
    OSCD1MetricSum = 0
    OSCD8MetricSum = 0
    OSCD5MetricSum = 0

    SLPAAmount = 0
    OSLOMAmount = 0
    CFINDERAmount = 0
    COPRAAmount = 0
    GCEAmount = 0
    QeAmount = 0

    OLAmount = 0
    OL1Amount = 0
    OL8Amount = 0
    OL5Amount = 0

    OSCDAmount = 0
    OSCD1Amount = 0
    OSCD8Amount = 0
    OSCD5Amount = 0

    merge = "/merge0.5"

    for input in ["enron", "grqc"  "hepph", "wiki", "youtube", "amazon", "dblp", ]:
        output.write('                  input ' + input + '\n')
        print "                   input {0}".format(input)
        # Qe
        bestMetric = 0.0

        for betta in ["1.02", "1.04", "1.06", "1.08", "1.1", "1.2", "1.3", "1.4"]:
            metric = GetMetricResultFromFile(
                '../../networks/' + input + '/metrics/' + metricName + '/Qe' + merge + '/betta' + betta + '.dat', isNMI)
            if metric > bestMetric:
                bestMetric = metric
        if bestMetric > 0:
            QeAmount += 1
        QeMetricSum += bestMetric

        #Ovelapping Louvain
        bestMetric = 0.0

        for betta in ["1.01", "1.02", "1.03", "1.04", "1.05", "1.06", "1.07", "1.08", "1.09", "1.1", "1.2", "1.3",
                      "1.4"]:
            metric = GetMetricResultFromFile(
                '../../networks/' + input + '/metrics/' + metricName + '/O-Louvain' + merge + '/betta' + betta + '.dat',
                isNMI)
            if metric > bestMetric:
                bestMetric = metric
        if merge == "/1":
            if bestMetric > 0:
                OLAmount += 1
            OLMetricSum += bestMetric
        elif merge == "/merge":
            if bestMetric > 0:
                OL1Amount += 1
            OL1MetricSum += bestMetric
        elif merge == "/merge0.8":
            if bestMetric > 0:
                OL8Amount += 1
            OL8MetricSum += bestMetric
        elif merge == "/merge0.5":
            if bestMetric > 0:
                OL5Amount += 1
            OL5MetricSum += bestMetric

        #SCD

        bestMetric = 0.0
        for betta in ["1.01", "1.02", "1.03", "1.04", "1.05", "1.06", "1.07", "1.08", "1.09", "1.1", "1.2", "1.3",
                      "1.4", "10.0", "20.0"]:
            metric = GetMetricResultFromFile(
                '../../networks/' + input + '/metrics/' + metricName + '/O-SCD' + merge + '/betta' + betta + '.dat',
                isNMI)
            if metric > bestMetric:
                bestMetric = metric

        if merge == "":
            if bestMetric > 0:
                OSCDAmount += 1
            OSCDMetricSum += bestMetric
        elif merge == "/merge":
            if bestMetric > 0:
                OSCD1Amount += 1
            OSCD1MetricSum += bestMetric
        elif merge == "/merge0.8":
            if bestMetric > 0:
                OSCD8Amount += 1
            OSCD8MetricSum += bestMetric
        elif merge == "/merge0.5":
            if bestMetric > 0:
                OSCD5Amount += 1
            OSCD5MetricSum += bestMetric


            #SLPA
        bestMetric = 0.0
        for k in range(1, 11):
            for r in ["0.01", "0.05", "0.1", "0.15", "0.2", "0.25", "0.3", "0.35", "0.4", "0.45", "0.5"]:
                metric = GetMetricResultFromFile(
                    '../../networks/' + input + '/metrics/' + metricName + '/SLPA/' + str(k) + '/r' + r + '.dat', isNMI)
                if metric > bestMetric:
                    bestMetric = metric
            if bestMetric > 0:
                SLPAAmount += 1

            SLPAMetricSum += bestMetric

            #OSLOM
        bestMetric = 0.0
        metric = GetMetricResultFromFile('../../networks/' + input + '/metrics/' + metricName + '/OSLOM/tp.dat', isNMI)

        if metric > bestMetric:
            bestMetric = metric
        tp = 1
        while os.path.isfile('../../networks/' + input + '/metrics/' + metricName + '/OSLOM/tp' + str(tp) + '.dat'):
            metric = GetMetricResultFromFile(
                '../../networks/' + input + '/metrics/' + metricName + '/OSLOM/tp' + str(tp) + '.dat', isNMI)
            if metric > bestMetric:
                bestMetric = metric
            tp += 1

        if bestMetric > 0:
            OSLOMAmount += 1

        OSLOMMetricSum += bestMetric

        #CFinder
        bestMetric = 0.0
        k = 3
        while os.path.isfile('../../networks/' + input + '/metrics/' + metricName + '/CFinder/CFinder' + str(
                k) + '.dat'):
            metric = GetMetricResultFromFile(
                '../../networks/' + input + '/metrics/' + metricName + '/CFinder/CFinder' + str(k) + '.dat', isNMI)

            if metric > bestMetric:
                bestMetric = metric
            k += 1
        if bestMetric > 0:
            CFINDERAmount += 1

        CFINDERMetricSum += bestMetric

        #COPRA
        bestMetric = 0.0
        for k in range(1, 11):
            metric = GetMetricResultFromFile(
                '../../networks/' + input + '/metrics/' + metricName + '/COPRA/COPRA-best-V-' + str(k) + '.dat', isNMI)
            if metric > bestMetric:
                bestMetric = metric
        if bestMetric > 0:
            COPRAAmount += 1

        COPRAMetricSum += bestMetric

        #GCE
        bestMetric = 0.0
        for k in range(3, 9):
            metric = GetMetricResultFromFile(
                '../../networks/' + input + '/metrics/' + metricName + '/GCE/minimumCliqueSize' + str(k) + '.dat',
                isNMI)
            if metric > bestMetric:
                bestMetric = metric
        if bestMetric > 0:
            GCEAmount += 1

        GCEMetricSum += bestMetric

    if QeAmount > 0 and QeMetricSum > 0:
        output.write('Qe Merge0.5 ' + str(QeMetricSum / float(QeAmount)) + '\n')

    if OL5Amount > 0 and OL5MetricSum > 0:
        output.write('O-Louvain5 ' + str(OL5MetricSum / float(OL5Amount)) + '\n')

    if OSCD5Amount > 0 and OSCD5MetricSum > 0:
        output.write('O-SCD5 ' + str(OSCD5MetricSum / float(OSCD5Amount)) + '\n')

    if GCEAmount > 0 and GCEMetricSum > 0:
        output.write('GCE ' + str(GCEMetricSum / float(GCEAmount)) + '\n')
    if COPRAAmount > 0 and COPRAMetricSum > 0:
        output.write('COPRA ' + str(COPRAMetricSum / float(COPRAAmount)) + '\n')
    if CFINDERAmount > 0 and CFINDERMetricSum > 0:
        output.write('CFinder ' + str(CFINDERMetricSum / float(CFINDERAmount)) + '\n')
    if OSLOMAmount > 0 and OSLOMMetricSum > 0:
        output.write('OSLOM ' + str(OSLOMMetricSum / float(OSLOMAmount)) + '\n')
    if SLPAAmount > 0 and SLPAMetricSum > 0:
        output.write('SLPA ' + str(SLPAMetricSum / float(SLPAAmount)) + '\n\n')
    output.close()

