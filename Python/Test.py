import C10082MD_v1 as sp
import matplotlib.pyplot as plt
def main():
    miniSpect = sp.C10082MD() 
    miniSpect._PlotSensorDataLive()

    xLambda = miniSpect._GetLambdaValues()
    signal = miniSpect._GetSensorData(numOfAverage = 10)
    miniSpect._PlotSensorData()


    del miniSpect

if __name__ == '__main__':
    main()
