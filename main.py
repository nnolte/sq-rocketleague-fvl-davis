# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits
import math

class Bot(GoslingAgent):
    # This function runs every in-game tick (every time the game updates anything)
    def distance_between(self, pos1, pos2):
        xdiff = pos1.x - pos2.x
        ydiff = pos1.y -  pos2.y
        return math.sqrt(xdiff*xdiff + ydiff*ydiff)

    def run(self):
        if self.intent is not None:
            return
        d1 = abs(self.ball.location.y - self.foe_goal.location.y)
        d2 = abs(self.me.location.y - self.foe_goal.location.y)
        infront_of_ball = d1 > d2
        if self.kickoff_flag:
            self.set_intent(kickoff())
            return
        
        if self.distance_between(self.ball.location, self.friend_goal.location) < 4000:
            print("defend")
            self.set_intent(goto(self.friend_goal.location))

        if self.distance_between(self.ball.location, self.me.location) < 1000:
            print("Ignore")
            self.set_intent(short_shot(self.foe_goal.location))
        
        # if self.me.boost >= 76:
        #     '''print("die")
        #     distance_between = math.sqrt((self.me.location.x - self.foes[0].location.x)*(self.me.location.x - self.foes[0].location.x) + (self.me.location.y - self.foes[0].location.y)*(self.me.location.y - self.foes[0].location.y))
        #     if distance_between < 5000:
        #         self.set_intent(gotoboost(self.foes[0].location))
        #     else:
        #         self.set_intent(goto(self.foes[0].location))
        #     return'''
        #     self.set_intent(kill)
        #     print("die")
        #     return
        
        targets = {
            'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post),
            'away_from_our_net': (self.friend_goal.right_post, self.friend_goal.left_post)
        }
        if self.me.boost <= 75 and self.me.boost >= 15:
            print("hits")
            hits = find_hits(self,targets)
            if len(hits['at_opponent_goal']) > 0:
                self.set_intent(hits['at_opponent_goal'][0])
                return
        
            if len(hits['away_from_our_net']) > 0:
                self.set_intent(hits['away_from_our_net'][0])
                return

            #if infront then retreat
            if infront_of_ball:
                self.set_intent(goto(self.friend_goal.location))
                return
            self.set_intent(short_shot(self.foe_goal.location))
        
        available_boots = [boost for boost in self.boosts if boost.large and boost.active]

        closest_boost = None
        closest_distance = 10000

        if self.me.boost <= 15:
            print("boost")
            for boost in available_boots:
                distance = (self.me.location - boost.location).magnitude()
                if closest_boost is None or distance < closest_distance:
                    closest_boost = boost
                    closest_distance = distance

        if closest_boost is not None:
            self.set_intent(goto(closest_boost.location))
            return
        
        