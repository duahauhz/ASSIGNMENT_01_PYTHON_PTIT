from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import uuid

# -----------------------------------------
# Dictionary containing table links with their names and IDs
# Từ điển chứa các liên kết bảng với tên và ID của chúng
TABLE_LINKS = {
    'Standard Stats': ('https://fbref.com/en/comps/9/stats/Premier-League-Stats', 'stats_standard'),
    'Shooting': ('https://fbref.com/en/comps/9/shooting/Premier-League-Stats', 'stats_shooting'),
    'Passing': ('https://fbref.com/en/comps/9/passing/Premier-League-Stats', 'stats_passing'),
    'Goal and Shot Creation': ('https://fbref.com/en/comps/9/gca/Premier-League-Stats', 'stats_gca'),
    'Defense': ('https://fbref.com/en/comps/9/defense/Premier-League-Stats', 'stats_defense'),
    'Possession': ('https://fbref.com/en/comps/9/possession/Premier-League-Stats', 'stats_possession'),
    'Miscellaneous': ('https://fbref.com/en/comps/9/misc/Premier-League-Stats', 'stats_misc'),
    'Goalkeeping': ('https://fbref.com/en/comps/9/keepers/Premier-League-Stats', 'stats_keeper')
}

# -----------------------------------------
# List of player data keys for initializing player dictionary
# Danh sách các khóa dữ liệu cầu thủ để khởi tạo từ điển cầu thủ
PLAYER_KEYS = [
    'name', 'nationality', 'position', 'team', 'age', 'games', 'games_starts',
    'minutes', 'goals', 'assist', 'cards_yellow', 'cards_red', 'xg', 'xg_assist',
    'progressive_carries', 'progressive_passes', 'progressive_passes_received', 'goals_per90',
    'assists_per90', 'xg_per90', 'xg_assist_per90', 'gk_goals_against_per90', 'gk_save_pct',
    'gk_clean_sheets_pct', 'gk_pens_save_pct', 'shots_on_target_pct', 'shots_on_target_per90',
    'goals_per_shot', 'average_shot_distance', 'passes_completed', 'passes_pct', 'passes_total_distance',
    'passes_pct_short', 'passes_pct_medium', 'passes_pct_long', 'assisted_shots',
    'passes_into_final_third', 'passes_into_penalty_area', 'crosses_into_penalty_area',
    'sca', 'sca_per90', 'gca', 'gca_per90', 'tackles', 'tackles_won', 'challenges',
    'challenges_lost', 'blocks', 'blocked_shots', 'blocked_passes', 'interceptions', 'touches',
    'touches_def_pen_area', 'touches_def_3rd', 'touches_mid_3rd', 'touches_att_3rd',
    'touches_att_pen_area', 'take_ons', 'take_ons_won_pct', 'take_ons_tackled_pct', 'carries',
    'carries_progressive_distance', 'carries_into_final_third', 'carries_into_penalty_area', 'miscontrols',
    'dispossessed', 'passes_received', 'fouls', 'fouled', 'offsides', 'crosses',
    'ball_recoveries', 'aerials_won', 'aerials_lost', 'aerials_won_pct'
]

# -----------------------------------------
def initialize_player_dict():
    """Initialize a dictionary with default player data keys set to 'N/a'.
    Khởi tạo từ điển với các khóa dữ liệu cầu thủ mặc định được đặt thành 'N/a'."""
    return {key: 'N/a' for key in PLAYER_KEYS}

