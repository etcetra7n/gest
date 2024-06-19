;======================================================
; Include

!include MUI2.nsh
!include "Sections.nsh"

;======================================================
; Macro definitions
!ifndef VERSION
  !define VERSION "1.0.0"
!endif
!ifndef ARCH
  !define ARCH "x86"
!endif
!ifndef LICENSE_PATH
  !define LICENSE_PATH "..\LICENSE"
!endif
!ifndef BUILD_DIR
  !define BUILD_DIR "..\dist\gest\"
!endif

;======================================================
; Installer Information

Name "GEST v${VERSION}"
OutFile "gest-v${VERSION}-win-${ARCH}-setup.exe"
!if ${ARCH} == "x86"
  InstallDir $PROGRAMFILES\gest
!else if ${ARCH} == "x64"
  InstallDir $PROGRAMFILES64\gest
!endif

;======================================================
; Interface Configuration

!define MUI_HEADERIMAGE
!define MUI_ABORTWARNING
!define MUI_COMPONENTSPAGE_SMALLDESC
!define MUI_HEADERIMAGE_BITMAP_NOSTRETCH
!define MUI_FINISHPAGE
BrandingText "GEST ${VERSION}"

;======================================================
; Installer pages

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE ${LICENSE_PATH}
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

;======================================================
; Uninstaller pages

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_COMPONENTS
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

;======================================================
; Languages

!insertmacro MUI_LANGUAGE "English"

;======================================================
; Installer Section

Section "Basic installation" SEC_BASIC_INSTALLATION
  ; Write gest.exe to $INSTDIR
  SetOutPath $INSTDIR
  File /nonfatal /a /r "${BUILD_DIR}"
  ;File ${CPY_ICO_PATH}

  ; Register application
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\gest.exe" "" "$INSTDIR\gest.exe"
  ;WriteRegStr HKCR Applications\gest.exe\DefaultIcon "" "$INSTDIR\gest.ico"
  WriteRegStr HKCR Applications\gest.exe\shell\open\command "" "$\"$INSTDIR\gest.exe$\" $\"%1$\""

  ; Write uninstaller
  WriteUninstaller $INSTDIR\uninst-gest.exe
SectionEnd

Section "Add to PATH" SEC_ADD_TO_PATH
  EnVar::SetHKCU
  EnVar::AddValue "PATH" "$INSTDIR"
SectionEnd

Section "Configure .gest and .gsav file type" SEC_CONFIG_GEST_FILE
  WriteRegStr HKCR .gest "" "GEST.GameFile.1"
  WriteRegStr HKCR .gest "Content Type" "text/plain"
  WriteRegStr HKCR .gest "PerceivedType" "text"
  WriteRegStr HKCR GEST.GameFile.1 "" "GEST Game File"
  ;WriteRegStr HKCR GEST.GameFile.1\DefaultIcon "" "$INSTDIR\gest.ico"
  WriteRegStr HKCR GEST.GameFile.1\shell\open\command "" "$\"$INSTDIR\gest.exe$\" $\"%1$\""
  WriteRegStr HKCU Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.gest\UserChoice "Progid" "GEST.GameFile.1"

  WriteRegStr HKCR .gsav "" "GEST.SaveFile.1"
  WriteRegStr HKCR .gsav "Content Type" "text/plain"
  WriteRegStr HKCR .gsav "PerceivedType" "text"
  WriteRegStr HKCR GEST.SaveFile.1 "" "GEST Save File"
  ;WriteRegStr HKCR GEST.SaveFile.1\DefaultIcon "" "$INSTDIR\gsav.ico"
  WriteRegStr HKCR GEST.SaveFile.1\shell\open\command "" "$\"$INSTDIR\gest.exe$\" $\"%1$\""
  WriteRegStr HKCU Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.gsav\UserChoice "Progid" "GEST.SaveFile.1"
SectionEnd

Section "Enable $\"Play$\" button in right-click context menu" SEC_ENABLE_CONTEXT_MENU
  WriteRegStr HKCR .gest\shell\gest "" "Play"
  WriteRegStr HKCR .gest\shell\gest\command "" "$\"$INSTDIR\gest.exe$\" $\"%1$\""

  WriteRegStr HKCR .gsav\shell\gest "" "Play"
  WriteRegStr HKCR .gsav\shell\gest\command "" "$\"$INSTDIR\gest.exe$\" $\"%1$\""
SectionEnd

;======================================================
; Uninstaller Section

Section "un.Basic uninstallation" UNSEC_BASIC_UNINSTALLATION
  ; Remove executables
  Delete $INSTDIR\gest.exe
  Delete $INSTDIR\uninst-gest.exe
  Delete $INSTDIR\gest.ico
  RMDir $INSTDIR

  ; Unregister application
  DeleteRegKey HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\gest.exe"
  DeleteRegKey HKCR Applications\gest.exe
SectionEnd

Section "un.Remove from PATH" UNSEC_REMOVE_FROM_PATH
  EnVar::SetHKCU
  EnVar::DeleteValue "PATH" "$INSTDIR"
SectionEnd

Section "un.Unconfigure .gest and .gsav file type" UNSEC_UNCONFIG_GEST_FILE
  DeleteRegKey HKCR GEST.GameFile.1
  DeleteRegKey HKCU Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.gest

  DeleteRegKey HKCR GEST.SaveFile.1
  DeleteRegKey HKCU Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.gsav
SectionEnd

Section "un.Disable $\"Play$\" button in right-click context menu" UNSEC_DISABLE_CONTEXT_MENU
  DeleteRegKey HKCR .gest\Shell\gest
  DeleteRegKey HKCR .gsav\Shell\gest
SectionEnd

;======================================================
; Component Description

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_BASIC_INSTALLATION} "Places files in the installation directory"
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_ADD_TO_PATH} "Lets you to use the `gest` command in the command line"
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_CONFIG_GEST_FILE} "Configures .gest and .gsav file types in your system"
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC_ENABLE_CONTEXT_MENU} "Adds a $\"Play$\" option to the right click context menu of every file types"
!insertmacro MUI_FUNCTION_DESCRIPTION_END

!insertmacro MUI_UNFUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${UNSEC_BASIC_UNINSTALLATION} "Removes files from the installation directory"
  !insertmacro MUI_DESCRIPTION_TEXT ${UNSEC_REMOVE_FROM_PATH} "You will no longer be able to use the `gest` command in the command line"
  !insertmacro MUI_DESCRIPTION_TEXT ${UNSEC_UNCONFIG_GEST_FILE} "Removes .gest and .gsav file type configuration from your system"
  !insertmacro MUI_DESCRIPTION_TEXT ${UNSEC_DISABLE_CONTEXT_MENU} "Removes the $\"Play$\" option from the right click context menu"
!insertmacro MUI_UNFUNCTION_DESCRIPTION_END

;======================================================
; Callback Functions

Function .onInstSuccess
  SendMessage ${HWND_BROADCAST} ${WM_SETTINGCHANGE} 0x002A 0 /TIMEOUT=5000
FunctionEnd

Function un.onUninstSuccess
  SendMessage ${HWND_BROADCAST} ${WM_SETTINGCHANGE} 0x002A 0 /TIMEOUT=5000
FunctionEnd

;======================================================
