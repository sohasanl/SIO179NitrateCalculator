import C10082MD_v1 as sp
import matplotlib.pyplot as plt
def main():
    miniSpect = sp.C10082MD()   
    signal = miniSpect._GetSensorData()
    xLambda = miniSpect._GetLambdaValues()
    fig, a = plt.subplots()
    a.plot(xLambda, signal,'-', label='Intensity signal')
    a.legend(loc='upper left', shadow=True, fontsize='large')
    plt.title('Intensity Graph')
    plt.xlabel('Lambda')
    plt.ylabel('Intensity')
    plt.show() 
    del miniSpect

if __name__ == '__main__':
    main()
