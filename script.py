from selenium import webdriver
import time
import pandas as pd
import re

lst1 = []
lst2 = []

def openBrowser():

    browser = webdriver.Chrome('<file path>')
    url = "<login page URL>"
    browser.get(url) #navigate to the page
    time.sleep(3)
    username = browser.find_element_by_id("username") #username form field
    password = browser.find_element_by_id("password") #password form field

    username.send_keys("<your ID>")
    password.send_keys("<password>")

    submitButton = browser.find_element_by_id("loginbtn")
    #button.click()
    submitButton.click()
    time.sleep(5)
    showAll = "<URL to scrape>"

    return browser, showAll


def profileSum():

    browser, showAll = openBrowser()

    browser.get(showAll)
    name = browser.find_elements_by_class_name("username")
    email = browser.find_elements_by_class_name("info")

    for el1, el2 in zip(name,email):
        lst1.append([el1.text,el2.text])


    for x in range(0, len(lst1)):
        extract = re.findall(r'[a-zA-Z0-9_.+-]+\@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', lst1[x][1], re.MULTILINE)
        lst1[x][1] = extract

    for i in range(0, len(lst1)):

        if len(lst1[i][1]) != 0:
            getEmail = lst1[i][1][0]
            lst1[i].append(getEmail)
            del lst1[i][1]

        elif len(lst1[i][1]) == 0:
            lst1[i].append("none")
            del lst1[i][1]

    df = pd.DataFrame(lst1)
    df.to_csv('./email.csv', sep=',', header=None, index=None)


def urlExtract():

    browser, showAll = openBrowser()

    browser.get(showAll)

    link = browser.find_elements_by_xpath("//td[@class='links cell c2 lastcol']/a")

    for g in link:
        lst2.append(g.get_attribute('href'))

    return lst2


def diveIn():

    browser, showAll = openBrowser()

    urllst = ["<list of URLs>"]

    masterlst = []

    for i in range(0,len(urllst)):
        print(urllst[i])
        browser.get(urllst[i])

        name = browser.find_elements_by_xpath("//div[@class='page-header-headings']/h2")
        body = browser.find_elements_by_class_name("no-overflow")
        restofthem = browser.find_elements_by_xpath("//li[@class='contentnode'][1 <= position() and position() < 7]/dl/dd")

        temp1=[]
        for a, b in zip(name,body):
            temp1.extend([a.text,b.text])

        temp2 = []
        for t in restofthem:
            temp2.append(t.text)

        masterlst.append(temp1+temp2)

    #browser.quit()
    #print (masterlst)
        df = pd.DataFrame(masterlst)
        df.to_csv('./student.csv', sep=',', header=None, index=None)

    return

def combineCsv():

    df1 = pd.read_csv('./email.csv')
    df2 = pd.read_csv('./student.csv')
    finaloutput = df1.join(df2, on='name', how='left',lsuffix='_left', rsuffix='_right')
    finaloutput.to_csv('./contact.csv', sep=',', header=None, index=None)



if __name__ == '__main__':

    #urlExtract()
    #diveIn()
    #profileSum()
    combineCsv()

