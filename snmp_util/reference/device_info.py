import sys
from pysnmp.hlapi import *
import configparser
import getopt
import json
import logging
import os
import re
import sys

# from reference.new_device_info import get
from snmp_util.reference import new_device_info
from pysnmp import hlapi


class device_info:
    def __init__(self, ip_interface = None ,community_string = None):
        self.community_string = community_string
        self.ip_interface = ip_interface
        #Do not alter any of this
        self.cdpCacheDeviceId = '.1.3.6.1.4.1.9.9.23.1.2.1.1.6'
        self.cdpCacheDevicePort = '.1.3.6.1.4.1.9.9.23.1.2.1.1.7'
        self.cdpCachePlatform = '.1.3.6.1.4.1.9.9.23.1.2.1.1.8'
        self.sysname = '.1.3.6.1.2.1.1.5.0'
        self.sysDesc = '.1.3.6.1.2.1.1.1.0'
        # self.sysModel = '1.3.6.1.2.1.1.1.0'

    #option 1 nextcommand
    # def run(self):
    #     is_valid = True
    #     for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
    #         SnmpEngine(),
    #         CommunityData(self.community_string),
    #         UdpTransportTarget((self.ip_interface, 161)),
    #         ContextData(),
    #         ObjectType(ObjectIdentity(self.cdpCacheDeviceId)),
    #         ObjectType(ObjectIdentity(self.cdpCacheDevicePort)),
    #         ObjectType(ObjectIdentity(self.cdpCachePlatform)),
    #         lookupMib=False,
    #         lexicographicMode=False
    #     ):
    #         if errorIndication or errorStatus or errorIndex:
    #             is_valid= False
    #             return None
    #     device_info = {
    #         'system_name': re.findall(r'([^(\n]+).*', str(varBinds[0][1]))[0],
    #         'system_description': str(varBinds[2][1])
    #         }
    #     return {'is_valid': is_valid , 'device_info': device_info }

    def cast(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                try:
                    return str(value)
                except (ValueError, TypeError):
                    pass
        return value

    def construct_object_types(list_of_oids):
        object_types = []
        for oid in list_of_oids:
            object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
        return object_types


    def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
        handler = hlapi.getCmd(
            engine,
            credentials,
            hlapi.UdpTransportTarget((target, port)),
            context,
            *construct_object_types(oids)
        )
        return fetch(handler, 1)[0]


    def fetch(handler, count):
        result = []
        for i in range(count):
            try:
                error_indication, error_status, error_index, var_binds = next(handler)
                if not error_indication and not error_status:
                    # items = {}
                    # for var_bind in var_binds:
                    #     items[str(var_bind[0])] = cast(var_bind[1])
                    result.append(cast(var_bind[1]))

                else:
                    raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
            except StopIteration:
                break
        return result

    def run(self):
        is_valid = True
        device_info = {
                    'system_name':"" ,
                    'system_description': ""
                }
        device_info["system_name"] =  new_device_info.get(self.ip_interface, [self.sysname], hlapi.CommunityData(self.community_string))
        device_info["system_description"] =  new_device_info.get(self.ip_interface, [self.sysDesc], hlapi.CommunityData(self.community_string))
    
        # device_info["system_description"] = "Cisco IOS Software, 3700 Software(C3725-ADVPSERVICESK9-M), Version 12.4(15)T5, RELEASE SOFTWARE (fc4) Technical Support http://www.cisco.com/techsupport Copyright (c) 1986-2008 by Cisco Systems, Inc. Compiled Wed 30-Apr-08 by prod_rel_team"
       
        if device_info["system_name"] == "":
            is_valid=False

        return {'is_valid': is_valid , 'device_info': device_info }




