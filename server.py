                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           __author__ = 'Guy'

import socket
from sys import *
import re
import subprocess
import os
import sys
from SocketServer import ThreadingMixIn
import thread
#from timeit import default_timer as timer
import time
import random
import platform
import urllib2
from PIL import ImageGrab
import shutil
import glob
import fnmatch
import sqlite3 as sql
import win32com.shell.shell as shell
'''
[server] - for tcp server events (bind, listen, accept)
[socket] - for socket events(send, recieve)
[!] - errors
[db] - for data base events
'''

PORT = 8880
IP = '127.0.0.1'
BUFFER_SIZE = 1024
END_THREAD = False
CONTINUE_THREAD = True

start_time = 0
admin = False


users_db_path = "users.db"
fonts_db_path = "fonts.db"
texts_db_path = "texts.db"

request_types_android = ["SIGNUP_2", "SIGNIN_2", "LOGOUT_2", "ERROR_2"]
request_types_pc = ["SIGNUP_1", "SIGNIN_1", "LOGOUT_1", "ERROR_1"]
request_types = ["SIGNUP", "SIGNIN", "LOGOUT", "ERROR"]
respond_types = ["SIGNUP_0","SIGNIN_0", "LOGOUT_0", "ERROR_0"]
logged_in_clients= {} #key: client_soc, value: dictionary of client - key: client_name, value: client_password

def main():

    '''start_time = time.time()
    if admin:
        respond = shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe')'''
    #print "ERR".startswith("ERROR")
    help_db_create_users_db()
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "[server] open socket"
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server.bind((IP, PORT))

    print "[server] binding successful"
    while True:
        tcp_server.listen(4)
        print "[server] listening..."
        client_soc, client_address = tcp_server.accept()
        thread.start_new_thread(handle_client, (client_soc, client_address))
    #help_test()

def handle_client(client_soc,client_address):

    print "[server] new connection"
    print"[.] ip:", client_address[0]
    print "[.] port:", client_address[1]
    #print "[.]socket:", str(client_soc.getpeername())
    _continue = CONTINUE_THREAD
    #_continue = END_THREAD

    while _continue == CONTINUE_THREAD :
        try:
            #get input from client
            client_data = help_socket_recieve_input(client_soc, BUFFER_SIZE)
            #parse input to message type and its arguments
            msg_type, args, platform = help_parse_request(client_data)
            #handle request
            _continue = handle_request(client_soc, msg_type, args, platform)
            #False if there was an error, True for continue loop
        except socket.error as err:
            print "socket error:", err.errno
            break
    if(help_is_client_connected(client_soc)):
        print"[server] client ",help_get_username_by_socket(client_soc), "logged out"
        help_remove_from_logged_in(client_soc)

    print"[socket] socket ",client_soc.getpeername(), "closed"
    client_soc.close()
    print"[server] End of thread"

'''def connect(client_soc, args):
    client_data = recieve_input(client_soc, BUFFER_SIZE)
    msg_type, args = parse_request(client_data)
    connected = connect(client_soc, args)
    respond = ""
    if (connected == True):
        respond = "yes"
    else:
        respond = "no"
    send_to_client(client_soc, "CONNECT_0", respond)
    #names_dict[client_soc] = args[0]'''

def handle_request(client_soc, msg_type, args, platform):
    '''
"SIGNUP_1"
"SIGNIN_1"
'''

    SIGNUP_LEN = 2 # username and password
    SIGNIN_LEN = 2 # username and password
    ERROR_LEN = 1 # error details


    connected = help_is_client_connected(client_soc)
    #is the client already singed up
    if(msg_type.startswith("LOGOUT")):
        return END_THREAD
    elif(msg_type.startswith("SIGNUP") and len(args) == SIGNUP_LEN):
        msg_signup(client_soc, args)
    elif (msg_type.startswith("SIGNIN") and len(args) == SIGNIN_LEN):
        msg_signin(client_soc, args)
    elif (msg_type.startswith("ERROR") and len(args) == ERROR_LEN):
        print"[!]client ", help_get_username_by_socket(client_soc) , "sent error"
        print "[.] error details - ", args[0]

        return END_THREAD
    else:
        error_type = ""
        if(not msg_type[0:-2] in request_types ):
            error_type = "unknown msg type"
        else:
            #print "[!] incorrect arguments for", msg_type, "request"
            error_type = "incorrect arguments for msg type"
        send_error_to_client(client_soc,error_type)
        return END_THREAD
    return CONTINUE_THREAD

def msg_signup(client_soc, args):
    username = args[0]
    password = args[1]
    return_msg = ""
    if(len(help_db_get_user(username)) == 0): #username isn't used
        if(help_db_add_user(username, password)):
            return_msg = "user added"
        else:
            return_msg = "an error has occurred while adding user to db"
            send_error_to_client(client_soc, return_msg)
            return
    else:
        return_msg = "username is already taken"
    help_socket_send_to_client(client_soc, "SIGNUP_0", return_msg)

