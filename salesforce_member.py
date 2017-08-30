import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.support.ui import WebDriverWait


# chrome-driver path setting
USER_NAME = ""
PASSWORD = ""

chromedriver = "/usr/local/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

# driver - driver used for working with SalesForce login/authentication + all other SalesForce related work
driver = webdriver.Chrome(chromedriver)
driver.get("https://login.salesforce.com/services/auth/sso/00D300000000iTzEAI/community?community=https%3A%2F%2Fsuccess.salesforce.com%2F&amp;startURL=%2FuserSetup%3Fgt%3Dhttps%253A%252F%252Fsuccess.salesforce.com%252F_ui%252Fcore%252Fchatter%252Fgroups%252FGroupProfilePage%253Fg%253D0F9300000001sX6")
username = driver.find_element_by_id("username")
username.send_keys(USER_NAME)
password = driver.find_element_by_id("password").send_keys(PASSWORD)
driver.find_element_by_id("Login").click()


# driver_mailinator used for working with mailinator website
driver_mailinator = webdriver.Chrome(chromedriver)
driver_mailinator.get("https://www.mailinator.com/inbox2.jsp?to=sfdeveloper#/#public_maildirdiv")


# for getting message inside mail the mail sent for verification code
message_title = driver_mailinator.find_elements_by_xpath("//div[contains(@class, 'innermail')]")
message_title[0].click()

time.sleep(5)

iframe = driver_mailinator.find_elements_by_tag_name('iframe')[0]
driver_mailinator.switch_to_frame(iframe)

message_body = driver_mailinator.find_element_by_tag_name("body").text


# getting verification code from the message inside the mail sent for verification code 
v_code_index = re.search(r"[^a-zA-Z](Verification Code:)[^a-zA-Z]", message_body)
v_code_start = v_code_index.start() + 20
v_code = message_body[v_code_start:]
v_code = v_code[:5]


driver.find_element_by_id("emc").send_keys(v_code)
driver.find_element_by_id("save").click()
time.sleep(5)


# going to groupmember page after login 
driver.get("https://success.salesforce.com/_ui/core/chatter/groups/GroupProfilePage?g=0F9300000001sX6")
time.sleep(5)


# clicking Show All link for getting Group Member Details popup
# show_all_link = driver.find_element_by_xpath("//span[contains(text(), 'Show All (113,664)')]")
show_all_link = driver.find_element_by_id("moreGroupMembersLink")
show_all_link.click()
time.sleep(3)


# loop for thousands of popups, 5000 is arbitrarily taken, can also be used generalised
member_no = 1
while True:
	
	time.sleep(5)
	member_title = []
	member_title = driver.find_elements_by_class_name("memberTableName")
	next_button = driver.find_element_by_xpath("//span[contains(@class, 'notLastPage')]")

	for i in range(26):

		try:
			trial_work = member_title[i]
			print "Serial No. : " + str(member_no)
			print "Member Name : " + member_title[i].find_elements_by_class_name("memberDisplayName")[0].find_elements_by_tag_name("a")[0].text
			print "Company Name : " + member_title[i].find_elements_by_class_name("memberDisplayName")[0].find_elements_by_class_name("chatterUserGuestBadge")[0].text
			try:
				print "Post : " + member_title[i].find_elements_by_class_name("titleSpan")[0].text
				print "\n\n\n"
			except IndexError:
				member_no = member_no + 1
				print "\n\n\n"
			member_no = member_no + 1
		except IndexError:
			pass

	time.sleep(5)
	
	if next_button.is_displayed() or next_button.is_Enabled():
		next_button.click()
		continue
	else:
		break


driver.quit()
driver_mailinator.quit()