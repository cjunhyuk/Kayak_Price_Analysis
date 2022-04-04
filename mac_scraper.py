from time import sleep, strftime
from datetime import date, timedelta
from random import randint
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

import smtplib
from email.mime.multipart import MIMEMultipart
import os

