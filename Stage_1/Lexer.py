from enum import IntEnum

class Tag(IntEnum):
	EOF = 65535
	ERROR = 65534
	## Operators ##
	GEQ = 258
	LEQ = 259
	NEQ = 260
	ASSIGN = 261
	## REGULAR EXPRESSIONS ##
	ID = 358
	NUMBER = 359
	STRING = 360
	TRUE = 361
	FALSE = 362
	## ADD THE MISSING RESERVED WORDS, JUST FOLLOW THE NUMBER SEQUENCE ##
	VAR = 457
	FORWARD = 458
	BACKWARD = 459
	LEFT = 460
	RIGHT = 461
	SETX = 462
	SETY = 463
	SETXY = 464
	CLEAR = 465
	CIRCLE = 466
	ARC = 467
	PENUP = 468
	PENDOWN = 469
	COLOR = 470
	PENWIDTH = 471
	PRINT = 472
	REPEAT = 473
	IF = 474
	IFELSE = 475
	HOME = 476
	NOT = 477
	OR = 478
	AND = 479
	MOD = 480
	
class Token:
	__tag = Tag.EOF
	__value = None
	
	def __init__(self, tagId, val = None):
		self.__tag = tagId
		self.__value = val
		
	def getTag(self):
		return self.__tag
	
	def getValue(self):
		return self.__value
		
	def __str__(self):
		if self.__tag == Tag.GEQ:
			return "'>='"
		elif self.__tag == Tag.LEQ:
			return "'<='"
		elif self.__tag == Tag.NEQ:
			return "'<>'"
		elif self.__tag == Tag.ASSIGN:
			return "':='"
		elif self.__tag == Tag.TRUE:
			return "'#t'"
		elif self.__tag == Tag.FALSE:
			return "'#f'"
		elif self.__tag == Tag.NUMBER:
			return "numeric constant"
		elif self.__tag == Tag.ID:
			return "'" + str(self.__value) + "'"
		elif self.__tag >= Tag.VAR and self.__tag <= Tag.MOD:
			return "'" +  str(self.__value).lower() + "'"
		elif self.__tag == Tag.STRING:
			return "string constant"
		else:
			return "'" + chr(self.__tag) + "'" 
			return "'" + chr(self.__tag) + "'" 
			
