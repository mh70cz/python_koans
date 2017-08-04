#!/usr/bin/env python
# -*- coding: utf-8 -*-

# EXTRA CREDIT:
#
# Create a program that will play the Greed Game.
# Rules for the game are in GREED_RULES.TXT.
#
# You already have a DiceSet class and score function you can use.
# Write a player class and a Game class to complete the project.  This
# is a free form assignment, so approach it however you desire.

from runner.koan import *
from .about_dice_project import DiceSet
from .about_scoring_project import score

class Player:
    def __init__(self, name):
        self._name = name
        self._score = 0
        self._playedGames = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        _name = name

    @property
    def score(self):
        return self._score

class Game:
    def __init__(self, name):
        self._name = name
        self._maxPlayers = 4
        self._maxRounds = 4
        self._currentRound = 0
        self._players = []
        self._internalScore = []
        self._game_over = False

    @property
    def current_round(self):
        return self._currentRound

    @property
    def players(self):
        return self._players

    @property
    def game_over(self):
        return self._game_over

    @property
    def internal_score(self):
        return self._internalScore

    def add_player(self, player):
        if len(self._players) == 4:
            return "too many players"
        if player in self._players:
            return "player is already in the game"
        if self._game_over:
            return "Game Over"
        if self._currentRound > 0:
            return "game in progress"
        self._players.append(player)
        self._internalScore.append(0)

    def play_round(self):
        if len(self._players) < 2:
            return "at least 2 players are required"
        if self._game_over:
            return "Game Over"
        self._currentRound += 1
        for idx, player in enumerate(self._players):
            ds = DiceSet()
            ds.roll(5)
            scr = score(ds.values)
            self._internalScore[idx] += scr
        if self._currentRound == self._maxRounds:
            self._game_over = True
            self._collect_score()
            return "Game Over"

    def remove_player(self, player):
        if player in self._players:
            del self._internalScore[self._players.index(player)]
            self._players.remove(player)
        else:
            return "not such a player in the game"
        if len(self._players) < 2 and self._currentRound > 0:
            self._game_over = True
            self._collect_score()
            return "not enough players to continue"

    def _collect_score(self):
        if self.game_over:
            for p in self._players:
                p._score += self._internalScore[self._players.index(p)]

