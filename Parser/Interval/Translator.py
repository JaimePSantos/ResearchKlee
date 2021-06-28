import sys
from Tokens import TT_INT, TT_FLOAT, TT_EOF, TT_LOWERLIM, TT_UPPERLIM, TT_SEPARATOR, TT_INTERVALPLUS,\
    TT_INTERVALMINUS, TT_INTERVALMULT, TT_INTERVALDIV,TT_GEQ,TT_SEQ,TT_GT,TT_ST,TT_NOT,TT_AND,TT_FORALL,TT_BOX,\
    TT_LPAREN, TT_RPAREN,TT_INTERVALVAR,TT_PROGTEST, TT_PROGAND,TT_PROGUNION,TT_PROGSEQUENCE,TT_PROGASSIGN,\
    TT_DIFFERENTIALVAR,TT_PROGDIFASSIGN,TT_IN,TT_KEYWORD,TT_IDENTIFIER,TT_IDENTIFIERDIF,TT_LBOX,TT_RBOX
from Errors import InvalidSyntaxError
from Nodes import LowerNumberNode,UpperNumberNode,IntervalVarNode,SeparatorNode,BinOpNode,PropOpNode,ProgOpNode,\
    UnaryOpNode,DifferentialVarNode,UnaryProgOpNode,ProgDifNode,UnaryForallOpNode,BoxNode,BoxPropNode
import string
DIGITS = '0123456789'
LETTERS = string.ascii_letters + "'"
LETTERS_DIGITS = LETTERS + DIGITS

class Translator:
    'Class that evalutates the input.'
    def __init__(self):
        self.varList = []
        self.intervalDict = {}
        self.varDict = {}
        self.translation = ""

    def buildTranslation(self):
        intervals = ''
        i = 0
        for interval in self.intervalDict.values():
            i+=1
            intervals += "(" + str(interval) + ")"
            if i == len(self.intervalDict):
                break
            else:
                intervals += " ∧ "
        builtTranslation = intervals + " -> " + self.translation
        return builtTranslation

    def visit(self, node):
        'Template of the function to visit each method.'
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        'If no acceptable method found, throw an exception.'
        raise Exception(f'No visit_{type(node).__name__} defined.')

    def visit_BinOpNode(self, node):
        '''
        Visits nodes that have binary operations on them. \
        If the token is + then we simply add all lower limit numbers and upper limit numbers separately. \
        If the token is * then we join lower limit numbers and upper limit numbers so we can perform interval multiplication on them.
        :param node:
        :return:
        '''
        # print("Found BinOpNode")
        #TODO: Repensar a logica dos intervalos, talvez usar um no para o intervalo todo e depois dividi-lo em upper e lower.
        if node.op_tok.type in TT_INTERVALPLUS:
            interval1 = self.visit(node.left_node)
            interval2 = self.visit(node.right_node)
            translation = '(' + str(interval1)+ ' + '+ str(interval2) + ')'
            self.translation = translation
            return translation

        if node.op_tok.type in TT_INTERVALMULT:
            self.visit(node.left_node)
            self.visit(node.right_node)
            # self.intervalNumberList = (self.lowerNumberList.extend(self.upperNumberList))
            return self.resultInterval

    def visit_UnaryOpNode(self,node):
        pass

    def visit_LowerNumberNode(self, node):
        'Visits the nodes that have lower limit values and constructs a list that keeps track of these values.'
        # print("Found LowerNumberNode")
        num = Number(node.tok.value).set_pos(node.pos_start,node.pos_end)
        return num

    def visit_UpperNumberNode(self, node):
        'Visits the nodes that have upper limit values and constructs a list that keeps track of these values.'
        # print("Found UpperNumberNode")
        num = Number(node.tok.value).set_pos(node.pos_start,node.pos_end)
        return num


    def visit_SeparatorNode(self, node):
        '''
        Visits the nodes with the SEPARATOR token.
        :param node:
        :return:
        '''
        # print("Found SeperatorNode")
        lower = self.visit(node.left_node)
        upper = self.visit(node.right_node)
        uniqueVar = self.makeUniqueVar()
        interval = TranslatedInterval(lower, upper,uniqueVar)
        self.intervalDict[uniqueVar] = interval
        #TODO: Estou a retornar a uniquevar de maneira a que a traducao fique apenas a variavel nova gerada. Talvez esta nao seja a melhor maneiora.
        return uniqueVar

    def visit_IntervalVarNode(self,node):
        return node.tok.value


    def visit_PropOpNode(self,node):
        leftNode = node.left_node
        rightNode = node.right_node
        visitLeftNode = self.visit(leftNode)
        visitRightNode = self.visit(rightNode)
        translatedOpTok = ''
        translation = ''
        if node.op_tok.type in [TT_ST,TT_GT,TT_GEQ,TT_SEQ]:
            if node.op_tok.type in TT_ST:
                translatedOpTok = '<'
            elif node.op_tok.type in TT_GT:
                translatedOpTok = '>'
            elif node.op_tok.type in TT_GEQ:
                translatedOpTok = '>='
            elif node.op_tok.type in TT_SEQ:
                translatedOpTok = '<='
            self.varDict[leftNode] = visitRightNode
        elif node.op_tok.type in (TT_KEYWORD, 'AND'):
            translatedOpTok = '∧'

        if translatedOpTok is not None:
            translation = str(visitLeftNode) + " " + translatedOpTok + " " + str(visitRightNode)
        else:
            translation = str(visitLeftNode) + " " + str(node.op_tok)+ " " + str(visitRightNode)
        self.translation = translation
        return translation

    def visit_ProgOpNode(self,node):
        print("Visited program node")
        thing1 = self.visit(node.left_node)
        thing2 = self.visit(node.right_node)
        print(thing2.type)
        translation = str(thing1) + " " + str(node.op_tok) + " " + str(thing2)
        return translation

    def makeUniqueVar(self):
        intervalVar = ''
        for var in LETTERS:
            if var not in self.varList:
                intervalVar = var
                self.varList.append(intervalVar)
                return intervalVar
            else:
                continue
        if intervalVar == '':
            return -1


    def reset(self):
        '''
        Clears the lists of numbers so each input has a clean slate.
        :return:
        '''
        self.lowerNumberNodeList = []
        self.upperNumberNodeList = []

