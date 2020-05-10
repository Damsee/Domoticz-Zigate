#!/usr/bin/env python3
# coding: utf-8 -*-
#
# Author: pipiche38
#
"""
    Module: legrand_netamo.py

    Description: All communications towards Zigate

"""

import Domoticz
import binascii
import struct
import json

from datetime import datetime
from time import time

from Modules.zigateConsts import MAX_LOAD_ZIGATE, ZIGATE_EP, LEGRAND_REMOTES
from Modules.pollControl import FastPollStop, PollControlCheckin
from Modules.logging import loggingLegrand
from Modules.output import raw_APS_request, write_attribute, write_attributeNoResponse
from Modules.zigateConsts import MAX_LOAD_ZIGATE, ZIGATE_EP, HEARTBEAT
from Modules.logging import loggingLegrand
from Modules.output import raw_APS_request, write_attribute, sendZigateCmd, raw_APS_request

def pollingLegrand( self, key ):

    """
    This fonction is call if enabled to perform any Manufacturer specific polling action
    The frequency is defined in the pollingSchneider parameter (in number of seconds)
    """
    return False


def callbackDeviceAwake_Legrand(self, NwkId, EndPoint, cluster):

    """
    This is fonction is call when receiving a message from a Manufacturer battery based device.
    The function is called after processing the readCluster part
    """

    #Domoticz.Log("callbackDeviceAwake_Legrand - Nwkid: %s, EndPoint: %s cluster: %s" \
    #        %(NwkId, EndPoint, cluster))

    return

def legrand_fake_read_attribute_response( self, nwkid ):

    cluster_frame = '11'
    sqn = '00'
    if (
        'SQN' in self.ListOfDevices[nwkid]
        and self.ListOfDevices[nwkid]['SQN'] != {}
        and self.ListOfDevices[nwkid]['SQN'] != ''
    ):
        sqn = '%02x' %(int(self.ListOfDevices[nwkid]['SQN'],16) + 1)
    payload = cluster_frame + sqn + '0100F0002311000000'
    raw_APS_request( self, nwkid, '01', '0000', '0104', payload)
    loggingLegrand( self, 'Debug', "legrand_fake_read_attribute_response nwkid: %s" %nwkid, nwkid)


def legrandReadRawAPS(self, Devices, srcNWKID, srcEp, ClusterID, dstNWKID, dstEP, MsgPayload):

    Domoticz.Log("legrandReadRawAPS - Nwkid: %s Ep: %s, Cluster: %s, dstNwkid: %s, dstEp: %s, Payload: %s" \
            %(srcNWKID, srcEp, ClusterID, dstNWKID, dstEP, MsgPayload))

    # At Device Annoucement 0x00 and 0x05 are sent by device

    FrameClusterField = MsgPayload[0:2]

    if FrameClusterField in ( '15', ): 
        # 0x15: Cluster Specifc, Manuf Code, Client to Srerve, Disable Default Response
        ManufacturerCode = MsgPayload[2:6]
        SQN = MsgPayload[6:8]
        Command = MsgPayload[8:10]
        Data = MsgPayload[10:]
        
    elif FrameClusterField in ( '11', ) :
        # 0x11: Cluster Specific, Client to Server, Disable Default response
        SQN = MsgPayload[2:4]
        Command = MsgPayload[4:6]
        Data = MsgPayload[6:]

    else:
        Domoticz.Log("legrandReadRawAPS - Unexpected FCF: %s" %(FrameClusterField))
        return

    if Command == '00': # No data (Cluster 0x0102)
        pass

    elif Command == '01': # No data (Cluster 0x0102)
        pass

    elif Command == '02': # 1 Byte lenght ( 0x00 )
        pass

    elif Command == '03': # 1 byte Lenght ( 0xff )
        pass

    elif Command == '09':
        _ieee = Data[0:16]
        _count = Data[16:18]
        Domoticz.Log("---> Decoding cmd 0x09 Ieee: %s Count: %s" %(_ieee, _count))
        LegrandGroupMemberShip = 'fefe'
        sendFC01Command( self, srcNWKID, srcEp, '0c', LegrandGroupMemberShip + _count)

    elif Command == '0a': 
        LegrandGroupMemberShip = Data[0:4]
        _ieee = Data[4:20]
        _code = Data[20:24]
        Domoticz.Log("---> Decoding cmd: 0x0a Group: %s, Ieee: %s Code: %s" %(LegrandGroupMemberShip, _ieee, _code))
        status = '00'
        #_ieee = '%08X' %struct.unpack('q',struct.pack('>Q',int(ieee,16)))[0]
        _ieee = '4fa5820000740400' # IEEE du Dimmer
        sendFC01Command( self, srcNWKID, srcEp, '10', status + _code + _ieee )


