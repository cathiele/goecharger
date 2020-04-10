# -*- coding: utf-8 -*-

# API-documentation: https://go-e.co/app/api.pdf

import requests
from enum import Enum


class GoeChargerStatusMapper:

    def __phaseDetection(self, phase, bit):
        if phase & bit:
            return 'on'
        else:
            return 'off'

    def mapApiStatusResponse(self, status):
        car_status = GoeCharger.GO_CAR_STATUS.get(status.get('car')) or 'unknown'
        charger_max_current = int(status.get('amp', 6))
        charger_absolute_max_current = int(status.get('ama', 0))
        charger_err = GoeCharger.GO_ERR.get(status.get('err')) or 'UNKNOWN'
        charger_access = GoeCharger.GO_ACCESS.get(status.get('ast')) or 'unknown'
        allow_charging = GoeCharger.GO_ALLOW_CHARGING.get(status.get('alw')) or 'unknown'
        stop_mode = GoeCharger.GO_STOP_MODE.get(status.get('stp')) or 'unknown'
        cable_max_current = int(status.get('cbl', 0))

        try:
            phase = int(status.get('pha'))

            pre_contactor_l3 = self.__phaseDetection(phase, 0x20)
            pre_contactor_l2 = self.__phaseDetection(phase, 0x10)
            pre_contactor_l1 = self.__phaseDetection(phase, 0x08)
            post_contactor_l3 = self.__phaseDetection(phase, 0x04)
            post_contactor_l2 = self.__phaseDetection(phase, 0x02)
            post_contactor_l1 = self.__phaseDetection(phase, 0x01)
        except Exception:
            pre_contactor_l1 = pre_contactor_l2 = pre_contactor_l3 = 'unknown'
            post_contactor_l1 = post_contactor_l2 = post_contactor_l3 = 'unknown'

        charger_temp = int(status.get('tmp', 0))
        current_session_charged_energy = round(int(status.get('dws', 0)) / 360000.0, 5)
        charge_limit = int(status.get('dwo', 0)) / 10.0
        adapter = GoeCharger.GO_ADAPTER.get(status.get('adi')) or 'unknown'
        unlocked_by_card = int(status.get('uby', 0))
        energy_total = int(status.get('eto', 0)) / 10.0
        wifi = 'connected' if status.get('wst') == '3' else 'unknown' if status.get('wst') is None else 'not connected'
        firmware = status.get('fwv', 'unknown')
        serial_number = status.get('sse', 'unknown')
        wifi_ssid = status.get('wss', 'unknown')
        wifi_enabled = 'on' if status.get('wen') == '1' else 'off' if status.get('wen') == '0' else 'unknown'
        timezone_offset = int(status.get('tof', 0)) - 100
        timezone_dst_offset = int(status.get('tds', 0))

        def valueOrNull(array, index):
            try:
                return array[index]
            except IndexError:
                return 0

        return ({
            'car_status': car_status,
            'charger_max_current': charger_max_current,
            'charger_absolute_max_current': charger_absolute_max_current,
            'charger_err': charger_err,
            'charger_access': charger_access,
            'allow_charging': allow_charging,
            'stop_mode': stop_mode,
            'cable_max_current': cable_max_current,
            'pre_contactor_l1': pre_contactor_l1,
            'pre_contactor_l2': pre_contactor_l2,
            'pre_contactor_l3': pre_contactor_l3,
            'post_contactor_l1': post_contactor_l1,
            'post_contactor_l2': post_contactor_l2,
            'post_contactor_l3': post_contactor_l3,
            'charger_temp': charger_temp,
            'current_session_charged_energy': current_session_charged_energy,
            'charge_limit': charge_limit,
            'adapter': adapter,
            'unlocked_by_card': unlocked_by_card,
            'energy_total': energy_total,
            'wifi': wifi,

            'u_l1': int(valueOrNull(status.get('nrg', []), GoeCharger.U_L1)),
            'u_l2': int(valueOrNull(status.get('nrg', []), GoeCharger.U_L2)),
            'u_l3': int(valueOrNull(status.get('nrg', []), GoeCharger.U_L3)),
            'u_n': int(valueOrNull(status.get('nrg', []), GoeCharger.U_N)),
            'i_l1': int(valueOrNull(status.get('nrg', []), GoeCharger.I_L1)) / 10.0,
            'i_l2': int(valueOrNull(status.get('nrg', []), GoeCharger.I_L2)) / 10.0,
            'i_l3': int(valueOrNull(status.get('nrg', []), GoeCharger.I_L3)) / 10.0,
            'p_l1': int(valueOrNull(status.get('nrg', []), GoeCharger.P_L1)) / 10.0,
            'p_l2': int(valueOrNull(status.get('nrg', []), GoeCharger.P_L2)) / 10.0,
            'p_l3': int(valueOrNull(status.get('nrg', []), GoeCharger.P_L3)) / 10.0,
            'p_n': int(valueOrNull(status.get('nrg', []), GoeCharger.P_N)) / 10.0,
            'p_all': int(valueOrNull(status.get('nrg', []), GoeCharger.P_ALL)) / 100.0,
            'lf_l1': int(valueOrNull(status.get('nrg', []), GoeCharger.LF_L1)),
            'lf_l2': int(valueOrNull(status.get('nrg', []), GoeCharger.LF_L2)),
            'lf_l3': int(valueOrNull(status.get('nrg', []), GoeCharger.LF_L3)),
            'lf_n': int(valueOrNull(status.get('nrg', []), GoeCharger.LF_N)),

            'firmware': firmware,
            'serial_number': serial_number,
            'wifi_ssid': wifi_ssid,
            'wifi_enabled': wifi_enabled,
            'timezone_offset': timezone_offset,
            'timezone_dst_offset': timezone_dst_offset

        })