# -----------------------------------------
def scrape_standard_stats():
    """Scrape player data from the 'Standard Stats' table.
    Thu thập dữ liệu cầu thủ từ bảng 'Standard Stats'."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)  # Wait for page elements to load / Chờ các phần tử trang tải
    try:
        url = TABLE_LINKS['Standard Stats'][0]
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, TABLE_LINKS['Standard Stats'][1])))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', attrs={'id': TABLE_LINKS['Standard Stats'][1]})

        player_set = {}

        if not table:
            print("Error: Could not find the 'Standard Stats' table.")
            return player_set

        rows = table.find_all('tr', attrs={'data-row': True})

        for row in rows:
            try:
                name = row.find('td', attrs={'data-stat': 'player'}).text.strip()
                nationality = row.find('td', attrs={'data-stat': 'nationality'}).text.strip()
                position = row.find('td', attrs={'data-stat': 'position'}).text.strip()
                team = row.find('td', attrs={'data-stat': 'team'}).text.strip()
                age = row.find('td', attrs={'data-stat': 'age'}).text.strip()
                games = row.find('td', attrs={'data-stat': 'games'}).text.strip()
                games_starts = row.find('td', attrs={'data-stat': 'games_starts'}).text.strip()
                minutes_str = row.find('td', attrs={'data-stat': 'minutes'}).text.strip()
                goals = row.find('td', attrs={'data-stat': 'goals'}).text.strip()
                assist = row.find('td', attrs={'data-stat': 'assists'}).text.strip()
                cards_yellow = row.find('td', attrs={'data-stat': 'cards_yellow'}).text.strip()
                cards_red = row.find('td', attrs={'data-stat': 'cards_red'}).text.strip()
                xg = row.find('td', attrs={'data-stat': 'xg'}).text.strip()
                xg_assist = row.find('td', attrs={'data-stat': 'xg_assist'}).text.strip()
                progressive_carries = row.find('td', attrs={'data-stat': 'progressive_carries'}).text.strip()
                progressive_passes = row.find('td', attrs={'data-stat': 'progressive_passes'}).text.strip()
                progressive_passes_received = row.find('td', attrs={'data-stat': 'progressive_passes_received'}).text.strip()
                goals_per90 = row.find('td', attrs={'data-stat': 'goals_per90'}).text.strip()
                assists_per90 = row.find('td', attrs={'data-stat': 'assists_per90'}).text.strip()
                xg_per90 = row.find('td', attrs={'data-stat': 'xg_per90'}).text.strip()
                xg_assist_per90 = row.find('td', attrs={'data-stat': 'xg_assist_per90'}).text.strip()

                player_data = initialize_player_dict()
                player_data.update({
                    'name': name,
                    'nationality': nationality,
                    'position': position,
                    'team': team,
                    'age': age,
                    'games': games,
                    'games_starts': games_starts,
                    'minutes': minutes_str,
                    'goals': goals,
                    'assist': assist,
                    'cards_yellow': cards_yellow,
                    'cards_red': cards_red,
                    'xg': xg,
                    'xg_assist': xg_assist,
                    'progressive_carries': progressive_carries,
                    'progressive_passes': progressive_passes,
                    'progressive_passes_received': progressive_passes_received,
                    'goals_per90': goals_per90,
                    'assists_per90': assists_per90,
                    'xg_per90': xg_per90,
                    'xg_assist_per90': xg_assist_per90
                })

                minutes_str_cleaned = minutes_str.replace(',', '')
                if minutes_str_cleaned.isdigit() and int(minutes_str_cleaned) <= 90:
                    continue

                player_key = str(name) + str(team)
                player_set[player_key] = player_data

            except Exception as e:
                print(f"Error processing row: {e}")
                continue

    finally:
        driver.quit()

    return player_set

# -----------------------------------------
def update_goalkeeping_stats(player_set):
    """Update player data with goalkeeping statistics.
    Cập nhật dữ liệu cầu thủ với thống kê thủ môn."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    try:
        url = TABLE_LINKS['Goalkeeping'][0]
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, TABLE_LINKS['Goalkeeping'][1])))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', attrs={'id': TABLE_LINKS['Goalkeeping'][1]})

        if not table:
            print("Error: Could not find the 'Goalkeeping' table.")
            return

        rows = table.find_all('tr', attrs={'data-row': True})

        for row in rows:
            try:
                name = row.find('td', attrs={'data-stat': 'player'}).text.strip()
                team = row.find('td', attrs={'data-stat': 'team'}).text.strip()
                player_key = str(name) + str(team)

                if player_key in player_set:
                    player_set[player_key].update({
                        'gk_goals_against_per90': row.find('td', attrs={'data-stat': 'gk_goals_against_per90'}).text.strip(),
                        'gk_save_pct': row.find('td', attrs={'data-stat': 'gk_save_pct'}).text.strip(),
                        'gk_clean_sheets_pct': row.find('td', attrs={'data-stat': 'gk_clean_sheets_pct'}).text.strip(),
                        'gk_pens_save_pct': row.find('td', attrs={'data-stat': 'gk_pens_save_pct'}).text.strip()
                    })
            except Exception as e:
                print(f"Error processing goalkeeping row: {e}")
                continue

    finally:
        driver.quit()

