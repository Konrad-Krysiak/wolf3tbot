import sys
import re

if (sys.version_info[0] < 3):
    import urllib2
    import urllib
else:
    import urllib.request
    import urllib.parse

agent = {'User-Agent':
    "Mozilla/4.0 (\
    compatible;\
    MSIE 6.0;\
    Windows NT 5.1;\
    SV1;\
    .NET CLR 1.1.4322;\
    .NET CLR 2.0.50727;\
    .NET CLR 3.0.04506.30\
    )"}
class Translate:
    def call(self, to_translate):
        try:
            TranslationLanguage = re.search(r"\[(.*)\]\s.*", to_translate).group(1)
        except:
            TranslationLanguage = 'en'
        translation = self.translate(to_translate, TranslationLanguage)
        return "^1Translation: ^7{}".format(translation)

    def translate(self, to_translate, to_language="auto", from_language="auto"):
        """Returns the translation using google translate
        you must shortcut the language you define
        (French = fr, English = en, Spanish = es, etc...)
        if not defined it will detect it or use english by default

        Example:
        print(translate("salut tu vas bien?", "en"))
        hello you alright?
        """
        base_link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s"
        if (sys.version_info[0] < 3):
            to_translate = urllib.quote_plus(to_translate)
            link = base_link % (to_language, from_language, to_translate)
            request = urllib2.Request(link, headers=agent)
            page = urllib2.urlopen(request).read()
        else:
            to_translate = urllib.parse.quote(to_translate)
            link = base_link % (to_language, from_language, to_translate)
            request = urllib.request.Request(link, headers=agent)
            page = urllib.request.urlopen(request).read().decode("utf-8")
        expr = r'class="t0">(.*?)<'
        result = re.findall(expr, page)
        result = ' '.join(result)
        if (len(result) == 0):
            return ("")
        result = re.sub(r"\[.*\]\s", "", result)
        return(result)
