from GameKitML.genmanager import Trainer

import math
import random

import pygame

pygame.init()
width, length = 1600, 950
screen = pygame.display.set_mode((width, length))
clock = pygame.time.Clock()
running = True
waitTime = .5
dt = clock.tick(60) / 1000
trainMode = False
randomStart = True

carImage = pygame.image.load('car.png').convert()

track = [[(299, 846), (1301, 869), (1476, 605), (1482, 303), (1319, 131), (956, 62), (419, 100), (201, 259), (137, 622),
          (299, 846)],
         [(632, 720), (1016, 672), (1172, 584), (1224, 419), (1077, 273), (713, 241), (486, 375), (566, 681),
          (632, 720)], (716, 787),
         [[(821, 654), (817, 895)], [(888, 635), (887, 894)], [(937, 630), (938, 890)], [(1001, 625), (1027, 901)],
          [(1065, 607), (1127, 862)], [(1073, 570), (1251, 862)], [(1129, 554), (1389, 764)],
          [(1059, 480), (1473, 644)], [(1140, 445), (1504, 474)], [(1158, 392), (1436, 171)], [(1094, 352), (1226, 71)],
          [(1005, 289), (1047, 49)], [(923, 303), (886, 43)], [(830, 332), (738, 25)], [(748, 351), (543, 28)],
          [(410, 67), (576, 395)], [(278, 154), (521, 452)], [(180, 232), (530, 484)], [(88, 456), (566, 533)],
          [(105, 580), (656, 567)], [(125, 731), (657, 645)], [(377, 900), (708, 694)], [(678, 862), (734, 686)]]]


def sign(x):
    if x != 0:
        return abs(x) / x
    return 0


def line_intersection(a, b, c, d):
    d1 = (
            (a[0] - b[0]) * (c[1] - d[1]) - (a[1] - b[1]) * (c[0] - d[0]))
    d2 = (
            (a[0] - b[0]) * (c[1] - d[1]) - (a[1] - b[1]) * (c[0] - d[0]))
    if d1 == 0 or d2 == 0:
        return [False, []]
    else:
        t = ((a[0] - c[0]) * (c[1] - d[1]) - (a[1] - c[1]) * (c[0] - d[0])) / d1
        u = ((a[0] - c[0]) * (a[1] - b[1]) - (a[1] - c[1]) * (a[0] - b[0])) / d2

    # check if line actually intersect
    if 0 <= t <= 1 and 0 <= u <= 1:
        return [True, (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))]
    else:
        return [False, []]


def BoxCollision(corners, line):
    for i in range(4):
        if i == 3:
            j = -1
        else:
            j = i
        boxLine = [corners[j], corners[j + 1]]
        collisionInfo = line_intersection(line[0], line[1], boxLine[0], boxLine[1])
        if collisionInfo[0]:
            return True

    return False


def DrawCheckPoints(cp):
    for i in range(len(cp)):
        if len(cp[i]) == 2:
            pygame.draw.line(screen, "green", cp[i][0], cp[i][1], 1)


def DrawTrack(track, drawCP):
    for wall in range(2):
        for i in range(len(track[wall]) - 1):
            pygame.draw.line(screen, "black", track[wall][i], track[wall][i + 1], 2)
    pygame.draw.circle(screen, 'green', track[2], 3)
    if drawCP:
        DrawCheckPoints(track[3])


layers = [len([-90, -37.5, -15, 0, 15, 37.5, 90]) + 1, 5]

acceleration = 3
breakStrength = 1
maxSpeed = 9
driftLength = 10
driftLength = 4
turnSpeed = 4
driftFriction = 14
friction = 0.4
baseTSValue = -.3
driftSpeed = .6
minDriftAngle = 20
normalSlip = .3
handBrakeSlip = normalSlip * 1.5
errorCorrectionStrength = 15


