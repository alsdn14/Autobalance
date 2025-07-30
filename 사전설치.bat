@echo off
setlocal

echo ---------------------------------
echo [Tesseract 설치 스크립트 시작]
echo ---------------------------------

REM 이미 설치파일이 있다면 바로 실행
if exist "tesseract_installer.exe" (
    echo [1] 설치 시작...
    start /wait tesseract_installer.exe /SILENT

    set "TESS_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe"
    if exist "%TESS_PATH%" (
        echo [2] 설치 완료됨! 경로: %TESS_PATH%
    ) else (
        echo [!] 설치 실패 또는 경로 다름. 수동 확인 필요.
    )
) else (
    echo [!] 설치 파일이 없습니다. 다운로드 필요.
)

echo ---------------------------------
echo 설치가 완료되었는지 확인해주세요.
pause
exit
