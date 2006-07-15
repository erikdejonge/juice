; $Id: iPodder2.2.nsi,v 1.17 2005/11/11 07:12:43 aegrumet Exp $
;
; Please edit file with windows line feeds so that it can be edited
; within the windows enviroment. -- sgrayban
;
; Script generated by the HM NIS Edit Script Wizard.


BGGradient 000000 FEF42 FFFFFF
XPStyle on

;; These are set to default values (NSIS v2.02) so we
;; probably don't need them.
SetDateSave on
SetDatablockOptimize on
CRCCheck on
SilentInstall normal


; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Juice"
!define PRODUCT_VERSION "2.2"
!define PRODUCT_PUBLISHER "Juice Team"
!define PRODUCT_WEB_SITE "http://juicereceiver.sourceforge.net/"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\Juice.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "C:\juice\icons_status\installer_icon.ico"
!define MUI_UNICON "C:\juice\icons_status\installer_icon.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "..\gpl.txt"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Components page
!insertmacro MUI_PAGE_COMPONENTS
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\Juice.exe"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\readme.txt"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "Juice22Setup.exe"
InstallDir "$PROGRAMFILES\Juice"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Section "-Juice" SEC01
  FindProcDLL::FindProc "Juice.exe"
  StrCmp $R0 "1" concurrentproc
  FindProcDLL::FindProc "iPodder.exe"
  StrCmp $R0 "0" readytowrite

  concurrentproc:

  MessageBox MB_RETRYCANCEL "Another copy of Juice is running.  Please quit Juice before continuing by selecting File -> Quit or right-clicking on the Lemon icon in the system tray and selecting Quit." IDCANCEL cancel


  FindProcDLL::FindProc "Juice.exe"
  StrCmp $R0 "1" concurrentproc
  FindProcDLL::FindProc "iPodder.exe"
  StrCmp $R0 "1" concurrentproc
  StrCmp $R0 "0" readytowrite

  cancel:

  Abort "Can't install"

  readytowrite:

  SetOutPath "$INSTDIR"

  SetOverwrite off
  File "..\dist\favorites.txt"
  SetOverwrite ifnewer
  File "..\dist\datetime.pyd"
  File "..\dist\gpl.txt"
  SetOverwrite on
  SetOutPath "$INSTDIR\gui"
  File "..\dist\gui\iPodder.xrc"
  SetOutPath "$INSTDIR\icons_status"
  File "..\dist\icons_status\application.ico"
  File "..\dist\icons_status\application_small.ico"
  File "..\dist\icons_status\box-checked.png"
  File "..\dist\icons_status\box-unchecked.png"
  File "..\dist\icons_status\icon_checkselected20.png"
  File "..\dist\icons_status\icon_disabled.ico"
  File "..\dist\icons_status\icon_downloading.ico"
  File "..\dist\icons_status\icon_episode_blank.gif"
  File "..\dist\icons_status\icon_episode_downloading.gif"
  File "..\dist\icons_status\icon_episode_paused.gif"
  File "..\dist\icons_status\icon_episode_problem_broken.gif"
  File "..\dist\icons_status\icon_episode_problem_intact.gif"
  File "..\dist\icons_status\icon_episode_up-downloading.gif"
  File "..\dist\icons_status\icon_episode_uploading.gif"
  File "..\dist\icons_status\icon_feed_checking.gif"
  File "..\dist\icons_status\icon_feed_disabled.gif"
  File "..\dist\icons_status\icon_feed_disabled.png"
  File "..\dist\icons_status\icon_feed_downloading.gif"
  File "..\dist\icons_status\icon_feed_downloading.png"
  File "..\dist\icons_status\icon_feed_idle.gif"
  File "..\dist\icons_status\icon_feed_idle_empty.gif"
  File "..\dist\icons_status\icon_feed_idle_empty.png"
  File "..\dist\icons_status\icon_feed_unsubscribed.gif"
  File "..\dist\icons_status\icon_feed_synced.png"
  File "..\dist\icons_status\icon_idle_empty.ico"
  File "..\dist\icons_status\icon_newitem.ico"
  File "..\dist\icons_status\icon_notconnected.ico"
  File "..\dist\icons_status\icon_scanning_feeds.ico"
  File "..\dist\icons_status\netflder.png"
  File "..\dist\icons_status\netflder_open.png"
  File "..\dist\icons_status\play-file.png"
  File "..\dist\icons_status\remote-sub.png"
  File "..\dist\icons_status\remote.png"
  File "..\dist\icons_status\sorting_arrow_down.png"
  File "..\dist\icons_status\sorting_arrow_up.png"
  File "..\dist\icons_status\tb_icon23_checkfeed.png"
  File "..\dist\icons_status\tb_icon25_addfeed.png"
  File "..\dist\icons_status\tb_icon25_canceldownload.png"
  File "..\dist\icons_status\tb_icon25_catchup.png"
  File "..\dist\icons_status\tb_icon25_checkfeed.gif"
  File "..\dist\icons_status\tb_icon25_checkfeed.png"
  File "..\dist\icons_status\tb_icon25_checkselectedfeed.png"
  File "..\dist\icons_status\tb_icon25_deletefeed.gif"
  File "..\dist\icons_status\tb_icon25_deletefeed.png"
  File "..\dist\icons_status\tb_icon25_dir_closeall.png"
  File "..\dist\icons_status\tb_icon25_dir_openall.png"
  File "..\dist\icons_status\tb_icon25_dir_refresh.png"
  File "..\dist\icons_status\tb_icon25_feedproperties.png"
  File "..\dist\icons_status\tb_icon25_pausedownload.png"
  File "..\dist\icons_status\tb_icon25_removelines.png"
  File "..\dist\icons_status\tb_icon25_scheduler_off.png"
  File "..\dist\icons_status\tb_icon25_scheduler_on.png"
  File "..\dist\icons_status\tb_icon25_spotlight.png"
  SetOutPath "$INSTDIR\images"
  File "..\dist\images\about_logo.bmp"
  File "..\dist\images\badge_ipodder.gif"
  File "..\dist\images\banner.png"
  File "..\dist\images\donate_header_please.bmp"
  File "..\dist\images\donate_header_thanks.bmp"
  File "..\dist\images\newlogo_ipodder_animated.gif"
  File "..\dist\images\paypal.gif"
  File "..\dist\images\spacer.gif"
  File "..\dist\images\splashscreen.bmp"
  SetOutPath "$INSTDIR"
  File "..\dist\Juice.exe"
  CreateDirectory "$SMPROGRAMS\Juice"
  CreateShortCut "$SMPROGRAMS\Juice\Juice.lnk" "$INSTDIR\Juice.exe"
  CreateShortCut "$DESKTOP\Juice.lnk" "$INSTDIR\Juice.exe"
  File "..\dist\Juice.exe.manifest"
  File "..\dist\library.zip"
  File "..\dist\pyexpat.pyd"
  File "..\dist\python23.dll"
  File "..\dist\pythoncom23.dll"
  File "..\dist\pywintypes23.dll"
  File "..\dist\readme.txt"
  File "..\dist\select.pyd"
  File "..\dist\unicodedata.pyd"
  File "..\dist\w9xpopen.exe"
  SetOutPath "$INSTDIR\win32"
  File "..\dist\win32\iPodder.ico"
  SetOutPath "$INSTDIR"
  File "..\dist\win32api.pyd"
  File "..\dist\win32clipboard.pyd"
  File "..\dist\win32evtlog.pyd"
  File "..\dist\win32file.pyd"
  File "..\dist\win32gui.pyd"
  File "..\dist\win32pipe.pyd"
  File "..\dist\win32process.pyd"
  File "..\dist\win32ui.pyd"
  File "..\dist\wxmsw253uh_vc.dll"
  File "..\dist\zlib.pyd"
  File "..\dist\_bsddb.pyd"
  File "..\dist\_controls_.pyd"
  File "..\dist\_core_.pyd"
  File "..\dist\_gdi_.pyd"
  File "..\dist\_html.pyd"
  File "..\dist\_misc_.pyd"
  File "..\dist\_socket.pyd"
  File "..\dist\_sre.pyd"
  File "..\dist\_ssl.pyd"
  File "..\dist\_win32sysloader.pyd"
  File "..\dist\_windows_.pyd"
  File "..\dist\_winreg.pyd"
  File "..\dist\_xrc.pyd"
  SetOutPath "$INSTDIR\localization\catalog"
  File "..\dist\localization\catalog\ca.py"
  File "..\dist\localization\catalog\da.py"
  File "..\dist\localization\catalog\de.py"
  File "..\dist\localization\catalog\el.py"
  File "..\dist\localization\catalog\en.py"
  File "..\dist\localization\catalog\es.py"
  File "..\dist\localization\catalog\et.py"
  File "..\dist\localization\catalog\eu.py"
  File "..\dist\localization\catalog\fi.py"
  File "..\dist\localization\catalog\fr.py"
  File "..\dist\localization\catalog\gl.py"
  File "..\dist\localization\catalog\he.py"
  File "..\dist\localization\catalog\hu.py"
  File "..\dist\localization\catalog\it.py"
  File "..\dist\localization\catalog\ja.py"
  File "..\dist\localization\catalog\ko.py"
  File "..\dist\localization\catalog\nl.py"
  File "..\dist\localization\catalog\pl.py"
  File "..\dist\localization\catalog\pt-BR.py"
  File "..\dist\localization\catalog\ru.py"
  File "..\dist\localization\catalog\sr.py"
  File "..\dist\localization\catalog\sv.py"
  File "..\dist\localization\catalog\zh-Hans.py"
  File "..\dist\localization\catalog\__init__.py"
  SetOutPath "$INSTDIR\plugins"
  File "..\dist\plugins\description_links.py"
  SetOutPath "$INSTDIR\compat"
  File "..\dist\compat\__init__.py"
  SetOutPath "$INSTDIR\compat\2x"
  File "..\dist\compat\2x\__init__.py"
  File "..\dist\compat\2x\iPodder.py"
  SetOutPath "$INSTDIR\docs"
  File "..\dist\docs\JuiceUserGuide.html"
