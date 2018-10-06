#!/usr/bin/env python3
# coding: utf-8 -*-
#

import Domoticz

import z_var		  # Global variables


def upgrade_v2( self, Devices ) :

	nbdev = 0
	upgradeflag = False

	for x in Devices : # initialise listeofdevices avec les devices en bases domoticz
		upgradeneedflag = False
		
		Domoticz.Debug("Upgrading - oldDevicesOptions = " +str(Devices[x].Name) + " Options = "  + str(Devices[x].Options) )
		newDevicesOptions=dict(Devices[x].Options)

		if Devices[x].Options.get('TypeName') :
			upgradeflag = True
			upgradeneedflag = True
			oldTypeName = newDevicesOptions['TypeName']

			# Remove 'TypeName' and add 'ClusterType'
			del newDevicesOptions['TypeName']
			newDevicesOptions['ClusterType'] = oldTypeName

		if  not Devices[x].Options.get('Zigate') :
			Domoticz.Error("Upgrading no Zigate content found for " +str(Devices[x].Name) )
			continue

		ZigateV2 = eval(newDevicesOptions['Zigate'])
		Domoticz.Debug("Upgrading - oldDevicesOptions['Zigate'] = " +str(Devices[x].Name) + " Zigate = "  + str(ZigateV2) )

		if ZigateV2.get('Version') != "2" :
			Domoticz.Debug("Upgrading to V2 " + str( Devices[x].DeviceID) )
			upgradeflag = True
			upgradeneedflag = True
			ZigateV2['Version'] = "2"
			newDevicesOptions['Zigate'] = ZigateV2

		Domoticz.Debug("Upgrading upgradeflag = " +str(upgradeflag) + " upgradeneeded = " +str(upgradeneedflag) + " ndev = " +str(nbdev) )

		if upgradeneedflag is True:
			nbdev = nbdev + 1
			Domoticz.Debug("Upgrading - newDevicesOptions = " +str(Devices[x].Name) + str(newDevicesOptions) )
			Domoticz.Debug("Upgrading " +str(Devices[x].Name) + " to version 2 with Options['Zigate']= " +str(ZigateV2) )
			nValue = Devices[x].nValue
			sValue = Devices[x].sValue

			Domoticz.Status("Upgrading " +str(Devices[x].Name) + " to version 2" )
			Devices[x].Update(nValue=int(nValue), sValue=str(sValue), Options={}, SuppressTriggers=True )
			Devices[x].Update(nValue=int(nValue), sValue=str(sValue), Options=newDevicesOptions, SuppressTriggers=True )
			Domoticz.Debug("Upgrading - upgraded = " +str(Devices[x].Name) + " Options = "  + str(Devices[x].Options) )
		else:
			Domoticz.Debug("NOT Upgrading " +str(Devices[x].Name) + " Options ="  + str(Devices[x].Options) )

	if upgradeflag is True :
		Domoticz.Log("Upgrade of Zigate structure to V2 completed. " + str(nbdev) + " devices updated")
	else:
		Domoticz.Status("Zigate Structure V2")
			


def upgrade_v3(self, Devices ):
	nbdev = 0
	upgradeflag = False
	for x in Devices : 
		if Devices[x].Options.get('Zigate') is None :
			Domoticz.Error("upgrade_v3 aborted. Zigate structutre not found : " +str(Zigate['Version']) + " for " +str(x) )
			return
		
		# Copy the old Structure in order to Create+Update the new Device
		Zaddr        = Devices[x].DeviceID
		Name         = Devices[x].Name
		Type         = Devices[x].Type
		Subtype      = Devices[x].Subtype
		Switchtype   = Devices[x].Switchtype
		Image        = Devices[x].Image
		Used         = Devices[x].Used
		Color        = Devices[x].Color
		Description  = Devices[x].Description
		BatteryLevel = Devices[x].BatteryLevel
		SignalLevel  = Devices[x].SignalLevel
		TypeName     = Devices[x].TypeName
		nValue       = Devices[x].nValue
		sValue       = Devices[x].sValue

		Options = dict(Devices[x].Options)
		Zigate  = eval(Options['Zigate'])

		if Zigate.get('IEEE') is None :
			Domoticz.Error("upgrade_v3 No IEEE for Device["+str(x)+"] - "+str(Device[x].Name ) + " " +str( Options ) )
			return
		if Zigate['Version'] != "2" :
			Domoticz.Error("upgrade_v3 aborted. found a non V2 version : " +str(Zigate['Version']) )
			return

		IEEE   = Zigate['IEEE']
		DomoID = Zigate['DomoID']

		if Zaddr != DomoID :
			# Mostlikely we had a device coming with a new sAddr, so we should use the latest one.
			Domoticz.Log("upgrade_v3 Zaddr " +Zaddr + " overwritted by " +DomoID )
			Zaddr = DomoID

		# Construct V3 as per construction Zigate is pointing to a Copy of Options
		DeviceID          = IEEE
		Zigate['Version'] = '3'
		Zigate['Zaddr']   = Zaddr
		del Zigate['DomoID']

		Domoticz.Status("Upgrading " +str(Devices[x].Name) + " to version 3" )
		Domoticz.Log("upgrade_v3  " +str(Devices[x].Name) + " to version 3 with DeviceID from '" +str(Zaddr) + "' to '" +str(DeviceID) + "'")

		# Change the Name of the old device
		Domoticz.Log("upgrade_v3 renaming old device into " +'V2 '+Name )
#		#Devices[x].Update(nValue=int(nValue), sValue=str(sValue), Name="V2 "+Name, SuppressTriggers=True )

		# Create a new device
		Domoticz.Log("upgradeèv3 creating new device DeviceID = " + str(DeviceID) + " Options = " +str(Options) )
#		#Domoticz.Device(DeviceID=str(DeviceID),Name=str(Name), Unit=FreeUnit(self, Devices), Type=Type, Subtype=Subtype, Switchtype=Switchtype, Options=Options ).Create()
		# Update the other parameters like Image, battery and Signal level , nValue, sValue ....
		for y in Devices : 
			if Devices[y].DeviceID == IEEE : # Look for the fresh created entry
				Domoticz.Log("upgrade_v3 Updaging new created device ")	
				#Devices[y].Update(nValue=int(nValue), sValue=str(sValue), Image=Image, Used=Used, Color=Color, Description=Description, BatterLevel=BatteryLevel, SignalLevel=SignalLevel, SuppressTriggers=True )

		nbdev = nbdev + 1
		upgradeflag = True

	if upgradeflag :
		Domoticz.Status("Upgrade of Zigate structure to V3 completed. " + str(nbdev) + " devices updated")
		