# -----------------------------------------
def update_shooting_stats(player_set):
    """Update player data with shooting statistics.
    Cập nhật dữ liệu cầu thủ với thống kê sút bóng."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    try:
        url = TABLE_LINKS['Shooting'][0]
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, TABLE_LINKS['Shooting'][1])))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', attrs={'id': TABLE_LINKS['Shooting'][1]})

        if not table:
            print("Error: Could not find the 'Shooting' table.")
            return

        rows = table.find_all('tr', attrs={'data-row': True})

        for row in rows:
            try:
                name = row.find('td', attrs={'data-stat': 'player'}).text.strip()
                team = row.find('td', attrs={'data-stat': 'team'}).text.strip()
                player_key = str(name) + str(team)

                if player_key in player_set:
                    player_set[player_key].update({
                        'shots_on_target_pct': row.find('td', attrs={'data-stat': 'shots_on_target_pct'}).text.strip(),
                        'shots_on_target_per90': row.find('td', attrs={'data-stat': 'shots_on_target_per90'}).text.strip(),
                        'goals_per_shot': row.find('td', attrs={'data-stat': 'goals_per_shot'}).text.strip(),
                        'average_shot_distance': row.find('td', attrs={'data-stat': 'average_shot_distance'}).text.strip()
                    })
            except Exception as e:
                print(f"Error processing shooting row: {e}")
                continue

    finally:
        driver.quit()

# -----------------------------------------
def update_passing_stats(player_set):
    """Update player data with passing statistics.
    Cập nhật dữ liệu cầu thủ với thống kê chuyền bóng."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    try:
        url = TABLE_LINKS['Passing'][0]
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, TABLE_LINKS['Passing'][1])))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', attrs={'id': TABLE_LINKS['Passing'][1]})

        if not table:
            print("Error: Could not find the 'Passing' table.")
            return

        rows = table.find_all('tr', attrs={'data-row': True})

        for row in rows:
            try:
                name = row.find('td', attrs={'data-stat': 'player'}).text.strip()
                team = row.find('td', attrs={'data-stat': 'team'}).text.strip()
                player_key = str(name) + str(team)

                if player_key in player_set:
                    player_set[player_key].update({
                        'passes_completed': row.find('td', attrs={'data-stat': 'passes_completed'}).text.strip(),
                        'passes_pct': row.find('td', attrs={'data-stat': 'passes_pct'}).text.strip(),
                        'passes_total_distance': row.find('td', attrs={'data-stat': 'passes_total_distance'}).text.strip(),
                        'passes_pct_short': row.find('td', attrs={'data-stat': 'passes_pct_short'}).text.strip(),
                        'passes_pct_medium': row.find('td', attrs={'data-stat': 'passes_pct_medium'}).text.strip(),
                        'passes_pct_long': row.find('td', attrs={'data-stat': 'passes_pct_long'}).text.strip(),
                        'assisted_shots': row.find('td', attrs={'data-stat': 'assisted_shots'}).text.strip(),
                        'passes_into_final_third': row.find('td', attrs={'data-stat': 'passes_into_final_third'}).text.strip(),
                        'passes_into_penalty_area': row.find('td', attrs={'data-stat': 'passes_into_penalty_area'}).text.strip(),
                        'crosses_into_penalty_area': row.find('td', attrs={'data-stat': 'crosses_into_penalty_area'}).text.strip(),
                        'progressive_passes': row.find('td', attrs={'data-stat': 'progressive_passes'}).text.strip()
                    })
            except Exception as e:
                print(f"Error processing passing row: {e}")
                continue

    finally:
        driver.quit()