class AboutExtraCredit(Koan):
    # Write tests here. If you need extra test classes add them to the
    # test suite in runner/path_to_enlightenment.py

    def inst_player_class(self, player_inst_names):
        player_insts = dict()
        for idx, p in enumerate(player_inst_names):
            inst_of_player = Player(str.capitalize(player_inst_names[idx]))
            player_insts[p] = inst_of_player
        return player_insts

    def test_create_and_add_player(self):
        player_names = ["stepan", "pepa", "jan", "karel"]
        player_insts = self.inst_player_class(player_names)
        hra = Game("Hra")
        for p in player_names:
            hra.add_player(player_insts[p])
        self.assertEqual(len(hra.players), 4)

    def test_player_can_play_in_more_games_simultaneously(self):
        hrac1 = Player("Hrac1")
        hrac2 = Player("Hrac2")
        hrac3 = Player("Hrac3")
        hra1 = Game("hra1")
        hra2 = Game("hra2")
        hra1.add_player(hrac1)
        hra1.add_player(hrac2)
        hra1.add_player(hrac3)
        hra2.add_player(hrac1)
        hra2.add_player(hrac2)
        self.assertEqual(len(hra1.players), 3)
        self.assertEqual(len(hra2.players), 2)

    def test_player_must_be_unique(self):
        hrac1 = Player("Hrac1")
        hrac2 = Player("Hrac2")
        hra = Game("hra")
        hra.add_player(hrac1)
        hra.add_player(hrac2)
        ret_val = hra.add_player(hrac1)
        self.assertRegex("player is already in the game", ret_val)

    def test_game_can_be_played_by_at_least_2_playes(self):
        hrac1 = Player("Hrac1")
        hra = Game("Hra")
        hra.add_player(hrac1)
        ret_val = hra.play_round()
        self.assertRegex(ret_val, "at least 2 players are required")

    def test_game_can_be_played_by_at_most_max_playes(self):
        player_names = ["stepan", "pepa", "jan", "karel", "andrej", "milos", "jarda"]
        player_insts = self.inst_player_class(player_names)
        extra_hrac = Player("Extra")
        hra = Game("Hra")
        for i in range(0, hra._maxPlayers):
            hra.add_player(player_insts[player_names[i]])
        self.assertEqual(len(hra.players), hra._maxPlayers)
        ret_val = hra.add_player(extra_hrac)
        self.assertRegex(ret_val, "too many players")

    def test_no_new_players_if_game_in_progress(self):
        hrac1 = Player("Hrac1")
        hrac2 = Player("Hrac2")
        hrac3 = Player("Hrac3")
        hra = Game("Hra")
        hra.add_player(hrac1)
        hra.add_player(hrac2)
        hra.play_round()
        ret_val = hra.add_player(hrac3)
        self.assertRegex(ret_val, "game in progress")

    def test_remove_player_before_start(self):
        hrac1 = Player("Hrac1")
        hrac2 = Player("Hrac2")
        hra = Game("Hra")
        hra.add_player(hrac1)
        hra.add_player(hrac2)
        hra.remove_player(hrac2)
        self.assertEqual(len(hra.players), 1)

    def test_try_remove_player_who_is_not_in_the_game(self):
        hrac1 = Player("Hrac1")
        hrac2 = Player("Hrac2")
        hrac3 = Player("Hrac3")
        hra = Game("Hra")
        hra.add_player(hrac1)
        hra.add_player(hrac2)      
        ret_val = hra.remove_player(hrac3)
        self.assertRegex(ret_val, "not such a player in the game")

    def test_remove_player_after_start(self):
        hrac1 = Player("Hrac1")
        hrac2 = Player("Hrac2")
        hrac3 = Player("Hrac3")
        hra = Game("Hra")
        hra.add_player(hrac1)
        hra.add_player(hrac2)
        hra.add_player(hrac3)
        hra.play_round()
        hra.remove_player(hrac2)
        self.assertEqual(len(hra.players), 2)

    def test_remove_player_after_start_too_few_players(self):
        hrac1 = Player("Hrac1")
        hrac2 = Player("Hrac2")
        hra = Game("Hra")
        hra.add_player(hrac1)
        hra.add_player(hrac2)
        hra.play_round()
        ret_val = hra.remove_player(hrac2)
        self.assertRegex(ret_val, "not enough players to continue")
        self.assertEqual(hra.game_over, True)

    def test_game_over_after_max_rounds(self):
        hrac1 = Player("Hrac1")
        hrac2 = Player("Hrac2")
        hrac3 = Player("Hrac3")
        hrac4 = Player("Hrac4")
        hra = Game("Hra")
        hra.add_player(hrac1)
        hra.add_player(hrac2)
        hra.add_player(hrac3)
        hra.add_player(hrac4)
        for i in range(0, hra._maxRounds):
            hra.play_round()
        ret_val = hra.play_round()
        self.assertRegex(ret_val, "Game Over")

    def test_can_collect_players_results_when_game_over(self):
        player_names = ["stepan", "pepa", "jan", "karel"]
        player_insts = self.inst_player_class(player_names)
        hra = Game("Hra")
        for p in player_names:
            hra.add_player(player_insts[p])
        for idx, p in enumerate(player_names):
            self.assertEqual(player_insts[p]._score, 0)
        for i in range(0, hra._maxRounds):
            hra.play_round()
        for idx, p in enumerate(player_names):
            self.assertEqual(player_insts[p]._score, hra.internal_score[idx], idx)
           
    def test_internal_score_is_not_messed_after_removal_of_player(self):
        hrac1 = Player("Hrac1")
        hrac2 = Player("Hrac2")
        hrac3 = Player("Hrac3")
        hrac4 = Player("Hrac4")
        hra = Game("Hra")
        hra.add_player(hrac1)
        hra.add_player(hrac2)
        hra.add_player(hrac3)
        hra.add_player(hrac4)
        hra.play_round()
        hra.play_round()
        hra.play_round()
        is_h1 = hra.internal_score[0]
        is_h2 = hra.internal_score[1]
        is_h4 = hra.internal_score[3]
        hra.remove_player(hrac3)
        self.assertEqual(is_h1, hra.internal_score[0])
        self.assertEqual(is_h2, hra.internal_score[1])
        self.assertEqual(is_h4, hra.internal_score[2])

    def test_removed_player_gets_no_points(self):
        hrac1 = Player("Hrac1")
        hrac2 = Player("Hrac2")
        hrac3 = Player("Hrac3")
        hrac4 = Player("Hrac4")
        starting_score_h3 = hrac3.score
        hra = Game("Hra")
        hra.add_player(hrac1)
        hra.add_player(hrac2)
        hra.add_player(hrac3)
        hra.add_player(hrac4)
        hra.play_round()
        hra.play_round()
        hra.play_round()
        hra.remove_player(hrac3)
        self.assertEqual(starting_score_h3, hrac3.score)

    def test_players_score_is_persisted(self):
        player_inst_names = ["stepan", "pepa", "jan", "karel"]
        player_insts = self.inst_player_class(player_inst_names)
        hra = Game("Hra")
        for p in player_inst_names:
            hra.add_player(player_insts[p])
        for i in range(0, hra._maxRounds):
            hra.play_round()

        score_after_first_game = []
        for p in player_inst_names:
            score_after_first_game.append(player_insts[p].score)

        nova_hra = Game("Nova hra")
        for p in player_inst_names:
            nova_hra.add_player(player_insts[p])
        for i in range(0, nova_hra._maxRounds):
            nova_hra.play_round()

        for idx, p in enumerate(player_inst_names):
            if nova_hra._internalScore[idx] == 0:
                #rare
                self.assertEqual(score_after_first_game[idx], player_insts[p].score, idx)
            else:
                self.assertLess(score_after_first_game[idx], player_insts[p].score, idx)
