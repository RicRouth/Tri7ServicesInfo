#  Copyright (c) GINESYS, Inc. 2023 All rights reserved.

trace=False
traceRuleList = False
factList = [] # [[factLabel, ConclusionExpression, assignedConclusionValue, cf]...]
ruleList = [] # list of rules, i.e. [[ruleLabel, conclusionExpresion, conclusionValue, CF, [[conditionExpression, operator, conditionValue], ...]], nextRule, ...]  NOTE: this is why the list of conditions for a rule is referred to as rule[4]
defaultList = [] #[defaultLabel, ConclusionExpression, assignedConclusionValue, cf]
sessionMemory = []   # cacheList structure: [[goalExpression, conclusionValue, cf, source],…]
expressionList = []  # expressionList = [[expressionString, "type", [list of possible values], "questionString"], ["the color of the rug", "string", ["blue", "yellow", "other"], "What is the color of the rug?"], ["the temperature of the vat", "number", ["any number"], "What is the temperature in the vat? (enter only a number):"], ["the gauge for gasket diameter in centimeters reads less than 15", "boolean", ["Yes", "No"], "Is it true that the guage for gasket diameter in centimeters reads less than 15?"]]  NOTE: expressions in expression list ONLY come from the conditions in RULES, but the expressionValues can come from POSSIBLE-VALUES-FOR statements, (or RULEs, FACTs, and DEFAULTs, if there are no POSSIBLE-VALUES-FOR statements for that expression).

class CommandProcessor:
     def __init__(self):
        dummy=[]
        command = "nothing"

     def getCommand():
          # used to be: command = input(f"\nCOMMAND>> ")
          commandList = ["STOP", "LIST", "SHOW"]
          command = UI.getCommnandFromUser (commandList)
          while command:
            if command == "STOP": exit()
            elif command == "LIST":
               p1 = Fact
               r1 = Rule
               d1 = Default
               p1.showFacts ()
               r1.showRules ()
               d1.showDefaults ()
            elif command == "SHOW":
               print (f"\nHere is dump of the sessionMemory:")
               for entry in sessionMemory:
                    print(f"{entry[0]} = {entry[1]} CF {entry[2]} (got this from {entry[3]})")

               
               
            # used to be: command = input(f"\nCOMMAND>> ")
            command = UI.getCommnandFromUser (commandList)
          
          
c1 = CommandProcessor

class Fact:   
  
     def __init__(self):
          dummy=[]

     def addFact (fact):
	     factList.append(fact)
	    
     def showFacts():
	     for fact in factList:
               print(f"{fact[0]}:\n{fact[1]} = {fact[2]} cf {fact[3]}.\n")

class Rule:   
  
     def __init__(self):
 	    dummy=[]
	 

     def addRule (rule):
	     ruleList.append(rule)
	    
     def showRules():
	     for rule in ruleList:
               print(f"{rule[0]}:")
               listOfConditions = rule[4]
               print(f"IF {listOfConditions[0][0]} {listOfConditions[0][1]} {listOfConditions[0][2]}")
               for condition in listOfConditions[1:len(listOfConditions)]:
                    print(f"AND {condition[0]} {condition[1]} {condition[2]}")
               print(f"THEN {rule[1]} = {rule[2]} CF {rule[3]}.\n")

class Default:   
  
    def __init__(self):
 	    dummy=[]

    def addDefault (default):
	    defaultList.append(default)
	    
    def showDefaults():
	    for default in defaultList:
             print(f"{default[0]}:\n{default[1]} = {default[2]} cf {default[3]}.\n")

