players_dict = {
    1: {'name': 'Vanya', 'team': 'A', 'status': 'Rest'},
    2: {'name': 'Lena', 'team': 'B', 'status': 'Training'},
    3: {'name': 'Maxim', 'team': 'C', 'status': 'Travel'},
    4: {'name': 'Egor', 'team': 'C', 'status': 'Rest'},
    5: {'name': 'Andrei', 'team': 'A', 'status': 'Training'},
    6: {'name': 'Sasha', 'team': 'A', 'status': 'Rest'},
    7: {'name': 'Alina', 'team': 'B', 'status': 'Rest'},
    8: {'name': 'Masha', 'team': 'C', 'status': 'Travel'}
}

# print('Члены команды А, которые отдыхают:', ' '.join([
#     player['name']
#     for player in players_dict.values()
#     if player['team'] == 'A' and player['status'] == 'Rest'
# ]))
# print('Члены команды B, которые тренеруются:', ' '.join([
#     player['name']
#     for player in players_dict.values()
#     if player['team'] == 'B' and player['status'] == 'Training'
# ]))
# print('Члены команды С, которые путешествуют:', ' '.join([
#     player['name']
#     for player in players_dict.values()
#     if player['team'] == 'C' and player['status'] == 'Travel'
# ]))

# Чтобы не прописывать решение "в лоб", вручную подставляя статус и команду - попробуем сформировать дополнительные словарь и список,
# чтобы автоматизировать этот процесс:
help_dict = {"Rest": "отдыхают",
             "Training": "тренируются",
             "Travel": "путешествуют"}

team_order = ["A", "B", "C"]

# Запустим цикл по словарю состояний и одновременно будем вести счёт состояний, чтобы на каждой итерации выбирать одну из команд:
for index, state in enumerate(help_dict):
    print("Все члены команды из команды {0}, которые {1}:".format(team_order[index], help_dict[state]))
    for _, player in players_dict.items():
        if player["status"] == state and player["team"] == team_order[index]:
            print(player["name"])