def sendFC01Command( self, nwkid, ep, cmd, data):
    fcf = MsgPayload[0:2] # uint8
    sqn = MsgPayload[2:4] # uint8
    cmd = MsgPayload[4:6] # uint8
    data = MsgPayload[6:] # all the rest

    if cmd == '00':
        # Read Attribute received
        attribute = data[2:4] + data[0:2]

        if ClusterID == '0000' and attribute == 'f000':
            # Respond to Time Of Operation
            cmd = "01"
            sqn = '%02x' %(int(sqn,16) + 1)
            status = "00"
            cluster_frame = "1c"           
            dataType = '23' #Uint32
            PluginTimeOfOperation = '%08X' %(self.HeartbeatCount * HEARTBEAT) # Time since the plugin started

            payload = cluster_frame + sqn + cmd + attribute + status + dataType + PluginTimeOfOperation[6:8] + PluginTimeOfOperation[4:6] + PluginTimeOfOperation[0:2] + PluginTimeOfOperation[2:4]
            raw_APS_request( self, srcNWKID, srcEp, ClusterID, '0104', payload, zigate_ep=ZIGATE_EP)

            loggingLegrand( self, 'Log', "loggingLegrand - Nwkid: %s/%s Cluster: %s, Command: %s Payload: %s" \
                %(srcNWKID,srcEp , ClusterID, cmd, data ))


def rejoin_legrand( self, nwkid):

    if nwkid not in self.ListOfDevices:
        Domoticz.Error("sendFC01Command - nwkid: %s do not exist" %nwkid)
        return

    manuf = '1021'
    manuf_id = '%04X' %(struct.unpack('h',struct.pack('>H',int(manuf,16)))[0])
    cluster_id = 'fc01'

    EPout = '01'
    for tmpEp in self.ListOfDevices[nwkid]['Ep']:
        if "fc01" in self.ListOfDevices[nwkid]['Ep'][tmpEp]:
            EPout= tmpEp

    cluster_frame = '1d' # Cluster Spec, Manuf Spec, Sever to Client, Disable Default Response
    sqn = '00'
    if 'SQN' in self.ListOfDevices[nwkid]:
        if self.ListOfDevices[nwkid]['SQN'] != {} and self.ListOfDevices[nwkid]['SQN'] != '':
            sqn = '%02x' %(int(self.ListOfDevices[nwkid]['SQN'],16) + 1)

    payload = cluster_frame + manuf_id + sqn + cmd + data
    raw_APS_request( self, nwkid, ep, 'fc01', '0104', payload, radius= 0x20)
    Domoticz.Log("send 0xFC01 command 0x%s for %s/%s with payload: %s" %(cmd, nwkid, ep, data))