# -----------------------------------------
def update_goal_shot_creation_stats(player_set):
    """Update player data with goal and shot creation statistics.
    Cập nhật dữ liệu cầu thủ với thống kê tạo bàn và tạo cơ hội sút."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    try:
        url = TABLE_LINKS['Goal and Shot Creation'][0]
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, TABLE_LINKS['Goal and Shot Creation'][1])))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', attrs={'id': TABLE_LINKS['Goal and Shot Creation'][1]})

        if not table:
            print("Error: Could not find the 'Goal and Shot Creation' table.")
            return

        rows = table.find_all('tr', attrs={'data-row': True})

        for row in rows:
            try:
                name = row.find('td', attrs={'data-stat': 'player'}).text.strip()
                team = row.find('td', attrs={'data-stat': 'team'}).text.strip()
                player_key = str(name) + str(team)

                if player_key in player_set:
                    player_set[player_key].update({
                        'sca': row.find('td', attrs={'data-stat': 'sca'}).text.strip(),
                        'sca_per90': row.find('td', attrs={'data-stat': 'sca_per90'}).text.strip(),
                        'gca': row.find('td', attrs={'data-stat': 'gca'}).text.strip(),
                        'gca_per90': row.find('td', attrs={'data-stat': 'gca_per90'}).text.strip()
                    })
            except Exception as e:
                print(f"Error processing goal and shot creation row: {e}")
                continue

    finally:
        driver.quit()

# -----------------------------------------
def update_defensive_stats(player_set):
    """Update player data with defensive actions statistics.
    Cập nhật dữ liệu cầu thủ với thống kê hành động phòng ngự."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    try:
        url = TABLE_LINKS['Defense'][0]
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, TABLE_LINKS['Defense'][1])))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', attrs={'id': TABLE_LINKS['Defense'][1]})

        if not table:
            print("Error: Could not find the 'Defense' table.")
            return

        rows = table.find_all('tr', attrs={'data-row': True})

        for row in rows:
            try:
                name = row.find('td', attrs={'data-stat': 'player'}).text.strip()
                team = row.find('td', attrs={'data-stat': 'team'}).text.strip()
                player_key = str(name) + str(team)

                if player_key in player_set:
                    player_set[player_key].update({
                        'tackles': row.find('td', attrs={'data-stat': 'tackles'}).text.strip(),
                        'tackles_won': row.find('td', attrs={'data-stat': 'tackles_won'}).text.strip(),
                        'challenges': row.find('td', attrs={'data-stat': 'challenges'}).text.strip(),
                        'challenges_lost': row.find('td', attrs={'data-stat': 'challenges_lost'}).text.strip(),
                        'blocks': row.find('td', attrs={'data-stat': 'blocks'}).text.strip(),
                        'blocked_shots': row.find('td', attrs={'data-stat': 'blocked_shots'}).text.strip(),
                        'blocked_passes': row.find('td', attrs={'data-stat': 'blocked_passes'}).text.strip(),
                        'interceptions': row.find('td', attrs={'data-stat': 'interceptions'}).text.strip()
                    })
            except Exception as e:
                print(f"Error processing defensive actions row: {e}")
                continue

    finally:
        driver.quit()

