from typing import Union, Tuple
from Util import Util, ResponseDataFrame, CommmandDataFrame, VoltageRange, CurrentRange, PowerSelector, ElementSelector
from Util import VoltageRangeError, CurrentRangeError, DatFrameError

class Register:
    def __init__(self, name, dtype, size):
        self.name = name
        self.dtype = dtype
        self.size = size
        self.value = 0
        
class EnergyErrorCalibration:
    class ReadbackSamplingDataRegister(Register):
        def __init__(self):
            self.Voltage_A = Register('Voltage_A', float, 4)
            self.VoltagePhase_A = Register('VoltagePhase_A', float, 4)
            self.Current_A = Register('Current_A', float, 4)
            self.CurrentPhase_A = Register('CurrentPhase_A', float, 4)
            self.PowerActive_A = Register('PowerActive_A', float, 4)
            self.PowerReactive_A = Register('PowerReactive_A', float, 4)
            self.Voltage_B = Register('Voltage_B', float, 4)
            self.VoltagePhase_B = Register('VoltagePhase_B', float, 4)
            self.Current_B = Register('Current_B', float, 4)
            self.CurrentPhase_B = Register('CurrentPhase_B', float, 4)
            self.PowerActive_B = Register('PowerActive_B', float, 4)
            self.PowerReactive_B = Register('PowerReactive_B', float, 4)
            self.Voltage_C = Register('Voltage_C', float, 4)
            self.VoltagePhase_C = Register('VoltagePhase_C', float, 4)
            self.Current_C = Register('Current_C', float, 4)
            self.CurrentPhase_C = Register('CurrentPhase_C', float, 4)
            self.PowerActive_C = Register('PowerActive_C', float, 4)
            self.PowerReactive_C = Register('PowerReactive_C', float, 4)
            self.TotalPowerActive = Register('TotalPowerActive', float, 4)
            self.TotalPowerReactive = Register('TotalPowerReactive', float, 4)
            
            self.registerList = (
                self.Voltage_A,
                self.VoltagePhase_A,
                self.Current_A,
                self.CurrentPhase_A,
                self.PowerActive_A,
                self.PowerReactive_A,
                self.Voltage_B,
                self.VoltagePhase_B,
                self.Current_B,
                self.CurrentPhase_B,
                self.PowerActive_B,
                self.PowerReactive_B,
                self.Voltage_C,
                self.VoltagePhase_C,
                self.Current_C,
                self.CurrentPhase_C,
                self.PowerActive_C,
                self.PowerReactive_C,
                self.TotalPowerActive,
                self.TotalPowerReactive,
            )

        def getValue(self) -> Tuple[Register]:
            return self.registerList
        
        def extractResponseDataFrame(self, dataFrame:ResponseDataFrame) -> Tuple[Register]:
            if not isinstance(dataFrame, ResponseDataFrame):
                raise TypeError(f'dataFrame expect ResponseDataFrame not {type(dataFrame)}')
            
            data = dataFrame.DATA
            if len(data) == len(self.registerList*4):
                pass
            else:
                raise DatFrameError(f'Dataframe length not comply {len(self.registerList)*4}')
            
            values = [data[i:i+4] for i in range(0, len(data), 4)]
            for reg, val in zip(self.registerList, values):
                reg.value = Util.Hex2float(val, size=reg.size)
            return self.getValue()
        
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
        self.readbackSamplingRegister = EnergyErrorCalibration.ReadbackSamplingDataRegister()
    
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
        
    # def readbackSamplingTranslator(self,data:dict) -> dict:
    #     '''
    #         parameter data has structure as following
    #         {   
    #             "SOI": _soi,
    #             "COMMAND" : 0xc1,
    #             "ERROR_CODE": _err_code,
    #             "DATA": [...],
    #             "CRC": [LowByte_CRC, HighByte_CRC]
    #         }

    #         this function expects got data value from SerialHandler::transaction(), so you no need to worry about data structure
    #     '''
    #     registers = {
    #         'Ua_amplitude'          : 0.0,
    #         'Ua_phase'              : 0.0,
    #         'Ia_amplitude'          : 0.0,
    #         'Ia_phase'              : 0.0,
    #         'Pa'                    : 0.0,
    #         'Qa'                    : 0.0,

    #         'Ub_amplitude'          : 0.0,
    #         'Ub_phase'              : 0.0,
    #         'Ib_amplitude'          : 0.0,
    #         'Ib_phase'              : 0.0,
    #         'Pb'                    : 0.0,
    #         'Qb'                    : 0.0,

    #         'Uc_amplitude'          : 0.0,
    #         'Uc_phase'              : 0.0,
    #         'Ic_amplitude'          : 0.0,
    #         'Ic_phase'              : 0.0,
    #         'Pc'                    : 0.0,
    #         'Qc'                    : 0.0,

    #         'P'                     : 0.0,
    #         'Q'                     : 0.0
    #     }
    #     if data['ERROR_CODE'] == 0:
    #         if len(data['DATA']) == 80:
    #             for idx,i in enumerate(registers):
    #                 temp = []
    #                 for j in range(4):
    #                     temp.append(data['DATA'].pop(0))
    #                 registers[i] = Util.Hex2float(temp)
    #             registers['Sa'] = math.hypot(registers['Pa'],registers['Qa'])
    #             registers['Sb'] = math.hypot(registers['Pb'],registers['Qb'])
    #             registers['Sc'] = math.hypot(registers['Pc'],registers['Qc'])
    #             registers['S'] = math.hypot(registers['P'],registers['Q'])
    #             return registers.copy()
    #     return {}
    
    def readbackErrorSampling(self, count:int=1) -> list:
        '''
            return data frame in list to request test bench feedback
        '''
        data = []
        control_flag_bit = 0

        if count == 1:
            control_flag_bit = 1
        elif count == '*':
            control_flag_bit = 2

        data.append(control_flag_bit)
        data = Util.genDataFrame(EnergyErrorCalibration.Command.READBACK_ERROR_SAMPLING, data)
        return data.copy()

    def errorSamplingTranslator(self, data:dict) -> dict:
        '''
            parameter data has structure as following
            {   
                "SOI": _soi,
                "COMMAND" : 0xc1,
                "ERROR_CODE": _err_code,
                "DATA": [...],
                "CRC": [LowByte_CRC, HighByte_CRC]
            }

            this function expects got data value from SerialHandler::transaction(), so you no need to worry about data structure
        '''
        registers = {
            'valid flag bit'        : 0.0,
            'meter 1 error valid'   : 0.0,
            'meter 2 error valid'   : 0.0,
            'meter 3 error valid'   : 0.0,
        }

        if data['ERROR_CODE'] == 0:           
            validBitFlag = data['DATA'].pop(0)
            errors = []
            for i in range(3):
                temp = []
                for i in range(4):
                    temp.append(data['DATA'].pop(0))
                errors.append(Util.Hex2float(temp))

            registers['valid flag bit'] = validBitFlag
            registers['meter 1 error valid'] = errors[0]
            registers['meter 2 error valid'] = errors[1]
            registers['meter 3 error valid'] = errors[2]
            return registers.copy()
        
if __name__ == '__main__':
    print('Hello world')