class InferenceEngine:
	
    def __init__(self):
 	    dummy=[]
            
    def getType(self, expression):
         for expressionEntry in expressionList:
              if expression == expressionEntry[0]:
                   return expressionEntry[1]
         return "type not found"
	
    def askUser(self, expression):
          for entry in expressionList:
               if entry[0] == expression:
                    if entry[1] == "string":
                        question = entry[3]
                        possibleAnswers = entry[2]
                        possibleAnswers.append("other or unknown")
                        # used to be: return input(f'\n{question}\n   {possibleAnswers}: >> ')
                        return UI.getUserResponseFor (question, possibleAnswers, "string")
                    if entry[1] == "number":
                        question = entry[3]
                        # used to be: return float(input(f'\n{question} >> '))
                        return UI.getUserResponseFor (question, "any number", "number")

                        
                    if entry[1] == "boolean":
                         question = entry[3]
                         # used to be: userAnswer = input(f'\n{question}  [Yes, or No, or Unknown]>> ')
                         userAnswer = UI.getUserResponseFor (question, ["Yes", "No", "Unknown"], "boolean")
                         if userAnswer == "Yes": return True
                         elif userAnswer == "yes": return True
                         elif userAnswer == "True": return True
                         elif userAnswer == "true": return True
                         elif userAnswer == "y": return True
                         elif userAnswer == "Y": return True
                         elif userAnswer == "No": return False
                         elif userAnswer == "no": return False
                         elif userAnswer == "False": return False
                         elif userAnswer == "false": return False
                         elif userAnswer == "N": return False
                         elif userAnswer == "n": return False
                         else: return userAnswer
          print('\nERROR: user did not enter an acceptable answer\n')


               
    
    def testPropValues(self,propValuesString, expressionType):
         if trace: print(f"\nfrom line 96, inside testPropValues and propValuesString is: {propValuesString}\n and expression type is: {expressionType}")
         if expressionType == "string":
              if trace: print(f"from line 98, The value of eval({propValuesString} = {eval(propValuesString)}")
              return eval(propValuesString)  # ?? xxx Where does this happen?
         elif expressionType == "boolean":
              if trace: print(f"from line 101 when epression Type is boolean, The value of eval propValuesString = {propValuesString}")
              return eval(propValuesString)
         elif expressionType == "number":
              if trace: print(f"from line 104 when epression Type is number, The value of eval propValuesString = {propValuesString}")
              removedDoubleQuotes = propValuesString.replace('"', '')
              removedBothTypeQuotes = removedDoubleQuotes.replace("'", "")
              truthValue = eval(removedBothTypeQuotes)
              if trace: print(f'from line 108, The value of the proposition {removedBothTypeQuotes} is: {truthValue}')
              return truthValue
         
         

    def backwardChainToTestProps(self, listOfExpectedGoalsAndValues): # input is a list of expressions, operators, and values [[expression, operator, expectedValue],...] and returns true if all in the input list are true, otherwise it returns false--also, it puts expressions and their values in the cache when it discovers them [expression, value, cf, source]
         conditionTruth = False
         conditionListTruth = False
         for prop in listOfExpectedGoalsAndValues:
              conditionTruth = False
              if trace: print(f"from line 114, from inside backwardChainToTestProps(), prop = {prop}")  # prop is a single prop and not the entire condition list
              for cacheEntry in sessionMemory:
                   if trace: print (f"from line 116, cacheEntry = {cacheEntry}")
                   if prop[0] == cacheEntry[0]:
                        evalString = f'"{cacheEntry[1]}" {prop[1]} "{prop[2]}"'
                        expressionType = self.getType(prop[0])
                        if trace: print(f'from line 119, evalString is: {evalString} AND expressionType is: {expressionType}') 
                        conditionTruth = self.testPropValues(evalString, expressionType)   #  this is working correctly
                        if not conditionTruth:
                             if trace: print(f"line 123 returning False")
                             return False
                        if conditionTruth:
                             if trace: print(f"line 126 returning true")
                             break    # leave this for loop because the condition is true as found in cache
                         
              if conditionTruth == True:
                   if trace: print(f'from line 129, abut to hit the continue statement. Before the continue, prop = {prop} \n     and listOfExpectedGoalsAndValues = {listOfExpectedGoalsAndValues}')
                   continue    
              for fact in factList:
                   if trace: print (f"from line 131, from inside backwardChainToTestProps(), fact = {fact}")
                   if prop[0] == fact[1]:   # yes, there is a fact for this expression
                        evalString = f'"{fact[2]}" {prop[1]} "{prop[2]}"'  # ??xxx
                        sessionMemory.append([prop[0], fact[2], fact[3], fact[0]])
                        
                        UI.outputToSessionMemoryWindow(prop[0], fact[2], fact[3], fact[0])
                        expressionType = self.getType(prop[0])
                        conditionTruth = self.testPropValues(evalString, expressionType)
                        if not conditionTruth:
                             if trace: print(f"line 140 returning False")
                             return False  # chek this for possibly needing to be a contiune statement
                        if conditionTruth:
                             if trace: print(f"line 143 breaking on true")
                             break
              if conditionTruth == True:
                   continue     
              if traceRuleList: print(f'from  line 147, inside backwardChaineToTestProps(), ruleList is: {ruleList}')                 
              for rule in ruleList:
                   if trace: print (f"\nfrom line 149, from inside backwardChainToTestProps(), prop[0] is: {prop[0]}, and rule = {rule}")
                   if prop[0] == rule[1]:
                        if trace: print(f'\nfrom line 151, about to call backwardChainToTestProps() with rule[4] is: {rule[4]}')
                        conditionListTruth = self.backwardChainToTestProps(rule[4])
                        if trace: print(f'from line 153, just returned from backwardChainToTestProps() and conditionListTruth is: {conditionListTruth}')
                        if not conditionListTruth:  
                             if trace: print(f"from line 155 returning False")
                             continue  
                        if conditionListTruth:
                             sessionMemory.append([prop[0], rule[2], rule[3], rule[0]])
                                
                             UI.outputToSessionMemoryWindow(prop[0], rule[2], rule[3], rule[0])
                             if trace: print(f"from line 159, just wrote this into session memory: [{prop[0]}, {rule[2]}, {rule[3]}, {rule[0]}]")
                             if trace: print(f'from line 160, about to break the inner for loop for rules and the next statement should be about doing a continue with outer loop')
                             conditionTruth = True
                             break
              if trace: print(f'from line 163, conditionTruth = {conditionTruth}')                 
              if conditionTruth == True:
                    if trace: print(f'from line 165, about to hit the continue statement which will either continue the outer loop with next prop or return True if input list of conditions has been completed. Before the continue, prop = {prop} \n     and listOfExpectedGoalsAndValues = {listOfExpectedGoalsAndValues}')
                    continue              
              for default in defaultList:
                   if trace: print(f"from line 168, from inside backwardChainToTestProps(), default = {default}")
                   if prop[0] == default[1]:
                        sessionMemory.append([prop[0], {default[2]}, {default[3]}, {default[0]}])
                       
                        UI.outputToSessionMemoryWindow(prop[0], {default[2]}, {default[3]}, {default[0]})
                        evalString = f'"{default[2]}" {prop[1]} "{prop[2]}"'
                        expressionType = self.getType(prop[0])
                        conditionTruth = self.testPropValues(evalString, expressionType)
                        if not conditionTruth:
                             if trace: print(f"line 174, from inside backwardChainToTestProps() in default for loop, returning False")
                             return False
                        if conditionTruth:
                             if trace: print(f'line 178, from inside backwardChainToTestProps() found default so... continuing which will result in  continue the outer loop with next prop or return True if input list of conditions has been completed. Before the continue, prop = {prop} \n     and listOfExpectedGoalsAndValues = {listOfExpectedGoalsAndValues}')
                             break
                   
              if conditionTruth == True:
                    continue    
                        
              valueFromUser = self.askUser (prop[0])
              if trace: print(f'from line 185, just returned from askUser() with {valueFromUser} as the value for the following expression: {prop[0]}')
               # if self.getType(prop[0]) == "number":
               #     valueFromUser = eval(valueFromUser)   # this is successfully converting a string to a number
              sessionMemory.append([prop[0], valueFromUser, 100, "user"])
              
              UI.outputToSessionMemoryWindow (prop[0], valueFromUser, 100, "user")

              evalString = f'"{valueFromUser}" {prop[1]} "{prop[2]}"'
              expressionType = self.getType(prop[0])
              if trace: print(f'from line 190, the expression type for {prop[0]} is {expressionType} ')
              conditionTruth = self.testPropValues(evalString, expressionType)
              if trace: print(f'from line 193, after asking user and calling testPropValues(), it was determined that conditionTruth = {conditionTruth}')
              if not conditionTruth:
                    if trace: print(f"line 195 returning False, because the condition '{prop}' is False")
                    return False
              if conditionTruth:
                    if trace: print(f"line 198, about to hit a continue statement because the condition is True")
                    continue
              
                        
         return True               
                    
                        
                        

    def findValuesFor (self, goalExpression): #returns list of lists [[goalExpression, conclusionValue, cf, source]…]  where values are found for goalExpression
								      
        goalValue = []
        if trace: print(f'from line 210, just entered findValuesFor() with goalExpression is: {goalExpression}')
        for expList in sessionMemory:
            if goalExpression == expList[0]:
                if trace: print(f"from line 213, inside findValuesFor() and returning cache entry: {expList}")
                return [expList]
	    
        for fact in factList:
            if fact[1] == goalExpression: 
                if trace: print(f"from line 218, inside findValuesFor() and returning fact: {fact}")
                return [[fact[1], fact[2], fact[3], fact[0]]]
	    
        for rule in ruleList:
              if trace: print(f"from line 222 inside findValuesFor(), looking at a rule in ruleList: rule = {rule}")
              if trace: print(f'from line 223. inside fndvaluesFor(), goalExpression is {goalExpression}; and rule[1] is: {rule[1]}')
              if goalExpression == rule[1] and self.backwardChainToTestProps(rule[4]):
                sessionMemory.append([goalExpression, rule[2], rule[3], rule[0]])
                
                UI.outputToSessionMemoryWindow (goalExpression, rule[2], rule[3], rule[0])
                if rule[3] == 100:
                    if trace: print(f"fromline 227, inside findValuesFor() and returning rule: {rule}")
                    return [[goalExpression, rule[2], rule[3], rule[0]]]
                else:
                    goalValue.append([goalExpression, rule[2], rule[3], rule[0]])

        if goalValue:
            if trace: print(f"from line 233, inside findValuesFor() last statement and returning goalValue: {goalValue}")
            return goalValue
	    
        for default in defaultList:
              if goalExpression == default[1]:
                    sessionMemory.append([goalExpression, default[2], default[3], default[0]])
                    
                    UI.outputToSessionMemoryWindow(goalExpression, rule[2], rule[3], rule[0])
                    if trace: print(f"from line 239, inside findValuersFor() and returning default: {default}")
                    return [[goalExpression, default[2], default[3], default[0]]]
              
        answer = askUser(goalExpressio)
        sessionMemory.append([goalExpression, {answer}, 100, "got this from user"])
        
        UI.outputToSessionMemoryWindow(goalExpression, {answer}, 100, "user")
        if trace: print(f"from line 244, inside findValuesFor() and returning user answer: {answer}")
        return [[goalExpression, answer, 100, "got this from user"]]
    