def msg_signin(client_soc, args):
    username = args[0]
    password = args[1]
    return_msg = ""
    user = help_db_get_user(username)

    return_msg = "username or password is wrong"
    #print user[0], ",", user[1]
    #username = user[0][0]
    #print user
    #or not user[0][0] == username or not user[0][1] == password
    if(len(user) == 0 or not user[0][0] == username or not user[0][1] == password):
    #username doesn't exist or values don't match
        return_msg = "username or password is wrong"
    elif(help_is_client_connected(client_soc)):
        return_msg = "user is already logged in"
    else:
        return_msg = "successful sign in"
        help_add_to_logged_in(client_soc, username)
    help_socket_send_to_client(client_soc, "SIGNIN_0", return_msg)

def send_error_to_client(client_soc, error_type):
    print "[!]", error_type
    help_socket_send_to_client(client_soc, "ERROR_0", error_type)

'''def msg_echo(client_soc, args):
    send_to_client(client_soc, "ECHO_0", args[0])

def msg_give_ip(client_soc, args):
    ip = socket.gethostbyname(socket.gethostname())
    send_to_client(client_soc, "GIVEIP_0", ip)

def msg_up_time(client_soc, args): #sends the time since it's started running in seconds
    end_time = time.time()
    time_elapsed = end_time - start_time
    send_to_client(client_soc, "UPTIME_0", time_elapsed)

def msg_who_am_i(client_soc, args): #TD
    client_name = names_dict[client_soc]
    os_info = platform.system() + " " + platform.release() + " " + platform.version() #td
    os_path = os.pathsep #TD
    str_msg = "You are the username \"" + client_name + "\", Running \"" + os_info + \
                                                        "\" installed in \"" + os_path + "\""
    send_to_client(client_soc, "WHOAMI_0", str_msg)

def msg_move_to(client_soc, args):
    cd_path = args[0]
    respond = "moved cd"
    try:
        os.chdir(cd_path)
    except:
        respond = "not " + respond
    print "[&]" + respond + " to", cd_path
    send_to_client(client_soc, "MOVETO_0", respond)

def msg_run(client_soc, args):
    output = ""
    command = args[0]
    try:
        output = help_run_cmd(command)
        print output
    except:
        output = "command doesn't exist"
    send_to_client(client_soc, "RUN_0", output)

def msg_printf(client_soc, args):
    file_name = args[0]
    file_data = ""
    with open(file_name, 'r') as myfile:
        file_data = myfile.read()
    print "[&]printing text of", file_name, ":"
    print file_data
    help_send_file(client_soc, file_name, "PRINTF_0")


def msg_go_away_f(client_soc, args):
    file_name = args[0]
    respond = help_remove_file_or_dir(client_soc ,file_name, "d_file")
    send_to_client(client_soc, "GOAWAYF_0", respond)

def msg_go_away_d(client_soc, args):
        dir_name = args[0]
        respond = help_remove_file_or_dir(client_soc ,dir_name, "d_directory")
        send_to_client(client_soc, "GOAWAYD_0", respond)

def msg_make_f(client_soc, args):
    file_name = args[0]
    respond = ""
    #if os.path.isfile(file_name):
    respond = help_remove_file_or_dir(client_soc ,file_name, "m_file")
    if(respond == "not exist" or respond == "deleted"):
        open(file_name, 'w')
        respond = "created"
    elif respond == "not deleted":
        respond = "not created"
    send_to_client(client_soc, "MAKEF_0", respond)

def msg_make_d(client_soc, args):
    dir_name = args[0]
    respond = ""
    #if os.path.isdir(dir_name):
    respond = help_remove_file_or_dir(client_soc ,dir_name, "m_directory")
    if(respond == "not exist" or respond == "deleted"):
        os.mkdir(dir_name)
        respond = "created"
    elif respond == "not deleted":
        respond = "not created"
    send_to_client(client_soc, "MAKED_0", respond)

def msg_copyf(client_soc, args):
        copied_file_name = args[0]
        deleted_file_name = args[1]
        #respond = remove_file_or_dir(client_soc ,dir_name, "d_directory")
        file_data = ""
        respond = ""
        try:
            if(not os.path.isfile(copied_file_name)):
                respond = "file 1 not exist"
            else:
                with open(copied_file_name, 'r') as copied_file:
                    file_data = copied_file.read()
            deleted_file = open(deleted_file_name, 'w')
            deleted_file.write(file_data)
            respond = "copied"
        except:
            respond = "not copied"



        send_to_client(client_soc, "COPYF_0", respond)

def msg_exec(client_soc, args):
        file_name = args[0]
        #str(file_name).replace("\\", "\\\\")
        respond = ""
        if(help_is_exe(file_name)):
            try:
                output = help_run_cmd(file_name)
            except:
                respond = "couldn't run file"
        else:
            respond = "file is not exe"
        send_to_client(client_soc, "EXEC_0", respond)


def msg_dl(client_soc, args):
        file_name = args[0]
        help_send_file(client_soc, file_name, "DL_0")

def msg_ping(client_soc, args):
        destination = args[0]
        response = help_run_cmd("ping " + destination)
        send_to_client(client_soc, "PING_0", response)

def msg_get(client_soc, args):
        destination = args[0]
        if not r"http://" in str(destination):
            destination = r"http://" + destination
        response = urllib2.urlopen(destination).read()

        send_to_client(client_soc, "GET_0", response)

def msg_screenshot(client_soc, args):
    file_path = "ScreenShots\\" + time.strftime("%Y%m%d-%H%M%S") + ".png"
    ImageGrab.grab().save(file_path, "JPEG")
    help_send_file(client_soc, file_path, "SCREENSHOT_0")
    #send_to_client(client_soc, "SCREENSHOT_0", response)'''



