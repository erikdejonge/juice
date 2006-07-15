# Minimal headless iPodder.

# Taskbar code based on the win32gui_taskbar.py script.
# Helpful commentary:
# http://aspn.activestate.com/ASPN/Mail/Message/Python-win32/997525
# Also useful:
# http://www.itamarst.org/software/win32taskbar.py

from win32api import *
from win32gui import *
from win32gui_struct import PackMENUITEMINFO
import win32ui
from pywin.mfc import dialog

import timer
import win32con
import sys, os
import logging, logging.handlers
import threading
import pythoncom
import platform
import webbrowser
import StringIO
import time

import ipodder
from ipodder import configuration
from ipodder import conlogging
from ipodder import hooks
from ipodder import state as statemodule
from ipodder import core
from ipodder import grabbers
from gui import scheduler

log = logging.getLogger('Juice')
SPAM = logging.DEBUG / 2

TIMER_INTERVAL = 1000
LOGSIZE = 1024*1024
APP_NAME = "Minimal Juice Receiver"
QUIT_TIMEOUT = 5.0

class iPodderDownload(threading.Thread):
    def __init__(self,caller,mask=None,catchup=0):
        threading.Thread.__init__(self)
        self.caller = caller
        self.mask = mask
        self.catchup = catchup
    def run(self):
        if "Win" in platform.system():
            pythoncom.CoInitialize()

        try:
            self.caller.ipodder.start(None,self.mask,self.catchup)
        finally:
            self.caller.DownloadThreadComplete(self,self.mask)

        if "Win" in platform.system():
            pythoncom.CoUninitialize()