class UI:
	
    def __init__(self):
 	    dummy=[]
    
    def outputToSessionMemoryWindow (expression, value, cf, source): # this function reports new Session Memory entries to a scrolling Session Memory window in the Web-based UI. It does not return anything back to the Python Inference Engine program.
        print(f"\n\n Reported for display in Session Memory window in the Web-based UI:\n{expression} = {value} (CF {cf}) -- got this from: {source}.\n\n")


    def outputToAuditWindow (outputString): # this function reports various things, all in the form of quoted strings, to a scrolling Audit window in the Web-based UI. It does not return anything back to the Python Inference Engine program.
        print (f'\n\nFor display in the Audit Window in the Web-based UI: \n {outputString}')

    def getUserResponseFor (question, possibleAnswers, type): # displays the question in the User Query Window in the Web-based UI, along with the possibleAnswers and returns the user's selested answer
        # question is a quoted string;  possibleAnswers is a list of quoted strings; and type is one of these three quoted strings: "boolean", "string", or "number"
        if type == "string":
            return input(f'\n\nFor display in the User Query Window in the Web-based UI:\n {question}\n   {possibleAnswers}: >> ')
        if type == "number":
            return input(f'\n\nFor display in the User Query Window in the Web-based UI:\n {question}\n (Enter a number:) >> ')
        if type == "boolean":
            return input(f'\n\nFor display in the User Query Window in the Web-based UI:\n {question}\n   {["Yes", "No", "Unknown"]}: >> ')
         
    def getCommnandFromUser (commandMenuList): # presents user with a list of commands in a menu-choose and returns the command the user chooses.  NOTE: This causes there to be two different simultaneous processes going: The user session process, and the Command session process.
        # CommandMenuList is a list of commands that need to be displayed in a menu-choose window. An example of what this list might look like is: ["SHOW", "LIST", "STOP", "RESTART", "EXIT", "SAVE SESSION MEMORY", "LOAD SESSION MEMORY", "TRACE"]
        return input (f'For display in a menu-choose in the Command Window in the Web-based UI:\nPlease select from the following menu:\n {commandMenuList}')
    
    def outputToReportWindow (goalExpression, conclusion, cf, rule): # this function reports teh system conclusions(s), which are all in the form of quoted strings (except for the cf which is an number), to a scrolling Report window in the Web-based UI. It does not return anything back to the Python Inference Engine program.
        print (f'\n\nFor display in the Report Window in the Web-based UI:\n The conclusion is:\n{goalExpression} = {conclusion} CF {cf} (from {rule})\n')
    
         

         
         
              
                    
