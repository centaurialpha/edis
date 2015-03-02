!define PRODUCT_NAME "Edis"
!define PRODUCT_VERSION "1.0"
!define PRODUCT_WEB_SITE "http://centaurialpha.github.io/edis"

!include "MUI2.nsh"
Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "${PRODUCT_NAME}-${PRODUCT_VERSION}-setup.exe"
InstallDir "$PROGRAMFILES\${PRODUCT_NAME}"

!define MUI_ABORTWARNING
!define MUI_ICON "edis.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP "sidebar.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "header.bmp"
!insertmacro MUI_PAGE_WELCOME
!define MUI_LICENSEPAGE
!insertmacro MUI_PAGE_LICENSE "COPYING"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Spanish"

LicenseData "COPYING"
ShowInstDetails show

Section "Main"
SetOutPath "$INSTDIR"
File /r "exe\"
CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
CreateShortcut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk" "$INSTDIR\${PRODUCT_NAME}.exe"
SectionEnd

!define MUI_FINISHPAGE_RUN "$INSTDIR\edis.exe"
!define MUI_FINISHPAGE_LINK "Web del proyecto"
!define MUI_FINISHPAGE_LINK_LOCATION "${PRODUCT_WEB_SITE}"

!insertmacro MUI_PAGE_FINISH