# -----------------------------------------
def update_possession_stats(player_set):
    """Update player data with possession statistics.
    Cập nhật dữ liệu cầu thủ với thống kê kiểm soát bóng."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    try:
        url = TABLE_LINKS['Possession'][0]
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, TABLE_LINKS['Possession'][1])))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', attrs={'id': TABLE_LINKS['Possession'][1]})

        if not table:
            print("Error: Could not find the 'Possession' table.")
            return

        rows = table.find_all('tr', attrs={'data-row': True})

        for row in rows:
            try:
                name = row.find('td', attrs={'data-stat': 'player'}).text.strip()
                team = row.find('td', attrs={'data-stat': 'team'}).text.strip()
                player_key = str(name) + str(team)

                if player_key in player_set:
                    player_set[player_key].update({
                        'touches': row.find('td', attrs={'data-stat': 'touches'}).text.strip(),
                        'touches_def_pen_area': row.find('td', attrs={'data-stat': 'touches_def_pen_area'}).text.strip(),
                        'touches_def_3rd': row.find('td', attrs={'data-stat': 'touches_def_3rd'}).text.strip(),
                        'touches_mid_3rd': row.find('td', attrs={'data-stat': 'touches_mid_3rd'}).text.strip(),
                        'touches_att_3rd': row.find('td', attrs={'data-stat': 'touches_att_3rd'}).text.strip(),
                        'touches_att_pen_area': row.find('td', attrs={'data-stat': 'touches_att_pen_area'}).text.strip(),
                        'take_ons': row.find('td', attrs={'data-stat': 'take_ons'}).text.strip(),
                        'take_ons_won_pct': row.find('td', attrs={'data-stat': 'take_ons_won_pct'}).text.strip(),
                        'take_ons_tackled_pct': row.find('td', attrs={'data-stat': 'take_ons_tackled_pct'}).text.strip(),
                        'carries': row.find('td', attrs={'data-stat': 'carries'}).text.strip(),
                        'carries_progressive_distance': row.find('td', attrs={'data-stat': 'carries_progressive_distance'}).text.strip(),
                        'carries_into_final_third': row.find('td', attrs={'data-stat': 'carries_into_final_third'}).text.strip(),
                        'carries_into_penalty_area': row.find('td', attrs={'data-stat': 'carries_into_penalty_area'}).text.strip(),
                        'miscontrols': row.find('td', attrs={'data-stat': 'miscontrols'}).text.strip(),
                        'dispossessed': row.find('td', attrs={'data-stat': 'dispossessed'}).text.strip(),
                        'passes_received': row.find('td', attrs={'data-stat': 'passes_received'}).text.strip()
                    })
            except Exception as e:
                print(f"Error processing possession row: {e}")
                continue

    finally:
        driver.quit()

# -----------------------------------------
def update_miscellaneous_stats(player_set):
    """Update player data with miscellaneous statistics.
    Cập nhật dữ liệu cầu thủ với thống kê linh tinh."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    try:
        url = TABLE_LINKS['Miscellaneous'][0]
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, TABLE_LINKS['Miscellaneous'][1])))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', attrs={'id': TABLE_LINKS['Miscellaneous'][1]})

        if not table:
            print("Error: Could not find the 'Miscellaneous' table.")
            return

        rows = table.find_all('tr', attrs={'data-row': True})

        for row in rows:
            try:
                name = row.find('td', attrs={'data-stat': 'player'}).text.strip()
                team = row.find('td', attrs={'data-stat': 'team'}).text.strip()
                player_key = str(name) + str(team)

                if player_key in player_set:
                    player_set[player_key].update({
                        'fouls': row.find('td', attrs={'data-stat': 'fouls'}).text.strip(),
                        'fouled': row.find('td', attrs={'data-stat': 'fouled'}).text.strip(),
                        'offsides': row.find('td', attrs={'data-stat': 'offsides'}).text.strip(),
                        'crosses': row.find('td', attrs={'data-stat': 'crosses'}).text.strip(),
                        'ball_recoveries': row.find('td', attrs={'data-stat': 'ball_recoveries'}).text.strip(),
                        'aerials_won': row.find('td', attrs={'data-stat': 'aerials_won'}).text.strip(),
                        'aerials_lost': row.find('td', attrs={'data-stat': 'aerials_lost'}).text.strip(),
                        'aerials_won_pct': row.find('td', attrs={'data-stat': 'aerials_won_pct'}).text.strip()
                    })
            except Exception as e:
                print(f"Error processing miscellaneous row: {e}")
                continue

    finally:
        driver.quit()

# -----------------------------------------
def get_player_name(player_dict):
    """Extract player name from dictionary for sorting.
    Trích xuất tên cầu thủ từ từ điển để sắp xếp."""
    return player_dict.get('name', '')

# -----------------------------------------
def format_player_data(player_dict):
    """Format player data into a list for export in correct order.
    Định dạng dữ liệu cầu thủ thành danh sách để xuất theo thứ tự đúng."""
    export_order_keys = [
        'name', 'nationality', 'team', 'position', 'age', 'games', 'games_starts', 'minutes', 'goals', 'assist',
        'cards_yellow', 'cards_red', 'xg', 'xg_assist', 'progressive_carries', 'progressive_passes',
        'progressive_passes_received', 'goals_per90', 'assists_per90', 'xg_per90', 'xg_assist_per90',
        'gk_goals_against_per90', 'gk_save_pct', 'gk_clean_sheets_pct', 'gk_pens_save_pct', 'shots_on_target_pct',
        'shots_on_target_per90', 'goals_per_shot', 'average_shot_distance', 'passes_completed', 'passes_pct',
        'passes_total_distance', 'passes_pct_short', 'passes_pct_medium', 'passes_pct_long', 'assisted_shots',
        'passes_into_final_third', 'passes_into_penalty_area', 'crosses_into_penalty_area', 'sca', 'sca_per90',
        'gca', 'gca_per90', 'tackles', 'tackles_won', 'challenges', 'challenges_lost', 'blocks', 'blocked_shots',
        'blocked_passes', 'interceptions', 'touches', 'touches_def_pen_area', 'touches_def_3rd', 'touches_mid_3rd',
        'touches_att_3rd', 'touches_att_pen_area', 'take_ons', 'take_ons_won_pct', 'take_ons_tackled_pct', 'carries',
        'carries_progressive_distance', 'carries_into_final_third', 'carries_into_penalty_area', 'miscontrols',
        'dispossessed', 'passes_received', 'fouls', 'fouled', 'offsides', 'crosses', 'ball_recoveries', 'aerials_won',
        'aerials_lost', 'aerials_won_pct'
    ]

    nationality = player_dict.get('nationality', 'N/a')
    age = player_dict.get('age', 'N/a')
    nationality_processed = nationality.split()[1] if ' ' in nationality else nationality
    age_processed = age.split('-')[0] if '-' in age else age

    exported_list = []
    for key in export_order_keys:
        if key == 'nationality':
            exported_list.append(nationality_processed)
        elif key == 'age':
            exported_list.append(age_processed)
        else:
            exported_list.append(player_dict.get(key, 'N/a'))

    return exported_list