#######################################
# VALUES
#######################################

class Number:
    '''
    This class helps us perform integer operations on the elements belonging to the NumberList class.
    '''
    def __init__(self, value):
        self.value = value
        self.set_pos()
        # self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        '''
        For keeping track of number position.
        :param pos_start:
        :param pos_end:
        :return:
        '''
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    # def set_context(self, context=None):
    #     self.context = context
    #     return self

    def __add__(self,other):
        if isinstance(other, Number):
            return Number(self.value + other.value)

    def __mul__(self,other):
        if isinstance(other, Number):
            return Number(self.value * other.value)

    def __lt__(self,other):
        if isinstance(other, Number):
            return self.value < other.value

    def __gt__(self,other):
        if isinstance(other, Number):
            return self.value > other.value

    def __le__(self,other):
        if isinstance(other, Number):
            return self.value <= other.value

    def __ge__(self,other):
        if isinstance(other, Number):
            return self.value >= other.value

    def __eq__(self,other):
        if isinstance(other, Number):
            return self.value == other.value

    def __repr__(self):
        return str(self.value)

class Interval:
    '''
    This class helps us represent the interval that resulted from an operation and keep track of errors.
    '''
    def __init__(self,lowerNum=None,upperNum=None):
        if lowerNum and upperNum is not None:
            self.lowerNum = lowerNum
            self.upperNum = upperNum
            self.set_pos()
        else:
            self.lowerNum = None
            self.upperNum = None

    def set_pos(self):
        '''
        So we know the position of our intervals.
        :return:
        '''
        self.pos_start = self.lowerNum.pos_start
        self.pos_end = self.upperNum.pos_end
        return self

    def __repr__(self):
        return '[' + str(self.lowerNum) + ',' + str(self.upperNum) + ']'

class TranslatedInterval:
    '''
    This class helps us represent the interval that resulted from an operation and keep track of errors.
    '''
    def __init__(self,lowerNum=None,upperNum=None,ineqVar=None):
        if lowerNum and upperNum is not None:
            self.lowerNum = lowerNum
            self.upperNum = upperNum
            self.ineqVar = ineqVar
            self.set_pos()
            self.set_lims()
        else:
            self.lowerNum = None
            self.upperNum = None

    def set_pos(self):
        '''
        So we know the position of our intervals.
        :return:
        '''
        self.pos_start = self.lowerNum.pos_start
        self.pos_end = self.upperNum.pos_end
        return self

    def set_lims(self):
        self.lowerLim = str(self.lowerNum) + '<=' + str(self.ineqVar)
        self.upperLim = str(self.ineqVar) + '<=' + str(self.upperNum)

    def __repr__(self):
        return self.lowerLim + ' ∧ ' + self.upperLim

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self