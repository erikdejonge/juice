!ifndef FUNCTIONS_GENERAL
!define FUNCTIONS_GENERAL
/*
_______________________________________________________________________________________________________

          This header is a general header file that has as many general functions as possible.
                     If the function is not used, the compiler will zero the code,
                        which is good for people who watch their exe head size.
                            
                      All the functions have their credits of where they came from.
_______________________________________________________________________________________________________

List of functions included:

CheckIEVersion
CheckWinver
ConnectInternet
GetParentDir
GetCmdLine
GetInstallerFilename
IsDotNETInstalled
IsFlashInstalled
IsRunning
StrStr
TrimNewLines


*/

 Function CheckIEVersion
 ; CheckIEVersion
 ;
 ; Based on Yazno's function, http://yazno.tripod.com/powerpimpit/
 ; Returns on top of stack
 ; 1-6 (Installed IE Version)
 ; or
 ; '' (IE is not installed)
 ;
 ; Usage:
 ;   Call CheckIEVersion
 ;   Pop $R0
 ;   ; at this point $R0 is "5" or whatnot

 Push $R0
   ClearErrors
   ReadRegStr $R0 HKLM "Software\Microsoft\Internet Explorer" "Version"
   IfErrors lbl_123 lbl_456

   lbl_456: ; ie 4+
     Strcpy $R0 $R0 1
   Goto lbl_done00

   lbl_123: ; older ie version
     ClearErrors
     ReadRegStr $R0 HKLM "Software\Microsoft\Internet Explorer" "IVer"
     IfErrors lbl_error00

       StrCpy $R0 $R0 3
       StrCmp $R0 '100' lbl_ie1
       StrCmp $R0 '101' lbl_ie2
       StrCmp $R0 '102' lbl_ie2

       StrCpy $R0 '3' ; default to ie3 if not 100, 101, or 102.
       Goto lbl_done00
         lbl_ie1:
           StrCpy $R0 '1'
         Goto lbl_done00
         lbl_ie2:
           StrCpy $R0 '2'
         Goto lbl_done00
     lbl_error00:
       StrCpy $R0 ''
   lbl_done00:
   Exch $R0
 FunctionEnd

