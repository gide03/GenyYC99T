from typing import Union
from Util import Util, VoltageRange, VoltageRangeError, ElementSelector, PowerSelector
from Util import CommmandDataFrame, ResponseDataFrame
from SerialMonitor import SerialMonitor
from ErrorCalibration import EnergyErrorCalibration
from GenySystemCommand import GenySys

class GenyTestBench(GenySys):
    class Mode:
        ENERGY_ERROR_CALIBRATION = 1
            
    def __init__(self, usbport, baudrate:int=115200):
        super().__init__()
        
        self.response = ResponseDataFrame()
        
        self.usbport = usbport
        self.baudrate = baudrate
        
        self.mode = GenyTestBench.Mode.ENERGY_ERROR_CALIBRATION
        self.serialMonitor = SerialMonitor(self.usbport, self.baudrate, self.onSerialReceived)
        self.energyErrorCalibration = EnergyErrorCalibration()
        
        self.documentation = {}
        
        # Set mode
        self.setMode(self.mode)
        
        self.serialMonitor.startMonitor()
        
    
    def setMode(self, mode:Mode):
        self.mode = mode
        if self.mode == GenyTestBench.Mode.ENERGY_ERROR_CALIBRATION:
            pass
    
    # Callback function
    def onSerialReceived(self, dataframe:bytearray):
        # print('[onSerialReceived] received incoming data')
        # print(dataframe)
        pass


    # API
    def open(self):
        buffer = self.connect()
        result = self.serialMonitor.transaction(buffer)
        self.response.extractDataFrame(result)
        if self.response.getErrorCode() == 0:
            return True
        return False
    
    def close(self):
        buffer = self.disconnect()
        result = self.serialMonitor.transaction(buffer)
        self.response.extractDataFrame(result)
        if self.response.getErrorCode() == 0:
            return True
        return False
    
    def setElementSelector(self, elementSelector:[ElementSelector.EnergyErrorCalibration, ElementSelector.ThreePhaseAcStandard]):
        '''
            combine or separate element selction
        '''
        if self.mode == GenyTestBench.Mode.ENERGY_ERROR_CALIBRATION:
            self.energyErrorCalibration.setElementSelector(elementSelector)

    def setPowerSelector(self, powerSelector:PowerSelector):
        '''
            power selection setting
        '''
        if self.mode == GenyTestBench.Mode.ENERGY_ERROR_CALIBRATION:
            self.energyErrorCalibration.setPowerSelector(powerSelector)
    
    def setVoltageRange(self, voltageRange:Union[VoltageRange.YC99T_5C, VoltageRange.YC99T_3C]):
        '''
            Set voltage range
            
            parameters:
                voltagerRange (int|Util.VoltageRange) voltage range. if voltage register is exceed voltage range, it will raise exception
        '''
        if self.mode == GenyTestBench.Mode.ENERGY_ERROR_CALIBRATION:
            if self.energyErrorCalibration.voltage > voltageRange.nominal:
                raise VoltageRangeError(f'Voltage range is exceed from voltage range you had set. Consider to set voltage first before set the voltage range')
            self.energyErrorCalibration.setVoltageRange(voltageRange)
    
    def setVoltage(self, voltage:float):
        '''
            Set voltage amplitude to corresponding mode
            
            parameters:
                voltage (float) aplitude of voltage. Raise exception if voltage range is exceed voltageRange
        '''
        if self.mode == GenyTestBench.Mode.ENERGY_ERROR_CALIBRATION:
            voltageRangeNominal = self.energyErrorCalibration.voltageRange.nominal
            if voltage > voltageRangeNominal:
                raise VoltageRangeError(f'Voltage set should not exceed {voltageRangeNominal}, or you could set the voltage range larger')            
            self.energyErrorCalibration.setVoltage(voltage)

    def setCurrent(self, current:float):
        '''
            Set current amplitude to corresponding mode
            
            parameters:
                current (float) aplitude of current. Raise exception if current range is exceed currentRange
                elementSelector (Util.ElementSelector) channel selection for Geny to transmit current. `Please consider match the selection and Geny's mode you've been set`
        '''
        if self.mode == GenyTestBench.Mode.ENERGY_ERROR_CALIBRATION:
            currentRangeNominal = self.energyErrorCalibration.currentRange.nominal
            if current > currentRangeNominal:
                raise VoltageRangeError(f'Current set should not exceed {currentRangeNominal}, or you could set the current range larger')
            self.energyErrorCalibration.setVoltage(current)
    
    def setFrequency(self, frequency:float):
        '''
            parameters:
                frequency (float) the signal frequency
        '''
        self.frequency = frequency
            
    def apply(self):
        if self.mode == GenyTestBench.Mode.ENERGY_ERROR_CALIBRATION:
            self.energyErrorCalibration.apply(verbose=True)

geny = GenyTestBench('COM1', 9600)
print('Connecting to Geny')
print(geny.open())
print('Closing port')
print(geny.close())

# geny.setMode(GenyTestBench.Mode.ENERGY_ERROR_CALIBRATION)
# geny.setPowerSelector(PowerSelector._3P4W_ACTIVE)
# geny.setVoltageRange(VoltageRange.YC99T_5C._220V)
# geny.setVoltage(220.0)
# geny.setCurrent(5.0)
# geny.setFrequency(50.0)
# geny.apply()

import time
while True:
    time.sleep(1)