import requests
from time import sleep
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

your_name = input("\n Enter your Name : ").capitalize()
username = input(" Enter your Telegram Username : ")
city_name = input("\n Enter City name : ").capitalize()
movie_name = input(" Enter Movie name : ")
select_language = input(" Select Language : ").capitalize()
select_format = input(" Select Format (2D/3D/4DX/7D/IMAX 2D/IMAX 3D/MX4D) : ").upper()
#print("\n For the following, Please press Enter key if you have no preference\n")
show_time = input(" Which Show-Time you prefer : ").capitalize()
preferred_venue = input(" Enter Preferred Venue (Type the full name of the Venue shown as in BMS) : ").title()

if your_name == '': your_name="Midhun"
if select_language == '': chosen_language="N/A" 
else: chosen_language=select_language
if select_format == '': chosen_format="N/A"
else: chosen_format=select_format
if show_time == '': chosen_time="N/A"
else: chosen_time=show_time
if preferred_venue == '': chosen_venue="N/A"
else: chosen_venue=preferred_venue

select_language=select_language.upper()
show_time=show_time.lower()

chrome_options = ChromeOptions().add_argument("--disable-notifications")
chrome_capa = DesiredCapabilities.CHROME
chrome_capa["pageLoadStrategy"] = "none"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options, desired_capabilities=chrome_capa)

def telegram_bot(bot_message):
    bot_message = encryption(bot_message)
    bot_token = '5119253303:AAFacw7KuJCK1dMxGtA9CWLE9I8dvcQeRqE'
    if username=='':
        bot_chat_id = '422860978'
    else:
        bot_chat_id = new_bot_chat_id
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + \
        '&parse_mode=MarkdownV2&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def encryption(bot_message):
    special_char = ["(",")",".","<",">","[","]","-"]
    for i in range(len(special_char)):
        bot_message = bot_message.replace(special_char[i]," ")
    return bot_message

