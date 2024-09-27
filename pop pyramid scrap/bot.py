from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from time import sleep

finalRes=[]

service = Service("msedgedriver.exe")
driver = webdriver.Edge(service=service)
driver.get("https://www.populationpyramid.net/")

# Find the list of countries
list2 = driver.find_element(By.ID, "countryDropdown")
countries = list2.find_elements(By.TAG_NAME, "a")

# Loop through each country
ct=1
for i in range(len(countries)):
    # Re-fetch the country list and href in case of stale element issues
    list2 = driver.find_element(By.ID, "countryDropdown")
    countries = list2.find_elements(By.TAG_NAME, "a")
    
    # Extract country href and name before navigating
    href = countries[i].get_attribute('href')
    country_name = countries[i].get_attribute('innerHTML')  # Store name BEFORE navigation
    
    if href:
        # Navigate to the country page
        driver.get(href)

        try:
            # Wait for the pyramid-container and get the SVG element
            element = driver.find_element(By.ID, "pyramid-container")
            svg = element.find_element(By.TAG_NAME, 'svg')
            graph = svg.find_element(By.ID, "pp-graph")
            bars = graph.find_elements(By.TAG_NAME, 'g')

            # Loop through each bar (generation) and check the population data
            gen = 0
            for bar in bars:
                class_ = bar.get_attribute('class')
                if class_ == "pp-hbar":
                    population = bar.find_elements(By.TAG_NAME, "text")
                    male = population[1].get_attribute('innerHTML')
                    female = population[0].get_attribute('innerHTML')

                    # Check if the male population is smaller than female
                    if float(male[:-1]) < float(female[:-1]):
                        if gen == 5:
                            # Open a file in append mode ('a')
                            with open('res.txt', 'a') as file:
                               file.write(f'{ct}: {country_name}\n')
                            ct=ct+1

                    gen += 1

        except Exception as e:
            print(f"An error occurred for {country_name}: {e}")

        sleep(2)

# Quit the driver
driver.quit()
