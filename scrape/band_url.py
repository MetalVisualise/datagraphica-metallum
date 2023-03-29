from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import csv as csv
import os


def create_csv():
    # Create or overwrite CSV file to save data in
    if os.path.isfile(r'data\raw\band_url.csv'):
        os.remove(r'data\raw\band_url.csv')

    with open(r'data\raw\band_url.csv', 'w', newline='',
              encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar=r'"')
        csv_writer.writerow(['band_url'])


def write_csv(band_url):
    with open(r'data\raw\band_url.csv', 'a', newline='',
              encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar=r'"')
        csv_writer.writerow([band_url])


def scrape_url(driver, wait, row):
    wait.until(expected_conditions.invisibility_of_element(
        (By.XPATH, '//*[@id"searchResultsBand_processing"]')))
    xpath_string = '/html/body/div/div[3]/div/div[1]/div/div/div/div/div[5]/' + 'table/tbody/tr[' + str(row) + ']/td[1]/a'
    band_url = wait.until(expected_conditions.presence_of_element_located(
        (By.XPATH, xpath_string))).get_attribute('href')

    write_csv(band_url)


def main():
    create_csv()

    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, timeout=20)
    driver.maximize_window()

    driver.get('https://www.metal-archives.com/search/advanced/searching/'
               'bands?bandName=&genre=&country=&yearCreationFrom=&'
               'yearCreationTo=&bandNotes=&status=&themes=&location=&'
               'bandLabelName=#bands')
    wait.until(expected_conditions.presence_of_element_located(
        (By.XPATH, '//*[@id="searchResultsBand_processing"]')))

    for page in range(789):
        for row in range(1, 201):
            scrape_url(driver, wait, row)
        driver.find_element(By.XPATH,
                            '//*[@id="searchResultsBand_next"]').click()

    driver.close()


if __name__ == "__main__":
    main()