def registrationLegrand( self, nwkid):

    # FCF: 0x40
    # dstEp: 01
    # Cluster: 0xfc01
    # Command: 0x0e
    # Data: 01

    if nwkid not in self.ListOfDevices:
        Domoticz.Error("registrationLegrand - unknown device %s" %nwkid)
        return

    if 'Model' not in self.ListOfDevices:
        Domoticz.Error("registrationLegrand - device without a Model Name %s" %nwkid)
        return

    if self.ListOfDevices['Model'] in LEGRAND_REMOTES:
        Domoticz.Log("registrationLegrand - Poll Control Management")
        PollControlCheckin(self, nwkid)
        FastPollStop(self, nwkid)


def rejoin_legrand_mainpower( self, nwkid):

    """
    Send a Write Attributes no responses
    """

    Domoticz.Log("Detected Legrand IEEE, broadcast Write Attribute 0x0000/0xf000")
    write_attributeNoResponse( self, 'ffff', ZIGATE_EP, '01', '0000', '1021', '01', 'f000', '23', '00000000')
    if (
        'SQN' in self.ListOfDevices[nwkid]
        and self.ListOfDevices[nwkid]['SQN'] != {}
        and self.ListOfDevices[nwkid]['SQN'] != ''
    ):
        sqn = '%02x' %(int(self.ListOfDevices[nwkid]['SQN'],16) + 1)
    payload = cluster_frame + sqn + '0500f02300000000'
    raw_APS_request( self, 'ffff', '01', '0000', '0104', payload)


