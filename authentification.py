from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import getpass
import argparse

def authentification(login, mdp):
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get("https://monportail.siinergy.net/user/login?destination=/")

    champs_login = driver.find_element(By.ID,"edit-name")
    champs_login.send_keys(login)

    champs_mdp = driver.find_element(By.ID, "edit-pass")
    champs_mdp.send_keys(mdp)
    
    time.sleep(1)
    btn = driver.find_element(By.ID,"edit-submit")
    btn.click()
    time.sleep(2)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("login", help="username to authenticate")
    parser.add_argument("mdp", help="password to authenticate")
    args = parser.parse_args()

    try:
        authentification(args.login, args.mdp)
    except:
        print('fail')


    