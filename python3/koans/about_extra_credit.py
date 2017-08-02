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


class Game:
    def __init__(self, name):
        self._name = name
        self._maxPlayers = 4
        self._maxRounds = 4
        self._currentRound = 0
        self._players = []
        self._internalScore = dict()
        self._game_over = False
    
    def some_method(self):
        pass
    
    def add_player(self, player):
        if len(self._players) == 4:
            return "too many players"
        if player in self._players:
            return "player is already in the game"
        if self._currentRound > 0:
            return "game in progress"
        self._players.append(player)
        self._internalScore[len(self._players) - 1] = 0

    def play_round(self):
        if len(self._players) < 2:
            return "at least 2 players are required"
        if self._currentRound == self._maxRounds:
            self._game_over = True
            return "Game Over"
        self._currentRound += 1
        for idx, player in enumerate(self._players):
            ds = DiceSet()
            ds.roll(5)
            scr = score(ds.values)
            self._internalScore[idx] += scr

    def remove_player(self, player):
            pass

class AboutExtraCredit(Koan):
    # Write tests here. If you need extra test classes add them to the
    # test suite in runner/path_to_enlightenment.py

    def inst_player_class(self,player_names):
        player_insts = dict()
        for idx, p in enumerate(player_names):
            inst_of_player = Player(str.capitalize(player_names[idx]))
            player_insts[p] = inst_of_player
        return player_insts

    def test_extra_credit_task(self):
        pass
  
    def test_create_and_add_player(self):
        player_names = ["stepan", "pepa", "jan", "karel"]
        player_insts = self.inst_player_class(player_names)
        hra = Game("Hra")
        for p in player_names:
            hra.add_player(player_insts[p])
        self.assertEqual(len(hra._players),4)
    
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
        self.assertEqual(len(hra._players),hra._maxPlayers)
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

    def test_can_collect_players_result_when_game_over(self):
        player_names = ["stepan", "pepa", "jan", "karel"]
        player_insts = self.inst_player_class(player_names)
        hra = Game("Hra")
        for p in player_names:
            hra.add_player(player_insts[p])
        for i in range(0, hra._maxRounds):
            hra.play_round()
        for idx, p in enumerate(player_names):
            player_insts[p]._score += hra._internalScore[idx]