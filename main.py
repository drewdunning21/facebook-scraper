from facebookDriver import FacebookDriver
from time import sleep

def main():
    driver = FacebookDriver('copped4you.dexter@gmail.com','34erft34')
    driver.login()
    driver.getInterests('https://www.facebook.com/eason.skelnik')

main()
