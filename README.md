# BioAccess
This project is a clock-in/clock-out system that leverages the power of facial recognition for seamless employee authentication. The application provides a simple and efficient solution, allowing users to log their work hours with just a glance. This application is developed in Raspberry PI. The purpose of this project, is to illustrate how easy it is to implement biometric solutions to real-life scenarios. I have chosen face recognition as my method because of different reasons.

In the new era of authentication, the days of using PIN, RFID tags and password might become a thing of the past. As technology continues to advance, the technologies of authentication seem to improve and is a field of constant innovation. 

Two of the most popular biometric authentication methods are fingerprint scanning and face recognition. “Fingerprint recognition is a type of physical biometrics. For this authentication method, a fingerprint scanner is used to authenticate data”. According to Recogtech, fingerprint recognition is the most popular and best-known form of biometric security. In my research, I have found out that most businesses that implement biometrics, are using fingerprint scanning as a form of authentication. While fingerprint recognition is widely adopted and acknowledged for its convenience and effectiveness, it's important to consider the potential negative sides and concerns associated with this biometric authentication method.

The main negative side of using biometric solutions including fingerprints, is that the safety and accuracy can easily be affected by external factors. “Although it’s fast, it may be less convenient in certain situations, such as when a person’s hands are dirty or wet, or when a lot of people need to be identified at once. Also, it can be a potential health hazard in sensitive cases.”. 

In addition to this, the idea of fingerprint technology has undergone a significant shift, especially after the complications of the COVID-19 pandemic. Fingerprint scanning became problematic, since it was recommended by almost all countries to not have any form of physical contact with objects or humans for prevention of contagion. Since fingerprint technology requires physical contact, this became quite a problem for workplaces. Therefore, the biometric technology that I find more suitable for my case is face recognition.
“Facial recognition is a way of identifying or confirming an individual’s identity using their face. Facial recognition systems can be used to identify people in photos, videos, or in real-time.”. 

In comparison to fingerprint scanning, face recognition is a technology that requires no sensors or readers, except a camera. This makes face recognition an economic alternative, as well as a hygiene friendly method. Since face recognition requires no form for physical contact, it will be a method which is hygiene friendly and will be fully functional even in a future pandemic.

Therefore, I have made it my mission to create an administration system which is using face recognition as authentication. With this project, I hope to illustrate how easily face recognition can be implemented into a company, as I will demonstrate this in this project.

# Installation


For the smooth operation of this project, installing the necessary libraries and components is crucial. Begin by ensuring you have a Raspberry Pi and a Picamera module. Although it's possible to use a different operating system, please note that the program is specifically designed for Raspberry Pi (Linux), and compatibility on other platforms is not guaranteed.

Next, make sure you have Python and PIP installed. If not, you can follow the installation instructions here (https://packaging.python.org/en/latest/tutorials/installing-packages/). Additionally, you'll need your own MySQL-hosted database or set up MySQL in your workbench. To connect the script to your database, modify the information in the Main.py file at the beginning. Locate the variable named mydatabase and update it with your database details.

Managing libraries is made convenient for users with a provided requirement file containing all the necessary dependencies. To correctly install the application, download the project as a regular folder or unzip it if downloaded as a zip file. Open the command prompt (CMD), navigate to the downloaded folder using the "cd" command (e.g., cd downloads if the project is in the "downloads" folder), and execute the following code:


```python 
pip install -r requirements.txt
```


# Using the application

To execute this application, simply run the Main.py file. Ensure that all files are placed in the same folder, required libraries are installed, and the Camera module is connected. Run the file by entering the following command in the command prompt (CMD), assuming Python is already installed:


```python 
python Main.py
```

If you have python3, then this will be the correct code

```python 
python3 Main.py
```

Finally, the script essential for this project is included as the sole .sql file. To replicate a database similar to the one utilized in this project, execute the provided code in your MySQL Workbench. Run the script to set up the necessary database structure and configurations.

# Enjoy the application!
