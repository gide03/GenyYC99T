import ctypes
from typing import Union
from .Util import Register, Form
from .Util import Util, CommmandDataFrame, VoltageRange, CurrentRange, PowerSelector, ElementSelector
from .Util import VoltageRangeError, CurrentRangeError

class ReadbackSamplingDataRegister(Form):
    def __init__(self):
        self.Voltage_A = Register('Voltage_A', ctypes.c_float)
        self.VoltagePhase_A = Register('VoltagePhase_A', ctypes.c_float)
        self.Current_A = Register('Current_A', ctypes.c_float)
        self.CurrentPhase_A = Register('CurrentPhase_A', ctypes.c_float)
        self.PowerActive_A = Register('PowerActive_A', ctypes.c_float)
        self.PowerReactive_A = Register('PowerReactive_A', ctypes.c_float)
        self.Voltage_B = Register('Voltage_B', ctypes.c_float)
        self.VoltagePhase_B = Register('VoltagePhase_B', ctypes.c_float)
        self.Current_B = Register('Current_B', ctypes.c_float)
        self.CurrentPhase_B = Register('CurrentPhase_B', ctypes.c_float)
        self.PowerActive_B = Register('PowerActive_B', ctypes.c_float)
        self.PowerReactive_B = Register('PowerReactive_B', ctypes.c_float)
        self.Voltage_C = Register('Voltage_C', ctypes.c_float)
        self.VoltagePhase_C = Register('VoltagePhase_C', ctypes.c_float)
        self.Current_C = Register('Current_C', ctypes.c_float)
        self.CurrentPhase_C = Register('CurrentPhase_C', ctypes.c_float)
        self.PowerActive_C = Register('PowerActive_C', ctypes.c_float)
        self.PowerReactive_C = Register('PowerReactive_C', ctypes.c_float)
        self.TotalPowerActive = Register('TotalPowerActive', ctypes.c_float)
        self.TotalPowerReactive = Register('TotalPowerReactive', ctypes.c_float)
    
class ReadBackErrorSamplingDataRegister(Form):
    def __init__(self):
        self.ValidFlagBit = Register('Valid Flag Bit', ctypes.c_bool)
        self.MeterError1 = Register('Meter 1 Error', ctypes.c_float)
        self.MeterError2 = Register('Meter 2 Error', ctypes.c_float)
        self.MeterError3 = Register('Meter 3 Error', ctypes.c_float)

class TestCommand(Form):
    def __init__(self):
        self.powerSelector = Register('Power Selector', )
        self.elementSelector = Register('Element Selector', )
        self.voltageRange = Register('Voltage Range', )
        self.currentRange = Register('Current Range', )
        self.voltage = Register('Voltage', )
        self.current = Register('Current', )
        self.powerFactor = Register('Power Factor', )
        self.powerFactorUnit = Register('Power Factor Unit', )
        self.frequency = Register('Frequency', )
        self.meterConstant = Register('MeterConstant', )
        self.calibMeasurementCycle = Register('Calib Measurement Cycle', )