class MainWindow:
    def __init__(self,ipodder):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
                win32con.WM_COMMAND: self.OnCommand,
                win32con.WM_USER+20 : self.OnTaskbarNotify,
        }
        self.ipodder = ipodder
        
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "JuiceReceiver"
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        wc.hCursor = LoadCursor( 0, win32con.IDC_ARROW )
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)

        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom, APP_NAME, style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        self._DoCreateIcons()

        self.InitLogging()
        
        # Set up the background timer and scheduler.
        if scheduler.ensure_config(self.ipodder.config,\
                                   self.ipodder.config.schedule_file):
            self.ipodder.config.flush()
        self.s = scheduler.Scheduler(self.ipodder.config)
        self.s.initScheduledRuns()      
        self.t = timer.set_timer(TIMER_INTERVAL, self.OnTimer)
        self.running = False
        log.info("Scheduler set to run at: %s" % str(self.ipodder.config.sched_runTimes))
        log.info("Run mode is: %s" % self.ipodder.config.sched_runMode)

        self.progress = self.ipodder.console_progress
        self.quitting = False
        self.waiting_for_quit = False
        
    def _DoCreateIcons(self):
        hinst =  GetModuleHandle(None)
        iconPathName = os.path.abspath(os.path.join( os.path.split(sys.argv[0])[0], "icons_status", "hiPodder.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        self.hicon_idle = LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        hinst =  GetModuleHandle(None)
        iconPathName = os.path.abspath(os.path.join( os.path.split(sys.argv[0])[0], "icons_status", "hiPodder_running.ico" ))
        self.hicon_running = LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        self.icon_flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, self.icon_flags, win32con.WM_USER+20, self.hicon_idle, APP_NAME)
        Shell_NotifyIcon(NIM_ADD, nid)

    def _ModifyIcon(self,hicon,message=""):
        if message:
            tooltip = "%s - %s" % (APP_NAME,message)
        else:
            tooltip = APP_NAME            
        nid = (self.hwnd, 0, self.icon_flags, win32con.WM_USER+20, hicon, tooltip)
        Shell_NotifyIcon(NIM_MODIFY, nid)
        
    def OnRestart(self, hwnd, msg, wparam, lparam):
        self._DoCreateIcons()

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        self.quitting = True
        timer.kill_timer(self.t)
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        if self.running:
            if self.ipodder.download_engine:
                self.ipodder.download_engine.stop(timeout=3)
                begin = time.time()
                delay = time.time() - begin
                while self.running and delay < QUIT_TIMEOUT:
                    time.sleep(0.1)
                    delay = time.time() - begin
        PostQuitMessage(0) # Terminate the app.

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam==win32con.WM_LBUTTONUP:
            pass
        elif lparam==win32con.WM_LBUTTONDBLCLK:
            #DestroyWindow(self.hwnd)
            self.OnSetup()
        elif lparam==win32con.WM_RBUTTONUP:
            menu = CreatePopupMenu()
            AppendMenu( menu, win32con.MF_STRING, 1024, "Sync now")
            AppendMenu( menu, win32con.MF_STRING, 1026, "Open log")
            AppendMenu( menu, win32con.MF_STRING, 1027, "Preferences")
            AppendMenu( menu, win32con.MF_STRING, 1023, "Setup")
            AppendMenu( menu, win32con.MF_STRING, 1025, "Exit program" )
            if self.running:
                info, extras = PackMENUITEMINFO(fState=win32con.MF_GRAYED)
                SetMenuItemInfo(menu,0,True,info)
            # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
            SetForegroundWindow(self.hwnd)
            pos = GetCursorPos()
            TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
            PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return 1

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = LOWORD(wparam)
        if id == 1023:
            self.OnSetup()
        elif id == 1024:
            self.OnCheckNow()
        elif id == 1025:
            DestroyWindow(self.hwnd)
        elif id == 1026:
            self.OnShowLog()
        elif id == 1027:
            self.OnPreferences()
        else:
            log.info("Unknown command -", id)

    def OnTimer(self, id, time):
        if self.ipodder.config.deferred_exception:
            temp_exception = self.ipodder.config.deferred_exception
            self.ipodder.config.deferred_exception = None
            if isinstance(temp_exception, configuration.ConfigManagerFirstRunError):
                self.OnSetup()
                return
            else:
                MessageBox(self.hwnd, str(temp_exception).strip('"'), "Error.", win32con.MB_OK)
                return
            
        if self.running:
            return
        
        if self.s.checkTimeToRun():
            self.s.logLastRun()
            self.OnCheckNow()    

    def OnCheckNow(self):
        self.running = True
        self._ModifyIcon(self.hicon_running,"Running")
        self.UpdateSubscriptions()
        dl = iPodderDownload(self)
        dl.setDaemon(True)
        dl.start()

    def DownloadThreadComplete(self,dl,mask):
        if not self.quitting:
            self._ModifyIcon(self.hicon_idle)
        self.running = False
        
    def InitLogging(self):
        newHandler = logging.handlers.RotatingFileHandler( \
            os.path.join(self.ipodder.config.appdata_dir,"hJuice.log"),maxBytes=LOGSIZE)
        newHandler.formatter = logging.Formatter("[%(asctime)s] %(message)s")
        otherHandlers = []
        for handler in log.handlers: 
            if isinstance(handler, logging.handlers.MemoryHandler): 
                handler.setTarget(newHandler)
                handler.flush()
            else: 
                otherHandlers.append(handler)
        log.handlers = otherHandlers
        log.addHandler(newHandler)

    def OnSetup(self):
        userid, password = GetLogin("Setup", self.ipodder.config.config_manager_username, \
                                    self.ipodder.config.config_manager_password)
        if userid != None:
            log.info("userid = %s" % userid)
        if password != None:
            log.info("password has %d characters" % len(password))
        if userid != None and password != None:
            self.ipodder.config.config_manager_username = userid
            self.ipodder.config.config_manager_password = password
            try:
                self.ipodder.config.load_remote_config()
                MessageBox(self.hwnd, "Login successful.", "Login successful.", win32con.MB_OK)
            except configuration.ConfigManagerConnectError, ex:
                log.info("Got error: %s" % str(ex))
                MessageBox(self.hwnd, str(ex).strip('"'), "Error connecting.", win32con.MB_OK)
                self.OnSetup()
                
    def OnShowLog(self):
        pathname = os.path.join(self.ipodder.config.appdata_dir,"hJuice.log")
        if os.path.exists(pathname):
            os.spawnv(os.P_NOWAIT, \
                  os.environ["COMSPEC"], \
                  ["/Q","/C",'notepad "%s"' % pathname])
    def OnPreferences(self):
        webbrowser.open(self.ipodder.config.config_manager_settings_url)

    def UpdateSubscriptions(self):
        if self.ipodder.config.feedmanager_enable and \
           self.ipodder.config.feedmanager_opml_url != '':
            opml_url = self.ipodder.config.feedmanager_opml_url
            
            sio = StringIO.StringIO()
            grabber = grabbers.BasicGrabber(opml_url, sio, politeness=0)
            try: 
                grabber()
            except grabbers.GrabError, ex: 
                log.error("Can't grab %s: %s", url, ex.message)
                return

            opml = sio.getvalue()
            self.ipodder.feeds.replace_from_manager_opml(opml_url,opml)

        
def MakeLoginDlgTemplate(title):
	style = win32con.DS_MODALFRAME | win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.DS_SETFONT
	cs = win32con.WS_CHILD | win32con.WS_VISIBLE

	# Window frame and title
	dlg = [ [title, (0, 0, 184, 40), style, None, (8, "MS Sans Serif")], ]

	# ID label and text box
	dlg.append([130, "User ID:", -1, (7, 9, 69, 9), cs | win32con.SS_LEFT])
	s = cs | win32con.WS_TABSTOP | win32con.WS_BORDER 
	dlg.append(['EDIT', None, win32ui.IDC_EDIT1, (50, 7, 60, 12), s])

	# Password label and text box
	dlg.append([130, "Password:", -1, (7, 22, 69, 9), cs | win32con.SS_LEFT])
	s = cs | win32con.WS_TABSTOP | win32con.WS_BORDER 
	dlg.append(['EDIT', None, win32ui.IDC_EDIT2, (50, 20, 60, 12), s | win32con.ES_PASSWORD])

	# OK/Cancel Buttons
	s = cs | win32con.WS_TABSTOP 
	dlg.append([128, "OK", win32con.IDOK, (124, 5, 50, 14), s | win32con.BS_DEFPUSHBUTTON])
	s = win32con.BS_PUSHBUTTON | s
	dlg.append([128, "Cancel", win32con.IDCANCEL, (124, 20, 50, 14), s])
	return dlg

class LoginDlg(dialog.Dialog):
	def __init__(self, title):
            dialog.Dialog.__init__(self, MakeLoginDlgTemplate(title) )
            self.AddDDX(win32ui.IDC_EDIT1,'userid')
            self.AddDDX(win32ui.IDC_EDIT2,'password')

def GetLogin(title='Login', userid='', password=''):
	d = LoginDlg(title)
	d['userid'] = userid
	d['password'] = password
	if d.DoModal() != win32con.IDOK:
		return (None, None)
	else:	
		return (d['userid'], d['password'])

def MakeOkDlgTemplate(title):
	style = win32con.DS_MODALFRAME | win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.DS_SETFONT
	cs = win32con.WS_CHILD | win32con.WS_VISIBLE

	# Window frame and title
	dlg = [ [title, (0, 0, 184, 40), style, None, (8, "MS Sans Serif")], ]

	# OK/Cancel Buttons
	s = cs | win32con.WS_TABSTOP 
	dlg.append([128, "OK", win32con.IDOK, (124, 5, 50, 14), s | win32con.BS_DEFPUSHBUTTON])
	s = win32con.BS_PUSHBUTTON | s
	dlg.append([128, "Cancel", win32con.IDCANCEL, (124, 20, 50, 14), s])
	return dlg

class OkCancelDlg(dialog.Dialog):
	def __init__(self, title):
            dialog.Dialog.__init__(self, MakeOkDlgTemplate(title) )
    
def main():
    # Initialise the logging module and configure it for our console logging.
    # I'll factor this out soon so it's less convoluted.
    logging.basicConfig()
    handler = logging.handlers.MemoryHandler(65536)
    handler.formatter = conlogging.ConsoleFormatter("%(message)s", wrap=False)
    log.addHandler(handler)
    log.propagate = 0
    logging.addLevelName(SPAM, "SPAM")
    
    # Parse our configuration files.
    # I'll factor this out soon so it's less convoluted.
    parser = configuration.makeCommandLineParser()
    options, args = parser.parse_args()
    if args:
        parser.error("only need options; no arguments.")
    if options.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    deferred_exception = None
    try:
        config = configuration.Configuration(options)
    except configuration.ConfigManagerConnectError, ex:
        deferred_exception = ex
    except configuration.ConfigManagerFirstRunError, ex:
        deferred_exception = ex
    if options.debug: # just in case config file over-rode it
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    # Tweak our sub-log detail.
    hooks.log.setLevel(logging.INFO)
    
    # Open our state database.
    state = statemodule.open(config)
    
    # Initialise our iPodder.
    ipodder = core.iPodder(config, state)

    # Run it. 
    try: 
        w=MainWindow(ipodder)
        PumpMessages()
    finally: 
        ipodder.state.close()  

if __name__=='__main__':
    main()
