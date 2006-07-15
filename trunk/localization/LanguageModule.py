
"""
Translation credits:

English: Lemon Team
Dutch: Martijn Venrooy (martijn@active8.nl) - Agreed
Spanish: Gabriela Rodriguez (gabelula@gmail.com) - Agreed
French: Olivier (olisker@gmail.com) - Invited
German: Nicole Simon (nisiatyahoo@gnak.de) - Agreed
Brazilian: Helio Chissini de Castro (heliocastro@gmail.com) - Agreed
Japans: tomoya kawanishi (tomoppi@users.sourceforge.net) - Agreed

"""

import os, sys
from xml.sax import make_parser, handler

languages_present = []
ENGLISH = 'en'

#Old codes.
DEPRECATED_DUTCH=360
DEPRECATED_ENGLISH=129
DEPRECATED_FRENCH=157
DEPRECATED_GERMAN=113
DEPRECATED_ITALIAN=232
DEPRECATED_SPANISH=135
DEPRECATED_BRAZILIAN_PORTUGUESE=190
DEPRECATED_JAPANESE=111

def get_default(deflang):
    """Set to English or translate deprecated numeric codes to
    RFC 1766 alpha codes"""
    if deflang:
        if deflang == DEPRECATED_DUTCH:
            return 'nl'
        elif deflang == DEPRECATED_ENGLISH:
            return 'en'
        elif deflang == DEPRECATED_FRENCH:
            return 'fr'
        elif deflang == DEPRECATED_GERMAN:
            return 'de'
        elif deflang == DEPRECATED_ITALIAN:
            return 'it'
        elif deflang == DEPRECATED_SPANISH:
            return 'es'
        elif deflang == DEPRECATED_BRAZILIAN_PORTUGUESE:
            return 'pt-BR'
        elif deflang == DEPRECATED_JAPANESE:
            return 'ja'

    from gui.skin import SCREEN_LANGUAGE
    return SCREEN_LANGUAGE
    
def supported_languages():
    """Use RFC 1766 alpha codes (http://www.faqs.org/rfcs/rfc1766.html).
    Place translations in the catalogs directory, in files named after the
    alpha codes, e.g. en.py for English and pt-BR.py for Brazilian Portuguese.
    """

    if not languages_present:
        base = os.path.abspath(os.path.split(sys.argv[0])[0])
        for f in os.listdir(os.path.join(base,"localization","catalog")):
            if not f.startswith("__") and f.endswith(".py"):
                languages_present.append(f.split('.')[0])

    return languages_present

class StringTable:
    class __impl:
        def __init__(self, language):   
            self.m_languages = supported_languages()
            self.m_string_table = {}
            for l in self.m_languages:
                self.m_string_table[l]={}            
            self.LoadLanguage(language)
            
        def LoadLanguage(self, language):
            base = os.path.abspath(os.path.split(sys.argv[0])[0])
            catalog = os.path.join(base,'localization','catalog')
            if not sys.path.count(catalog):
                sys.path.append(catalog)
            translations = __import__("%s" % language, globals(), locals(), [''])
            translations.AddStrings(self)
               
        def AddText(self, language, label, text):
            if (self.m_string_table[language].has_key(label)):
                # label exsists hence ignored."
                pass
            else:
                self.m_string_table[language][label]=text
            
        def GetText(self, language, label, args=None):
            if self.m_string_table[language].has_key(label):
                if args:
                    return self.m_string_table[language][label] % args
                else:
                    return self.m_string_table[language][label]
            else:               
                # can't find the label defaulting to English
                if not self.m_string_table['en'].has_key(label):
                    self.LoadLanguage('en')
                if self.m_string_table['en'].has_key(label):
                    if args:
                        return self.m_string_table['en'][label] % args
                    else:
                        return self.m_string_table['en'][label]
                else:
                    # still can't find it
                    return label
                
        def GetLanguages(self):
            return self.m_languages 

    __instance = None

    def __init__(self, language):
        if StringTable.__instance is None:
            StringTable.__instance = StringTable.__impl(language)
        self.__dict__['_StringTable__instance'] = StringTable.__instance
                
    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)

class XRCEventHandler(handler.ContentHandler):
    def __init__(self):
        self.m_labels = []
        self.m_xrc = ""
        self.m_label = ""
        self.p_label = False
        
    def startElement(self, name, attrs):
        if name=="label": 
            self.p_label = True
    
    def endElement(self,name):                    
        if name=="label": 
            self.p_label = False
            self.m_labels.append(self.m_label)
            self.m_label = ""
        
    def characters(self,ch):
        if self.p_label:
            self.m_label += ch
        self.m_xrc += ch
                      
def parse_xml_gui():
    import StringIO
    xml_xrc = ""
    xrc = open("./gui/iPodderFeed.xrc", "r")
    for line in xrc:
        xml_xrc += line

    parser = make_parser()
    result = XRCEventHandler()
    parser.setContentHandler(result)
    io_xml_xrc = StringIO.StringIO(xml_xrc)
    parser.parse(io_xml_xrc)
        
    str_table = StringTable();
    
    for language in str_table.m_languages:
        for text in result.m_labels:
            print "s1.AddText(" + language + ", \"str_" + text.lower() + "\", \"" +  text + "\")";
     
def unittest():
    print "unit test"
    strt = StringTable()
    print "--------------"
    print strt.GetText(ENGLISH, "str_license_gpl")
    print "--------------"
    print strt.GetText(DUTCH, "str_license_gpl")
    print "--------------"
    print strt.GetText(FRENCH, "str_license_gpl")
    print "--------------"
    print strt.GetText(GERMAN, "str_license_gpl")
    print "--------------"
    print strt.GetText(ITALIAN, "str_license_gpl")
    print "--------------"
    print strt.GetText(SPANISH, "str_license_gpl")
    print "--------------"
    print strt.GetText(BRAZILIANPORTUGUESE, "str_license_gpl")
       
if __name__ == '__main__':
    unittest();
