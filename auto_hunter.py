import time
import pyautogui
import pygetwindow as gw
from datetime import datetime, timedelta
import re
from ocr_utils import capture_and_ocr, get_save_dir
import tkinter.messagebox as msgbox
import pandas as pd
import webbrowser
from PIL import ImageGrab, Image

exp_data = []
window_info = []

def start_auto_hunt(hunt_time_entry, server_entry):
    global exp_data, window_info
    exp_data.clear()
    window_info.clear()

    windows = gw.getWindowsWithTitle("게임 이름")
    if not windows:
        print("게임창을 찾을 수 없습니다.")
        return

    for i, win in enumerate(windows):
        try:
            print(f"{i+1} 번째 창 실행 : {win.title}")
            win.activate()
            time.sleep(1)
            win.moveTo(100, 100)
            time.sleep(1)
            win.resizeTo(1280, 720)
            time.sleep(1)

            #EXP 버튼 클릭
            left, top = win.left, win.top
            exp_x = left + int(win.width * 0.10)
            exp_y = top + int(win.height * 0.97)

            time.sleep(1)
            pyautogui.click(exp_x, exp_y)
            print(f"EXP 클릭 좌표 : ({exp_x}, {exp_y})")

            # OCR 영역
            region = (exp_x + 22, exp_y - 45, exp_x + 310, exp_y-15)
            text = capture_and_ocr(region, f"exp_start_{i+1}.png")
            print("캡쳐된 원본 :", text)

            
            # 경험치 앞글자 추출용
            numbers = re.findall(r'\d+', text)
            if numbers:
                start_exp = numbers[0]
            else:
                start_exp = "인식에 실패했습니다."

            print(f"{i+1}번째 창 시작 경험치 : {start_exp}")
            exp_data.append({"창 번호": i+1, "시작 경험치": start_exp})

            time.sleep(1)

            # 레벨 아이콘 클릭 ( 능력치 저장하려고)
            level_icon_x = left + int(win.width * 0.03)
            level_icon_y = top + int(win.height * 0.08)
            pyautogui.click(level_icon_x, level_icon_y)
            time.sleep(2)

            #능력치 창 캡쳐 해서 저장
            region = (level_icon_x - 30, level_icon_y - 20, level_icon_x + 450, win.top + win.height)
            screenshot = ImageGrab.grab(bbox=region)
            screenshot.save(f"{get_save_dir()}/능력치_{i+1}번.png")
            print(f"{i+1} 번째 능력치 저장")

            try:
                region = (level_icon_x + 30, level_icon_y - 20, level_icon_x + 240, level_icon_y + 25)
                text = capture_and_ocr(region, f"name_{i + 1}.png")
                print(f"{i+1}번째 창 이름 : {text}")
                match = re.search(r'Lv\.\d+\s+([^\n]+)', text)
                if match:
                    character_name = match.group(1).strip()
                else:
                    character_name = "인식 실패"
                exp_data[i]["이름"] = character_name

            except Exception:
                print(f"{i+1}번째 창 이름 인식 실패: {e}")
                exp_data[i]["이름"] = "인식실패"

            time.sleep(0.5)
            win.activate()
            time.sleep(1)
            pyautogui.keyDown("esc")
            time.sleep(0.1)
            pyautogui.keyUp("esc")
            time.sleep(0.5)

            window_info.append({"index": i, "win": win, "exp_x": exp_x, "exp_y": exp_y}) #창 정보

        except Exception as e:
            print(f"EXP 검사 실패: {e}")
            exp_data.append({"창 번호": i + 1, "EXP": "오류"})

    for info in window_info:

        win = info["win"]
        try:
            win.activate()
            time.sleep(1)
            pyautogui.press("`")
            time.sleep(2)
            pyautogui.typewrite("/테스트용 명령어(킬 수 화면에 보여주는)")
            time.sleep(0.5)
            pyautogui.press("enter")
            time.sleep(0.5)
            pyautogui.press("`")
            time.sleep(2)
            pyautogui.keyDown("ctrlleft")
            time.sleep(0.2)
            pyautogui.keyUp("ctrlleft")
            time.sleep(0.5)

            now = datetime.now()
            exp_data[info["index"]]["시작 시간"] = now.strftime("%H:%M:%S")
            exp_data[info["index"]]["시작 날짜"] = now.strftime("%Y-%m-%d")

        except Exception as e:
            print(f"자동 사냥 시작 실패 : {e}")

    # 사냥 대기 시간
    try:
        hunt_time_min = float(hunt_time_entry.get())
        wait_seconds = int(hunt_time_min * 60)
        print(f"사냥 대기 시간: {wait_seconds}초")

        from gui import root
        if wait_seconds > 10:
            from gui import show_countdown_alert, root
            root.after((wait_seconds - 10) * 1000, show_countdown_alert) # 밀리초라서 1000 곱하기
        root.after(wait_seconds * 1000, lambda: continue_after_wait(server_entry))
    except ValueError:
        print("사냥 시간 입력 오류")