def legrand_fc01( self, nwkid, command, OnOff):

            # EnableLedInDark -> enable to detect the device in dark 
            # EnableDimmer -> enable/disable dimmer
            # EnableLedIfOn -> enable Led with device On

    loggingLegrand( self, 'Debug', "legrand_fc01 Nwkid: %s Cmd: %s OnOff: %s " %(nwkid, command, OnOff), nwkid)

    LEGRAND_REFRESH_TIME = ( 3 * 3600) + 15
    LEGRAND_CLUSTER_FC01 = {
            'Dimmer switch wo neutral':  { 'EnableLedInDark': '0001'  , 'EnableDimmer': '0000'   , 'EnableLedIfOn': '0002' },
            'Connected outlet': { 'EnableLedIfOn': '0002' },
            'Mobile outlet': { 'EnableLedIfOn': '0002' },
            'Shutter switch with neutral': { 'EnableLedShutter': '0001' },
            'Micromodule switch': { 'None': 'None' },
            'Cable outlet': { 'LegrandFilPilote': '0000' } }

    LEGRAND_COMMAND_NAME = ( 'LegrandFilPilote', 'EnableLedInDark', 'EnableDimmer', 'EnableLedIfOn', 'EnableLedShutter')

    if nwkid not in self.ListOfDevices:
        return

    if command not in LEGRAND_COMMAND_NAME:
        Domoticz.Error("Unknown Legrand command %s" %command)
        return

    if 'Model' not in self.ListOfDevices[nwkid]:
        return

    if self.ListOfDevices[nwkid]['Model'] == {} or self.ListOfDevices[nwkid]['Model'] == '':
        return

    if self.ListOfDevices[nwkid]['Model'] not in LEGRAND_CLUSTER_FC01:
        loggingLegrand( self, 'Error', "%s is not an Legrand known model: %s" %( nwkid, self.ListOfDevices[nwkid]['Model']), nwkid)
        return

    if 'Legrand' not in self.ListOfDevices[nwkid]:
        self.ListOfDevices[nwkid]['Legrand'] = {}

    for cmd in LEGRAND_COMMAND_NAME:
        if cmd not in self.ListOfDevices[nwkid]['Legrand']:
            self.ListOfDevices[nwkid]['Legrand'][ cmd ] = 0

    if command == 'EnableLedInDark' and command in LEGRAND_CLUSTER_FC01[ self.ListOfDevices[nwkid]['Model'] ]:
        if time() < self.ListOfDevices[nwkid]['Legrand']['EnableLedInDark'] + LEGRAND_REFRESH_TIME:
            return
        self.ListOfDevices[nwkid]['Legrand']['EnableLedInDark'] = int(time())
        data_type = "10" # Bool
        if OnOff == 'On': 
            Hdata = '01' # Enable Led in Dark
        elif OnOff == 'Off': 
            Hdata = '00' # Disable led in dark
        else: Hdata = '00'
        loggingLegrand( self, 'Debug', "--------> %s  Nwkid: %s  data_type: %s Hdata: %s " %( command, nwkid, data_type, Hdata), nwkid)
        
    elif command == 'EnableLedShutter' and command in LEGRAND_CLUSTER_FC01[ self.ListOfDevices[nwkid]['Model'] ]:
        if time() < self.ListOfDevices[nwkid]['Legrand']['EnableLedShutter'] + LEGRAND_REFRESH_TIME:
            return
        self.ListOfDevices[nwkid]['Legrand']['EnableLedShutter'] = int(time())
        data_type = "10" # Bool
        if OnOff == 'On': 
            Hdata = '01' # Enable Led in Dark
        elif OnOff == 'Off': 
            Hdata = '00' # Disable led in dark
        else: Hdata = '00'
        loggingLegrand( self, 'Debug', "--------> %s  Nwkid: %s  data_type: %s Hdata: %s " %( command, nwkid, data_type, Hdata), nwkid)
        
    elif command == 'EnableDimmer' and command in LEGRAND_CLUSTER_FC01[ self.ListOfDevices[nwkid]['Model'] ]:
        if time() < self.ListOfDevices[nwkid]['Legrand']['EnableDimmer'] + LEGRAND_REFRESH_TIME:
            return
        self.ListOfDevices[nwkid]['Legrand']['EnableDimmer'] = int(time())
        data_type = "09" #16-bit Data
        if OnOff == 'On': 
            Hdata = '0101' # Enable Dimmer
        elif OnOff == 'Off': 
            Hdata = '0100' # Disable Dimmer
        else: Hdata = '0000'
        loggingLegrand( self, 'Debug', "--------> %s  Nwkid: %s  data_type: %s Hdata: %s " %( command, nwkid, data_type, Hdata), nwkid)

    elif command == 'LegrandFilPilote' and command in LEGRAND_CLUSTER_FC01[ self.ListOfDevices[nwkid]['Model'] ]:
        if time() < self.ListOfDevices[nwkid]['Legrand']['LegrandFilPilote'] + LEGRAND_REFRESH_TIME:
            return
        self.ListOfDevices[nwkid]['Legrand']['LegrandFilPilote'] = int(time())
        data_type = "09" #  16-bit Data
        if OnOff == 'On': 
            Hdata = '0001' # Enable 
        elif OnOff == 'Off': 
            Hdata = '0002' # Disable
        else: Hdata = '0000'
        loggingLegrand( self, 'Debug', "--------> %s  Nwkid: %s  data_type: %s Hdata: %s " %( command, nwkid, data_type, Hdata), nwkid)

    elif command == 'EnableLedIfOn' and command in LEGRAND_CLUSTER_FC01[ self.ListOfDevices[nwkid]['Model'] ]:
        if time() < self.ListOfDevices[nwkid]['Legrand']['EnableLedIfOn'] + LEGRAND_REFRESH_TIME:
            return
        self.ListOfDevices[nwkid]['Legrand']['EnableLedIfOn'] = int(time())
        data_type = "10" # Bool
        if OnOff == 'On': 
            Hdata = '01' # Enable Led when On
        elif OnOff == 'Off': 
            Hdata = '00' # Disable led when On 
        else: Hdata = '00'
        loggingLegrand( self, 'Debug', "--------> %s  Nwkid: %s  data_type: %s Hdata: %s " %( command, nwkid, data_type, Hdata), nwkid)
    else:
        return

    Hattribute = LEGRAND_CLUSTER_FC01[ self.ListOfDevices[nwkid]['Model'] ][command]
    manuf_id = "0000"
    manuf_spec = "00"
    cluster_id = "%04x" %0xfc01

    EPout = '01'
    for tmpEp in self.ListOfDevices[nwkid]['Ep']:
        if "fc01" in self.ListOfDevices[nwkid]['Ep'][tmpEp]:
            EPout= tmpEp

    loggingLegrand( self, 'Debug', "legrand %s OnOff - for %s with value %s / cluster: %s, attribute: %s type: %s"
            %(command, nwkid,Hdata,cluster_id,Hattribute,data_type), nwkid=nwkid)
    write_attribute( self, nwkid, "01", EPout, cluster_id, manuf_id, manuf_spec, Hattribute, data_type, Hdata)


