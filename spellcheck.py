import language_tool_python


class SpellChecker:
    def __init__(self, lang="nl"):
        self.tool = language_tool_python.LanguageTool(lang)
        

    def check(self,text):
        return self.tool.check(text)
    
    def suggestions_for(self, word):
        matches = self.tool.check(word)
        if matches:
            return matches[0].replacements
        return []    
    
