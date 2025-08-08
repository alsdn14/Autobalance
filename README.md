## 게임 밸런스 테스트 자동화 도구입니다.

## 1. 목적
* 경험치, 드랍률 등 밸런스 수치 기반 테스트를 자동화하여 반복적이고 정량적인 검증 환경을 구축
* 휴먼 에러를 최소화하고 테스트 효율을 극대화

GUI 기반으로 자동 사냥, 경험치 OCR 추출, 치트키 명령 실행 등이 가능하고  
최종 실행 파일은 PyInstaller로 빌드되어 .exe 형태로 제공됩니다. (GitHub에는 포함하지 않았습니다.)    
  
벨런스 자동화 테스트 프로그램  
├── auto_hunter.py  ← 자동 사냥 실행 로직  
├── cheat_controller.py  ← 치트 명령 입력 로직  
├── gui.py  ← GUI 관련  
├── main.py  ← 프로그램 실행  
├── ocr_utils.py  ← OCR 유틸 함수  
├── 사전 설치.bat ← 설치 자동화용 배치 파일 ( 폴더에 tesseract_installer.exe 파일이 있어야 함 )  

| 파일명 | 역할 및 내용 |
| ------ | ------ |
|auto_hunter.py||
|cheat_controller.py||
|gui.py||
|main.py||
|ocr_utils.py||
|사전 설치.bat||