def legrand_fc40( self, nwkid, Mode ):
    # With the permission of @Thorgal789 who did the all reverse enginnering of this cluster

    CABLE_OUTLET_MODE = { 
            'Confort': 0x00,
            'Confort -1' : 0x01,
            'Confort -2' : 0x02,
            'Eco': 0x03,
            'Hors-gel' : 0x04,
            'Off': 0x05
            }

    if Mode not in CABLE_OUTLET_MODE:
        return
    Hattribute = '0000'
    data_type = '30' # 8bit Enum
    Hdata = CABLE_OUTLET_MODE[ Mode ]
    manuf_id = "1021" #Legrand Code
    manuf_spec = "01" # Manuf specific flag
    cluster_id = "%04x" %0xfc40

    EPout = '01'
    for tmpEp in self.ListOfDevices[nwkid]['Ep']:
        if "fc40" in self.ListOfDevices[nwkid]['Ep'][tmpEp]:
            EPout= tmpEp

    loggingLegrand( self, 'Debug', "legrand %s Set Fil pilote mode - for %s with value %s / cluster: %s, attribute: %s type: %s"
            %( Mode, nwkid,Hdata,cluster_id,Hattribute,data_type), nwkid=nwkid)
    write_attribute( self, nwkid, "01", EPout, cluster_id, manuf_id, manuf_spec, Hattribute, data_type, Hdata)



def legrand_dimOnOff( self, OnOff):
    '''
    Call from Web
    '''

    loggingLegrand( self, 'Debug', "legrand_dimOnOff %s" %OnOff)
    for NWKID in self.ListOfDevices:
        if (
            'Manufacturer Name' in self.ListOfDevices[NWKID]
            and self.ListOfDevices[NWKID]['Manufacturer Name'] == 'Legrand'
            and 'Model' in self.ListOfDevices[NWKID]
            and self.ListOfDevices[NWKID]['Model'] != {}
            and self.ListOfDevices[NWKID]['Model']
            in ('Dimmer switch wo neutral',)
        ):
            if 'Legrand' in self.ListOfDevices[NWKID]:
                self.ListOfDevices[NWKID]['Legrand']['EnableDimmer'] = 0
            legrand_fc01( self, NWKID, 'EnableDimmer', OnOff)
                        #else:
                        #    Domoticz.Error("legrand_ledOnOff not a matching device, skip it .... %s " %self.ListOfDevices[NWKID]['Model'])

def legrand_ledIfOnOnOff( self, OnOff):
    '''
    Call from Web 
    '''

    loggingLegrand( self, 'Debug', "legrand_ledIfOnOnOff %s" %OnOff)
    for NWKID in self.ListOfDevices:
        if (
            'Manufacturer Name' in self.ListOfDevices[NWKID]
            and self.ListOfDevices[NWKID]['Manufacturer Name'] == 'Legrand'
            and 'Model' in self.ListOfDevices[NWKID]
            and self.ListOfDevices[NWKID]['Model'] != {}
            and self.ListOfDevices[NWKID]['Model']
            in (
                'Connected outlet',
                'Mobile outlet',
                'Dimmer switch wo neutral',
                'Shutter switch with neutral',
                'Micromodule switch',
            )
        ):
            if 'Legrand' in self.ListOfDevices[NWKID]:
                self.ListOfDevices[NWKID]['Legrand']['EnableLedIfOn'] = 0
            legrand_fc01( self, NWKID, 'EnableLedIfOn', OnOff)
                        #else:
                        #    Domoticz.Error("legrand_ledOnOff not a matching device, skip it .... %s " %self.ListOfDevices[NWKID]['Model'])