#########################################################################################
#########################################################################################
####################                                                 ####################
####################                                                 ####################
####################                       Help                      ####################
####################                     Functions                   ####################
####################                                                 ####################
####################                                                 ####################
#########################################################################################
#########################################################################################

def help_test():
    command = ""
    while not command == "end":
        #CREATE TABLE USERS (USERNAME TEXT PRIMARY KEY NOT NULL, PASSWORD TEXT NOT NULL);
        # SELECT * FROM USERS WHERE username = 'guy'
        #INSERT INTO USERS VALUES('guy', '123456')

        command = raw_input(">>>")
        print help_db_exec(users_db_path, command)

def help_parse_request(requset_str): #type, args, platform - android or pc
    param_list = requset_str.split(r"\x")
    #print param_list[0]
    MIN_NUM_OF_PARAMETERS = 2
    if len(param_list) < MIN_NUM_OF_PARAMETERS :
        #print "[!]not enough parameters"
        return "",0,[],""
    msg_type = param_list[0]
    if not msg_type[0:-2] in request_types :
        return "",0,[],""
        #print "[!]unknown msg type"
    platform = "pc"
    if(msg_type[-1] == "2"):
        platform = "android"
    num_of_args = int(param_list[1])
    args_list = []
    if num_of_args > 0:
        args_list = param_list[2:]
    print "[.]type:", msg_type[0:-2]
    print "[.]args:", args_list
    print "[.]platform:", platform
    return msg_type, args_list, platform

def help_is_client_connected(client_soc):
    if(len(logged_in_clients) == 0):
        return False
    return (bool)(client_soc in logged_in_clients.keys())
def help_is_user_connected(username):
    if(len(logged_in_clients) == 0):
        return False
    return (bool)(username in logged_in_clients.values())

def help_get_username_by_socket(client_soc):
    if(help_is_client_connected(client_soc)):
        return logged_in_clients[client_soc]
    return ""

def help_add_to_logged_in(client_soc, username):
    logged_in_clients[client_soc] = username

def help_remove_from_logged_in(client_soc):
    logged_in_clients.pop(client_soc, None)

def help_encrypt_msg(str):
    #TODO - encrypt
    return str

def help_decrypt_msg(str):
    #TODO - decrypt
    return str

def help_encrypt_db(str):
    #TODO - encrypt
    return str

def help_decrypt_db(str):
    #TODO - decrypt
    return str


#########################################################################################
####################                                                 ####################
####################                      Socket                     ####################
####################                     Functions                   ####################
####################                                                 ####################
#########################################################################################

#help functions that actually use socket

def help_socket_recieve_input(client_soc, buffer_size):
    client_data = client_soc.recv(buffer_size)
    #print "msg - ", client_data
    client_data = help_encrypt_msg(client_data) #decrypt the data
    #client_data = raw_input()
    if(not help_is_client_connected(client_soc)):
        socket_name = client_soc.getpeername()
    else:
        socket_name = "user: " + help_get_username_by_socket(client_soc)

    print "[socket] msg from", socket_name

    return client_data

def help_socket_send_to_client(client_soc, msg_type, data):
    data_to_client = msg_type + r"\x" + data
    print "[socket] msg sent."
    print"[.]socket:",client_soc.getpeername()
    print "[.]type:", msg_type
    #data_to_client += data

    data_to_client = help_encrypt_msg(data_to_client) #encrypt the data
    #data_to_client += r"\x" #add \x to let client know that the msg ended

    client_soc.send(data_to_client)
    #print "data to client:", data_to_client

