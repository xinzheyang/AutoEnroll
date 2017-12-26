from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init():
	url = "https://css.adminapps.cornell.edu/psp/cuselfservice/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?"
	driver = webdriver.Chrome()
	driver.implicitly_wait(10)
	driver.get(url)
	return driver




def preadd(driver, netid, passwd):
	#web login
	driver.find_element_by_id("netid").send_keys(netid)
	driver.find_element_by_id("password").send_keys(passwd)
	driver.find_element_by_name("Submit").click()

	#locate iframe

	driver.switch_to.frame(0)

	#click enroll
	driver.find_element_by_id("DERIVED_SSS_SCR_SSS_LINK_ANCHOR3").click()
	

	#driver.switch_to.frame(0)
	#click Fall
	#driver.find_element_by_id("SSR_DUMMY_RECV1$sels$1$$0").click()
	#driver.find_element_by_id("DERIVED_SSS_SCT_SSR_PB_GO").click()

	

def select_section(driver, prefer):
	if len(driver.find_elements_by_id("SSR_CLS_TBL_RE$fviewall$0")) > 0:
		#click View all
		driver.find_element_by_id("SSR_CLS_TBL_RE$fviewall$0").click()

		#Explicitly wait for View 5 to be present
		element = WebDriverWait(driver, 10).until(
	        EC.text_to_be_present_in_element((By.ID, "SSR_CLS_TBL_RE$fviewall$0"), "View 5")
	    )


	tbody = driver.find_element_by_xpath('//*[@id="SSR_CLS_TBL_RE$scroll$0"]/tbody/tr[1]/td/table/tbody')
	children = tbody.find_elements_by_tag_name("tr")
	total_sections = len(children)-1
	if prefer != []:
		for i in prefer:
			section = driver.find_element_by_id("win0divDERIVED_CLS_DTL_SSR_STATUS_LONG$"+str(i-1))
			status_img = section.find_element_by_tag_name("img")
			status = status_img.get_attribute("alt")
			if status == "Open":
				select = driver.find_element_by_id("SSR_CLS_TBL_RE$sels$%s$$0" %str(i-1))
				select.click()
				driver.find_element_by_id("DERIVED_CLS_DTL_NEXT_PB").click()
				next_click = driver.find_element_by_id("ACE_DERIVED_SASSMSG_")
				next_click.find_element_by_id("DERIVED_CLS_DTL_NEXT_PB").click()
				#final next
				driver.find_element_by_id("DERIVED_CLS_DTL_NEXT_PB$280$").click()
				return 1
		return 0
	#loop over all sections
	else:
		for i in range(total_sections):
			print i
			section = driver.find_element_by_id("win0divDERIVED_CLS_DTL_SSR_STATUS_LONG$"+str(i))
			status_img = section.find_element_by_tag_name("img")
			status = status_img.get_attribute("alt")
			if status == "Open":
				select = driver.find_element_by_id("SSR_CLS_TBL_RE$sels$%s$$0" %str(i))
				select.click()
				driver.find_element_by_id("DERIVED_CLS_DTL_NEXT_PB").click()
				next_click = driver.find_element_by_id("ACE_DERIVED_SASSMSG_")
				next_click.find_element_by_id("DERIVED_CLS_DTL_NEXT_PB").click()
				#final next
				driver.find_element_by_id("DERIVED_CLS_DTL_NEXT_PB$280$").click()
				return 1
		return 0
def add(driver, number, prefer):
	"sec: the section to be added, string in the form 'CS 3110 202'"
	
	
	driver.find_element_by_id("DERIVED_REGFRM1_CLASS_NBR").send_keys(number)
	driver.find_element_by_id("DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$9$").click()
	
	select_section(driver, prefer)
	#proceed
	driver.find_element_by_id("DERIVED_REGFRM1_LINK_ADD_ENRL$82$").click()
	#finish enrolling
	driver.find_element_by_id("DERIVED_REGFRM1_SSR_PB_SUBMIT").click()
	section = driver.find_element_by_id("win0divDERIVED_REGFRM1_SSR_STATUS_LONG$0")
	status_img = section.find_element_by_tag_name("img")
	status = status_img.get_attribute("alt")
	if status == "Success":
		driver.quit()
		return 1


	raise Exception
	#driver.switch_to_default_content()
	#driver.switch_to.frame(0)

	
	

	

if __name__ == '__main__':
	driver = init()
	preadd(driver, "netid", "passwd")
	add(driver, [])