def legrand_ledShutter( self, OnOff):
    '''
    Call from Web 
    '''
    loggingLegrand( self, 'Debug', "legrand_ledShutter %s" %OnOff)

    for NWKID in self.ListOfDevices:
        if (
            'Manufacturer Name' in self.ListOfDevices[NWKID]
            and self.ListOfDevices[NWKID]['Manufacturer Name'] == 'Legrand'
            and 'Model' in self.ListOfDevices[NWKID]
            and self.ListOfDevices[NWKID]['Model'] != {}
            and self.ListOfDevices[NWKID]['Model']
            in ('Shutter switch with neutral')
        ):
            if 'Legrand' in self.ListOfDevices[NWKID]:
                self.ListOfDevices[NWKID]['Legrand']['EnableLedShutter'] = 0
            legrand_fc01( self, NWKID, 'EnableLedShutter', OnOff)
                        #else:
                        #    Domoticz.Error("legrand_ledInDark not a matching device, skip it .... %s " %self.ListOfDevices[NWKID]['Model'])



def legrand_ledInDark( self, OnOff):
    '''
    Call from Web 
    '''

    loggingLegrand( self, 'Debug', "legrand_ledInDark %s" %OnOff)
    for NWKID in self.ListOfDevices:
        if (
            'Manufacturer Name' in self.ListOfDevices[NWKID]
            and self.ListOfDevices[NWKID]['Manufacturer Name'] == 'Legrand'
            and 'Model' in self.ListOfDevices[NWKID]
            and self.ListOfDevices[NWKID]['Model'] != {}
            and self.ListOfDevices[NWKID]['Model']
            in (
                'Connected outlet',
                'Mobile outlet',
                'Dimmer switch wo neutral',
                'Shutter switch with neutral',
                'Micromodule switch',
            )
        ):
            if 'Legrand' in self.ListOfDevices[NWKID]:
                self.ListOfDevices[NWKID]['Legrand']['EnableLedInDark'] = 0
            legrand_fc01( self, NWKID, 'EnableLedInDark', OnOff)
                        #else:
                        #    Domoticz.Error("legrand_ledInDark not a matching device, skip it .... %s " %self.ListOfDevices[NWKID]['Model'])



def legrandReenforcement( self, NWKID):

    rescheduleAction = False
    if (
        'Manufacturer Name' in self.ListOfDevices[NWKID]
        and self.ListOfDevices[NWKID]['Manufacturer Name'] == 'Legrand'
    ):
        for cmd in ( 'LegrandFilPilote', 'EnableLedInDark', 'EnableDimmer', 'EnableLedIfOn', 'EnableLedShutter'):
            if not self.busy and len(self.ZigateComm.zigateSendingFIFO) <= MAX_LOAD_ZIGATE:
                if self.pluginconf.pluginConf[ cmd ]:
                    legrand_fc01( self, NWKID, cmd , 'On')
                else:
                    legrand_fc01( self, NWKID, cmd, 'Off')
            else:
                rescheduleAction = True
    return rescheduleAction

def ZigateTimeOfOperation( self):

    # Send a Read Attribute Request to Zigate to get it's Reporting Time of Operation

    loggingLegrand( self, 'Log', "ZigateTimeOfOperation sending a Request to Zigate", '0000')
    datas = "02" + '0000' + '01' + '01' + '0000' + '00' + '00' + '0000' + '01' + 'f000'
    sendZigateCmd(self, "0100", datas )
