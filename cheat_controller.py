import time
import pyautogui

# 테스트용 자동화 치트 입력 함수
# 일부 명령어는 실제 치트 명령과 유사하지만, 보안을 위해 가데이터 형태로 작성됨
def run_cheat_commands(item_ids, item_qtys, stat_entries, cheat_group):
    time.sleep(1)

    # 콘솔창 열기 (예: ` 키)
    pyautogui.press("`") 
    time.sleep(1)

    # 예) 아이템 지급 치트
    for i in range(6):
        item_id = item_ids[i].get().strip()
        qty = item_qtys[i].get().strip()

        if not item_id:
            continue

        # 실제 명령은 보안상 변경, 예시 명령어 입니다.
        if qty:
            command = f"/put_item {item_id} {qty}"  # 예시 명령어
        else:
            command = f"/put_item {item_id}"        # 예시 명령어

        pyautogui.typewrite(f"{command}")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(0.5)
    time.sleep(1)

    # 예) 스탯 추가 명령
    stat_commands = {
        "공격력": "damage",
        "방어력": "defense",
        "명중": "hit_accuracy",
        "공격 속도": "attack_speed",
        "아이템 획득 확률": "drop_item",
        "무게": "max_weight"
    }

    for stat_label, entry in stat_entries.items():
        value = entry.get().strip()
        if not value:
            continue
        try:
            int_value = int(value)
        except ValueError:
            continue

        cmd_key = stat_commands.get(stat_label)
        if not cmd_key:
            continue

        # 예) 명령어: 퍼센트 포함 항목 구분
        if stat_label in ["공격 속도", "아이템 획득 확률"]:
            command = f"/add_status {cmd_key}+{int_value}%"
        else:
            command = f"/add_status {cmd_key}+{int_value}"

        pyautogui.typewrite(command)
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(0.5)

    # 예) 치트 그룹 실행
    if cheat_group:
        pyautogui.typewrite(f"/cheat_group_run {cheat_group}")
        time.sleep(0.5)
        pyautogui.press("enter")
    time.sleep(0.5)

    # 콘솔창 닫기
    pyautogui.press("`")