!macro CHECKWINVER
 ; CheckWinver
 ;
 ; Based on Yazno's function, http://yazno.tripod.com/powerpimpit/
 ; Updated by Joost Verburg
 ;
 ; Modified for use in a header and for InstallSpider by Jason Ross aka JasonFriday13
 ;
 ; Windows Version (95, 98, ME, NT x.x, 2000, XP, 2003, Vista)
 ; or
 ; '' (Unknown Windows Version)
 ; NOTE: Vista is only experimental at this stage. I will update this function when Vista is released.
 ;
 ; If you want to install on any system, don't include the defines or the macro.
 ;
 ; Usage:
 ;   Function .oninit
 ;     !define win98
 ;     !define winXP
 ;     !insertmacro CHECKWINVER
 ;   ; If the system is not one of those defined, the macro puts up an error message
 ;   ; saying which versions this program can be installed on.


   Push $0
   Push $1
   Push $2
   Push $3
   Push $4
   Push $5
   Push $6
   Push $7

   Push $R0
   Push $R1
   Push $R2
   Push $R3
   Push $R4
   Push $R5

   strcpy $R3 0
   
   strcpy $0 false
   strcpy $1 false
   strcpy $2 false
   strcpy $3 false
   strcpy $4 false
   strcpy $5 false
   strcpy $6 false
   strcpy $7 false

   ClearErrors

   strcpy $R2 0

   ReadRegStr $R0 HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion" CurrentVersion

   IfErrors 0 lbl_winnt

   ; we are not NT
   ReadRegStr $R0 HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion" VersionNumber

   StrCpy $R1 $R0 1
   StrCmp $R1 '4' 0 lbl_error01

   StrCpy $R1 $R0 3

   StrCmp $R1 '4.0' lbl_win32_95
   StrCmp $R1 '4.9' lbl_win32_ME lbl_win32_98
   
   goto lbl_error01

   lbl_win32_95:
     strcpy $0 true
     Goto Message
   lbl_win32_98:
     strcpy $1 true
     Goto Message
   lbl_win32_ME:
     strcpy $2 true
     Goto Message

   lbl_winnt:
   StrCpy $R1 $R0 1

   StrCmp $R1 '3' lbl_winnt_x
   StrCmp $R1 '4' lbl_winnt_x

   StrCpy $R1 $R0 3

   StrCmp $R1 '5.0' lbl_winnt_2000
   StrCmp $R1 '5.1' lbl_winnt_XP
   StrCmp $R1 '5.2' lbl_winnt_2003 lbl_error01
   StrCmp $R1 '6.0' lbl_winnt_VISTA
   goto lbl_error01

   lbl_winnt_x:
     !ifdef winNT
       StrCpy $R0 $R0 3
       IntCmp $R0 ${winNT} lbl_done01 0 lbl_done01
       strcpy $3 true
       Goto Message
     !endif
   lbl_winnt_2000:
     strcpy $4 true
     Goto Message

   lbl_winnt_2003:
     strcpy $5 true
     Goto Message

   lbl_winnt_XP:
     strcpy $6 true
     Goto Message

   lbl_winnt_VISTA:
     strcpy $7 true
     Goto Message

   lbl_error01:
     MessageBox MB_OK|MB_ICONSTOP "This setup program is running on an unsupported operating system. Setup will now close."
     Quit
   Message:

        !ifdef winVISTA
          strcmp $7 false 0 lbl_done01
            push "Windows Vista"
            intop $R2 $R2 + 1
        !endif
        !ifdef winXP
          strcmp $6 false 0 lbl_done01
            push "Windows XP"
            intop $R2 $R2 + 1
        !endif
        !ifdef win2003
          strcmp $5 false 0 lbl_done01
            push "Windows 2003"
            intop $R2 $R2 + 1
        !endif
        !ifdef win2000
          strcmp $4 false 0 lbl_done01
            push "Windows 2000"
            intop $R2 $R2 + 1
        !endif
        !ifdef winNT
          strcmp $3 false 0 lbl_done01
            push "Windows NT ${winNT} and above"
            intop $R2 $R2 + 1
        !endif
        !ifdef winME
          strcmp $2 false 0 lbl_done01
            push "Windows ME"
            intop $R2 $R2 + 1
        !endif
        !ifdef win98
          strcmp $1 false 0 lbl_done01
            push "Windows 98"
            intop $R2 $R2 + 1
        !endif
        !ifdef win95
          strcmp $0 false 0 lbl_done01
            push "Windows 95"
            intop $R2 $R2 + 1
        !endif

     StrCpy $R3 0

     Loop01:
     pop $R4
     strcmp $R3 0 +3 0
     strcpy $R5 "$R5, $R4"
     goto +2
     strcpy $R5 $R4
     intop $R3 $R3 + 1
     StrCmp $R3 $R2 0 Loop01

     MessageBox MB_OK|MB_ICONSTOP "This program can only be installed on the following operating systems: $R5."
     Quit
   lbl_done01:

   Pop $R5
   Pop $R4
   Pop $R3
   Pop $R2
   Pop $R1
   Pop $R0

   Pop $7
   Pop $6
   Pop $5
   Pop $4
   Pop $3
   Pop $2
   Pop $1
   Pop $0

 !macroend
 
 Function ConnectInternet
 ; ConnectInternet (uses Dialer plugin)
 ; Written by Joost Verburg
 ;
 ; This function attempts to make a connection to the internet if there is no
 ; connection available. If you are not sure that a system using the installer
 ; has an active internet connection, call this function before downloading
 ; files with NSISdl.
 ;
 ; The function requires Internet Explorer 3, but asks to connect manually if
 ; IE3 is not installed.
 ;
 ; Usage:
 ; Call ConnectInternet
 ; pop $R0
 ; ; $R0 will be the status, either 'error' or 'connected'. This function has its own message box.

   Push $R0

     ClearErrors
     Dialer::AttemptConnect
     IfErrors noie3

     Pop $R0
     StrCmp $R0 "online" connected
       MessageBox MB_OK|MB_ICONSTOP "Cannot connect to the internet."
       ;Quit ;This will quit the installer. You might want to add your own error handling.
       goto error
     noie3:

     ; IE3 not installed
     MessageBox MB_OK|MB_ICONINFORMATION "Please connect to the internet now."

     error:
     strcpy $R0 'error'
     connected:

   push 'connected'
   Exch $R0

 FunctionEnd

 Function GetParentDir

 ; GetParentDir
 ; input, top of stack  (e.g. C:\Program Files\Poop)
 ; output, top of stack (replaces, with e.g. C:\Program Files)
 ; modifies no other variables.
 ;
 ; Usage:
 ;   Push "C:\Program Files\Directory\Whatever"
 ;   Call GetParent
 ;   Pop $R0
 ;   ; at this point $R0 will equal "C:\Program Files\Directory"

   Exch $R0
   Push $R1
   Push $R2
   Push $R3

   StrCpy $R1 0
   StrLen $R2 $R0

   loop:
     IntOp $R1 $R1 + 1
     IntCmp $R1 $R2 get 0 get
     StrCpy $R3 $R0 1 -$R1
     StrCmp $R3 "\" get
     Goto loop

   get:
     StrCpy $R0 $R0 -$R1

     Pop $R3
     Pop $R2
     Pop $R1
     Exch $R0

 FunctionEnd
 
 Function GetCmdLine

 ; This function was taken directly from the scripting reference.
 ;
 ; Usage:
 ;
 ; Function .oninit
 ; call GETCMDLINE
 ; pop $0
 ; ;at this point $0 has the commands line parameters in it.
 ; FunctionEnd


   Push $R0
   Push $R1
   Push $R2
   Push $R3

   StrCpy $R2 1
   StrLen $R3 $CMDLINE

   ;Check for quote or space
   StrCpy $R0 $CMDLINE $R2
   StrCmp $R0 '"' 0 +3
     StrCpy $R1 '"'
     Goto loop
   StrCpy $R1 " "

   loop:
     IntOp $R2 $R2 + 1
     StrCpy $R0 $CMDLINE 1 $R2
     StrCmp $R0 $R1 get
     StrCmp $R2 $R3 get
     Goto loop

   get:
     IntOp $R2 $R2 + 1
     StrCpy $R0 $CMDLINE 1 $R2
     StrCmp $R0 " " get
     StrCpy $R0 $CMDLINE "" $R2

   Pop $R3
   Pop $R2
   Pop $R1
   Exch $R0

 FunctionEnd
 
 Function GetInstallerFilename
 ; Usage:
 ; call GetInstallerFilename
 ; pop $R0
 ; ; $R0 contains the installer filename

   push $R0
   System::Call 'kernel32::GetModuleFileNameA(i 0, t .R0, i 1024) i r1'
   ;$R0 will contain the installer filename
   Exch $R0
 FunctionEnd

 Function IsDotNETInstalled
 ; IsDotNETInstalled
 ;
 ; Usage:
 ;   Call IsDotNETInstalled
 ;   Pop $0
 ;   StrCmp $0 1 found.NETFramework no.NETFramework
   Push $0
   Push $1
   Push $2
   Push $3
   Push $4

   ReadRegStr $4 HKEY_LOCAL_MACHINE \
     "Software\Microsoft\.NETFramework" "InstallRoot"
   # remove trailing back slash
   Push $4
   Exch $EXEDIR
   Exch $EXEDIR
   Pop $4
   # if the root directory doesn't exist .NET is not installed
   IfFileExists $4 0 noDotNET

   StrCpy $0 0

   EnumStart:

     EnumRegKey $2 HKEY_LOCAL_MACHINE \
       "Software\Microsoft\.NETFramework\Policy"  $0
     IntOp $0 $0 + 1
     StrCmp $2 "" noDotNET

     StrCpy $1 0

     EnumPolicy:

       EnumRegValue $3 HKEY_LOCAL_MACHINE \
         "Software\Microsoft\.NETFramework\Policy\$2" $1
       IntOp $1 $1 + 1
        StrCmp $3 "" EnumStart
         IfFileExists "$4\$2.$3" foundDotNET EnumPolicy

   noDotNET:
     StrCpy $0 0
     Goto done

   foundDotNET:
     StrCpy $0 1

   done:
     Pop $4
     Pop $3
     Pop $2
     Pop $1
     Exch $0
 FunctionEnd

 Function IsFlashInstalled
 ; IsFlashInstalled
 ;
 ; By Yazno, http://yazno.tripod.com/powerpimpit/
 ; Returns on top of stack
 ; 0 (Flash is not installed)
 ; or
 ; 1 (Flash is installed)
 ;
 ; Usage:
 ;   Call IsFlashInstalled
 ;   Pop $R0
 ;   ; $R0 at this point is "1" or "0"

  Push $R0
  ClearErrors
  ReadRegStr $R0 HKCR "CLSID\{D27CDB6E-AE6D-11cf-96B8-444553540000}" ""
  IfErrors lbl_na
    StrCpy $R0 1
  Goto lbl_end
  lbl_na:
    StrCpy $R0 0
  lbl_end:
  Exch $R0
 FunctionEnd
 
 Function IsRunning
 ; Usage:
 ; Function .oninit
 ; call IsRunning
 ; ; the installer will quit if the installer is already running.


   System::Call 'kernel32::CreateMutexA(i 0, i 0, t "2345h2lh54l2j34bnbh4g2542hg4hb7g78trygvkt34wdyd4yerdyuyi7grf5r6") i .r1 ?e'
   Pop $R0

   StrCmp $R0 0 +3
     MessageBox MB_OK|MB_ICONEXCLAMATION "The installer is already running."
     Quit
 FunctionEnd

 Function StrStr
 ; StrStr
 ; input, top of stack = string to search for
 ;        top of stack-1 = string to search in
 ; output, top of stack (replaces with the portion of the string remaining)
 ; modifies no other variables.
 ;
 ; Usage:
 ;   Push "this is a long ass string"
 ;   Push "ass"
 ;   Call StrStr
 ;   Pop $R0
 ;  ($R0 at this point is "ass string")
 
   Exch $R1 ; st=haystack,old$R1, $R1=needle
   Exch    ; st=old$R1,haystack
   Exch $R2 ; st=old$R1,old$R2, $R2=haystack
   Push $R3
   Push $R4
   Push $R5
   StrLen $R3 $R1
   StrCpy $R4 0
   ; $R1=needle
   ; $R2=haystack
   ; $R3=len(needle)
   ; $R4=cnt
   ; $R5=tmp
   loop:
     StrCpy $R5 $R2 $R3 $R4
     StrCmp $R5 $R1 done
     StrCmp $R5 "" done
     IntOp $R4 $R4 + 1
     Goto loop
 done:
   StrCpy $R1 $R2 "" $R4
   Pop $R5
   Pop $R4
   Pop $R3
   Pop $R2
   Exch $R1
 FunctionEnd
 
 Function TrimNewlines
 ; TrimNewlines
 ; input, top of stack  (e.g. whatever$\r$\n)
 ; output, top of stack (replaces, with e.g. whatever)
 ; modifies no other variables.

   Exch $R0
   Push $R1
   Push $R2
   StrCpy $R1 0

 loop:
   IntOp $R1 $R1 - 1
   StrCpy $R2 $R0 1 $R1
   StrCmp $R2 "$\r" loop
   StrCmp $R2 "$\n" loop
   IntOp $R1 $R1 + 1
   IntCmp $R1 0 no_trim_needed
   StrCpy $R0 $R0 $R1

 no_trim_needed:
   Pop $R2
   Pop $R1
   Exch $R0
 FunctionEnd

!endif