import time
import ctypes
import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class C10082MD:
    INVALID_HANDLE_VALUE = -1
    USBDEV_SUCCESS = 0
    USBDEV_INVALID_HANDLE = 1
    USBDEV_UNSUCCESS = 2
    USBDEV_INVALID_VALUE = 3
    USBDEV_CHECK_NORMAL = 11
    USBDEV_CHECK_INVALID = 12
    USBDEV_CHECK_REMOVE = 13
    USBDEV_BULK_SIZE_ERROR = 20
    USBDEV_BULK_READ_ERROR = 21
    USBDEV_BULK_NOT_UPDATED = 22
    USBDEV_ADC_OUTPUT_ERROR = 30
    USBDEV_TIME_OVER_ERROR = 101
    USBDEV_TIME_UNDER_ERROR = 102
    USBDEV_TIME_SET_ERROR = 103
    USBDEV_SET_GAIN_ERROR = 106
    USBDEV_SET_TRIGGER_ERROR = 108
    USBDEV_RW_EEP_ADDR_ERROR = 201
    USBDEV_RW_EEP_SIZE_ERROR = 202
    USBDEV_RW_EEP_OVER_ERROR = 203
    USBDEV_RW_EEP_ERROR = 204

    def __init__(self, nProductId = 0x2908, usPixelSize = 1024):

        dllName = "specu1a.dll"
        spec1adllpath = os.path.join(os.path.dirname(__file__), os.path.join('..', 'Dependencies', dllName)) 
        print(spec1adllpath)
        self.specdll = ctypes.WinDLL(spec1adllpath)
        self.calibCoefficients = None
        self.sensorData = None
        self.usPixelSize = usPixelSize
        self.unitID = ctypes.c_int(nProductId)
        self.deviceHandle = self.specdll.USB_OpenDevice(self.unitID)
        if self.deviceHandle == self.INVALID_HANDLE_VALUE:
            print("The target miniSpectrometer does not exist.")
        self.deviceStatus = self.specdll.USB_CheckDevice(self.deviceHandle)
        if self.deviceStatus == self.USBDEV_CHECK_INVALID:
            self.specdll.USB_CloseDevice(self.deviceHandle)
            print("Specified USB device handle is invalid.")
        elif  self.deviceStatus == self.USBDEV_CHECK_REMOVE:
            print("USB device was removed.")

        self.pipeHandle = self.specdll.USB_OpenPipe(self.deviceHandle)
################################################
        self.fig, self.ax = plt.subplots()
        xLambda = self._GetLambdaValues()
        signal = self._GetSensorData(1)
        self.yPlt, = self.ax.plot(xLambda, signal,'-')
        self.animation = animation.FuncAnimation(self.fig, self.animate, interval=25, blit=True)
        self.ax.set_ylim(0,65000)
        signalList = []
        signalList.append(xLambda.T.tolist())
        signalList.append(signal.T.tolist())
        df = pd.DataFrame(np.transpose(signalList),columns=['Lambda','Intensity'])
        self.ax.grid()
        plt.show()
        csvPath =  os.path.join(os.path.dirname(__file__), os.path.join('..', 'Data', 'SignalData.csv')) 
        df.to_csv(csvPath)

    def animate(self, i):
        signal = self._GetSensorData(1)
        self.yPlt.set_ydata(signal)  # update the data
        return self.yPlt,

#################################################
        
    def _ReadCalibrationCoefficients(self):
        clibdata = (ctypes.c_double*6)()
        calibdata = ctypes.cast(clibdata, ctypes.POINTER(ctypes.c_double))
        self.specdll.USB_ReadCalibrationValue(self.deviceHandle, calibdata)
        self.calibCoefficients = [calibdata[i] for i in range(6)]
        return self.calibCoefficients


    def _GetSensorData(self, numOfAverage = 10):
        self.sensorData = []
        aryBuffer =  (ctypes.c_ushort * self.usPixelSize)()
        aryusBuffer = ctypes.cast(aryBuffer, ctypes.POINTER(ctypes.c_ushort))
        for ind in range(numOfAverage):
            time.sleep(0.1)
            self.specdll.USB_GetSensorData(self.deviceHandle, self.pipeHandle, self.usPixelSize, aryusBuffer)
            self.sensorData.append([aryusBuffer[i] for i in range(self.usPixelSize)])
        return np.mean(self.sensorData, axis=0)
    def _GetLambdaValues(self):
        x = np.array(range(self.usPixelSize))
        coeffs = self._ReadCalibrationCoefficients()
        return coeffs[0] + (coeffs[1]*x) + coeffs[2]*(x^2) + coeffs[3]*(x^3) - coeffs[4]*(x^4) + coeffs[5]*(x^5)

    def __del__(self):
        self.specdll.USB_ClosePipe(self.pipeHandle)
        self.specdll.USB_CloseDevice(self.deviceHandle)