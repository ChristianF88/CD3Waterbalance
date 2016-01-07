# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:46:53 2015

@author: Gerhard
"""


class Need_to_have_modelinput:
    
    def __init__(self, rainfile, evapofile, sun_zenith, sundown):
         self.rainfile = rainfile
         self.evapofile = evapofile
         self.sun_zenith = sun_zenith
         self.sundown = sundown
         
         self.string1="""           <node id="File_Reader_0" class="File_Reader">
                <parameter name="" type="string" value="""
         self.string2="""/>
            </node>
            <node id="File_Reader_1" class="File_Reader">
                <parameter name="" type="string" value="""
         self.string3="""/>
            </node>
            <node id="Evapotranspirationmodule_0" class="Evapotranspirationmodule">
                <parameter name="Sun_Zenith_[0-23h]" type="double" value="""
         self.string4="""/>
                <parameter name="Sundown_[0-23h]" type="double" value="""
         self.string5="""/>
            </node> \n """
            
         self.Modelinputnodesstring = self.string1 +'"'+ str(self.rainfile) +'"'+ self.string2 +'"'+ str(self.evapofile) +'"'+ self.string3 +'"'+ str(self.sun_zenith) +'"'+ self.string4 +'"'+ str(self.sundown) +'"'+ self.string5
  