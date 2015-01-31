#!/usr/bin/env python
#

"""
// The DoTurn function is where your code goes. The PlanetWars object contains
// the state of the game, including information about all planets and fleets
// that currently exist. Inside this function, you issue orders using the
// pw.IssueOrder() function. For example, to send 10 ships from planet 3 to
// planet 8, you would say pw.IssueOrder(3, 8, 10).
//
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own. Check out the tutorials and articles on the contest website at
// http://www.ai-contest.com/resources.
"""
from PlanetWars import PlanetWars

import random
import sys

messageHistory = []
allies_nicks = []

def DoTurn(pw, group_ids, nickname, f):

  # write message log
  tmp = []
  for mes in pw.Messages():
    tmp.append((mes.Nickname(), mes.Number()))
  messageHistory.append(tmp)

  # send planet position
  if not messageHistory:
    mes = pw.MyPlanets()[0].PlanetID()
  else:
    mes = random.randint(-214783648, 2147483647)

  # # find out and remember party nickname  
  if not allies_nicks and messageHistory:
    tmp = messageHistory[-1]
    for msh in tmp:
      # f.write('=====msh[1]' + str(msh[1] ) + '\n')
      for pln in pw.Planets():
        if pln.PlanetID() == int(msh[1]) and \
          pln.Owner() in group_ids:
          # f.write('=====if' + str(pln.PlanetID() ) + '\n')
          for gip in group_ids:
            if pln.Owner() == int(gip):
              allies_nicks.append(( msh[0], pln.Owner() ))
              # f.write('=====planet.Owner()' + str(pln.Owner() ) + '\n')
              

        
  f.write('======= ' + str(messageHistory) + '\n')
  f.write('======= ' + str(allies_nicks) + '\n')
  pw.SendMessage(nickname,mes)



    # f.write('======= ' + str(mes.Number()) + '\n')

  # (1) If we currently have a fleet in flight, just do nothing.
  # if len(pw.MyFleets()) >= 2:
  #   return
  
  # Ship count
  mySize = 0
  alliesSize = 0
  enemySize = 0
  # Ships growth
  myGrowth = 0
  alliesGrowth = 0
  enemyGrowth = 0

  # My power
  for p in pw.MyPlanets():
    mySize += p.NumShips()
    myGrowth += p.GrowthRate()

  # Allies power
  for p in pw.EnemyPlanets():
    if p.Owner() in group_ids:
      alliesSize += p.NumShips()
      alliesGrowth += p.GrowthRate()

  # Enemies power
  for p in pw.EnemyPlanets():
    enemySize += p.NumShips()
    enemyGrowth += p.GrowthRate()

  # # Enemies targets
  # for fleet in pw.EnemyFleets():
  #   if fleet.Owner() in group_ids:
  #     continue
  #   enemyTargets.append(fleet)

  if ( enemySize <= 0 ):
    winRatio = 0
  else:
    # winRatio = float(mySize/enemySize)
    winRatio = float(mySize)/enemySize
    # winRatio = float(mySize + alliesSize/enemyGrowth) / (enemySize/(myGrowth+alliesGrowth))

  f.write('======= winRatio: ' + str(winRatio) + '\n')

  # (2) Find my strongest planet.
  source = -1
  source_score = -999999.0
  # source_num_ships = 0
  my_planets = pw.MyPlanets()
  for p in my_planets:
    score = float(p.NumShips())
    # if score > source_score:
    if score > p.GrowthRate() * 10:
      source_score = score
      source = p #.PlanetID()
      # source_num_ships = p.NumShips()

      # (3) Find the weakest enemy or neutral planet.
      # dest = -1
      # dest_score = -999999.0
      # not_my_planets = pw.NotMyPlanets()
      planets = pw.Planets()
      
      # (3.1) remove group members planets from list
      tmp = []
      for p in planets:
        if p.Owner() in group_ids:
          continue
        tmp.append(p)
      planets = tmp
      # f.write('not_my_planets: ' + ', '.join([str( p.Owner() ) for p in not_my_planets]) + '\n')
      
      # (3.2) remove planets which awaiting group member fleets
      planet_ids = [] # not_my_planets ids
      if planets:
        planet_ids = ([p.PlanetID() for p in planets])
      # f.write('planet_ids: ' + ', '.join([str( p ) for p in planet_ids]) + '\n')
      # f.write('planet_ids: ' + ', '.join([str( p ) for p in planet_ids]) + '\n')
      gfp_ids = [] # group_fleet_planet_ids
      # f.write('EnemyFleets DestinationPlanets: ' + ', '.join([str( fl.DestinationPlanet() ) for fl in pw.EnemyFleets() ]) + '\n')
      for fl in pw.EnemyFleets():
        if fl.Owner() in group_ids and fl.DestinationPlanet() in planet_ids:
          gfp_ids.append(fl.DestinationPlanet())
      gfp_ids = set(gfp_ids)
      # f.write('gfp_ids: ' + ', '.join([str( fl ) for fl in gfp_ids]) + '\n')

      # (3.3) remove planets which awaiting my fleets
      # my_fp_ids = [] # my_fleet_planet_ids
      # # f.write('EnemyFleets DestinationPlanets: ' + ', '.join([str( fl.DestinationPlanet() ) for fl in pw.EnemyFleets() ]) + '\n')
      # for fl in pw.MyFleets():
      #   if fl.DestinationPlanet() in planet_ids:
      #     my_fp_ids.append(fl.DestinationPlanet())
      # my_fp_ids = set(my_fp_ids)

      # ATTACK Planets
      # not_my_planets

      my_planet_ids = ([p.PlanetID() for p in pw.MyPlanets()])
      # (4) analyze planets
      # not_my_planets = tmp
      # f.write('not_my_planets: ' + ', '.join([str( p.Owner() ) for p in not_my_planets]) + '\n')
      planets_rank = [] 
      for p in planets:
        if p.PlanetID() in gfp_ids: # or p.PlanetID() in my_fp_ids:
          continue 
        # planet's obtain score or defeat
        killrate = 1
        defeat = 1
        if winRatio >= 1.5:
          # Killer mode
          f.write('KILLMODE \n')
          if p.Owner() != 0: # enemy
            killrate += 1000
        elif p.PlanetID() in my_planet_ids:
          for fleet in pw.EnemyFleets():
            if fl.Owner() in group_ids:
              continue
            if fleet.DestinationPlanet() == p.PlanetID():
              defeat = 1000
              # defeat = ( pw.Distance(source.PlanetID(), p.PlanetID()) )
        score = (1.0 * p.GrowthRate() * killrate * defeat ) / (1 + p.NumShips() + 2 * pw.Distance(source.PlanetID(), p.PlanetID())) 

        planets_rank.append([p, score])
        # if score > dest_score:
        #   dest_score = score
        #   dest = p #.PlanetID()
      # f.write('planets_rank: ' + ', '.join([str( p[1] ) for p in planets_rank]) + '\n')
      planets_rank.sort(key=lambda x: x[1], reverse=True)
      f.write('planets_rank Owner: ' + ', '.join([str( p[0].Owner() ) for p in planets_rank]) + '\n')
      # f.write('planets_rank NumShips: ' + ', '.join([str( p[0] ) for p in planets_rank]) + '\n')
      f.write('planets_rank: ' + ', '.join([str( p[1] ) for p in planets_rank]) + '\n')

      # (5) Send ships from my strongest planet to others
      sent_ships = 0
      for elem in planets_rank:
        f.write('planet: ' + str(elem[0]) + '\n')
        f.write('planets score: ' + str(elem[1]) + '\n')
        if (source.NumShips() - sent_ships * 3) <= 0:
          return
        dest = elem[0] # planet
        req_num_ships = dest.NumShips()

        # NOTE: worse result on current
        #
        for fleet in pw.EnemyFleets():
          if fl.Owner() in group_ids:
            continue
          if fleet.DestinationPlanet() == dest.PlanetID():
            req_num_ships += fleet.NumShips()

        for fleet in pw.MyFleets():
          if fleet.DestinationPlanet() == dest.PlanetID():
            req_num_ships -= fleet.NumShips()

        if req_num_ships < 0:
          continue 

        f.write('req_num_ships: ' + str(req_num_ships) + '\n')
        add_ships = 1
        f.write('dest.Owner(): ' + str(dest.Owner()) + '\n')
        if dest.Owner() != 0: # foe (not neutral)
          add_ships += dest.GrowthRate() * int(pw.Distance(source.PlanetID(), dest.PlanetID() ))
          f.write('add_ships: ' + str(add_ships) + '\n')
          if winRatio >= 1.5:
            # Killer mode
            add_ships += int(add_ships * 0.3)
        num_ships = req_num_ships * 2 + add_ships
        f.write('num_ships: ' + str(num_ships) + '\n')
        if (source.NumShips() - sent_ships - num_ships) >= 0:
          sent_ships += num_ships
          pw.IssueOrder(source.PlanetID(), dest.PlanetID(), num_ships)
        # else:
        #   num_ships = source.NumShips() - sent_ships
        #   if num_ships > 50:
        #     sent_ships += int(num_ships/2)
        #     pw.IssueOrder(source.PlanetID(), dest.PlanetID(), int(num_ships/2))






def main():
  f = open('MyBot4.log', 'w')
  group_ids = []
  nickname = 'X'
  if '-g' in sys.argv:
    group_ids = [int(k) for k in sys.argv[2].split(',')]
  if '-n' in sys.argv:
    nickname = str(sys.argv[4])
  f.write('group: ' + str(group_ids) + '\n')
  f.write('nick: ' + str(nickname) + '\n')

  map_data = ''
  while(True):
    current_line = raw_input()
    f.write(current_line + '\n')
    if len(current_line) >= 1 and current_line.startswith("."):
      pw = PlanetWars(map_data)
      f.write('-------------- NEW TURN ----------------\n')
      DoTurn(pw, group_ids, nickname, f)
      f.write('----------------------------------------\n')
      pw.FinishTurn()
      map_data = ''
    else:
      map_data += current_line + '\n'


if __name__ == '__main__':
  try:
    import psyco
    psyco.full()
  except ImportError:
    pass
  try:
    main()
  except KeyboardInterrupt:
    print 'ctrl-c, leaving ...'