# -----------------------------------------
def export_to_csv(player_set_dict):
    """Export player data to a CSV file.
    Xuất dữ liệu cầu thủ ra file CSV."""
    playerlist = list(player_set_dict.values())
    playerlist.sort(key=get_player_name)
    result = [format_player_data(player_dict) for player_dict in playerlist]

    column_names = [
        'Name', 'Nation', 'Team', 'Position', 'Age', 'Matches Played', 'Starts', 'Minutes', 'Goals', 'Assists',
        'Yellow Cards', 'Red Cards', 'Expected Goals (xG)', 'Expected Assist Goals (xAG)', 'Progressive Carries (PrgC)',
        'Progressive Passes (PrgP)', 'Progressive Passes Received (PrgR)', 'Goals per 90', 'Assists per 90',
        'xG per 90', 'xAG per 90', 'Goals Against per 90 (GA90)', 'Save Percentage (Save%)', 'Clean Sheets Percentage (CS%)',
        'Penalty Kicks Save Percentage', 'Shots on Target Percentage (SoT%)', 'Shots on Target per 90 (SoT/90)',
        'Goals per Shot (G/Sh)', 'Average Shot Distance (Dist)', 'Passes Completed (Cmp)', 'Pass Completion Percentage (Cmp%)',
        'Total Passing Distance (TotDist)', 'Short Pass Completion Percentage', 'Medium Pass Completion Percentage',
        'Long Pass Completion Percentage', 'Key Passes (KP)', 'Passes into Final Third (1/3)', 'Passes into Penalty Area (PPA)',
        'Crosses into Penalty Area (CrsPA)', 'Shot-Creating Actions (SCA)', 'SCA per 90', 'Goal-Creating Actions (GCA)',
        'GCA per 90', 'Tackles (Tkl)', 'Tackles Won (TklW)', 'Challenges (Tkl)', 'Challenges Lost (TklD)', 'Blocks',
        'Blocked Shots (Sh)', 'Blocked Passes (Pass)', 'Interceptions (Int)', 'Touches', 'Touches in Defensive Penalty Area',
        'Touches in Defensive Third', 'Touches in Middle Third', 'Touches in Attacking Third', 'Touches in Attacking Penalty Area',
        'Take-Ons (Att)', 'Take-On Success Percentage (Succ%)', 'Take-On Tackled Percentage (Tkl%)', 'Carries',
        'Progressive Carrying Distance (TotDist)', 'Carries into Final Third (1/3)', 'Carries into Penalty Area (CPA)',
        'Miscontrols (Mis)', 'Dispossessed (Dis)', 'Passes Received (Rec)', 'Fouls Committed (Fls)', 'Fouls Drawn (Fld)',
        'Offsides (Off)', 'Crosses (Crs)', 'Ball Recoveries (Recov)', 'Aerials Won (Won)', 'Aerials Lost (Lost)',
        'Aerials Won Percentage (Won%)'
    ]

    df = pd.DataFrame(result, columns=column_names)
    output_file = 'premier_league_player_stats.csv'
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Data exported successfully to {output_file}")

# -----------------------------------------
def main():
    """Main function to orchestrate the scraping and exporting process.
    Hàm chính để điều phối quá trình thu thập và xuất dữ liệu."""
    print("Starting data scraping...")
    player_set = scrape_standard_stats()
    if not player_set:
        print("No player data collected. Exiting.")
        return

    print("Updating player data with additional stats...")
    update_goalkeeping_stats(player_set)
    update_shooting_stats(player_set)
    update_passing_stats(player_set)
    update_goal_shot_creation_stats(player_set)
    update_defensive_stats(player_set)
    update_possession_stats(player_set)
    update_miscellaneous_stats(player_set)

    print("Exporting data to CSV...")
    export_to_csv(player_set)

# -----------------------------------------
if __name__ == "__main__":
    main()