class Lexer:
	__peek = ' '
	__words = {}
	__input = None

	def __init__(self, filepath):
		self.__input = open(filepath, "r")
		self.__peek = ' '

		self.__words["VAR"] = Token(Tag.VAR, "VAR")
		self.__words["FORWARD"] = Token(Tag.FORWARD, "FORWARD")
		self.__words["FD"] = Token(Tag.FORWARD, "FORWARD")
		## ADD THE REST RESERVED WORDS, REMEMBER THAT SOME RESERVER WORDS HAVE THE SAME TAG ##
		self.__Tokens["BACKWARD"] = Token(Tag.BACKWARD, "BACKWARD")
		self.__Tokens["BK"] = Token(Tag.BACKWARD, "BACKWARD")
		self.__Tokens["LEFT"] = Token(Tag.LEFT, "LEFT")
		self.__Tokens["LT"] = Token(Tag.LEFT, "LEFT")
		self.__Tokens["RIGHT"] = Token(Tag.RIGHT, "RIGHT")
		self.__Tokens["RT"] = Token(Tag.RIGHT, "RIGHT")
		self.__Tokens["SETX"] = Token(Tag.SETX, "SETX")
		self.__Tokens["SETY"] = Token(Tag.SETY, "SETY")
		self.__Tokens["SETXY"] = Token(Tag.SETXY, "SETXY")
		self.__Tokens["HOME"] = Token(Tag.HOME, "HOME")
		self.__Tokens["CLEAR"] = Token(Tag.CLEAR, "CLEAR")
		self.__Tokens["CLS"] = Token(Tag.CLEAR, "CLEAR")
		self.__Tokens["ARC"] = Token(Tag.ARC, "ARC")
		self.__Tokens["PENUP"] = Token(Tag.PENUP, "PENUP")
		self.__Tokens["PU"] = Token(Tag.PENUP, "PENUP")
		self.__Tokens["PENDOWN"] = Token(Tag.PENDOWN, "PENDOWN")
		self.__Tokens["PD"] = Token(Tag.PENDOWN, "PENDOWN")
		self.__Tokens["COLOR"] = Token(Tag.COLOR, "COLOR")
		self.__Tokens["PENWIDTH"] = Token(Tag.PENWIDTH, "PENWIDTH")
		self.__Tokens["PRINT"] = Token(Tag.PRINT, "PRINT")
		self.__Tokens["REPEAT"] = Token(Tag.REPEAT, "REPEAT")
		self.__Tokens["IF"] = Token(Tag.IF, "IF")
		self.__Tokens["IFELSE"] = Token(Tag.IFELSE, "IFELSE")
		self.__Tokens["NOT"] = Token(Tag.NOT, "NOT")
		self.__Tokens["OR"] = Token(Tag.OR, "OR")
		self.__Tokens["AND"] = Token(Tag.AND, "AND")
		self.__Tokens["MOD"] = Token(Tag.MOD, "MOD")

	def read(self):
		self.__peek = self.__input.read(1)
	
	def readch(self, c):
		self.read()
		if self.__peek != c:
			return False

		self.__peek = ' '
		return True

	def __skipSpaces(self):
		while True:
			if self.__peek == ' ' or self.__peek == '\t' or self.__peek == '\r' or self.__peek == '\n':
				self.read()
			else:
				break
	
	def scan(self):
		self.__skipSpaces()

		## ADD CODE TO SKIP COMMENTS HERE ##
		if self.__peek == '%':
			while True:
				self.__read()
				if self.__peek == '\n':
					break
			self.__skipSpaces()

		if self.__peek == '<':
			if self.readch('='):
				return Token(Tag.LEQ, "<=")
			elif self.readch('>'):
				return Token(Tag.NEQ, "<>")
			else:
				return Token(ord('<'))
		elif self.__peek == '>':
			if self.readch('='):
				return Word(Tag.GEQ, ">=")
			else:
				return Token(ord('>'))
		elif self.__peek == '#':
			if self.readch('t'):
				return Token(Tag.TRUE, "#t")
			elif self.readch('f'):
				return Token(Tag.FALSE, "#f")
			else:
				return Token(ord('#'))
		elif self.__peek == ':':
			if self.readch('='):
				#print("reading :=")
				return Token(Tag.ASSIGN, ":=")
			else:
				return Token(ord(':'))

		if self.__peek  == '"':
			val = ""
			while True:
				val = val + self.__peek
				self.read()
				if self.__peek == '"':
					break
			
			val = val + self.__peek
			self.read()
			return Token(Tag.STRING, val)

		if self.__peek.isdigit():
			val = 0
			while True:
				val = (val * 10) + int(self.__peek)
				self.read()
				if not(self.__peek.isdigit()):
					break
			## ADD CODE TO PROCESS DECIMAL PART HERE ##
			if self.__peek  == '.':
				self.__read()
				if self.__peek.isdigit():
					divisor = 10.0
					while True:
						val = val + (float(self.__peek) / divisor)
						divisor = divisor * 10.0
						self.__read()
						if not(self.__peek.isdigit()):
							break
				else:
					raise Exception('Lexical Exception')
			return Token(Tag.NUMBER, val)

		if self.__peek.isalpha():
			val = ""
			while True:
				val = val + self.__peek.upper()
				self.read()
				if not(self.__peek.isalnum()):
					break

			if val in self.__words:
				return self.__words[val]

			w = Token(Tag.ID, val)
			self.__words[val] = Token(Tag.ID, val)
			return w

		if not(self.__peek):
			return Token(Tag.EOF)			

		token = Token(ord(self.__peek))
		self.__peek = ' ' 
		return token