class EnergyErrorCalibration:            
    class Buffer:
        def __init__(self):
            self.POWER_SELECTION = 0
            self.ELEMENT_SELECTION = 0
            self.VOLTAGE_RANGE = VoltageRange.YC99T_5C._220V
            self.VOLTAGE_AMPLITUDE = 0
            self.CURRENT_AMPLITUDE = 0
            self.POWER_FACTOR = 0
            self.POWER_FACTOR_UNIT = EnergyErrorCalibration.PFUnit._L
            self.FREQUENCY = 50
            self.METER_CONSTANT = 0
            self.CALIBRATION_CYCLE = 0
    
    class Command:
        TEST_COMMAND = 0xd0
        ONLINE_ADJUST_COMMAND = 0xd1
        STOP_TEST_COMMAND = 0xd3
        READBACK_SAMPLING_DATA = 0xd2
        READBACK_ERROR_SAMPLING = 0xd5
            
    class PFUnit:
        _NO_UNIT    = 0x00
        _L          = 0x01
        _C          = 0x02
    
    def __init__(self):        
        self.powerSelector = PowerSelector._3P4W_ACTIVE
        self.elementSelector = ElementSelector.EnergyErrorCalibration._COMBINE_ALL
        self.voltageRange = VoltageRange.YC99T_5C._220V
        self.currentRange = CurrentRange.YC99T_5C._20A
        self.voltage = 0.0
        self.current = 0.0
        self.powerFactor = 1
        self.powerFactorUnit = EnergyErrorCalibration.PFUnit._L
        self.frequency = 50
        self.meterConstant = 0
        self.calibMeasurementCycle = 0
        
        self.commandDataFrame = CommmandDataFrame()
        self.readbackSamplingRegister = ReadbackSamplingDataRegister()
        self.errorSamplingRegister = ReadBackErrorSamplingDataRegister()
    
    #
    # Internal Util
    #
    def resetDefault(self):
        self.powerSelector = PowerSelector._3P4W_ACTIVE
        self.elementSelection = ElementSelector.EnergyErrorCalibration._COMBINE_ALL
        self.voltageRange = VoltageRange.YC99T_5C._220V
        self.currentRange = CurrentRange.YC99T_5C._20A
        self.voltage = 0.0
        self.current = 0.0
        self.powerFactor = 1
        self.powerFactorUnit = EnergyErrorCalibration.PFUnit._L
        self.meterConstant = 0
        self.calibMeasurementCycle = 0
    #
    
    #
    # PARAMETER SETTER
    #
    
    # ELEMENT_SELECTION SET
    def setElementSelector(self, elementSelector:[ElementSelector.EnergyErrorCalibration, ElementSelector.ThreePhaseAcStandard]):
        '''
            combine or separate element selction
        '''
        self.elementSelector = elementSelector
    
    # POWER_SELECTION SET
    def setPowerSelector(self, powerSelector:PowerSelector):
        '''
            power selection setting
        '''
        self.powerSelector = powerSelector
    
    # VOLTAGE RANGE SET
    def setVoltageRange(self, range:Union[VoltageRange.YC99T_3C, VoltageRange.YC99T_5C]):
        '''
            set voltage range
            
            parameter:
                range (int|VoltageRange) mode selection for voltage range
        '''
        self.voltageRange = range
    
    # VOLTAGE SET
    def setVoltage(self, voltage:float):
        '''
            parameters:
                voltage (float) amplitude of voltage. raise exception if voltage bigger than voltage range nominal
                elementSelector (int|ElementSelector) voltage transmission selector for A or B or C
        '''
        if self.voltage > self.voltageRange.nominal:
            raise VoltageRangeError(f'Voltage set should not exceed {self.voltageRange.nominal}, or you could set the voltage range bigger')
        
        self.voltage = voltage
    
    # CURRENT RANGE SET
    def setCurrentRange(self, currentRange:Union[CurrentRange.YC99T_5C, CurrentRange.YC99T_3C]):
        '''
            set current range
            
            parameter:
        '''
        self.currentRange = currentRange
    
    # CURRENT SET
    def setCurrent(self, current:float):
        '''
            parameters:
                current (float) amplitude of currenet. raise exception if current bigger than current range nominal
        '''
        if self.current > self.currentRange.nominal:
            raise CurrentRangeError(f'Current set should not exceed {self.currentRange.nominal}, or you could set the current range bigger')
        self.current = current        
     
    # FREQUENCY SET
    def setFrequency(self, frequency:float):
        '''
            parameters:
                frequency (float) the signal frequency
        '''
        self.frequency = frequency
        
    # SET POWER FACTOR
    def setPowerFactor(self, powerFactor:float):
        '''
            parameters:
                powerFactor (float) the value of power factor
        '''
        self.powerFactor = powerFactor
    
    # SET POWER FACTOR UNIT
    def setPowerFactorUnit(self, powerFactorUnit:PFUnit):
        '''
            paramters:
                powerFactorUnit (PFUnit) power factor characteristic
        '''
        self.powerFactorUnit = powerFactorUnit        
        
    # SET CALIBRATION CYCLE
    def setCalibrationConstants(self, meterConstant:int, cycle:int):
        '''
            parameters:
                meterConstant (int) meter LED blink constant per energy unit
                value (int) number of measurement cycles
        '''
        self.meterConstant = meterConstant
        self.calibMeasurementCycle = cycle
    #
    
    # SEND DATA
    def apply(self, verbose:bool=False):
        '''
            apply register configuration to test bench
            
            parameters:
                verbose (bool) If true will show configuration summary
        '''
        if verbose:
            self.info()
        
        print('[EnergyCalibration] Applying configuration')
        return self.setTestCommandForm()
    
    def info(self):
        print('========================================')
        print('Summary Of Energy Error Calibration:')
        print('========================================')
        print(f"Power Selection             : {self.powerSelector.enum}")
        print(f"Element Selection           : {self.elementSelector.enum}")
        print(f"Voltage Range               : {self.voltageRange.enum}")
        print(f"Voltage Amplitude           : {self.voltage}")
        print(f"Current Amplitude           : {self.current}")
        print(f"Power Factor                : {self.powerFactor}")
        print(f"Power Factor Unit           : {self.powerFactorUnit}")
        print(f"Frequency                   : {self.frequency}")
        print(f"Meter Constant              : {self.meterConstant}")
        print(f"Calibratino Measure Cycle   : {self.calibMeasurementCycle}")
    
    def setTestCommandForm(self, verbose= False):
        '''
            Set test command form
            # return data frame in list for test command GENY mode Energy Error Calibration. Refer to Energy Error Calibration test command in Geny documentation.
        '''
        if verbose:
            self.info()
            
        register = ( # NOTE: Please don't change the arrangemet
            self.powerSelector.enum,
            self.elementSelector.enum,
            self.voltageRange.enum,
            self.voltage,
            self.current,
            self.powerFactor,
            self.powerFactorUnit,
            self.frequency,
            self.meterConstant,
            self.calibMeasurementCycle,
        )
        registerSize = (1,1,1,4,4,4,1,4,4,2)
        apdu = []
        for reg, regSize in zip(register, registerSize):
            if regSize == 1:
                apdu.append(reg)
            elif regSize == 2:
                apdu.extend(Util.uint2byteList(reg, regSize))
            else:
                apdu.extend(Util.float2byte(reg, regSize))
        
        dataFrame = self.commandDataFrame.genDataFrame(EnergyErrorCalibration.Command.TEST_COMMAND, apdu)
        return dataFrame
    
    def stopCommand(self) -> list:
        '''
            return data frame to stop Energy Error Calibration source in list structure
        '''
        self.bufferRegister = self.defaultBufferRegister.copy() # Set back buffer to default value
        df = Util.genDataFrame(EnergyErrorCalibration.Command.STOP_TEST_COMMAND, [])      # Generate data frame
        return df.copy()
    
    def readbackSampling(self,count:int=1) -> list:
        '''
            return data frame in list to request test bench feedback
        '''
        df = [] # for storing dataframe that will be send
        control_flag_bit = 0

        if count == 1:
            control_flag_bit = 1
        elif count == '*':
            control_flag_bit = 2

        df.append(control_flag_bit)
        df = self.commandDataFrame.genDataFrame(EnergyErrorCalibration.Command.READBACK_SAMPLING_DATA, df)
        return df
    
    def readbackErrorSampling(self, count:int=1) -> list:
        '''
            NOTE: I still not understand, is there a miss understanding. In the documentation error sampling readback is 0xd4 not 0xd5
            
            return data frame in list to request test bench feedback
        '''
        data = []
        control_flag_bit = 0

        if count == 1:
            control_flag_bit = 1
        elif count == '*':
            control_flag_bit = 2

        data.append(control_flag_bit)
        df = self.commandDataFrame.genDataFrame(EnergyErrorCalibration.Command.READBACK_ERROR_SAMPLING, data)
        return df