# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision F, 08/29/2022

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

#########################################################
import os
import sys
import platform
import time
import datetime
import math
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
#########################################################

#########################################################
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
#########################################################

#########################################################
if sys.version_info[0] < 3:
    import Queue  # Python 2
else:
    import queue as Queue  # Python 3
#########################################################

#########################################################
if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input
######################################################### "sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

###########################################################
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.DigitalOutput import *
###########################################################

class PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    #######################################################################################################################
    #######################################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__ starting. ####################")

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        #########################################################
        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0
        #########################################################

        #########################################################
        self.DetectedDeviceName = "default"
        self.DetectedDeviceID = "default"
        self.DetectedDeviceVersion = "default"
        self.DetectedDeviceSerialNumber = "default"
        #########################################################

        self.DigitalOutputsList_PhidgetsDigitalOutputObjects = list()

        self.NumberOfDigitalOutputs = 4

        self.DigitalOutputsList_AttachedAndOpenFlag = [-1.0] * self.NumberOfDigitalOutputs
        self.DigitalOutputsList_ErrorCallbackFiredFlag = [-1.0] * self.NumberOfDigitalOutputs

        self.DigitalOutputsList_State = [-1] * self.NumberOfDigitalOutputs
        self.DigitalOutputsList_State_NeedsToBeChangedFlag = [1] * self.NumberOfDigitalOutputs
        self.DigitalOutputsList_State_ToBeSet = [0] * self.NumberOfDigitalOutputs

        self.MostRecentDataDict = dict()

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: ERROR, must pass in 'root'")
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 0.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))

        #print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredSerialNumber" in setup_dict:
            try:
                self.DesiredSerialNumber = int(setup_dict["DesiredSerialNumber"])
            except:
                print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: Error, DesiredSerialNumber invalid.")
                return
        else:
            self.DesiredSerialNumber = -1
        
        print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: DesiredSerialNumber: " + str(self.DesiredSerialNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "WaitForAttached_TimeoutDuration_Milliseconds" in setup_dict:
            self.WaitForAttached_TimeoutDuration_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WaitForAttached_TimeoutDuration_Milliseconds", setup_dict["WaitForAttached_TimeoutDuration_Milliseconds"], 0.0, 60000.0))

        else:
            self.WaitForAttached_TimeoutDuration_Milliseconds = 5000

        print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: WaitForAttached_TimeoutDuration_Milliseconds: " + str(self.WaitForAttached_TimeoutDuration_Milliseconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UsePhidgetsLoggingInternalToThisClassObjectFlag" in setup_dict:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UsePhidgetsLoggingInternalToThisClassObjectFlag", setup_dict["UsePhidgetsLoggingInternalToThisClassObjectFlag"])
        else:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = 1

        print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.DigitalOutputsList_ListOfOnAttachCallbackFunctionNames = [self.DigitalOutput0onAttachCallback, self.DigitalOutput1onAttachCallback, self.DigitalOutput2onAttachCallback, self.DigitalOutput3onAttachCallback]
        self.DigitalOutputsList_ListOfOnDetachCallbackFunctionNames = [self.DigitalOutput0onDetachCallback, self.DigitalOutput1onDetachCallback, self.DigitalOutput2onDetachCallback, self.DigitalOutput3onDetachCallback]
        self.DigitalOutputsList_ListOfOnErrorCallbackFunctionNames = [self.DigitalOutput0onErrorCallback, self.DigitalOutput1onErrorCallback, self.DigitalOutput2onErrorCallback, self.DigitalOutput3onErrorCallback]
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            #########################################################
            for DigitalOutputChannel in range(0, self.NumberOfDigitalOutputs):

                self.DigitalOutputsList_PhidgetsDigitalOutputObjects.append(DigitalOutput())

                if self.DesiredSerialNumber != -1:
                    self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].setDeviceSerialNumber(self.DesiredSerialNumber)

                self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].setChannel(DigitalOutputChannel)
                self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].setOnAttachHandler(self.DigitalOutputsList_ListOfOnAttachCallbackFunctionNames[DigitalOutputChannel])
                self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].setOnDetachHandler(self.DigitalOutputsList_ListOfOnDetachCallbackFunctionNames[DigitalOutputChannel])
                self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].setOnErrorHandler(self.DigitalOutputsList_ListOfOnErrorCallbackFunctionNames[DigitalOutputChannel])
                self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            #########################################################
            
            self.PhidgetsDeviceConnectedFlag = 1

        except PhidgetException as e:
            self.PhidgetsDeviceConnectedFlag = 0
            print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: Failed to attach, Phidget Exception %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.PhidgetsDeviceConnectedFlag == 1:

            #########################################################
            if self.UsePhidgetsLoggingInternalToThisClassObjectFlag == 1:
                try:
                    Log.enable(LogLevel.PHIDGET_LOG_INFO, os.getcwd() + "\PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class_PhidgetLog_INFO.txt")
                    print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: Enabled Phidget Logging.")

                except PhidgetException as e:
                    print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: Failed to enable Phidget Logging, Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceName = self.DigitalOutputsList_PhidgetsDigitalOutputObjects[0].getDeviceName()
                print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: DetectedDeviceName: " + self.DetectedDeviceName)

            except PhidgetException as e:
                print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: Failed to call 'getDeviceName', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceSerialNumber = self.DigitalOutputsList_PhidgetsDigitalOutputObjects[0].getDeviceSerialNumber()
                print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: DetectedDeviceSerialNumber: " + str(self.DetectedDeviceSerialNumber))

            except PhidgetException as e:
                print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: Failed to call 'getDeviceSerialNumber', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceID = self.DigitalOutputsList_PhidgetsDigitalOutputObjects[0].getDeviceID()
                print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: DetectedDeviceID: " + str(self.DetectedDeviceID))

            except PhidgetException as e:
                print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: Failed to call 'getDeviceID', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceVersion = self.DigitalOutputsList_PhidgetsDigitalOutputObjects[0].getDeviceVersion()
                print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: DetectedDeviceVersion: " + str(self.DetectedDeviceVersion))

            except PhidgetException as e:
                print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: Failed to call 'getDeviceVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceLibraryVersion = self.DigitalOutputsList_PhidgetsDigitalOutputObjects[0].getLibraryVersion()
                print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: DetectedDeviceLibraryVersion: " + str(self.DetectedDeviceLibraryVersion))

            except PhidgetException as e:
                print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: Failed to call 'getLibraryVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            if self.DesiredSerialNumber != -1:  # '-1' means we should open the device regardless os serial number.
                if self.DetectedDeviceSerialNumber != self.DesiredSerialNumber:
                    print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class __init__: The desired Serial Number (" + str(self.DesiredSerialNumber) + ") does not match the detected serial number (" + str(self.DetectedDeviceSerialNumber) + ").")
                    self.CloseAllDigitalOutputChannels()
                    time.sleep(0.25)
                    return
            #########################################################

            #########################################################
            self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
            self.MainThread_ThreadingObject.start()
            #########################################################

            #########################################################
            if self.USE_GUI_FLAG == 1:
                self.StartGUI(self.root)
            #########################################################

            #########################################################
            time.sleep(0.25)
            #########################################################

            #########################################################
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
            #########################################################

        #########################################################
        #########################################################

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def __del__(self):
        pass
    #######################################################################################################################
    #######################################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber):

        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be 0 or 1 (value was " +
                          str(InputNumber_ConvertedToFloat) +
                          "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat >= RangeMinValue and InputNumber_ConvertedToFloat <= RangeMaxValue:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be in the range [" +
                          str(RangeMinValue) +
                          ", " +
                          str(RangeMaxValue) +
                          "] (value was " +
                          str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CloseAllDigitalOutputChannels(self):

        try:
            for DigitalOutputChannel in range(0, self.NumberOfDigitalOutputs):
                self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].close()

        except PhidgetException as e:
            print("CloseAllDigitalOutputChannels, Phidget Exception %i: %s" % (e.code, e.details))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutputGENERALonAttachCallback(self, DigitalOutputChannel):

        try:
            self.DigitalOutputsList_AttachedAndOpenFlag[DigitalOutputChannel] = 1
            self.MyPrint_WithoutLogFile("$$$$$$$$$$ DigitalOutputGENERALonAttachCallback event for DigitalOutputChannel " + str(DigitalOutputChannel) + ", Attached! $$$$$$$$$$")

        except PhidgetException as e:
            self.DigitalOutputsList_AttachedAndOpenFlag[DigitalOutputChannel] = 0
            self.MyPrint_WithoutLogFile("DigitalOutputGENERALonAttachCallback event for DigitalOutputChannel " + str(DigitalOutputChannel) + ", ERROR: Failed to attach DigitalOutput0, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutputGENERALonDetachCallback(self, DigitalOutputChannel):

        self.DigitalOutputsList_AttachedAndOpenFlag[DigitalOutputChannel] = 0
        self.MyPrint_WithoutLogFile("$$$$$$$$$$ DigitalOutputGENERALonDetachCallback event for DigitalOutputChannel " + str(DigitalOutputChannel) + ", Detatched! $$$$$$$$$$")

        try:
            self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("DigitalOutputGENERALonDetachCallback event for DigitalOutput Channel " + str(DigitalOutputChannel) + ", failed to openWaitForAttachment, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutputGENERALonErrorCallback(self, DigitalOutputChannel, code, description):

        self.DigitalOutputsList_ErrorCallbackFiredFlag[DigitalOutputChannel] = 1

        self.MyPrint_WithoutLogFile("DigitalOutputGENERALonErrorCallback event for DigitalOutput Channel " + str(DigitalOutputChannel) + ", Error Code " + ErrorEventCode.getName(code) + ", description: " + str(description))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput0onAttachCallback(self, HandlerSelf):

        DigitalOutputChannel = 0
        self.DigitalOutputGENERALonAttachCallback(DigitalOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput0onDetachCallback(self, HandlerSelf):

        DigitalOutputChannel = 0
        self.DigitalOutputGENERALonDetachCallback(DigitalOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput0onErrorCallback(self, HandlerSelf, code, description):

        DigitalOutputChannel = 0
        self.DigitalOutputGENERALonErrorCallback(DigitalOutputChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput1onAttachCallback(self, HandlerSelf):

        DigitalOutputChannel = 1
        self.DigitalOutputGENERALonAttachCallback(DigitalOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput1onDetachCallback(self, HandlerSelf):

        DigitalOutputChannel = 1
        self.DigitalOutputGENERALonDetachCallback(DigitalOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput1onErrorCallback(self, HandlerSelf, code, description):

        DigitalOutputChannel = 1
        self.DigitalOutputGENERALonErrorCallback(DigitalOutputChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput2onAttachCallback(self, HandlerSelf):

        DigitalOutputChannel = 2
        self.DigitalOutputGENERALonAttachCallback(DigitalOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput2onDetachCallback(self, HandlerSelf):

        DigitalOutputChannel = 2
        self.DigitalOutputGENERALonDetachCallback(DigitalOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput2onErrorCallback(self, HandlerSelf, code, description):

        DigitalOutputChannel = 2
        self.DigitalOutputGENERALonErrorCallback(DigitalOutputChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput3onAttachCallback(self, HandlerSelf):

        DigitalOutputChannel = 3
        self.DigitalOutputGENERALonAttachCallback(DigitalOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput3onDetachCallback(self, HandlerSelf):

        DigitalOutputChannel = 3
        self.DigitalOutputGENERALonDetachCallback(DigitalOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput3onErrorCallback(self, HandlerSelf, code, description):

        DigitalOutputChannel = 3
        self.DigitalOutputGENERALonErrorCallback(DigitalOutputChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetRelayState(self, DigitalOutputChannel, State_ToBeSet):

        if DigitalOutputChannel in range(0, self.NumberOfDigitalOutputs):
            if State_ToBeSet in [0, 1]:
                self.DigitalOutputsList_State_ToBeSet[DigitalOutputChannel] = State_ToBeSet
                self.DigitalOutputsList_State_NeedsToBeChangedFlag[DigitalOutputChannel] = 1
            else:
                print("SetRelayState ERROR, State_ToBeSet must be 0 or 1.")
        else:
            print("SetRelayState ERROR, DigitalOutputChannel must be in " + str(list(range(0, self.NumberOfDigitalOutputs))) + ".")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:
            self.MostRecentDataDict = dict([("DigitalOutputsList_State", self.DigitalOutputsList_State),
                                             ("DigitalOutputsList_ErrorCallbackFiredFlag", self.DigitalOutputsList_ErrorCallbackFiredFlag),
                                             ("Time", self.CurrentTime_CalculatedFromMainThread)])

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict() #So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromMainThread = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ########################################################################################################## unicorn
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ##########################################################################################################

            ##########################################################################################################
            for DigitalOutputChannel in range(0, self.NumberOfDigitalOutputs):

                if self.DigitalOutputsList_State_NeedsToBeChangedFlag[DigitalOutputChannel] == 1:

                    self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].setState(self.DigitalOutputsList_State_ToBeSet[DigitalOutputChannel])
                    time.sleep(0.002)

                    self.DigitalOutputsList_State[DigitalOutputChannel] = self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].getState()
                    if self.DigitalOutputsList_State[DigitalOutputChannel] == self.DigitalOutputsList_State_ToBeSet[DigitalOutputChannel]:
                        self.DigitalOutputsList_State_NeedsToBeChangedFlag[DigitalOutputChannel] = 0

            ##########################################################################################################

            ########################################################################################################## USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            self.UpdateFrequencyCalculation_MainThread()

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                time.sleep(self.MainThread_TimeToSleepEachLoop)
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        self.CloseAllDigitalOutputChannels()

        self.MyPrint_WithoutLogFile("Finished MainThread for PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent):

        self.GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread, args=(GuiParent,))
        self.GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        self.GUI_Thread_ThreadingObject.start()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class object.")

        ###################################################
        self.root = parent
        self.parent = parent
        ###################################################

        ###################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        ###################################################

        ###################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        ###################################################

        #################################################
        self.DeviceInfo_label = Label(self.myFrame, text="Device Info", width=50)

        self.DeviceInfo_label["text"] = self.NameToDisplay_UserSet + \
                                         "\nDevice Name: " + self.DetectedDeviceName + \
                                         "\nDevice Serial Number: " + str(self.DetectedDeviceSerialNumber) + \
                                         "\nDevice Version: " + str(self.DetectedDeviceVersion)

        self.DeviceInfo_label.grid(row=0, column=0, padx=5, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.DigitalOutputs_Label = Label(self.myFrame, text="DigitalOutputs_Label", width=70)
        self.DigitalOutputs_Label.grid(row=0, column=1, padx=5, pady=1, columnspan=1, rowspan=1)
        #################################################
        
        #################################################
        self.DigitalOutputButtonsFrame = Frame(self.myFrame)
        self.DigitalOutputButtonsFrame.grid(row = 1, column = 0, padx = 1, pady = 1, rowspan = 1, columnspan = 1)

        self.DigitalOutputsList_ButtonObjects = []
        for DigitalOutputChannel in range(0, self.NumberOfDigitalOutputs):
            self.DigitalOutputsList_ButtonObjects.append(Button(self.DigitalOutputButtonsFrame, text="Relay " + str(DigitalOutputChannel), state="normal", width=8, command=lambda i=DigitalOutputChannel: self.DigitalOutputsList_ButtonObjectsResponse(i)))
            self.DigitalOutputsList_ButtonObjects[DigitalOutputChannel].grid(row=1, column=DigitalOutputChannel, padx=1, pady=1)
        #################################################

        ###################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=2, column=0, padx=1, pady=1, columnspan=1, rowspan=10)
        ###################################################

        ###################################################
        self.GUI_ready_to_be_updated_flag = 1
        ###################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:
                    #######################################################
                    for DigitalOutputChannel in range(0, self.NumberOfDigitalOutputs):
                        if self.DigitalOutputsList_State[DigitalOutputChannel] == 1:
                            self.DigitalOutputsList_ButtonObjects[DigitalOutputChannel]["bg"] = self.TKinter_LightGreenColor
                        elif self.DigitalOutputsList_State[DigitalOutputChannel] == 0:
                            self.DigitalOutputsList_ButtonObjects[DigitalOutputChannel]["bg"] = self.TKinter_LightRedColor
                        else:
                            self.DigitalOutputsList_ButtonObjects[DigitalOutputChannel]["bg"] = self.TKinter_DefaultGrayColor
                    #######################################################

                    #######################################################
                    self.DigitalOutputs_Label["text"] = "\nDigital States: " + str(self.DigitalOutputsList_State) + \
                                                "\nTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 0, 3) + \
                                                "\nData Frequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 0, 3)
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutputsList_ButtonObjectsResponse(self, DigitalOutputChannel):

        if self.DigitalOutputsList_State[DigitalOutputChannel] == 1:
            self.DigitalOutputsList_State_ToBeSet[DigitalOutputChannel] = 0
        else:
            self.DigitalOutputsList_State_ToBeSet[DigitalOutputChannel] = 1

        self.DigitalOutputsList_State_NeedsToBeChangedFlag[DigitalOutputChannel] = 1

        self.MyPrint_WithoutLogFile("DigitalOutputsList_ButtonObjectsResponse: Event fired for DigitalOutputChannel " + str(DigitalOutputChannel))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, InputToCheck):

        result = isinstance(InputToCheck, list)
        return result
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

        number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

        ListOfStringsToJoin = []

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if isinstance(input, str) == 1:
            ListOfStringsToJoin.append(input)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
            element = float(input)
            prefix_string = "{:." + str(number_of_decimal_places) + "f}"
            element_as_string = prefix_string.format(element)

            ##########################################################################################################
            ##########################################################################################################
            if element >= 0:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
                element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
            else:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
            ##########################################################################################################
            ##########################################################################################################

            ListOfStringsToJoin.append(element_as_string)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, list) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, tuple) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, dict) == 1:

            if len(input) > 0:
                for Key in input: #RECURSION
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a dict()
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        else:
            ListOfStringsToJoin.append(str(input))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if len(ListOfStringsToJoin) > 1:

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            StringToReturn = ""
            for Index, StringToProcess in enumerate(ListOfStringsToJoin):

                ################################################
                if Index == 0: #The first element
                    if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                        StringToReturn = "{"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                        StringToReturn = "("
                    else:
                        StringToReturn = "["

                    StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
                ################################################

                ################################################
                elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                    StringToReturn = StringToReturn + StringToProcess + ", "
                ################################################

                ################################################
                else: #The last element
                    StringToReturn = StringToReturn + StringToProcess

                    if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                        StringToReturn = StringToReturn + "}"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                        StringToReturn = StringToReturn + ")"
                    else:
                        StringToReturn = StringToReturn + "]"

                ################################################

            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        elif len(ListOfStringsToJoin) == 1:
            StringToReturn = ListOfStringsToJoin[0]

        else:
            StringToReturn = ListOfStringsToJoin

        return StringToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

