#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 13:09:51 2018

@author: 3415104
"""

class Adventurer():
    def __init__(self):
        self.objects = []
        self.case = None
    
    def goIn(self, case):
        self.case = case