SectionEnd

Section "Desktop shortcut"
  CreateShortCut "$DESKTOP\Juice.lnk" "$INSTDIR\Juice.exe"
SectionEnd

Section /o "Add to Startup Group"
  CreateShortCut "$SMSTARTUP\Juice.lnk" "$INSTDIR\Juice.exe"
SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\Juice\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\Juice\Uninstall.lnk" "$INSTDIR\uninst.exe"
  CreateShortCut "$SMPROGRAMS\Juice\UserGuide.lnk" "$INSTDIR\docs\JuiceUserGuide.html"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\Juice.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\Juice.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"

  ; File type registrations
  WriteRegStr HKCR "Applications\Juice.exe" "" "Juice"
  WriteRegStr HKCR "Applications\Juice.exe\shell\open\command" "" "$\"$INSTDIR\Juice.exe$\" --open $\"%1$\""
  WriteRegStr HKCR "Applications\Juice.exe\DefaultIcon" "" "$INSTDIR\icons_status\application.ico,1"
  WriteRegStr HKCR "Juice.rss" "" "Podcast Subscription File"
  WriteRegStr HKCR "Juice.rss\shell\open\command" "" "$\"$INSTDIR\Juice.exe$\" --add-feed-from-rss $\"%1$\""
  WriteRegStr HKCR ".rss\OpenWithList\Juice.exe" "" ""
  WriteRegBin HKCR ".rss\OpenWithProgIds" "Juice.rss" 0
  WriteRegStr HKCR "Juice.pcast" "" "Podcast Subscription File"
  WriteRegStr HKCR "Juice.pcast\shell\open\command" "" "$\"$INSTDIR\Juice.exe$\" --add-feed-from-pcast $\"%1$\""
  WriteRegStr HKCR ".pcast\OpenWithList\Juice.exe" "" ""
  WriteRegBin HKCR ".pcast\OpenWithProgIds" "Juice.pcast" 0