def continue_after_wait(server_entry):
    global exp_data, window_info
    print("경험치 체크 시작")
    from gui import root

    for info in window_info:
        try:
            win = info["win"]
            win.activate()
            time.sleep(1)
            win.moveTo(100, 100)
            time.sleep(1)
            win.resizeTo(1280,720)
            time.sleep(1)
            pyautogui.keyDown("ctrlleft")
            time.sleep(0.3)
            pyautogui.keyUp("ctrlleft")
            time.sleep(1)

            end_time = datetime.now()
            exp_data[info["index"]]["종료 시간"] = end_time.strftime("%H:%M:%S")
            exp_data[info["index"]]["종료 날짜"] = end_time.strftime("%Y-%m-%d")

            #EXP 버튼 클릭
            left, top = win.left, win.top
            exp_x = left + int(win.width * 0.10)
            exp_y = top + int(win.height * 0.97)

            time.sleep(1)
            pyautogui.click(exp_x, exp_y)
            print(f"EXP 클릭 좌표 : ({exp_x}, {exp_y})")
            # OCR 대상 영역
            region = (exp_x + 22, exp_y - 45, exp_x + 310, exp_y-15)
            text = capture_and_ocr(region, f"exp_end_{info['index']+1}.png")
            print("캡쳐된 원본 :", text)
            # 경험치 앞글자
            numbers = re.findall(r'\d+', text)
            if numbers:
                end_exp = numbers[0]
            else:
                end_exp = "인식 실패"
            print(f"{info['index']+1}번째 창 종료 경험치 : {end_exp}")

            exp_data[info["index"]]["종료 경험치"] = end_exp

            time.sleep(1)

            try:
                start_val = int(exp_data[info["index"]]["시작 경험치"])
                end_val = int(end_exp)
                exp_data[info["index"]]["획득 경험치"] = start_val - end_val
            except:
                exp_data[info["index"]]["획득 경험치"] = "계산 오류"

            try:
                start_str = f"{exp_data[info['index']]['시작 날짜']} {exp_data[info['index']]['시작 시간']}"
                start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
                delta = end_time - start_dt
                exp_data[info["index"]]["소요 시간"] = str(delta)
            except:
                exp_data[info["index"]]["소요 시간"] = "계산 오류"

            # 킬 카운트 세기
            try:
                time.sleep(1)
                pyautogui.click(win.left + 1237, win.top + 60)
                time.sleep(0.5)
                pyautogui.click(win.left + 1168, win.top + 532)
                time.sleep(1)

                region = (win.right - 270, win.top + 100, win.right - 10, win.top + 170)
                text = capture_and_ocr(region, f"kill_count_{info['index'] + 1}.png")
                print(text)

                kill_numbers = re.findall(r'\d+', text)
                if kill_numbers:
                    kill_count = int(kill_numbers[0]) # 첫번째 숫자 사용
                    exp_data[info["index"]]["킬 수"] = kill_count
                else:
                    exp_data[info["index"]]["킬 수"] = "인식실패"

                pyautogui.press("`")
                time.sleep(2)
                pyautogui.typewrite("/portal 107")
                time.sleep(0.5)
                pyautogui.press("enter")
                time.sleep(0.5)
                pyautogui.press("`")
                time.sleep(1)

            except Exception as e:
                print(f"킬 카운트 OCR 실패: {e}")
        except Exception as e:
            print(f"EXP 종료 측정 실패: {e}")

    server_name = server_entry.get().strip()
    if server_name:
        for entry in exp_data:
            try:
                character_name = entry.get("이름", "unknown").replace(" ", "")

                #KST 기준 시간
                start_kst = f"{entry.get('시작 날짜', '')} {entry.get('시작 시간', '')}"
                end_kst = f"{entry.get('종료 날짜', '')} {entry.get('종료 시간', '')}"

                # UTC로 변환 하자
                start_utc = (datetime.strptime(start_kst, "%Y-%m-%d %H:%M:%S") - timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
                end_utc = (datetime.strptime(end_kst, "%Y-%m-%d %H:%M:%S") - timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")

                #DB 이름
                db_name = f"game_log_project_alpha_0{server_name}"  # DB 이름을 임의로 설정

                #쿼리 함수
                query = (
                    f"SELECT * FROM `{db_name}`.`your_table` " #DB 테이블 이름 임의로 설정
                    f"WHERE character_name = '{character_name}' "
                    f"AND event_date BETWEEN '{start_utc}' AND '{end_utc}';"
                )
                entry["쿼리"] = query
            except Exception as e:
                entry["쿼리"] = "쿼리 생성 실패"

        webbrowser.open_new("SQL 입력을 위한 웹 DB 링크")
    else:
        for entry in exp_data:
            entry["쿼리"] = ""

    if exp_data:
        df = pd.DataFrame(exp_data, columns=["창 번호", "이름", "시작 경험치", "종료 경험치", "획득 경험치", "소요 시간", "킬 수", "시작 시간", "종료 시간", "쿼리"])
        filename = f"밸런스 테스트 결과_{time.strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(filename, index=False)
        print(f"엑셀 저장 완료: {filename}")
        msgbox.showinfo("알림", "사냥이 종료되었습니다. 결과가 저장되었습니다.")