class Agent:
    boxSize = 2
    allAgents = []
    startAngle = 0

    def __init__(self):
        self.image = pygame.image.load('car.png').convert_alpha()
        self.size = 3
        self.image = pygame.transform.scale(self.image, (self.size * 10, self.size * 10))
        self.acc = acceleration
        self.turnSpeed = turnSpeed
        self.slip = normalSlip
        sa = random.uniform(-Agent.startAngle, Agent.startAngle)
        self.dir = sa
        self.angle = sa
        self.vel = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(track[2][0], track[2][1])
        self.speed = 0
        self.car = self.image.get_rect(center=(self.pos.x, self.pos.y))
        self.hbColor = "green"
        self.carCorners = [(self.pos.x - self.size * Agent.boxSize, self.pos.y - self.size * Agent.boxSize),
                           (self.pos.x + self.size * Agent.boxSize, self.pos.y - self.size * Agent.boxSize),
                           (self.pos.x + self.size * Agent.boxSize, self.pos.y + self.size * Agent.boxSize),
                           (self.pos.x - self.size * Agent.boxSize, self.pos.y + self.size * Agent.boxSize)]
        self.angles = [-90, -37.5, -15, 0, 15, 37.5, 90]
        self.vision = self.Vision()
        self.nn_inputs = self.vision[0] + [self.speed]
        self.score = 0
        self.nextCP = 0
        self.isDead = False
        Agent.allAgents.append(self)

    def Vision(self):

        positions = []
        endPositions = []
        rayDist = 100000
        dists = []
        for i in range(len(self.angles)):
            pos = pygame.Vector2(math.cos(math.radians(self.angle + self.angles[i])) * rayDist + self.pos.x,
                                 math.sin(math.radians(self.angle + self.angles[i])) * rayDist + self.pos.y)
            positions.append(pos)
            endPos = pos
            wallDists = []
            for walls in range(2):
                for wall in range(len(track[walls]) - 1):
                    intersection = line_intersection(self.pos, pos, track[walls][wall], track[walls][wall + 1])
                    if intersection[0]:
                        wallDist = math.dist(self.pos, pygame.Vector2(intersection[1][0], intersection[1][1]))
                        wallDists.append(wallDist)

                        if wallDist == min(wallDists):
                            endPos = pygame.Vector2(intersection[1][0], intersection[1][1])
            if wallDists:
                dists.append(min(wallDists))
            else:
                dists.append(0)
            endPositions.append(endPos)
        return [dists, endPositions]

    def DrawVision(self, endPositions):
        for i in range(len(endPositions)):
            pygame.draw.line(screen, "purple", self.pos, endPositions[i], 1)
            pygame.draw.circle(screen, "orange", endPositions[i], 5)

    def HitBox(self, draw):
        if draw:
            for i in range(4):
                if i == 3:
                    j = -1
                else:
                    j = i

                pygame.draw.line(screen, self.hbColor, self.carCorners[j], self.carCorners[j + 1], 2)

    def DrawCar(self):

        self.car = self.image.get_rect(center=(self.pos.x, self.pos.y))
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        # Update the car's rectangle to the new rotated image's rectangle
        self.car = rotated_image.get_rect(center=self.car.center)
        # Draw the rotated image onto the screen
        screen.blit(rotated_image, self.car)

    def DriftTrail(self, dist, wid):
        driftAngle = abs(((self.angle - self.dir + 540) % 360 - 180))
        if driftAngle >= minDriftAngle and abs(self.speed) > driftSpeed:
            endPos = pygame.Vector2(
                sign(self.speed) * math.cos(math.radians(self.dir)) * dist + self.pos.x + self.size,
                sign(self.speed) * math.sin(math.radians(self.dir)) * dist + self.pos.y)
            pygame.draw.line(screen, (40, 40, 30), self.pos, endPos, wid)
            endPos = pygame.Vector2(
                sign(self.speed) * math.cos(math.radians(self.dir)) * dist + self.pos.x - self.size,
                sign(self.speed) * math.sin(math.radians(self.dir)) * dist + self.pos.y)
            pygame.draw.line(screen, (40, 40, 30), self.pos, endPos, wid)

    def DrawAngle(self, dist, draw):
        if draw:
            endPos = pygame.Vector2(math.cos(math.radians(self.dir)) * dist + self.pos.x,
                                    math.sin(math.radians(self.dir)) * dist + self.pos.y)
            pygame.draw.line(screen, "blue", self.pos, endPos, self.size)
            endPos = pygame.Vector2(math.cos(math.radians(self.angle)) * dist + self.pos.x,
                                    math.sin(math.radians(self.angle)) * dist + self.pos.y)
            pygame.draw.line(screen, "red", self.pos, endPos, self.size)

    def ApplyVelocity(self):
        self.carCorners = [(self.pos.x - self.size * Agent.boxSize, self.pos.y - self.size * Agent.boxSize),
                           (self.pos.x + self.size * Agent.boxSize, self.pos.y - self.size * Agent.boxSize),
                           (self.pos.x + self.size * Agent.boxSize, self.pos.y + self.size * Agent.boxSize),
                           (self.pos.x - self.size * Agent.boxSize, self.pos.y + self.size * Agent.boxSize)]
        self.vision = self.Vision()

        self.nn_inputs = self.vision[0] + [self.speed]

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

    @staticmethod
    def ResetAgent(self):
        sa = random.uniform(-Agent.startAngle, Agent.startAngle)
        self.dir = sa
        self.angle = sa
        self.speed = 0
        self.score = 0
        self.nextCP = 0
        self.isDead = False
        self.pos = pygame.Vector2(track[2][0], track[2][1])

    def AgentDeath(self):
        self.isDead = True

    def TrackCollisions(self):
        for walls in range(2):
            for wall in range(len(track[walls]) - 1):

                coll = BoxCollision(self.carCorners, (track[walls][wall], track[walls][wall + 1]))
                if coll:
                    self.score -= 1
                    self.AgentDeath()

    def TrackCheckpoints(self, draw):
        coll = BoxCollision(self.carCorners, track[3][self.nextCP])
        if draw:
            pygame.draw.line(screen, "green", track[3][self.nextCP][0], track[3][self.nextCP][1], 1)
        if coll:
            self.score += 1
            if self.nextCP == len(track[3]) - 1:
                self.nextCP = 0
            else:
                self.nextCP += 1

    def BorderCollisions(self):
        if 0 >= self.pos.x:
            self.AgentDeath()

        if self.pos.x >= width:
            self.AgentDeath()

        if 0 >= self.pos.y:
            self.AgentDeath()

        if self.pos.y >= length:
            self.AgentDeath()

    def ApplyDirection(self):
        if abs(self.speed) >= maxSpeed:
            self.speed = maxSpeed * sign(self.speed)
        self.vel.x = -math.cos(math.radians(self.dir)) * self.speed
        self.vel.y = -math.sin(math.radians(self.dir)) * self.speed

    def Controls(self, outputs):
        angleError = ((self.angle - self.dir + 540) % 360 - 180)
        if outputs[0]:
            self.speed -= self.acc * dt
        if abs(self.speed) > driftSpeed:
            self.speed += driftFriction * dt * (abs(angleError) / 180) * -sign(self.speed)
        self.speed += friction * -sign(self.speed) * dt

        if outputs[4]:
            self.slip = handBrakeSlip
            if self.speed < 0:
                self.speed += self.acc * dt * breakStrength
            else:
                self.speed = 0
        else:
            self.slip = normalSlip

        if outputs[1]:
            if self.speed < 0:
                self.speed += self.acc * dt * breakStrength
            else:
                self.speed = 0
        if outputs[2]:
            # angle error changes positively
            self.angle += self.turnSpeed
            if self.speed != 0:
                self.dir += self.turnSpeed * (1 - self.slip)
            else:
                self.dir = self.angle
            if angleError < 0:
                self.dir += sign(angleError) * errorCorrectionStrength * (abs(angleError) / 180)


        elif outputs[3]:
            # angle error changes negatively
            self.angle -= self.turnSpeed
            if self.speed != 0:
                self.dir -= self.turnSpeed * (1 - self.slip)
            else:
                self.dir = self.angle
            if angleError > 0:
                self.dir += sign(angleError) * errorCorrectionStrength * (abs(angleError) / 180)


        else:
            self.dir += sign(angleError) * (driftLength * .25)
        # b = 4 * axTurnSpeed / maxSpeed ** 2
        # self.turnSpeed = -b * (baseTSValue + abs(self.speed)) * (
        #         baseTSValue - maxSpeed + abs(self.speed)) + ShiftUpTS

    @staticmethod
    def DrawInputs(inputs):
        inputColor = ["green" if input else "red" for input in inputs]
        pygame.draw.circle(screen, inputColor[0], pygame.Vector2(25, 10), 5)
        pygame.draw.circle(screen, inputColor[1], pygame.Vector2(10, 25), 5)
        pygame.draw.circle(screen, inputColor[2], pygame.Vector2(25, 25), 5)
        pygame.draw.circle(screen, inputColor[3], pygame.Vector2(40, 25), 5)
        pygame.draw.rect(screen, inputColor[4], (5, 35, 40, 10))

    @staticmethod
    def OutputToInput(output_list):

        return [output > 0 for output in output_list]


    @staticmethod
    def UpdateAgent(self, inputs):
        self.ApplyVelocity()
        self.ApplyDirection()
        self.Controls(inputs)
        self.TrackCheckpoints(True)
        self.TrackCollisions()
        self.BorderCollisions()

        self.DriftTrail(10 * self.size, 5 * self.size)
        self.DrawAngle(50, False)
        self.DrawCar()



trainer = Trainer(Agent)
trainer.Set_NN_Info(layers, 0.1, 0.2, "Tanh")
trainer.Set_Run_Info(Agent.UpdateAgent, Agent.OutputToInput, "nn_inputs")
trainer.Set_Gen_Info(5, "isDead", Agent.ResetAgent, "score")
trainer.Initialize_Agents(20)

wait = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    dt = clock.tick(60) / 1000
    screen.fill([120, 120, 110])
    keys = [pygame.key.get_pressed()[pygame.K_w], pygame.key.get_pressed()[pygame.K_s],
            pygame.key.get_pressed()[pygame.K_d], pygame.key.get_pressed()[pygame.K_a],
            pygame.key.get_pressed()[pygame.K_SPACE]]
    DrawTrack(track, False)
    trainer.Run_Gen()
    pygame.display.flip()

pygame.quit()
