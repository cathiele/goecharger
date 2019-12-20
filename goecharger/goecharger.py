# -*- coding: utf-8 -*-

# API-documentation: https://go-e.co/app/api.pdf

import requests
from enum import Enum

class GoeCharger:
    host = ''

    def __init__(self, host):
        self.host = host


    GO_CAR_STATUS = {
        '1': 'Charger ready, no vehicle',
        '2': 'charging',
        '3': 'Waiting for vehicle',
        '4': 'charging finished, vehicle still connected'
    }

    GO_ADAPTER = {
        '0': 'No Adapter',
        '1': '16A-Adapter'
    }

    class AccessType(Enum):
        FREE = 0
        RFID_APP = 1
        AUTO = 2

    class LockType(Enum):
        UNLOCKCARFIRST = 0
        AUTOMATIC = 1
        LOCKED = 2

    U_L1 = 0
    U_L2 = 1
    U_L3 = 2
    U_N  = 3
    I_L1 = 4
    I_L2 = 5
    I_L3 = 6
    P_L1 = 7
    P_L2 = 8
    P_L3 = 9
    P_N  = 10
    P_ALL= 11
    LF_L1= 12
    LF_L2= 13
    LF_L3= 14
    LF_N = 15

    GO_ERR = {
        '0': 'OK',
        '1': 'RCCB',
        '2': 'PHASE',
        '8': 'NO_GROUND',
        '10': 'INTERNAL'
    }

    GO_ACCESS = {
        '0': 'free',
        '1': 'rfid/app' ,
        '2': 'cost based / automatic'
    }

    GO_ALLOW_CHARGING = {
        '0': 'off',
        '1': 'on'
    }
    GO_STOP_MODE = {
        '0': 'manual',
        '2': 'kWh based'
    }

    def __phaseDetection(self, phase, bit):
        if phase & bit:
            return 'on'
        else:
            return 'off'

    def __mapStatusReponse(self, status):
        car_status = GoeCharger.GO_CAR_STATUS.get(status['car']) or 'unknown'
        charger_amp_pwm = int(status['amp'])
        charger_err = GoeCharger.GO_ERR.get(status['err']) or 'UNKNOWN'
        charger_access = GoeCharger.GO_ACCESS.get(status['ast']) or 'unknown'
        allow_charging = GoeCharger.GO_ALLOW_CHARGING.get(status['alw']) or 'unknown'
        stop_mode = GoeCharger.GO_STOP_MODE.get(status['stp']) or 'unknown'
        cable_amp = int(status['cbl'])

        phase = int(status['pha'])

        pre_contactor_l1 = self.__phaseDetection(phase, 0x20)
        pre_contactor_l2 = self.__phaseDetection(phase, 0x10)
        pre_contactor_l3 = self.__phaseDetection(phase, 0x08)
        post_contactor_l1 = self.__phaseDetection(phase, 0x04)
        post_contactor_l2 = self.__phaseDetection(phase, 0x02)
        post_contactor_l3 = self.__phaseDetection(phase, 0x01)

        charger_tmp = int(status['tmp'])
        current_session_charged_energy = round(int(status['dws']) / 360000.0,5)
        charge_limit = int(status['dwo']) / 10.0
        adapter = GoeCharger.GO_ADAPTER.get(status['adi']) or 'unknown'
        unlocked_by_card = int(status['uby'])
        energy_total = int(status['eto']) / 10.0
        wifi = 'connected' if status['wst'] == '3' else 'not connected'
        firmware = status['fwv']
        serial_number = status['sse']
        wifi_ssid = status['wss']
        wifi_enabled = 'on' if status['wen'] == '1' else 'off'
        timezone_offset = int(status['tof']) - 100
        timezone_dst_offset = int(status['tds']) 

        return ( {
            'car_status': car_status,
            'charger_amp_pwm': charger_amp_pwm,
            'charger_err': charger_err,
            'charger_access': charger_access,
            'allow_charging': allow_charging,
            'stop_mode': stop_mode,
            'cable_amp': cable_amp,
            'pre_contactor_l1': pre_contactor_l1,
            'pre_contactor_l2': pre_contactor_l2,
            'pre_contactor_l3': pre_contactor_l3,
            'post_contactor_l1': post_contactor_l1,
            'post_contactor_l2': post_contactor_l2,
            'post_contactor_l3': post_contactor_l3,
            'charger_tmp': charger_tmp,
            'current_session_charged_energy': current_session_charged_energy,
            'charge_limit': charge_limit,
            'adapter': adapter,
            'unlocked_by_card': unlocked_by_card,
            'energy_total': energy_total,
            'wifi': wifi,

            'u_l1': int(status['nrg'][GoeCharger.U_L1]),
            'u_l2': int(status['nrg'][GoeCharger.U_L2]),
            'u_l3' : int(status['nrg'][GoeCharger.U_L3]),
            'u_n': int(status['nrg'][GoeCharger.U_N]),
            'i_l1': int(status['nrg'][GoeCharger.I_L1]) / 10.0,
            'i_l2': int(status['nrg'][GoeCharger.I_L2]) / 10.0,
            'i_l3': int(status['nrg'][GoeCharger.I_L3]) / 10.0,
            'p_l1': int(status['nrg'][GoeCharger.P_L1]) / 10.0,
            'p_l2': int(status['nrg'][GoeCharger.P_L2]) / 10.0,
            'p_l3': int(status['nrg'][GoeCharger.P_L3]) / 10.0,
            'p_n': int(status['nrg'][GoeCharger.P_N]) / 10.0,
            'p_all': int(status['nrg'][GoeCharger.P_ALL]) / 100.0,
            'lf_l1': int(status['nrg'][GoeCharger.LF_L1]),
            'lf_l2': int(status['nrg'][GoeCharger.LF_L2]),
            'lf_l3': int(status['nrg'][GoeCharger.LF_L3]),
            'lf_n': int(status['nrg'][GoeCharger.LF_N]),

            'firmware': firmware,
            'serial_number': serial_number,
            'wifi_ssid': wifi_ssid,
            'wifi_enabled': wifi_enabled,
            'timezone_offset': timezone_offset,
            'timezone_dst_offset': timezone_dst_offset

        })

    def __queryStatusApi(self):
        statusRequest = requests.get("http://%s/status" % self.host)
        status = statusRequest.json()
        return status
    
    def __setParameter(self, parameter, value):
        setRequest = requests.get("http://%s/mqtt?payload=%s=%s" % (self.host, parameter, value))
        return self.__mapStatusReponse(setRequest.json())

    def setChargerAmpere(self, ampere):
        if ampere < 6:
            ampere = 6
        if ampere > 32:
            ampere = 32
        return self.__setParameter('amp', str(ampere))

    def setAccessType(self, accessType):
        if accessType == GoeCharger.AccessType.FREE or accessType == GoeCharger.AccessType.RFID_APP or accessType == GoeCharger.AccessType.AUTO:
            return self.__setParameter('ast', str(accessType.value))

        raise Exception('Invalid AccessType: %d provided' % accessType)

    def setLockType(self, lockType):
        if lockType == GoeCharger.LockType.UNLOCKCARFIRST or lockType == GoeCharger.LockType.AUTOMATIC or lockType == GoeCharger.LockType.LOCKED:
            return self.__setParameter('ust', str(lockType.value))

        raise Exception('Invalid AccessType: %d provided' % lockType)

    def setAllowCharging(self, allow):
        if allow:
            return self.__setParameter('alw', '1')
        else:
            return self.__setParameter('alw', '0')

    # TODO: not working with fw 033
    def setAutoStop(self, autoStop):
        if autoStop:
            return self.__setParameter('stp', '2')
        else:
            return self.__setParameter('stp', '0')

    def setStandbyColor(self, color):
        color = color & 0xFFFFFF
        return self.__setParameter('cid', str(color))

    def setChargingActiveColor(self, color):
        color = color & 0xFFFFFF
        return self.__setParameter('cch', str(color))

    def setChargingFinishedColor(self, color):
        color = color & 0xFFFFFF
        return self.__setParameter('cfi', str(color))

    def setLedBrightness(self, brightness):
        if brightness < 0:
            brightness = 0
        if brightness > 255:
            brightness = 255
        return self.__setParameter('lbr', str(brightness))

    # TODO: not working with fw 033
    def setLedAutoTurnOff(self, autoTurnOff):
        if autoTurnOff:
            return self.__setParameter('lse', '1')
        else:
            return self.__setParameter('lse', '0')

    def setAbsoluteMaxAmpere(self, maxAmp):
        if maxAmp < 6:
            maxAmp = 6
        if maxAmp > 32:
            maxAmp = 32
        return self.__setParameter('ama', str(maxAmp))

    def setChargeLimit(self, chargeLimit):
        limit = int(chargeLimit * 10) if chargeLimit >= 0 else 0
        return self.__setParameter('dwo', str(limit))

    def setButtonAmpValue(self, step, amp):
        if step < 1 or step > 5:
            raise Exception('Invalid Button step %d requested!' % step)
        if amp < 6:
            amp = 0
        if amp > 32:
            amp = 32
        return self.__setParameter('al%d' % step, str(amp))

    def requestStatus(self):
        status = self.__queryStatusApi()
        response = self.__mapStatusReponse(status)
        return response