from unittest import (TestCase, mock)
from goecharger.goecharger import (GoeChargerStatusMapper)

SAMPLE_API_STATUS_RESPONSE = {"version":"B","tme":"2612191302","rbc":"18","rbt":"769989354","car":"4","amp":"16","err":"0","ast":"0","alw":"1","stp":"0","cbl":"32","pha":"56","tmp":"3","dws":"1124887","dwo":"0","adi":"0","uby":"0","eto":"490","wst":"3","txi":"0","nrg":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],"fwv":"033","sse":"111111","wss":"SSID","wke":"********","wen":"1","cdi":"0","tof":"101","tds":"1","lbr":"100","aho":"3","afi":"7","azo":"0","ama":"16","al1":"6","al2":"10","al3":"16","al4":"0","al5":"0","cid":"65535","cch":"255","cfi":"65280","lse":"1","ust":"0","wak":"aaaaaaaaaa","r1x":"0","dto":"0","nmo":"0","sch":"AAAAAAAAAAAAAAAA","sdp":"0","eca":"0","ecr":"0","ecd":"0","ec4":"0","ec5":"0","ec6":"0","ec7":"0","ec8":"0","ec9":"0","ec1":"0","rca":"CACACACA","rcr":"","rcd":"","rc4":"","rc5":"","rc6":"","rc7":"","rc8":"","rc9":"","rc1":"","rna":"","rnm":"","rne":"","rn4":"","rn5":"","rn6":"","rn7":"","rn8":"","rn9":"","rn1":"","loe":0,"lot":0,"lom":0,"lop":0,"log":"","lon":0,"lof":0,"loa":0,"lch":260254,"mce":0,"mcs":"","mcp":0,"mcu":"","mck":"","mcc":0}
SAMPLE_REQUEST_STATUS_RESPONSE = {'car_status': 'charging finished, vehicle still connected', 'charger_max_current': 16, 'charger_absolute_max_current': 16, 'charger_err': 'OK', 'charger_access': 'free', 'allow_charging': 'on', 'stop_mode': 'manual', 'cable_max_current': 32, 'pre_contactor_l1': 'on', 'pre_contactor_l2': 'on', 'pre_contactor_l3': 'on', 'post_contactor_l1': 'off', 'post_contactor_l2': 'off', 'post_contactor_l3': 'off', 'charger_temp': 3, 'current_session_charged_energy': 3.12469, 'charge_limit': 0.0, 'adapter': 'No Adapter', 'unlocked_by_card': 0, 'energy_total': 49.0, 'wifi': 'connected', 'u_l1': 1, 'u_l2': 2, 'u_l3': 3, 'u_n': 4, 'i_l1': 0.5, 'i_l2': 0.6, 'i_l3': 0.7, 'p_l1': 0.8, 'p_l2': 0.9, 'p_l3': 1.0, 'p_n': 1.1, 'p_all': 0.12, 'lf_l1': 13, 'lf_l2': 14, 'lf_l3': 15, 'lf_n': 16, 'firmware': '033', 'serial_number': '111111', 'wifi_ssid': 'SSID', 'wifi_enabled': 'on', 'timezone_offset': 1, 'timezone_dst_offset': 1}

