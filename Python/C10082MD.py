import ctypes
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

specdll = ctypes.WinDLL ("C:\\Users\\Omid\\Desktop\\SIO 179\\Nitrate\\Hamamatsu Evaluation Software\\32\\EvaluationSoftware\\specu1a.dll")
    
nProductId = ctypes.c_int(0x2908)   #TM Series(CMOS)  :0x2908(C10082MD, C10083MD)
deviceHandle = specdll.USB_OpenDevice(nProductId)
deviceStatus = specdll.USB_CheckDevice(deviceHandle)
if deviceStatus == USBDEV_CHECK_INVALID:
    specdll.USB_CloseDevice(deviceHandle)
    print("Specified USB device handle is invalid.")
elif  deviceStatus == USBDEV_CHECK_REMOVE:
    print("USB device was removed.")
else:
    pipeHandle = specdll.USB_OpenPipe(deviceHandle)
    clibdata = (ctypes.c_double*6)()
    calibdata = ctypes.cast(clibdata, ctypes.POINTER(ctypes.c_double))

    specdll.USB_ReadCalibrationValue(deviceHandle, calibdata)
    usPixelSize = ctypes.c_ushort(1024) #Number of Pixels
    aryBuffer =  (ctypes.c_ushort * 1024)()
    aryusBuffer = ctypes.cast(aryBuffer, ctypes.POINTER(ctypes.c_ushort))
    specdll.USB_GetSensorData(deviceHandle, pipeHandle, usPixelSize, aryusBuffer)
    calib_result = [calibdata[i] for i in range(6)]
    list_of_results = [aryusBuffer[i] for i in range(1024)]
    print(calib_result)
    print(list_of_results)
    print(deviceHandle)
    specdll.USB_ClosePipe(pipeHandle)
    specdll.USB_CloseDevice(deviceHandle)

    