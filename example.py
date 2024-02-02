if __name__ == '__main__':
    from src.GenyTestBench import GenyTestBench
    from src.Util import ElementSelector, PowerSelector, VoltageRange
    import time
    
    geny = GenyTestBench('COM6', 115200)
    geny.setMode(GenyTestBench.Mode.ENERGY_ERROR_CALIBRATION)
        
    def login_logout():
        print('[login_logout] opening port')
        print(geny.open())
        print('[login_logout] closing port')
        print(geny.close())
        exit()

    def apply_voltage():
        print('[apply_voltage] opening port')
        print(geny.open())
        print('[apply_voltage] set power selector')
        geny.setPowerSelector(PowerSelector._3P4W_ACTIVE)
        
        # channel selector
        elementSelector = (
            ElementSelector.EnergyErrorCalibration._A_ELEMENT,
            ElementSelector.EnergyErrorCalibration._B_ELEMENT,
            ElementSelector.EnergyErrorCalibration._C_ELEMENT,
            ElementSelector.EnergyErrorCalibration._COMBINE_ALL
        )
        for element in elementSelector:
            print(f'[apply_voltage] set channel selector: {element}')        
            geny.setElementSelector(element)        
            print('[apply_voltage] set voltage range')
            geny.setVoltageRange(VoltageRange.YC99T_5C._220V)
            print('[apply_voltage] set voltage')
            geny.setVoltage(220)
            print('[apply_voltage] apply test bench configuration')
            result = geny.apply()
            print(f'[apply_voltage] result: {result}')
            if result == False:
                print('[apply_voltage] could not satisfied your command')
                print('[apply_voltage] closing port')
                geny.close()
                exit(1)
            
            input('Enter to continue')
            timeWait = 10
            for i in range(timeWait):
                print(f'[apply_voltage] wait {timeWait-1-i}')
                time.sleep(1)
        print('[apply_voltage] closing port')
        geny.close()

    def apply_current():
        print('[apply_voltage] opening port')
        print(geny.open())
        print('[apply_voltage] set power selector')
        geny.setPowerSelector(PowerSelector._3P4W_ACTIVE)
        
        # channel selector
        elementSelector = (
            ElementSelector.EnergyErrorCalibration._A_ELEMENT,
            ElementSelector.EnergyErrorCalibration._B_ELEMENT,
            ElementSelector.EnergyErrorCalibration._C_ELEMENT,
            ElementSelector.EnergyErrorCalibration._COMBINE_ALL
        )
        for element in elementSelector:
            print(f'[apply_voltage] set channel selector: {element}')        
            geny.setElementSelector(element)        
            print('[apply_voltage] set voltage range')
            geny.setVoltageRange(VoltageRange.YC99T_5C._220V)
            print('[apply_voltage] set voltage')
            geny.setVoltage(220)
            print('[apply_voltage] set current')
            geny.setCurrent(5)
            print('[apply_voltage] apply test bench configuration')
            result = geny.apply()
            print(f'[apply_voltage] result: {result}')
            if result == False:
                print('[apply_voltage] could not satisfied your command')
                print('[apply_voltage] closing port')
                geny.close()
                exit(1)
            
            input('Enter to continue')
            timeWait = 10
            for i in range(timeWait):
                print(f'[apply_voltage] wait {timeWait-1-i}')
                time.sleep(1)
        print('[apply_voltage] closing port')
        geny.close()
    
    def readback_sampling_data():
        print('[apply_voltage] opening port')
        print(geny.open())
        print('[apply_voltage] set power selector')
        geny.setPowerSelector(PowerSelector._3P4W_ACTIVE)
        
        # channel selector
        elementSelector = (
            ElementSelector.EnergyErrorCalibration._A_ELEMENT,
            ElementSelector.EnergyErrorCalibration._B_ELEMENT,
            ElementSelector.EnergyErrorCalibration._C_ELEMENT,
            ElementSelector.EnergyErrorCalibration._COMBINE_ALL
        )
        for element in elementSelector:
            print(f'[apply_voltage] set channel selector: {element}')        
            geny.setElementSelector(element)        
            print('[apply_voltage] set voltage range')
            geny.setVoltageRange(VoltageRange.YC99T_5C._220V)
            print('[apply_voltage] set voltage')
            geny.setVoltage(220)
            print('[apply_voltage] set current')
            geny.setCurrent(5)
            print('[apply_voltage] apply test bench configuration')
            result = geny.apply()
            print(f'[apply_voltage] result: {result}')
            if result == False:
                print('[apply_voltage] could not satisfied your command')
                print('[apply_voltage] closing port')
                geny.close()
                exit(1)
            geny.readBackSamplingData(verbose = True)
            input('Enter to continue')
        print('[apply_voltage] closing port')
        geny.close()
    
    def apply_power_factor():
        print('[apply_voltage] opening port')
        print(geny.open())
        print('[apply_voltage] set power selector')
        geny.setPowerSelector(PowerSelector._3P4W_ACTIVE)
        
        # channel selector
        elementSelector = (
            ElementSelector.EnergyErrorCalibration._A_ELEMENT,
            ElementSelector.EnergyErrorCalibration._B_ELEMENT,
            ElementSelector.EnergyErrorCalibration._C_ELEMENT,
            ElementSelector.EnergyErrorCalibration._COMBINE_ALL
        )
        for element in elementSelector:
            print(f'[apply_voltage] set channel selector: {element}')        
            geny.setElementSelector(element)        
            print('[apply_voltage] set voltage range')
            geny.setVoltageRange(VoltageRange.YC99T_5C._220V)
            print('[apply_voltage] set voltage')
            geny.setVoltage(220)
            print('[apply_voltage] set current')
            geny.setCurrent(5)
            print('[apply_voltage] set power factor')
            geny.setPowerFactor(75, inDegree=True)
            print('[apply_voltage] apply test bench configuration')
            result = geny.apply()
            print(f'[apply_voltage] result: {result}')
            if result == False:
                print('[apply_voltage] could not satisfied your command')
                print('[apply_voltage] closing port')
                geny.close()
                exit(1)
            geny.readBackSamplingData(verbose = True)
            input('Enter to continue')
        print('[apply_voltage] closing port')    
        geny.close()
        
    def readback_error_sampling():
        print('[apply_voltage] opening port')
        print(geny.open())
        print('[apply_voltage] set power selector')
        geny.setPowerSelector(PowerSelector._3P4W_ACTIVE)
        
        # channel selector
        elementSelector = (
            # ElementSelector.EnergyErrorCalibration._A_ELEMENT,
            # ElementSelector.EnergyErrorCalibration._B_ELEMENT,
            # ElementSelector.EnergyErrorCalibration._C_ELEMENT,
            ElementSelector.EnergyErrorCalibration._COMBINE_ALL,
        )
        for element in elementSelector:
            print(f'[apply_voltage] set channel selector: {element}')        
            geny.setElementSelector(element)        
            print('[apply_voltage] set voltage range')
            geny.setVoltageRange(VoltageRange.YC99T_5C._220V)
            print('[apply_voltage] set voltage')
            geny.setVoltage(220)
            print('[apply_voltage] set current')
            geny.setCurrent(10)
            print('[apply_voltage] set power factor')
            geny.setPowerFactor(40, inDegree=True)
            print('[apply_voltage] set calibration constants')
            geny.setCalibrationConstants(1000, 5)
            print('[apply_voltage] apply test bench configuration')
            result = geny.apply()
            print(f'[apply_voltage] result: {result}')
            if result == False:
                print('[apply_voltage] could not satisfied your command')
                print('[apply_voltage] closing port')
                geny.close()
                exit(1)
            geny.readBackSamplingData(verbose = True)
            geny.readBackError(verbose = True)
            input('Enter to continue')
        print('[apply_voltage] closing port')    
        geny.close()
    
    # Test Case
    login_logout()
    apply_voltage()
    apply_current()
    readback_sampling_data()
    apply_power_factor()
    readback_error_sampling()