class GoeCharger:
    host = ''

    def __init__(self, host):
        if (host is None or host == ''):
            raise ValueError("host must be specified")
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
    U_N = 3
    I_L1 = 4
    I_L2 = 5
    I_L3 = 6
    P_L1 = 7
    P_L2 = 8
    P_L3 = 9
    P_N = 10
    P_ALL = 11
    LF_L1 = 12
    LF_L2 = 13
    LF_L3 = 14
    LF_N = 15

    GO_ERR = {
        '0': 'OK',
        '1': 'RCCB',
        '3': 'PHASE',
        '8': 'NO_GROUND',
        '10': 'INTERNAL'
    }

    GO_ACCESS = {
        '0': 'free',
        '1': 'rfid/app',
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

    def __queryStatusApi(self):
        try:
            statusRequest = requests.get("http://%s/status" % self.host, timeout=5)  # TODO: Configurable Timeout
            status = statusRequest.json()
            return status
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return {}

    def __setParameter(self, parameter, value):
        setRequest = requests.get("http://%s/mqtt?payload=%s=%s" % (self.host, parameter, value))
        return GoeChargerStatusMapper().mapApiStatusResponse(setRequest.json())

    def setAccessType(self, accessType):
        if (
            accessType == GoeCharger.AccessType.FREE or
            accessType == GoeCharger.AccessType.RFID_APP or
            accessType == GoeCharger.AccessType.AUTO
        ):
            return self.__setParameter('ast', str(accessType.value))

        raise ValueError('Invalid AccessType: %d provided' % accessType)

    def setLockType(self, lockType):
        if (
            lockType == GoeCharger.LockType.UNLOCKCARFIRST or
            lockType == GoeCharger.LockType.AUTOMATIC or
            lockType == GoeCharger.LockType.LOCKED
        ):
            return self.__setParameter('ust', str(lockType.value))

        raise ValueError('Invalid LockType: %d provided' % lockType)

    def setAllowCharging(self, allow):
        if allow:
            return self.__setParameter('alw', '1')
        else:
            return self.__setParameter('alw', '0')

    # TODO: not necessary (tested with fw 033)
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

    def setLedAutoTurnOff(self, autoTurnOff):
        if autoTurnOff:
            return self.__setParameter('r2x', '1')
        else:
            return self.__setParameter('r2x', '0')

    def setAbsoluteMaxCurrent(self, maxCurrent):
        if maxCurrent < 6:
            maxCurrent = 6
        if maxCurrent > 32:
            maxCurrent = 32
        return self.__setParameter('ama', str(maxCurrent))

    def setMaxCurrent(self, current):
        if current < 6:
            current = 6
        if current > 32:
            current = 32
        return self.__setParameter('amp', str(current))

    def setChargeLimit(self, chargeLimit):
        limit = int(chargeLimit * 10) if chargeLimit >= 0 else 0
        return self.__setParameter('dwo', str(limit))

    def setButtonCurrentValue(self, step, current):
        if step < 1 or step > 5:
            raise ValueError('Invalid Button step %d requested!' % step)
        if current < 6:
            current = 0
        if current > 32:
            current = 32
        return self.__setParameter('al%d' % step, str(current))

    def requestStatus(self):
        status = self.__queryStatusApi()
        response = GoeChargerStatusMapper().mapApiStatusResponse(status)
        return response