class TestGoeChargerMapper(TestCase):

    def __helper_get_mapped_key(self, key, value):
        apiResponse = dict(SAMPLE_API_STATUS_RESPONSE)
        apiResponse[key] = value
        return GoeChargerStatusMapper().mapApiStatusResponse(apiResponse)

    def test_map_car(self):
        self.assertEqual("Charger ready, no vehicle", self.__helper_get_mapped_key('car','1').get('car_status'))
        self.assertEqual("charging", self.__helper_get_mapped_key('car','2').get('car_status'))
        self.assertEqual("Waiting for vehicle", self.__helper_get_mapped_key('car','3').get('car_status'))
        self.assertEqual("charging finished, vehicle still connected", self.__helper_get_mapped_key('car','4').get('car_status'))
        self.assertEqual("unknown", self.__helper_get_mapped_key('car','5').get('car_status'))

    def test_map_max_current(self):
        self.assertEqual(10, self.__helper_get_mapped_key('amp', 10).get('charger_max_current'))

    def test_map_absolute_max_current(self):
        self.assertEqual(31, self.__helper_get_mapped_key('ama', 31).get('charger_absolute_max_current'))

    def test_map_charger_err(self):
        self.assertEqual("RCCB", self.__helper_get_mapped_key('err','1').get('charger_err'))
        self.assertEqual("PHASE", self.__helper_get_mapped_key('err','3').get('charger_err'))
        self.assertEqual("NO_GROUND", self.__helper_get_mapped_key('err','8').get('charger_err'))
        self.assertEqual("INTERNAL", self.__helper_get_mapped_key('err','10').get('charger_err'))
        self.assertEqual("OK", self.__helper_get_mapped_key('err','0').get('charger_err'))
        self.assertEqual("UNKNOWN", self.__helper_get_mapped_key('err','12').get('charger_err'))

    def test_map_access(self):
        self.assertEqual("free", self.__helper_get_mapped_key('ast','0').get('charger_access'))
        self.assertEqual("rfid/app", self.__helper_get_mapped_key('ast','1').get('charger_access'))
        self.assertEqual("cost based / automatic", self.__helper_get_mapped_key('ast','2').get('charger_access'))

    def test_map_allow_charging(self):
        self.assertEqual("off", self.__helper_get_mapped_key('alw','0').get('allow_charging'))
        self.assertEqual("on", self.__helper_get_mapped_key('alw','1').get('allow_charging'))

    def test_map_stop_mode(self):
        self.assertEqual("manual", self.__helper_get_mapped_key('stp','0').get('stop_mode'))
        self.assertEqual("kWh based", self.__helper_get_mapped_key('stp','2').get('stop_mode'))
 
    def test_map_cable_max_current(self):
        self.assertEqual(9, self.__helper_get_mapped_key('cbl', 9).get('cable_max_current'))

    def test_map_pre_contactor_l1(self):
        self.assertEqual('on', self.__helper_get_mapped_key('pha', 0x20).get('pre_contactor_l1'))
        self.assertEqual('off', self.__helper_get_mapped_key('pha', 0x00).get('pre_contactor_l1'))

    def test_map_pre_contactor_l2(self):
        self.assertEqual('on', self.__helper_get_mapped_key('pha', 0x10).get('pre_contactor_l2'))
        self.assertEqual('off', self.__helper_get_mapped_key('pha', 0x00).get('pre_contactor_l2'))

    def test_map_pre_contactor_l3(self):
        self.assertEqual('on', self.__helper_get_mapped_key('pha', 0x08).get('pre_contactor_l3'))
        self.assertEqual('off', self.__helper_get_mapped_key('pha', 0x00).get('pre_contactor_l3'))

    def test_map_post_contactor_l1(self):
        self.assertEqual('on', self.__helper_get_mapped_key('pha', 0x04).get('post_contactor_l1'))
        self.assertEqual('off', self.__helper_get_mapped_key('pha', 0x00).get('post_contactor_l1'))

    def test_map_post_contactor_l2(self):
        self.assertEqual('on', self.__helper_get_mapped_key('pha', 0x02).get('post_contactor_l2'))
        self.assertEqual('off', self.__helper_get_mapped_key('pha', 0x00).get('post_contactor_l2'))

    def test_map_post_contactor_l3(self):
        self.assertEqual('on', self.__helper_get_mapped_key('pha', 0x01).get('post_contactor_l3'))
        self.assertEqual('off', self.__helper_get_mapped_key('pha', 0x00).get('post_contactor_l3'))

    def test_map_charger_temp(self):
        self.assertEqual(3, self.__helper_get_mapped_key('tmp', 3).get('charger_temp'))

    def test_map_current_session_charged_energy(self):
        self.assertEqual(1, self.__helper_get_mapped_key('dws', 360000).get('current_session_charged_energy'))

    def test_map_charge_limit(self):
        self.assertEqual(1, self.__helper_get_mapped_key('dwo', 10).get('charge_limit'))

    def test_map_adapter(self):
        self.assertEqual('No Adapter', self.__helper_get_mapped_key('adi', '0').get('adapter'))
        self.assertEqual('16A-Adapter', self.__helper_get_mapped_key('adi', '1').get('adapter'))

    def test_map_unlocked_by_card(self):
        self.assertEqual(2, self.__helper_get_mapped_key('uby', '2').get('unlocked_by_card'))

    def test_map_energy_total(self):
        self.assertEqual(42, self.__helper_get_mapped_key('eto', 420).get('energy_total'))

    def test_map_wifi(self):
        self.assertEqual('connected', self.__helper_get_mapped_key('wst', '3').get('wifi'))
        self.assertEqual('not connected', self.__helper_get_mapped_key('wst', '0').get('wifi'))

    def test_map_firmware(self):
        self.assertEqual('33', self.__helper_get_mapped_key('fwv', '33').get('firmware'))

    def test_map_serial(self):
        self.assertEqual('123456', self.__helper_get_mapped_key('sse', '123456').get('serial_number'))

    def test_map_wifi_ssid(self):
        self.assertEqual('ssid', self.__helper_get_mapped_key('wss', 'ssid').get('wifi_ssid'))

    def test_map_wifi_enabled(self):
        self.assertEqual('off', self.__helper_get_mapped_key('wen', '0').get('wifi_enabled'))
        self.assertEqual('on', self.__helper_get_mapped_key('wen', '1').get('wifi_enabled'))

    def test_map_timezone_offset(self):
        self.assertEqual(100, self.__helper_get_mapped_key('tof', '200').get('timezone_offset'))

    def test_map_timezone_dst_offset(self):
        self.assertEqual(200, self.__helper_get_mapped_key('tds', '200').get('timezone_dst_offset'))

    def test_map_meter_values(self):
        self.assertEqual(1, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('u_l1'))
        self.assertEqual(2, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('u_l2'))
        self.assertEqual(3, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('u_l3'))
        self.assertEqual(4, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('u_n'))
        self.assertEqual(0.5, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('i_l1'))
        self.assertEqual(0.6, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('i_l2'))
        self.assertEqual(0.7, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('i_l3'))
        self.assertEqual(0.8, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('p_l1'))
        self.assertEqual(0.9, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('p_l2'))
        self.assertEqual(1.0, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('p_l3'))
        self.assertEqual(1.1, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('p_n'))
        self.assertEqual(0.12, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('p_all'))
        self.assertEqual(13, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('lf_l1'))
        self.assertEqual(14, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('lf_l2'))
        self.assertEqual(15, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('lf_l3'))
        self.assertEqual(16, GoeChargerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('lf_n'))

    