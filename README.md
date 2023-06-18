# Multiserver-Racing-Game
The project is a client server game, where the server can support multiple games at once, and each game contains up to 4 different clients. It uses TCP connections and a database to store the game states.

## How To Run

First, install pygame if it is not already installed.

'''bash
pip install pygame
'''

### SERVER

While in directory of the project:

'''bash
python server\main.py
'''

### CLIENT

While in directory of the project

'''bash
python client\main.py
'''


### LIBRARIES USED

'''python

#### client

import pygame
import pygame_gui
import atexit

#### server
import pickle #### dumps

import socket #### socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, SHUT_RDWR

import selectors #### DefaultSelector

import weakref #### WeakValueDictionary

import threading #### Thread

#### database

import django