def help_socket_send_file(client_soc, file_name, msg_type):
    read = 'rb'
    '''if(msg_type == "SCREENSHOT_0"): #TODO - replace screeenshot
        read = 'rb'''''
    with open(file_name, read) as file:
        file_data = file.read() + r"\y\y\y"
    file_len = len(file_data)
    start = 0
    if(file_len < 1024):
        end = file_len
    else:
        end = 1024
    while start < end:
        msg = file_data[start : end]
        start = end
        if(end + 1024 > file_len):
            end = file_len
        else:
            end += 1024
        help_socket_send_to_client(client_soc, msg_type, msg)


#########################################################################################
####################                                                 ####################
####################                     Data Base                   ####################
####################                     Functions                   ####################
####################                                                 ####################
#########################################################################################

#help functions that actually use db

def help_db_create_users_db():

    print "[db] create users db"
    execute_msg = "CREATE TABLE IF NOT EXISTS USERS (NAME TEXT PRIMARY KEY NOT NULL, PASSWORD TEXT NOT NULL)"
    answer = help_db_exec(users_db_path, execute_msg)
    if(not answer == None and str(answer).startswith("error")):
        return str(answer).replace("error", "")

def help_db_get_user(username): #return (username, password). None if not existed

    print "[db] get user by username"
    execute_msg = "SELECT * FROM USERS WHERE NAME = \'" + username + "\'"
    user = help_db_exec(users_db_path, execute_msg)
    #print "user - ", user

    return user

def help_db_add_user(username, password): # returns true if successful insert, false if not
    success = True
    print "[db] add user"
    execute_msg = "INSERT INTO USERS VALUES(\'" + username + "\', \'" + \
    help_encrypt_db(password) + "\')"
    user = help_db_exec(users_db_path, execute_msg)
    if (type(user) == "list" and user.startswith("error")):
        print "[!] db error -", user.replace("error", "")
        success = False

    return success

def help_db_exec(db_path, execute_msg):
    answer = ""
    try:
        print "[.] open db  -", db_path
        db = sql.connect(db_path)
        print "[.] execute command:", execute_msg
        execute_msg = execute_msg.strip()
        cur = db.cursor()
        cur.execute(execute_msg) #execute the command
        db.commit()
        answer = cur.fetchall()
        print "[.] answer -", answer

    except sql.Error as e:
        #print "[!] An error occurred in db:"
        db.close()
        return "error", e.args[0]
    finally:
        print "[.] close db  -", db_path
        db.close()
        return answer

'''def help_remove_file_or_dir(client_soc, _path, _type):
    respond = ""
    answer = "no"
    msg_type = ""
    if(_type == "m_file"):
        msg_type = "MAKEF_0"
    elif(_type == "m_directory"):
        msg_type = "MAKED_0"

    if(((_type == "d_file" or _type == "m_file") and os.path.isfile(_path)) or \
      ((_type == "d_directory" or _type == "m_directory")and os.path.isdir(_path))):

        if _type == "m_file"or _type == "m_directory":

            print "[?] wait for agreement of client..."

            send_to_client(client_soc, msg_type, "exist")
            msg_type, args = parse_request(recieve_input(client_soc, BUFFER_SIZE))
            answer = ""
            if (len(args) > 0 and ((_type == "m_file" and msg_type == "MAKEF_1") or\
                                   (_type == "m_directory" and msg_type == "MAKED_1"))):
                answer = args[0]
            print"[?]client returned:", answer
        else:
            answer = "yes"
    else:
        send_to_client(client_soc, msg_type, "not exist")
        return "not exist"

    if(answer == "yes"):
        respond = help_delete_os(_type, _path)
    else:
        respond = "not deleted"


    return respond

def help_delete_os(_type, _path):
    try:
        if(_type[2:] == "file"):
            os.remove(_path)
        else:
            help_delete_files_in_directory(_path)
            os.rmdir(_path)
        print "[&]", _type[2:], "deleted"
        respond = "deleted"
    except OSError as detail:
        print "[!]", _type[2:], "not deleted"
        print"[!]Error details - ", detail.errno
        respond = "not deleted"
        pass
    return respond

def help_delete_files_in_directory(_path):
    if(os.path.isdir(_path)):
        file_list = os.listdir(_path)
        os.chdir(_path)
        for file in file_list:
            if(os.path.isdir(file)):
                help_delete_files_in_directory(file)
                os.rmdir(file)
            else:
                os.remove(file)
        os.chdir("..")

def help_is_exe(file_path):
        return os.path.exists(file_path) and \
               ((file_path.split('.')[-1]) == "exe" or not '.' in file_path)

def help_run_cmd(command):
    respond = ""
    try:
        respond = subprocess.check_output(command, shell = True)
        #respond =  subprocess.call(['runas', '/user:Administrator', command])
        #respond = shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+command)

    except:
        respond = ""
    return respond'''












if __name__ == "__main__":
    main()