class ExpressionList:   
  
     def __init__(self):
 	    dummy=[]
            
     def isnum(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

     def buildExpressionList(self):  # expressionList = [[expressionString, "type", [list of possible values], "questionString"], ["the color of the rug", "string", ["blue", "yellow", "other"], "What is the color of the rug?"], ["the temperature of the vat", "number", ["any number"], "What is the temperature in the vat? (enter only a number):"], ["the gauge for gasket diameter in centimeters reads less than 15", "boolean", ["Yes", "No"], "Is it true that the guage for gasket diameter in centimeters reads less than 15?"]]  NOTE: expressions in expression list ONLY come from the conditions in RULES, but the expressionValues can come from POSSIBLE-VALUES-FOR statements, (or RULEs, FACTs, and DEFAULTs, if there are no POSSIBLE-VALUES-FOR statements for that expression).
         
          global expressionList
          
          for rule in ruleList:
               for condition in rule[4]:
                    middleForLoopMarker = False
                    # determine if expression is in expressionList
                    if expressionList == []:  # nothing in expressionList, yet.
                         expression = condition[0]
                         expressionType = self.getExpressionType(condition[2])
                         question = self.getQuestion(condition[0],expressionType)
                         if expressionType == "string":
                              newEntry = [expression, expressionType,[condition[2]], question]
                              expressionList == expressionList.append(newEntry)
                              continue
                         elif expressionType == "number":
                              newEntry = [expression, expressionType,["any number"], question]
                              expressionList == expressionList.append(newEntry)
                              continue
                         elif expressionType == "boolean":
                              newEntry = [expression, expressionType, ["Yes", "No"], question]
                              expressionList == expressionList.append(newEntry)
                              continue
                         else: 
                              print(f'Error at line 289: did not match any expresionType which was: {expressionType}')
                              continue
                    if trace: print(f'\n\nfrom line 291, expressionList is:\n{expressionList}\n\n')
                    for entry in expressionList:  # check all entries in the expressionList until you find an entry for the expression, then add the value to the possibleValues list for that entry, then break this for-loop and continue with next outer for-loop to look at next condition in rule[4]
                         expression = condition[0]
                         if entry[0] == expression:
                              if trace: print(f'from line 295, entry is: {entry} and entry[2] is: {entry[2]}, and condition[2] is: {condition[2]}')
                              entry[2].append(condition[2])  # this ends up changing the entry{2] list to be None
                              if trace: print(f'from line 297, entry is: {entry} and entry[2] is: {entry[2]}, and condition[2] is: {condition[2]}')
                              middleForLoopMarker = True
                              break
                    if middleForLoopMarker: continue
                    # if it gets to this point, the condition's expression does not yet exist in the expressionList and it must be added to it.

                    expression = condition[0]
                    if trace: print(f'from line 303, condition[2] is: {condition[2]}')
                    expressionType = self.getExpressionType(condition[2])
                    question = self.getQuestion(condition[0],expressionType)
                    if expressionType == "string":
                         newEntry = [expression, expressionType,[condition[2]], question]
                         expressionList == expressionList.append(newEntry)
                         continue
                    elif expressionType == "number":
                         newEntry = [expression, expressionType,["any number"], question]
                         expressionList == expressionList.append(newEntry)
                         continue
                    elif expressionType == "boolean":
                         newEntry = [expression, expressionType, ["Yes", "No"], question]
                         expressionList == expressionList.append(newEntry)
                         continue
                    else: 
                         print(f'Error at line 319: did not match any expresionType which was: {expressionType}')
                         continue
          
          if trace: print(f'\n\nfrom line 323, starting elimination of duplicate possible answers. expressionList is: \n{expressionList}\n\n')
          for entry in expressionList:
               entry[2] = self.removeDuplicates(entry[2])
          if trace: print(f'from line 326, after removing duplicates, expressionList is: \n{expressionList}\n\n')

          # here we iterate through customQuestionList and possibleAnswersList lists to add the entries from these lists to the expressionList
          for entry in customQuestionList:  # list of lists of customQuestion entries: [[expression, customQuestionString], ["the color of the rug", "What is the color of the rug"], ...]
               for item in expressionList:
                    if item[0] == entry[0]:
                         item[3] = entry[1]
                         break
          for entry in possibleAnswersList:  # list of lists of possibleAnswers entries: [[expression, [possibleAnswers in a list]], ["the color of the rug", ["blue", "yellow", "green"]], ...]
               for item in expressionList:
                    if item[0] == entry[0]:
                         item[2] = entry[1]
                         break
          


     def removeDuplicates(self, valuesList): # returns list without duplicates
          uniq_items = []
          for item in valuesList:
               if item not in uniq_items:
                    uniq_items.append(item)
          return uniq_items
          

     def getExpressionType(self, valueOfExpression):
          if self.isnum(valueOfExpression):  # determines if value type is a number
               expressionType = "number"
               return expressionType
          if valueOfExpression == "True" or valueOfExpression == "False":
               expressionType = "boolean"
               return expressionType
          else:
               expressionType = "string"
               return expressionType

     def getQuestion(self, expression, expressionType):
          if expressionType == "number":
               return f"What is {expression}? (please enter a number) "
          if expressionType == "boolean":
               return f"Is it true that: {expression}? "
          else:
               return f"What is {expression}? "
          
         
          

# for test purposes during coding ONLY
# Rule structure [ruleLabel, conclusionExpression, assignedConclusionValue, cf [ [conditionExpression, operator, expectedValue]… ] ]

r1=Rule
f1 = Fact
d1 = Default

# ********  Insert parsed rulebase below here  *********************************

goalExpression = "the correct action"


r1.addRule (['RULE 1', 'the correct action', 'turn up the heat by 15 degrees', 100, [['the color of the rug', '==', 'blue'], ['the size of the gasket', '==', 'small'], ['the temperature of the vat', '<', 90]]])

r1.addRule (['RULE 25', 'the correct action', 'discard the sample', 95, [['the color of the rug', '==', 'yellow'], ['the size of the gasket', '==', 'large']]])

r1.addRule (['RULE 13', 'the correct action', 'replace the gizmo with a new one', 100, [['the color of the rug', '==', 'blue'], ['the size of the gasket', '==', 'medium'], ['the temperature of the vat', '>', 120]]])

r1.addRule (['RULE 4', 'the correct action', 'package the glopper drivet and send it to the client', 100, [['the color of the rug', '==', 'blue'], ['the size of the gasket', '==', 'medium'], ['the temperature of the vat', '>', 90], ['the temperature of the vat', '<', 120], ['there is a hissing sound coming from the relief valve', '==', 'False']]])

r1.addRule (['RULE 5', 'the size of the gasket', 'small', 100, [['the gauge for gasket diameter in centimeters reads less than 15', '==', 'True']]])

f1.addFact (['FACT 1', 'the color of the liquid in the vat', 'clear', 100])

r1.addRule (['RULE 61', 'the size of the gasket', 'medium', 100, [['the gauge for gasket diameter in centimeters reads between 15 and 30', '==', 'True']]])

d1.addDefault (['DEFAULT 1', 'the correct action', 'do the default thing', 100])

r1.addRule (['RULE 703', 'the size of the gasket', 'large', 100, [['the gauge for gasket diameter in centimeters reads more than 30', '==', 'True']]])

r1.addRule (['RULE 282', 'the correct action', 'replace the gasket with a small one', 99, [['the gasket diameter in centimeters', '>', 33]]])

f1.addFact (['FACT 2', 'the part', 'the A3 gizmo', 100])

customQuestionList = [['the gasket diameter in centimeters', 'What is the diameter of the gasket (in centimeters) for {the part}?']]

possibleAnswersList = [['the color of the rug', ['blue', 'green', 'yellow']]]

# ********  Insert parsed rulebase above here  *********************************

if trace: f1.showFacts ()
if trace: r1.showRules ()
if trace: d1.showDefaults ()

i1 = InferenceEngine()
s1 = ExpressionList()

s1.buildExpressionList ()
if trace: print(f'\n\nfrom line 379, epressionList is: \n{expressionList}\n\n')

goal = i1.findValuesFor (goalExpression)   #  this starts the inferencing to determine the value of the goalExpression
if trace: print (f"\nHere is dump of the sessionMemory:\n{sessionMemory}\n")
# used to be: print (f"\nHere is the system recommendation: {goal}\n")
print (f'goal = {goal}\ngoalExpression = {goalExpression}\nconclusion = {goal[0][1]}\nCF = {goal[0][2]}\nRule = {goal[0][3]}\n\n')
UI.outputToReportWindow (goalExpression, goal[0][1], goal[0][2], goal[0][3])
commandPrompt = c1.getCommand()


