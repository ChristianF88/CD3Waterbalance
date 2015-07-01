# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:46:53 2015

@author: Gerhard
"""

from Global_meaning_list import Global_meaning_list

def Purpose_Finder_Collectors(word):
    for i in range(len(Global_meaning_list.collectors)):
        if word in Global_meaning_list.collectors[i]:
            print Global_meaning_list.collectors[i][1]
        else:
            pass
            

Purpose_Finder_Collectors('Collector_116')

