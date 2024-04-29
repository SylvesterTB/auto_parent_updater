from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# Creates driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


# uses find element to find and click button
def click_button(by_value, value_value, wait_time):
    if wait_time:
        try:
            wait = WebDriverWait(driver, timeout=wait_time)
            wait.until(ec.element_to_be_clickable((by_value, value_value)))

        except TimeoutException:
            return "dne"

    button = (driver.find_element(by=by_value, value=value_value))
    button.click()
    return button


# Opens aspen and logs in, input username and password as strings
def login_aspen(username, password):
    driver.get("https://aspen.cpsd.us/aspen/home.do")
    if click_button(By.CLASS_NAME, "button", 2) == "dne":
        return False

    username_box = click_button(By.NAME, "username", 0)
    if username_box == "dne":
        return False
    username_box.send_keys(username)

    password_box = click_button(By.NAME, "password", 0)
    if password_box == "dne":
        return False
    password_box.send_keys(password)

    if click_button(By.CLASS_NAME, "button-text", 0) == "dne":
        return False

    try:
        driver.find_element(by=By.NAME, value="logonForm")
    except NoSuchElementException:
        return True
    else:
        return False


def get_Class_Info(class_, aspen_class_code):
    # Input the class code as a str, gets a list of the student ids of the students in the class
    # (as strs)
    def get_school_ids(class_code):
        gradebook = click_button(By.PARTIAL_LINK_TEXT, "Gradebook", 2)
        class_button = click_button(By.PARTIAL_LINK_TEXT, class_code, 2)
        roster_button = click_button(By.PARTIAL_LINK_TEXT, "Roster", 2)
        if gradebook == "dne" or class_button == "dne" or roster_button == "dne":
            return False
        try:
            raw_data = driver.find_elements(by=By.CSS_SELECTOR, value="td")
        except NoSuchElementException:
            return False
        str_data = [item.text for item in raw_data]
        student_ids = [student_id for student_id in str_data if student_id.isdigit() and len(student_id) == 7]
        return student_ids

    # returns [student_email, [parent_email, parent_email]]
    def go_to_profile(student_id):
        click_button(By.PARTIAL_LINK_TEXT, "Student", 2)
        can_continue = True
        student_nonexistant = False
        while can_continue and click_button(By.PARTIAL_LINK_TEXT, student_id, 1) == "dne":
            student_nonexistant = click_button(By.PARTIAL_LINK_TEXT, student_id, 1) == "dne"
            next_button = driver.find_element(by=By.NAME, value="nextPageButton")
            can_continue = next_button.is_enabled()
            next_button.click()

        if student_nonexistant and not can_continue:
            return "na" + student_id

        return True

    def get_phone():
        a_wait = WebDriverWait(driver, timeout=1)
        a_wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "td")))
        elements = driver.find_elements(By.CSS_SELECTOR, "td")

        text_elements = [a.text for a in elements]
        final_numbers = [text for text in text_elements if "-" in text and len(text) == 12]

        return list(set(final_numbers))

    def get_emails():
        click_button(By.PARTIAL_LINK_TEXT, "Contacts", 2)
        raw_data = driver.find_elements(by=By.CSS_SELECTOR, value="a")
        an_emails = [item.text for item in raw_data if "@" in item.text]

        return list(set(an_emails))

    def get_name():
        std_name = driver.find_element(By.ID, "propertyValue(stdViewName)-span").text
        i = std_name.index(",")

        return std_name[i + 2:] + " " + std_name[:i]

    def get_birthday():
        bday_box = driver.find_element(By.ID, "propertyValue(relStdPsnOid_psnDob)-span")
        return bday_box.text[:bday_box.text.index(" ")]

    cc = aspen_class_code

    student_ids = get_school_ids(cc)
    if not student_ids:
        raise Exception("Could not get student ids")

    master_dict = {}
    all_numbers = []
    final_emails = []
    all_names = []
    all_birthdays = []
    secondary_dict = {}
    for student_id in student_ids:
        go_to_profile(student_id)
        phone_number = get_phone()
        std_name = get_name()
        birthday = get_birthday()
        emails = get_emails()

        all_numbers += phone_number
        final_emails += emails
        all_names += std_name
        master_dict[student_id] = [std_name, emails, phone_number, birthday]
        secondary_dict[std_name] = [emails, phone_number]

    number_file = str(class_) + "_phone_numbers"
    add_number = open(number_file, 'a')
    # add_number.write("\n")

    for number in range(len(all_numbers) - 1):
        add_number.write(all_numbers[number] + "\n")

    email_file = str(class_) + "_emails"
    add_email = open(email_file, 'a')
    # add_email.write("\n")

    for email in range(len(final_emails) - 1):
        add_email.write(final_emails[email] + "\n")

    driver.quit()



username = ""
password = ""

    # Logging into aspen and scraping the info
# if not login_aspen(username, password):
#     raise Exception("Could not login")


# get_Class_Info("Computer Science 2", "T527-001")




