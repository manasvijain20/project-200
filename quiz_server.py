import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 5500

server.bind((ip_address, port))
server.listen()
clients = []
nicknames = []

questions = ["Who was the very first 'American Idol' winner?\n a.Billie Eilish\n b.Kelly Clarkson\n c.Caleb Johnson\n d.Maddie Poppe",
             "What was Madonna's first top 10 hit?\n a.Holiday\n b.Material Girl\n c.Crazy for you\n d.Frozen",
             "Who is the only country artist to have a Top 20 hit on the Billboard Hot Country Songs chart for six straight decades?\n a.Doja Cat\n b.Carrie Underwood\n c.Blake Shelton\n d.Dolly Parton",
             "What is the name of the Rapper who does a featured guest appearance in Justin Bieber's 'Baby?'\n a.Ludacris\n b.Drake\n c.Eminem\n d.Lil Wayne",
             "Who officially became the Female Artist with the Most Grammy Awards in 2021?\n a.Madona\n b.Taylor Swift\n c.Beyonce\n d.Lady Gaga",
             "Which Miley Cyrus song mentions Jay-Z and Britney Spears?\n a.Wrecking Ball\n b.Party in The USA\n c.Midnight Sky\n d.Nobody's Perfect",
             "Who is the youngest singer to win four major categories at the Grammy Awards?\n a.Taylor Swift\n b.Billie EIlish\n c.Cardi B\n d.Melanie Martinez",
             "Who did Dua Lipa collaborate with on her 2018 single 'One Kiss', that went-on to win the 2019 Brit Award for Song Of The Year?\n a.Conan Gray\n b.Charlie Puth\n c.J Balvin\n d.Calvin Harris",
             "What female pop singer went on to become a billionaire with her cosmetics brand, Fenty Beauty?\n a.Rihanna\n b.Selena Gomez\n c.Kylie Jenner\n d.Ariana Grande",
             "Which of Katy Perry's albums has been her most successful?\n a.Teenage Dream\n b.Smile\n c.Prism\n d.Cosmic Energy",
             "Which musician was known as the “King of Pop”?\n a.Bruno Mars\n b.Ed sheeran\n c.Michael Jackson\n d.Harry Styles",
             "Which member of One Direction left the band to become a solo artist?\n a.Zayn Malik\n b.Harry Styles\n c.Niall Horan\n d.Liam Payne",
             "Which female artist released the song 'Summertime Sadness'?\n a.Beyonce\n b.Whitney Houston\n c.Lana Del Ray\n d.Sia",
             "What was Olivia Rodrigo's first No. 1 hit single?\n a.Driver's Liscence\n b.Good 4 You\n c.All I want\n d.Happier"]
answers = ['b','a','d','a','c','b','b','d','a','a','c','a','c','a']

print("server has started")
def get_random_question_answer(conn):
    random_index = random.randint(0, len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_answer, random_question, random_index

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn, nickname):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will recieve a question. The answer to the question should be one of a, b, c or d\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    print(answer)

    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message: 
                if message.split(": ")[-1].lower() == answer:
                    score += 1
                    conn.send("Bravo! your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect Answer! better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
                print(answer)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

def remove(connection):
    if connection in clients:
        clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    conn,addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    clients.append(conn)
    nicknames.append(nickname)
    print(nickname +" is connected!")
    new_thread = Thread(target=clientthread, args=(conn,nickname))
    new_thread.start()