SectionEnd

Function .onInit

  ReadRegStr $R0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "UninstallString"

  ReadRegStr $R2 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "DisplayVersion"
  ; For future OS detection using the General.nsh macro file
  ; Need version.dll and General.nsh from the nsis_tools directory.
  ; Read the README.txt in the win32/nsis_tools/
  ; -- sgrayban
  ; !include "General.nsh"
  ; !define winNT
  ; !insertmacro CHECKWINVER

FunctionEnd

Function .onInstSuccess

  StrCmp $R0 "" done
  StrCmp $R2 "1.0.0" onePointOh
  StrCmp $R2 "1.1" onePointEx
  StrCmp $R2 "1.1.2" onePointEx
  StrCmp $R2 "1.1.3" onePointEx
  StrCmp $R2 "1.1.4" onePointEx

  ;Assume done for all unknown release numbers.
  Goto done
  
  onePointOh:  
  ; They're upgrading from 1.0
  
  ; $R0 is the 1.0 uninstall string.  It should look like this: 1.0INSTDIR\uninst.exe
  ; $R1 is the old installation directory.
  StrCpy $R1 $R0 -11
  
  ExpandEnvStrings $0 "%APPDATA%"

  StrCmp $0 "%APPDATA%" 0 +2
    ExpandEnvStrings $0 "%HOMEDRIVE%%HOMEPATH%\Application Data"

  IfFileExists $0\*.* 0 done
  IfFileExists $0\iPodder\*.* +2 0
    CreateDirectory $0\iPodder

  ;copy any old configuration
  IfFileExists $0\iPodder\history.txt +3 0
  IfFileExists $R1\history.txt 0 +2
  CopyFiles $R1\history.txt $0\iPodder

  IfFileExists $0\iPodder\schedule.txt +3 0
  IfFileExists $R1\schedule.txt 0 +2
  CopyFiles $R1\schedule.txt $0\iPodder
  
  IfFileExists $0\iPodder\favorites.txt +3 0
  IfFileExists $R1\favorites.txt 0 +2
  CopyFiles $R1\favorites.txt $0\iPodder

  onePointEx:
  ;They're upgrading from 1.1 - 1.1.4.  Backup the state db in case they want to go back.

  ExpandEnvStrings $0 "%APPDATA%"

  StrCmp $0 "%APPDATA%" 0 +2
    ExpandEnvStrings $0 "%HOMEDRIVE%%HOMEPATH%\Application Data"

  IfFileExists $0\iPodder\iPodder.db 0 +3
    CopyFiles $0\iPodder\iPodder.db $0\iPodder\iPodder.db-$R2
    ;MessageBox MB_OK "iPodder $R2 data backed up to $0\iPodder\iPodder.db-$R2"

  done:

FunctionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\readme.txt"
  Delete "$INSTDIR\_xrc.pyd"
  Delete "$INSTDIR\_winreg.pyd"
  Delete "$INSTDIR\_win32sysloader.pyd"
  Delete "$INSTDIR\_windows_.pyd"
  Delete "$INSTDIR\_ssl.pyd"
  Delete "$INSTDIR\_sre.pyd"
  Delete "$INSTDIR\_socket.pyd"
  Delete "$INSTDIR\_misc_.pyd"
  Delete "$INSTDIR\_html.pyd"
  Delete "$INSTDIR\_gdi_.pyd"
  Delete "$INSTDIR\_core_.pyd"
  Delete "$INSTDIR\_controls_.pyd"
  Delete "$INSTDIR\_bsddb.pyd"
  Delete "$INSTDIR\zlib.pyd"
  Delete "$INSTDIR\wxmsw253uh_vc.dll"
  Delete "$INSTDIR\win32ui.pyd"
  Delete "$INSTDIR\win32process.pyd"
  Delete "$INSTDIR\win32pipe.pyd"
  Delete "$INSTDIR\win32gui.pyd"
  Delete "$INSTDIR\win32file.pyd"
  Delete "$INSTDIR\win32evtlog.pyd"
  Delete "$INSTDIR\win32clipboard.pyd"
  Delete "$INSTDIR\win32api.pyd"
  Delete "$INSTDIR\win32\iPodder.ico"
  Delete "$INSTDIR\w9xpopen.exe"
  Delete "$INSTDIR\unicodedata.pyd"
  Delete "$INSTDIR\select.pyd"
  Delete "$INSTDIR\readme.txt"
  Delete "$INSTDIR\pywintypes23.dll"
  Delete "$INSTDIR\pythoncom23.dll"
  Delete "$INSTDIR\python23.dll"
  Delete "$INSTDIR\pyexpat.pyd"
  Delete "$INSTDIR\library.zip"
  Delete "$INSTDIR\Juice.exe.manifest"
  Delete "$INSTDIR\Juice.exe"
  Delete "$INSTDIR\images\splashscreen.bmp"
  Delete "$INSTDIR\images\spacer.gif"
  Delete "$INSTDIR\images\paypal.gif"
  Delete "$INSTDIR\images\newlogo_ipodder_animated.gif"
  Delete "$INSTDIR\images\donate_header_thanks.bmp"
  Delete "$INSTDIR\images\donate_header_please.bmp"
  Delete "$INSTDIR\images\badge_ipodder.gif"
  Delete "$INSTDIR\images\banner.png"
  Delete "$INSTDIR\images\about_logo.bmp"
  Delete "$INSTDIR\icons_status\tb_icon25_spotlight.png"
  Delete "$INSTDIR\icons_status\tb_icon25_scheduler_on.png"
  Delete "$INSTDIR\icons_status\tb_icon25_scheduler_off.png"
  Delete "$INSTDIR\icons_status\tb_icon25_removelines.png"
  Delete "$INSTDIR\icons_status\tb_icon25_pausedownload.png"
  Delete "$INSTDIR\icons_status\tb_icon25_feedproperties.png"
  Delete "$INSTDIR\icons_status\tb_icon25_dir_refresh.png"
  Delete "$INSTDIR\icons_status\tb_icon25_dir_openall.png"
  Delete "$INSTDIR\icons_status\tb_icon25_dir_closeall.png"
  Delete "$INSTDIR\icons_status\tb_icon25_deletefeed.png"
  Delete "$INSTDIR\icons_status\tb_icon25_deletefeed.gif"
  Delete "$INSTDIR\icons_status\tb_icon25_checkselectedfeed.png"
  Delete "$INSTDIR\icons_status\tb_icon25_checkfeed.png"
  Delete "$INSTDIR\icons_status\tb_icon25_checkfeed.gif"
  Delete "$INSTDIR\icons_status\tb_icon25_catchup.png"
  Delete "$INSTDIR\icons_status\tb_icon25_canceldownload.png"
  Delete "$INSTDIR\icons_status\tb_icon25_addfeed.png"
  Delete "$INSTDIR\icons_status\tb_icon23_checkfeed.png"
  Delete "$INSTDIR\icons_status\sorting_arrow_up.png"
  Delete "$INSTDIR\icons_status\sorting_arrow_down.png"
  Delete "$INSTDIR\icons_status\remote.png"
  Delete "$INSTDIR\icons_status\remote-sub.png"
  Delete "$INSTDIR\icons_status\play-file.png"
  Delete "$INSTDIR\icons_status\netflder_open.png"
  Delete "$INSTDIR\icons_status\netflder.png"
  Delete "$INSTDIR\icons_status\icon_notconnected.ico"
  Delete "$INSTDIR\icons_status\icon_scanning_feeds.ico"
  Delete "$INSTDIR\icons_status\icon_newitem.ico"
  Delete "$INSTDIR\icons_status\icon_idle_empty.ico"
  Delete "$INSTDIR\icons_status\icon_feed_unsubscribed.gif"
  Delete "$INSTDIR\icons_status\icon_feed_synced.png"
  Delete "$INSTDIR\icons_status\icon_feed_idle_empty.png"
  Delete "$INSTDIR\icons_status\icon_feed_idle_empty.gif"
  Delete "$INSTDIR\icons_status\icon_feed_idle.gif"
  Delete "$INSTDIR\icons_status\icon_feed_downloading.png"
  Delete "$INSTDIR\icons_status\icon_feed_downloading.gif"
  Delete "$INSTDIR\icons_status\icon_feed_disabled.png"
  Delete "$INSTDIR\icons_status\icon_feed_disabled.gif"
  Delete "$INSTDIR\icons_status\icon_feed_checking.gif"
  Delete "$INSTDIR\icons_status\icon_episode_uploading.gif"
  Delete "$INSTDIR\icons_status\icon_episode_up-downloading.gif"
  Delete "$INSTDIR\icons_status\icon_episode_problem_intact.gif"
  Delete "$INSTDIR\icons_status\icon_episode_problem_broken.gif"
  Delete "$INSTDIR\icons_status\icon_episode_paused.gif"
  Delete "$INSTDIR\icons_status\icon_episode_downloading.gif"
  Delete "$INSTDIR\icons_status\icon_episode_blank.gif"
  Delete "$INSTDIR\icons_status\icon_downloading.ico"
  Delete "$INSTDIR\icons_status\icon_disabled.ico"
  Delete "$INSTDIR\icons_status\icon_checkselected20.png"
  Delete "$INSTDIR\icons_status\box-unchecked.png"
  Delete "$INSTDIR\icons_status\box-checked.png"
  Delete "$INSTDIR\icons_status\application.ico"
  Delete "$INSTDIR\icons_status\application_small.ico"
  Delete "$INSTDIR\gui\iPodder.xrc"
  Delete "$INSTDIR\gpl.txt"
  Delete "$INSTDIR\favorites.txt"
  Delete "$INSTDIR\datetime.pyd"
  Delete "$INSTDIR\localization\catalog\ca.py"
  Delete "$INSTDIR\localization\catalog\da.py"
  Delete "$INSTDIR\localization\catalog\de.py"
  Delete "$INSTDIR\localization\catalog\el.py"
  Delete "$INSTDIR\localization\catalog\en.py"
  Delete "$INSTDIR\localization\catalog\es.py"
  Delete "$INSTDIR\localization\catalog\et.py"
  Delete "$INSTDIR\localization\catalog\eu.py"
  Delete "$INSTDIR\localization\catalog\fi.py"
  Delete "$INSTDIR\localization\catalog\fr.py"
  Delete "$INSTDIR\localization\catalog\gl.py"
  Delete "$INSTDIR\localization\catalog\he.py"
  Delete "$INSTDIR\localization\catalog\hu.py"
  Delete "$INSTDIR\localization\catalog\it.py"
  Delete "$INSTDIR\localization\catalog\ja.py"
  Delete "$INSTDIR\localization\catalog\ko.py"
  Delete "$INSTDIR\localization\catalog\nl.py"
  Delete "$INSTDIR\localization\catalog\pl.py"
  Delete "$INSTDIR\localization\catalog\pt-BR.py"
  Delete "$INSTDIR\localization\catalog\ru.py"
  Delete "$INSTDIR\localization\catalog\sr.py"
  Delete "$INSTDIR\localization\catalog\sv.py"
  Delete "$INSTDIR\localization\catalog\zh-Hans.py"
  Delete "$INSTDIR\localization\catalog\__init__.py"
  Delete "$INSTDIR\plugins\description_links.py"
  Delete "$INSTDIR\compat\2x\__init__.py"
  Delete "$INSTDIR\compat\2x\iPodder.py"
  Delete "$INSTDIR\compat\__init__.py"
  Delete "$INSTDIR\docs\JuiceUserGuide.html"

  Delete "$SMPROGRAMS\Juice\Uninstall.lnk"
  Delete "$SMPROGRAMS\Juice\Website.lnk"
  Delete "$DESKTOP\Juice.lnk"
  Delete "$SMPROGRAMS\Juice\Juice.lnk"

  RMDir "$SMPROGRAMS\Juice"
  RMDir "$INSTDIR\win32"
  RMDir "$INSTDIR\images"
  RMDir "$INSTDIR\icons_status"
  RMDir "$INSTDIR\gui"
  RMDir "$INSTDIR\localization\catalog"
  RMDir "$INSTDIR\localization"
  RMDir "$INSTDIR\compat\2x"
  RMDir "$INSTDIR\compat"
  RMDir "$INSTDIR\docs"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  DeleteRegKey HKCR "Applications\Juice.exe"
  DeleteRegKey HKCR "Juice.rss"
  DeleteRegKey HKCR "Juice.pcast"
  DeleteRegKey HKCR ".rss\OpenWithList\Juice.exe"
  DeleteRegValue HKCR ".rss\OpenWithProgIds" "Juice.rss"
  DeleteRegKey HKCR ".pcast\OpenWithList\Juice.exe"
  DeleteRegValue HKCR ".pcast\OpenWithProgIds" "Juice.pcast"

  SetAutoClose true
SectionEnd
