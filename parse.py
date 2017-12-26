import requests 
from bs4 import BeautifulSoup



def get_section(inp):
	"inp: the class to be added, string in the form 'CS 3110 DIS 202'"
	splited = inp.split()
	subj = splited[0]
	course = splited[1]
	class_type = splited[2]
	sect = splited[3]
	url = "https://classes.cornell.edu/browse/roster/FA17/class/%s/%s" % (subj, course)
	r = requests.get(url, timeout=30)
	r.encoding = r.apparent_encoding
	soup = BeautifulSoup(r.text.encode("utf8"), "lxml")
	section = soup.find(attrs={"aria-label":"Class Section "+class_type+" "+sect})
	
	return section

def get_five_digit(section):
	a = section.contents[0].contents[1].contents[0]
	return a["data-content"]
	
def is_open(section):
	s = str(section)
	if 'data-content="Closed"' in s:
		return False
	if 'data-content="Open"' in s:
		return True


if __name__ == '__main__':
	section = get_section("CS 3110 LEC 001")
	print is_open(section)
	print get_five_digit(section)
