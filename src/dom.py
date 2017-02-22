#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dom.py
#  
#  Copyright 2017 Andrei Tumbar <atuser@Kronos>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


# JSON.parse(JSON.stringify(a), function(key, value){ if (/[0-9]+/.test(key)) return undefined; else return value; })     <-- For future reference of CSS styling

class Document ( object ):
    def __init__ (self, doc_root):
        self.node = doc_root['node']
        
        # Self the root document memory point
        self.alloc = '0x0'
        self.mem = '0x0'
        
        self.raw = doc_root
        
        self.children = {} # Map allocation point to dom object (only toplevel objects)
        self.DOM = {} # Same as above but will map all objects
        
        for child in doc_root['child']:
            mem = self.dom_alloc ()
            self.children[mem] = DOM (mem, self, self.mem, child)
            self.DOM [mem] = self.children[mem]
    
    def dom_alloc (self):
        self.alloc = hex(int(self.alloc, 16) + 1)
        return self.alloc
    
    def add_child (self, mem, s):
        self.DOM[mem] = s

class DOM ( object ):
    
    def __init__ (self, mem, root, parent, obj):
        self.node = obj['node'] # Type of DOM object: element, comment, root, or text
        try:
            self.child = obj['child']
        except KeyError:
            self.child = []
        try:
            self.attr = obj['attr']
        except KeyError:
            self.attr = None
        
        if self.node == "element":
            self.tag = obj['tag']
        self.parent = parent
        self.mem = mem
        self.children = {}
        self.root = root
        self.root.add_child (self.mem, self)
        self.gen_children ()
    
    def gen_children (self):
        for i in self.child:
            mem = self.root.dom_alloc ()
            self.children[mem] = DOM (mem, self.root, self.mem, i)
            self.root.DOM [mem] = self.children[mem]
