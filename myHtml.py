def find(string, target, rank):
    place = -1
    for i in range(rank):
        place = string.find(target, place+1)
    return place


class HtmlElement:
	def __init__(self, eleStr, show=False):
		self.attrs = {}
		self.subEle = []
		self.value = ""
		self.name = ""
		if eleStr != "":
			self.create(eleStr, show=show)

	def create(self, eleStr, show=False):
		self.attrs = {}
		self.subEle = []
		attrHeader = eleStr[1:eleStr.find(">")]
		if show:
			print(attrHeader)
			print("****************************")
		while len(attrHeader) != 0 and attrHeader[0] != " ":
			self.name += attrHeader[0]
			attrHeader = attrHeader[1:]
		while len(attrHeader) != 0 and (attrHeader[0] == " " or attrHeader[0] == "\n" or attrHeader[0] == "\r"):
			attrHeader = attrHeader[1:]
		while len(attrHeader) != 0:
			attr = ""
			val = ""
			while attrHeader[0] != "=":
				attr += attrHeader[0]
				attrHeader = attrHeader[1:]
			attrHeader = attrHeader[2:]
			while attrHeader[0] != "\"":
				val += attrHeader[0]
				attrHeader = attrHeader[1:]
			attrHeader = attrHeader[1:]
			self.attrs[attr] = val
			while len(attrHeader) != 0 and (attrHeader[0] == " " or attrHeader[0] == "\n" or attrHeader[0] == "\r"):
				attrHeader = attrHeader[1:]

		eleStr = eleStr[eleStr.find(">")+1:]
		self.value = eleStr[:eleStr.find("<")]
		eleStr = eleStr[eleStr.find("<"):]
		while eleStr[:2] != '</':
			sub = HtmlElement("")
			eleStr = sub.create(eleStr, show=show)
			self.subEle.append(sub)
		if eleStr[2:2+len(self.name)] == self.name:
			eleStr = eleStr[eleStr[2:].find("<")+2:]
		return eleStr
		
		
	def find_element(self, name, attrs):
		for sub in self.subEle:
			if name == sub.name and attrs == sub.attrs:
				return sub
			else:
				ele = sub.find_element(name, attrs)
				if ele != None:
					return ele
		return None
	
	def find_element_name(self, name):
		for sub in self.subEle:
			if name == sub.name:
				return sub
			else:
				ele = sub.find_element_name(name)
				if ele != None:
					return ele
		return None
