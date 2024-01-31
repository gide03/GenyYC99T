from Util import Util
import math

class EnergyErrorCalibration:
    class Buffer:
        def __init__(self):
            self.POWER_SELECTION = 0
            self.ELEMENT_SELECTION = 0
            self.VOLTAGE_RANGE = Util.YC99T_5C.VoltageRange._220V
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
        
    class PowerSelection:
        _3P4W_ACTIVE            = 0x00
        _3P3W_ACTIVE            = 0x01
        _SINGLE_PHASE_ACTIVE    = 0x02
        _3P4W_REAL_REACTIVE     = 0x03
        _3P3W_REAL_REACTIVE     = 0x04
        _2_ELEMENTS_60_REACTIVE = 0x05
        _2_ELEMENTS_90_REACTIVE = 0x06
        _3_ELEMENTS_90_REACTIVE = 0x07
    
    class ElementSelector:
        _COMBINE_ALL            = 0x00
        _A_ELEMENT              = 0x01
        _B_ELEMENT              = 0x02
        _C_ELEMENT              = 0x03
        _PHASE_ABC_OUTPUT       = 0x04
        _PHASE_AB_OUTPUT        = 0x05
        _PHASE_A_OUTPUT         = 0x06
    
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
        self.defaultBufferRegister = {
            'power_selection'           : EnergyErrorCalibration.PowerSelection._3P4W_ACTIVE,
            'element_selection'         : EnergyErrorCalibration.ElementSelector._COMBINE_ALL,
            'U_range'                   : 8,
            'U_amplitude'               : 0,
            'I_amplitude'               : 0,
            'pf_value'                  : 0,
            'pf_unit'                   : EnergyErrorCalibration.PFUnit._L,
            'frequency'                 : 50,
            'meter constant'            : 0,
            'calib cycle'               : 0
        }
        self.buffer = self.defaultBufferRegister.copy()
        
        self.powerSelection = EnergyErrorCalibration.PowerSelection._3P4W_ACTIVE
        self.elementSelection = EnergyErrorCalibration.ElementSelector._COMBINE_ALL
        self.voltageRange = Util.YC99T_5C.VoltageRange._220V
        self.currentRange = Util.YC99T_5C.CurrentRange._20A
        self.voltage = 0.0
        self.current = 0.0
        self.powerFactor = 1
        self.powerFactorUnit = EnergyErrorCalibration.PFUnit._L
        self.meterConstant = 0
        self.calibMeasurementCycle = 0
    
    #
    # Internal Util
    #
    def resetDefault(self):
        self.powerSelection = EnergyErrorCalibration.PowerSelection._3P4W_ACTIVE
        self.elementSelection = EnergyErrorCalibration.ElementSelector._COMBINE_ALL
        self.voltageRange = Util.YC99T_5C.VoltageRange._220V
        self.currentRange = Util.YC99T_5C.CurrentRange._20A
        self.voltage = 0.0
        self.current = 0.0
        self.powerFactor = 1
        self.powerFactorUnit = EnergyErrorCalibration.PFUnit._L
        self.meterConstant = 0
        self.calibMeasurementCycle = 0
    #
    

    def testCommand(self) -> list:
        '''
            return data frame in list for test command GENY mode Energy Error Calibration. Refer to Energy Error Calibration test command in Geny documentation.
        '''
        byte_form_size = (1,1,1,4,4,4,1,4,4,2)
        output = []
        for i,reg in enumerate(self.bufferRegister):
            if byte_form_size[i] == 2:
                output.extend(Util.uint2byteList(self.bufferRegister[reg], bytesize=byte_form_size[i]))
            elif byte_form_size[i] == 1:
                output.append(self.bufferRegister[reg])
            else:
                temp = Util.float2byte(self.bufferRegister[reg], bytesize=byte_form_size[i])
                output.extend(temp) 
        df = Util.genDataFrame(EnergyErrorCalibration.Command.TEST_COMMAND, output)
        return df[:]
    
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