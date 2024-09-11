                                                                                      SCRAPE


This project is created to solve the problem of making alerts and watchlist of the scrips of NEPSE for "FREE". This project provides :

1. Authentication System
2. Scrape Scrip

  ![image](https://github.com/user-attachments/assets/75adc5a4-170b-4f82-8daf-44adadc14218)
Scrape Scrip to know latest information about the scrip in market.

3. Create Alerts
  - User can create alerts for scrips of their choice.
  ![image](https://github.com/user-attachments/assets/015ce60f-a073-4f4c-a0af-3f89d6cde52f)

  - Can view their alerts list.
   ![image](https://github.com/user-attachments/assets/6ef940d7-9884-4e87-b0be-d14bd3ef1a05)

  - Can Delete their alerts.
    
4. Create Watchlist
   - User can create wathlist of their wish
    ![image](https://github.com/user-attachments/assets/3617cd5e-02b3-4b8d-99be-da7df44953a3)

    - Can view their watchlist
    ![image](https://github.com/user-attachments/assets/aed7dad2-34e2-4b28-9751-2b4af2c049a4)

5. Daily Market Status
   ![image](https://github.com/user-attachments/assets/9c6520e9-205d-48ce-aa45-cde6107425e3)

6. Alert Notification
  User gets notification if the Target gets met through their email.



                                                                              Run SCRAPE in your local device :

1. Clone the repository:
    git clone https://github.com/Temba23/scrape.git
   
2.Create env and install packages:
    pip install -r requirements.txt

3. Make migrations:
  python manage.py makemigrations
  python manage.py migrate

4. Run application:
  python manage.py runserver

Project By : Temba
