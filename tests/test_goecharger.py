from unittest import (TestCase, mock)
from goecharger import (GoeCharger)
from goecharger.goecharger import (GoeChargerStatusMapper)

SAMPLE_API_STATUS_RESPONSE = {"version":"B","tme":"2612191302","rbc":"18","rbt":"769989354","car":"4","amp":"16","err":"0","ast":"0","alw":"1","stp":"0","cbl":"32","pha":"56","tmp":"3","dws":"1124887","dwo":"0","adi":"0","uby":"0","eto":"490","wst":"3","txi":"0","nrg":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],"fwv":"033","sse":"111111","wss":"SSID","wke":"********","wen":"1","cdi":"0","tof":"101","tds":"1","lbr":"100","aho":"3","afi":"7","azo":"0","ama":"16","al1":"6","al2":"10","al3":"16","al4":"0","al5":"0","cid":"65535","cch":"255","cfi":"65280","lse":"1","ust":"0","wak":"aaaaaaaaaa","r1x":"0","dto":"0","nmo":"0","sch":"AAAAAAAAAAAAAAAA","sdp":"0","eca":"0","ecr":"0","ecd":"0","ec4":"0","ec5":"0","ec6":"0","ec7":"0","ec8":"0","ec9":"0","ec1":"0","rca":"CACACACA","rcr":"","rcd":"","rc4":"","rc5":"","rc6":"","rc7":"","rc8":"","rc9":"","rc1":"","rna":"","rnm":"","rne":"","rn4":"","rn5":"","rn6":"","rn7":"","rn8":"","rn9":"","rn1":"","loe":0,"lot":0,"lom":0,"lop":0,"log":"","lon":0,"lof":0,"loa":0,"lch":260254,"mce":0,"mcs":"","mcp":0,"mcu":"","mck":"","mcc":0}
SAMPLE_REQUEST_STATUS_RESPONSE = {'car_status': 'charging finished, vehicle still connected', 'charger_max_current': 16, 'charger_absolute_max_current': 16, 'charger_err': 'OK', 'charger_access': 'free', 'allow_charging': 'on', 'stop_mode': 'manual', 'cable_max_current': 32, 'pre_contactor_l1': 'on', 'pre_contactor_l2': 'on', 'pre_contactor_l3': 'on', 'post_contactor_l1': 'off', 'post_contactor_l2': 'off', 'post_contactor_l3': 'off', 'charger_temp': 3, 'current_session_charged_energy': 3.12469, 'charge_limit': 0.0, 'adapter': 'No Adapter', 'unlocked_by_card': 0, 'energy_total': 49.0, 'wifi': 'connected', 'u_l1': 1, 'u_l2': 2, 'u_l3': 3, 'u_n': 4, 'i_l1': 0.5, 'i_l2': 0.6, 'i_l3': 0.7, 'p_l1': 0.8, 'p_l2': 0.9, 'p_l3': 1.0, 'p_n': 1.1, 'p_all': 0.12, 'lf_l1': 13, 'lf_l2': 14, 'lf_l3': 15, 'lf_n': 16, 'firmware': '033', 'serial_number': '111111', 'wifi_ssid': 'SSID', 'wifi_enabled': 'on', 'timezone_offset': 1, 'timezone_dst_offset': 1}
SAMPLE_REQUEST_STATUS_RESPONSE_UNAVAIL = {'car_status': 'unknown', 'charger_max_current': 6, 'charger_absolute_max_current': 0, 'charger_err': 'UNKNOWN', 'charger_access': 'unknown', 'allow_charging': 'unknown', 'stop_mode': 'unknown', 'cable_max_current': 0, 'pre_contactor_l1': 'unknown', 'pre_contactor_l2': 'unknown', 'pre_contactor_l3': 'unknown', 'post_contactor_l1': 'unknown', 'post_contactor_l2': 'unknown', 'post_contactor_l3': 'unknown', 'charger_temp': 0, 'current_session_charged_energy': 0.0, 'charge_limit': 0.0, 'adapter': 'unknown', 'unlocked_by_card': 0, 'energy_total': 0.0, 'wifi': 'unknown', 'u_l1': 0, 'u_l2': 0, 'u_l3': 0, 'u_n': 0, 'i_l1': 0.0, 'i_l2': 0.0, 'i_l3': 0.0, 'p_l1': 0.0, 'p_l2': 0.0, 'p_l3': 0.0, 'p_n': 0.0, 'p_all': 0.0, 'lf_l1': 0, 'lf_l2': 0, 'lf_l3': 0, 'lf_n': 0, 'firmware': 'unknown', 'serial_number': 'unknown', 'wifi_ssid': 'unknown', 'wifi_enabled': 'unknown', 'timezone_offset': -100, 'timezone_dst_offset': 0}

def helper_create_instance_without_host():
    return GoeCharger(None)

def helper_setButtonCurrentValue_ValueError():
    return GoeCharger('http://127.0.0.1').setButtonCurrentValue(0,6)

def helper_setAccessType_ValueError():
    return GoeCharger('http://127.0.0.1').setAccessType(1111)

