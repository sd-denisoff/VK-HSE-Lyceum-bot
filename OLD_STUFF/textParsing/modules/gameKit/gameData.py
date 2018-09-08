import sys
sys.path.append('textParsing/modules/gameKit/games/')

import allGames

class GamesData:
    gamesClass = {}
    searchKeyWords = {}

    for game in allGames.games:
        gamesClass[game.__title__] = game.Game()
        for word in game.__searchWords__:
            searchKeyWords[word] = game.__title__
