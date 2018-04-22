#!/usr/bin/python
# -*- coding: utf-8 -*-


import urllib.request
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True
            
    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                line = "Title: " + self.theContent + "."
                file.write('<li>' + str(line) + '</li>' + '\n') 
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                file.write('<li><a href =' + self.theContent + '>' + str(self.theContent) + '</a></li>') 
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog

# Load parser and driver

file = open('barrapunto.html','w')
#La solución de los caracteres especiales la saque de aquí:
#https://www.gestiweb.com/?q=content/problemas-html-acentos-y-e%C3%B1es-charset-utf-8-iso-8859-1
opening_lines = '<!DOCTYPE html>' + '\n' + '<html>' + '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />' + '\n'
opening_lines  += '<head>' + '\n' + '<title>/.Titulares</title>' + '\n' + '</head>' + '\n'
opening_lines +=  '<h1>Titulares de Barrapunto: </h1>' + '\n'
opening_lines  += '<body>' + '\n' + '<ul>'
file.write(opening_lines)

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

xmlFile = urllib.request.urlopen('http://barrapunto.com/index.rss')
theParser.parse(xmlFile)

closing_lines = '</ul>'+ '\n'+ '</body>' + '\n' + '</html>'+ '\n'
file.write(closing_lines)
print ("Parse complete")
print("HTML file created")