def helper_setLockType_ValueError():
    return GoeCharger('http://127.0.0.1').setLockType(1111)

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, response):
            self._response = response
            self.status_code = status_code

        def json(self):
            return self._response

    if args[0] == 'http://127.0.0.1/status' or args[0].startswith('http://127.0.0.1/mqtt?payload='):
        return MockResponse(200, SAMPLE_API_STATUS_RESPONSE)
    return MockResponse(404, None)

class TestGoeCharger(TestCase):

    def test_create_without_host(self):
        self.assertRaises(ValueError, helper_create_instance_without_host)

    def test_create_with_host(self):
        self.assertIsNotNone(GoeCharger('127.0.0.1'))

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_requestStatus(self, mock_get):
        status = GoeCharger('127.0.0.1').requestStatus()
        self.assertEqual(SAMPLE_REQUEST_STATUS_RESPONSE, status)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAccessType(self, mock_get):
        response = GoeCharger('127.0.0.1').setAccessType(GoeCharger.AccessType.FREE)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=ast=0')
        self.assertIsNotNone(response)

    def test_setAccessTypeInvalidValue(self):
        self.assertRaises(ValueError, helper_setAccessType_ValueError)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLockType(self, mock_get):
        response = GoeCharger('127.0.0.1').setLockType(GoeCharger.LockType.AUTOMATIC)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=ust=1')
        self.assertIsNotNone(response)

    def test_setLockTypeInvalidValue(self):
        self.assertRaises(ValueError, helper_setLockType_ValueError)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setButtonCurrentValue(self, mock_get):
        response = GoeCharger('127.0.0.1').setButtonCurrentValue(1,6)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=al1=6')
        self.assertIsNotNone(response)

    def test_setButtonCurrentValueInvalidButton(self):
        self.assertRaises(ValueError, helper_setButtonCurrentValue_ValueError)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setButtonCurrentValueToLow(self, mock_get):
        response = GoeCharger('127.0.0.1').setButtonCurrentValue(1,5)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=al1=0')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setButtonCurrentValueToHigh(self, mock_get):
        response = GoeCharger('127.0.0.1').setButtonCurrentValue(1,33)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=al1=32')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setChargeLimit(self, mock_get):
        response = GoeCharger('127.0.0.1').setChargeLimit(2.4)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=dwo=24')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setMaxCurrent(self, mock_get):
        response = GoeCharger('127.0.0.1').setMaxCurrent(10)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=amp=10')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setMaxCurrentToLow(self, mock_get):
        response = GoeCharger('127.0.0.1').setMaxCurrent(5)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=amp=6')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setMaxCurrentToHigh(self, mock_get):
        response = GoeCharger('127.0.0.1').setMaxCurrent(33)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=amp=32')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAbsoluteMaxCurrent(self, mock_get):
        response = GoeCharger('127.0.0.1').setAbsoluteMaxCurrent(32)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=ama=32')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAbsoluteMaxCurrentToLow(self, mock_get):
        response = GoeCharger('127.0.0.1').setAbsoluteMaxCurrent(5)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=ama=6')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAbsoluteMaxCurrentToHigh(self, mock_get):
        response = GoeCharger('127.0.0.1').setAbsoluteMaxCurrent(33)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=ama=32')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedAutoTurnOffTrue(self, mock_get):
        response = GoeCharger('127.0.0.1').setLedAutoTurnOff(True)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=r2x=1')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedAutoTurnOffFalse(self, mock_get):
        response = GoeCharger('127.0.0.1').setLedAutoTurnOff(False)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=r2x=0')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAllowChargingTrue(self, mock_get):
        response = GoeCharger('127.0.0.1').setAllowCharging(True)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=alw=1')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAllowChargingFalse(self, mock_get):
        response = GoeCharger('127.0.0.1').setAllowCharging(False)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=alw=0')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAutoStopTrue(self, mock_get):
        response = GoeCharger('127.0.0.1').setAutoStop(True)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=stp=2')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAutoStopFalse(self, mock_get):
        response = GoeCharger('127.0.0.1').setAutoStop(False)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=stp=0')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setStandbyColor(self, mock_get):
        response = GoeCharger('127.0.0.1').setStandbyColor(0x808080)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=cid=8421504')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setChargingActiveColor(self, mock_get):
        response = GoeCharger('127.0.0.1').setChargingActiveColor(0x808080)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=cch=8421504')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setChargingFinishedColor(self, mock_get):
        response = GoeCharger('127.0.0.1').setChargingFinishedColor(0x808080)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=cfi=8421504')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedBrightness(self, mock_get):
        response = GoeCharger('127.0.0.1').setLedBrightness(100)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=lbr=100')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedBrightnessToLow(self, mock_get):
        response = GoeCharger('127.0.0.1').setLedBrightness(-1)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=lbr=0')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedBrightnessToHigh(self, mock_get):
        response = GoeCharger('127.0.0.1').setLedBrightness(256)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=lbr=255')
        self.assertIsNotNone(response)

    def test_chargerNotAvailable(self):
        status = GoeCharger('127.0.0.2').requestStatus()
        self.maxDiff = None
        self.assertEqual(SAMPLE_REQUEST_STATUS_RESPONSE_UNAVAIL, status)