found=False
while(True):
    try:
        wait = WebDriverWait(driver, 10)
        mid_wait = WebDriverWait(driver, 30)
        long_wait = WebDriverWait(driver, 60)

        while(True):
            if username != '':
                driver.get('https://api.telegram.org/bot5119253303:AAFacw7KuJCK1dMxGtA9CWLE9I8dvcQeRqE/getUpdates')

                paragraph = wait.until(EC.presence_of_element_located((By.XPATH, "//pre"))).text

                def find_all(a_str, sub):
                    start = 0
                    while True:
                        start = a_str.find(sub, start)
                        if start == -1: return
                        yield start
                        start += len(sub)

                end_index=0
                user_start = list(find_all(paragraph, 'username'))
                user_end = list(find_all(paragraph, 'language_code'))
                for i in range(len(user_start)):
                    for j in range(len(user_end)):
                        if paragraph[user_start[i]+11:user_end[j]-3]==username:
                            end_index = user_end[j]

                if end_index!=0:
                    new_bot_chat_id = paragraph[end_index+34:end_index+43]
                    break
                else:
                    print("\n Please send a hi to our telegram bot : @bmsalerts_bot")
                    print(" Note : This token will only available for 24 Hrs")
                    choice = input("\n Have you sent (Y/N) : ")
            else:
                break

        driver.get('https://in.bookmyshow.com')

        try:      
            select_city = mid_wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search for your city']")))
            driver.execute_script("window.stop();")
            select_city.send_keys(city_name)
            sleep(3)
            select_city.send_keys(Keys.ENTER)
        except:
            mid_wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Search for Movies, Events, Plays, Sports and Activities']")))
            driver.execute_script("window.stop();")  

        avail_break = 0
        movie_name_found=0
        print_once = 0

        while(True): 
            search_bar = long_wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Search for Movies, Events, Plays, Sports and Activities']")))
            search_bar.click()

            movie_search_bar = long_wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search for Movies, Events, Plays, Sports and Activities']")))
            movie_search_bar.click()
            movie_search_bar.send_keys(movie_name)
            sleep(2)
            movie_search_bar.send_keys(Keys.ENTER)

            movie_name = long_wait.until(EC.presence_of_element_located((By.XPATH, "//div[1]/div[1]/div[2]/section[1]/div/div/div[2]/h1")))
            movie_name = movie_name.text
            #driver.execute_script("window.stop();")

            if movie_name_found==0:
                telegram_bot("Hi "+your_name+",\n\nYour Request\nCity Name : "+city_name+"\nMovie Name : "+movie_name
                        +"\nLanguage : "+chosen_language+"\nFormat : "+chosen_format+"\nShow Time : "+chosen_time
                        +"\nVenue : "+chosen_venue)
                movie_name_found=1

            flag1=0
            flag2=0
            flag3=0
            flag4=0
            i=0

            while(True):
                if flag1==1:
                    break

                try:
                    try:
                        book_tickets = long_wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Book tickets']")))
                        driver.execute_script("window.stop();")

                        book_tickets.click()
                    except:
                        try:
                            long_wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Refresh']")))
                            driver.refresh()
                            book_tickets = long_wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Book tickets']")))
                            book_tickets.click()
                        except:
                            flag4=1

                    try:
                        wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='__venue-name']")))
                        available_lang = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='__text _languages-text _highlighted']")))
                        if avail_break==0:
                            telegram_bot("Available Language and Format : "+available_lang.text)
                            avail_break = 1
                        break
                    except:
                        total_lang = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li/section[1]/span")))
                        for j in range(1,len(total_lang)+1):
                            if flag1==1 :
                                break
                            retrieved_lang = wait.until(EC.presence_of_element_located((By.XPATH, "//li[" + str(j) + "]/section[1]/span")))
                            if select_language == retrieved_lang.text:
                                total_format = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[" + str(j) + "]/section[2]/div/span")))
                                for k in range(1,len(total_format)+1):
                                    retrieved_format = wait.until(EC.presence_of_element_located((By.XPATH, "//li[" + str(j) + "]/section[2]/div[" + str(k) + "]/span")))
                                    if select_format == retrieved_format.text:
                                        retrieved_format.click()
                                        long_wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='__venue-name']")))
                                        flag1=1
                                        break
                                    if k==len(total_format):
                                        flag3=1
                                        wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='__venue-name']")))
                            if j==len(total_lang):
                                flag2=1
                                wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='__venue-name']")))
                                    
                except:
                    i=i+1
                    if i==4:
                        break
                    if flag1==1:
                        break
                    if print_once==0:
                        if flag2==1:
                            print("\n\n >> Select language not yet available\n\n    Available languages : ")
                            send_message = "Select language not yet available\n\nAvailable languages :\n"
                            for x in total_lang:
                                print(" ",x.text.capitalize())
                                send_message = send_message + x.text.capitalize() + "\n"   
                            telegram_bot(send_message)
                        if flag3==1:
                            print("\n\n >> Select format not yet available\n\n    Available formats : ")
                            send_message = "Select format not yet available\n\nAvailable formats :\n"
                            for x in total_format:
                                print(" ",x.text.upper())
                                send_message = send_message + x.text.upper() + "\n"
                            telegram_bot(send_message)
                        if flag4==1:
                            print("\n\n >> Booking not yet available\n    We'll keep on looking")
                            telegram_bot("Booking not yet available\nWe'll keep on looking")
                            print_once = 1
                    sleep(500)
                    driver.refresh()

            try:            
                date_details = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='date-href']")))
                date_numeric = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='date-numeric']")))
                date_day = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='date-day']")))
            except:
                driver.get('https://in.bookmyshow.com')
                continue
            
            i=0
            while(True):
                if found==True:
                    break

                venues = long_wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='__venue-name']")))

                try:
                    if preferred_venue == '':
                        if show_time != '' :
                            long_wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li/div[2]/div[2]/div/a[@data-showtime-filter-index='" + str(show_time) +"']/div[1]/div[1]")))
                            for j in range(0,len(venues)):
                                if venues[j].text != '':
                                    print("\n\n",movie_name,"Booking Found on",date_numeric[i].text,date_day[i].text)
                                    print("\n Movie screening in these locations during",show_time,": \n")
                                    telegram_bot(movie_name+" Booking Found on "+date_numeric[i].text+" "+date_day[i].text)
                                    telegram_bot("Movie screening in these locations during "+show_time+" :")
                                    break
                        else:
                            for j in range(0,len(venues)):
                                if venues[j].text != '':
                                    print("\n\n",movie_name,"Booking Found on",date_numeric[i].text,date_day[i].text)
                                    print("\n Movie screening in these locations : \n")
                                    telegram_bot(movie_name+" Booking Found on "+date_numeric[i].text+" "+date_day[i].text)
                                    telegram_bot("Movie screening in these locations : ")
                                    break

                        for j in range(0,len(venues)):
                            if venues[j].text != '':
                                send_message = ""
                                send_message = send_message + venues[j].text + "\n"
                                if show_time != '' :
                                    show_times = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-name='" + str(venues[j].text) + "']/div[2]/div[2]/div/a[@data-showtime-filter-index='" + str(show_time) +"']/div[1]/div[1]")))
                                else:
                                    show_times = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-name='" + str(venues[j].text) + "']/div[2]/div[2]/div/a/div[1]/div[1]")))
                                print(" >> ",venues[j].text)
                                for k in range(0,len(show_times)):
                                    if show_times[k].text != '':
                                        print("    ",show_times[k].text)
                                        send_message = send_message + show_times[k].text + "\n"
                                telegram_bot(send_message)
                                print("\n")
                                found = True

                    if preferred_venue != '':
                        if show_time != '':
                            show_times = long_wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-name='" + str(preferred_venue) + "']/div[2]/div[2]/div/a[@data-showtime-filter-index='" + str(show_time) +"']/div[1]/div[1]")))
                            for j in range(0,len(show_times)):
                                if show_times[j].text != '':
                                    print("\n\n",movie_name,"Booking Found on",date_numeric[i].text,date_day[i].text)
                                    print("\n ",show_time.capitalize(),"show-times in",preferred_venue," :-\n")
                                    telegram_bot(movie_name+" Booking Found on "+date_numeric[i].text+" "+date_day[i].text)
                                    telegram_bot(show_time.capitalize()+" show times in "+preferred_venue+" :")
                                    break  
                        else:
                            show_times = long_wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@data-name='" + str(preferred_venue) + "']/div[2]/div[2]/div/a/div[1]/div[1]")))
                            for j in range(0,len(show_times)):
                                if show_times[j].text != '':
                                    print("\n\n",movie_name,"Booking Found on",date_numeric[i].text,date_day[i].text)
                                    print("\n Show-times in",preferred_venue," :-\n")
                                    telegram_bot(movie_name+" Booking Found on "+date_numeric[i].text+" "+date_day[i].text)
                                    telegram_bot("Show times in "+preferred_venue+" :")
                                    break
                        
                        send_message = ""
                        for j in range(0,len(show_times)):
                            if show_times[j].text != '':
                                print(" >> ",show_times[j].text)
                                send_message = send_message + show_times[j].text + "\n"
                        telegram_bot(send_message)
                        print("")
                        found = True

                    if found==True:
                        for i in range(20):
                            telegram_bot("Book Now")
                    
                except:
                    i=i+1
                    if i==len(date_details):
                        print("\n\n Not found any shows as per your request\n We'll keep on looking...")
                        telegram_bot("Haven't found any shows as per your requirement\nWe'll keep on looking...")
                        break

                    date_details[i].click()
                    sleep(5)
                    date_numeric = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='date-numeric']")))
                    date_day = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='date-day']")))
                    
            if found==True:
                break        
            else:
                sleep(300)
                    
    except:
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")
        if found!=True:
            driver.save_screenshot(current_time+'.png')
            telegram_bot("System Error, Restarting Run")
