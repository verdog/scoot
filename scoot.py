import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util import *

class Scoot(BaseAgent):

    def initialize_agent(self):
        #This runs once before the bot starts up
        self.controller_state = SimpleControllerState()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        self.preprocess(packet)

        return self.controller_state 

    def preprocess(self, packet: GameTickPacket):
        self.me = packet.game_cars[self.index]

        self.ball = packet.game_ball
        self.ball.local_location = target_to_local(self.me.physics.location, self.me.physics.rotation, self.ball.physics.location)