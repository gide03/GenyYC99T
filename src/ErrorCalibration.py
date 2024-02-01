from typing import Union
from Util import Util, CommmandDataFrame, VoltageRange, CurrentRange, PowerSelector, ElementSelector
from Util import VoltageRangeError, CurrentRangeError
import math
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
        
    # class PowerSelection:
    #     _3P4W_ACTIVE            = 0x00
    #     _3P3W_ACTIVE            = 0x01
    #     _SINGLE_PHASE_ACTIVE    = 0x02
    #     _3P4W_REAL_REACTIVE     = 0x03
    #     _3P3W_REAL_REACTIVE     = 0x04
    #     _2_ELEMENTS_60_REACTIVE = 0x05
    #     _2_ELEMENTS_90_REACTIVE = 0x06
    #     _3_ELEMENTS_90_REACTIVE = 0x07
    
    # class ElementSelector:
    #     _COMBINE_ALL            = 0x00
    #     _A_ELEMENT              = 0x01
    #     _B_ELEMENT              = 0x02
    #     _C_ELEMENT              = 0x03
    #     _PHASE_ABC_OUTPUT       = 0x04
    #     _PHASE_AB_OUTPUT        = 0x05
    #     _PHASE_A_OUTPUT         = 0x06
    
    class PFUnit:
        _NO_UNIT    = 0x00
        _L          = 0x01
        _C          = 0x02
    
    # CMD_REGISTER = {
    #     "TEST_COMMAND"                  : 0xd0,
    #     "ONLINE_ADJUST_COMMAND"         : 0xd1,
    #     "STOP_TEST_COMMAND"             : 0xd3,
    #     "READBACK_SAMPLING_DATA"        : 0xd2,
    #     "READBACK_ERROR_SAMPLING"       : 0xd5,
    # }
    
    
    # defaultBufferRegister = {
    #     'power_selection'           : PowerSelection._3P4W_ACTIVE,
    #     'element_selection'         : ElementSelector._COMBINE_ALL,
    #     'U_range'                   : 8,
    #     'U_amplitude'               : 0,
    #     'I_amplitude'               : 0,
    #     'pf_value'                  : 0,
    #     'pf_unit'                   : PFUnit._L,
    #     'frequency'                 : 50,
    #     'meter constant'            : 0,
    #     'calib cycle'               : 0
    # }
    # bufferRegister = defaultBufferRegister.copy()


    def __init__(self):
        # self.defaultBufferRegister = {
        #     'power_selection'           : EnergyErrorCalibration.PowerSelection._3P4W_ACTIVE,
        #     'element_selection'         : EnergyErrorCalibration.ElementSelector._COMBINE_ALL,
        #     'U_range'                   : 8,
        #     'U_amplitude'               : 0,
        #     'I_amplitude'               : 0,
        #     'pf_value'                  : 0,
        #     'pf_unit'                   : EnergyErrorCalibration.PFUnit._L,
        #     'frequency'                 : 50,
        #     'meter constant'            : 0,
        #     'calib cycle'               : 0
        # }
        # self.buffer = self.defaultBufferRegister.copy()
        
        self.powerSelector = PowerSelector._3P4W_ACTIVE
        self.elementSelection = ElementSelector.EnergyErrorCalibration._COMBINE_ALL
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
        print(f"Element Selection           : {self.elementSelection.enum}")
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
            self.elementSelection.enum,
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
        
        
        # for i,reg in enumerate(self.bufferRegister):
        #     if byte_form_size[i] == 2:
        #         output.extend(Util.uint2byteList(self.bufferRegister[reg], bytesize=byte_form_size[i]))
        #     elif byte_form_size[i] == 1:
        #         output.append(self.bufferRegister[reg])
        #     else:
        #         temp = Util.float2byte(self.bufferRegister[reg], bytesize=byte_form_size[i])
        #         output.extend(temp) 
        # df = Util.genDataFrame(EnergyErrorCalibration.Command.TEST_COMMAND, output)
        # return df[:]
    
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
        data = []
        control_flag_bit = 0

        if count == 1:
            control_flag_bit = 1
        elif count == '*':
            control_flag_bit = 2

        data.append(control_flag_bit)
        data = Util.genDataFrame(EnergyErrorCalibration.Command.READBACK_SAMPLING_DATA, data)
        return data
    
    def readbackSamplingTranslator(self,data:dict) -> dict:
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
            'Ua_amplitude'          : 0.0,
            'Ua_phase'              : 0.0,
            'Ia_amplitude'          : 0.0,
            'Ia_phase'              : 0.0,
            'Pa'                    : 0.0,
            'Qa'                    : 0.0,

            'Ub_amplitude'          : 0.0,
            'Ub_phase'              : 0.0,
            'Ib_amplitude'          : 0.0,
            'Ib_phase'              : 0.0,
            'Pb'                    : 0.0,
            'Qb'                    : 0.0,

            'Uc_amplitude'          : 0.0,
            'Uc_phase'              : 0.0,
            'Ic_amplitude'          : 0.0,
            'Ic_phase'              : 0.0,
            'Pc'                    : 0.0,
            'Qc'                    : 0.0,

            'P'                     : 0.0,
            'Q'                     : 0.0
        }
        if data['ERROR_CODE'] == 0:
            if len(data['DATA']) == 80:
                for idx,i in enumerate(registers):
                    temp = []
                    for j in range(4):
                        temp.append(data['DATA'].pop(0))
                    registers[i] = Util.Hex2float(temp)
                registers['Sa'] = math.hypot(registers['Pa'],registers['Qa'])
                registers['Sb'] = math.hypot(registers['Pb'],registers['Qb'])
                registers['Sc'] = math.hypot(registers['Pc'],registers['Qc'])
                registers['S'] = math.hypot(registers['P'],registers['Q'])
                return registers.copy()
        return {}
    
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