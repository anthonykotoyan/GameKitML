from GameKitML.genmanager import Trainer


import math
import random
import time
import pygame

pygame.init()
width, length = 1300, 800
screen = pygame.display.set_mode((width, length))
clock = pygame.time.Clock()
running = True
waitTime = .5
dt = clock.tick(60) / 1000
trainMode = False
randomStart = True

carImage = pygame.image.load('car.png').convert()

track = [[(98, 146), (112, 140), (170, 131), (240, 114), (308, 100), (362, 87), (420, 88), (481, 122), (513, 163),
          (571, 190), (650, 209), (701, 215), (753, 218), (814, 201), (899, 170), (979, 134), (1123, 121), (1166, 116),
          (1211, 140), (1246, 176), (1260, 239), (1261, 357), (1254, 447), (1262, 564), (1281, 655), (1271, 687),
          (1233, 745), (1173, 780), (1131, 786), (1061, 785), (994, 779), (916, 759), (842, 715), (788, 682),
          (736, 659), (674, 639), (593, 647), (522, 682), (473, 701), (417, 718), (347, 740), (259, 745), (160, 717),
          (80, 601), (72, 582), (50, 510), (51, 447), (51, 383), (50, 326), (50, 256), (72, 155), (98, 146)],
         [(247, 648), (294, 656), (361, 656), (437, 635), (491, 605), (527, 583), (613, 550), (673, 543), (777, 556),
          (847, 597), (906, 639), (1015, 688), (1136, 675), (1171, 630), (1176, 565), (1159, 506), (1158, 443),
          (1152, 328), (1151, 251), (1105, 200), (1044, 190), (974, 225), (899, 267), (878, 273), (833, 292),
          (783, 313), (716, 331), (661, 337), (610, 311), (547, 286), (484, 267), (459, 249), (446, 218), (416, 195),
          (381, 179), (309, 158), (276, 168), (232, 192), (185, 206), (160, 241), (160, 287), (148, 328), (130, 372),
          (117, 427), (128, 495), (154, 539), (181, 571), (225, 616), (247, 648)], (729, 611),
         [[(761, 546), (743, 712)], [(776, 542), (771, 702)], [(822, 548), (813, 725)], [(897, 607), (836, 766)],
          [(938, 635), (877, 762)], [(1000, 657), (898, 776)], [(1023, 672), (949, 785)], [(1037, 672), (1007, 799)],
          [(1079, 659), (1049, 799)], [(1102, 669), (1102, 794)], [(1131, 648), (1120, 792)],
          [(1155, 663), (1184, 786)], [(1135, 627), (1260, 743)], [(1144, 616), (1290, 666)],
          [(1152, 584), (1278, 619)], [(1163, 570), (1274, 565)], [(1161, 550), (1263, 540)],
          [(1180, 526), (1290, 492)], [(1158, 485), (1295, 460)], [(1130, 420), (1294, 414)],
          [(1120, 367), (1261, 379)], [(1133, 305), (1277, 288)], [(1142, 271), (1274, 245)],
          [(1125, 245), (1267, 128)], [(1115, 230), (1212, 132)], [(1102, 222), (1168, 114)],
          [(1078, 213), (1110, 109)], [(1075, 216), (1060, 115)], [(1037, 241), (1030, 113)], [(1012, 240), (988, 131)],
          [(975, 245), (934, 163)], [(962, 265), (858, 151)], [(908, 328), (803, 154)], [(817, 327), (763, 184)],
          [(777, 358), (733, 170)], [(708, 372), (698, 202)], [(661, 353), (681, 176)], [(613, 357), (669, 177)],
          [(548, 329), (632, 160)], [(493, 302), (625, 119)], [(452, 255), (604, 128)], [(436, 235), (577, 139)],
          [(405, 223), (528, 140)], [(419, 216), (500, 117)], [(402, 209), (466, 101)], [(380, 207), (463, 94)],
          [(357, 195), (424, 97)], [(347, 201), (357, 64)], [(323, 184), (326, 84)], [(305, 189), (284, 101)],
          [(283, 202), (258, 112)], [(258, 222), (206, 88)], [(226, 199), (181, 101)], [(208, 255), (145, 108)],
          [(208, 242), (90, 118)], [(182, 228), (60, 170)], [(181, 261), (41, 205)], [(188, 280), (42, 243)],
          [(149, 302), (24, 269)], [(153, 339), (46, 322)], [(169, 388), (36, 374)], [(133, 406), (48, 410)],
          [(135, 439), (31, 456)], [(176, 463), (44, 494)], [(143, 489), (49, 555)], [(149, 521), (20, 591)],
          [(192, 520), (88, 632)], [(220, 553), (115, 692)], [(235, 593), (165, 721)], [(308, 598), (231, 761)],
          [(345, 654), (345, 753)], [(367, 609), (449, 778)], [(480, 579), (507, 741)], [(534, 552), (565, 704)],
          [(583, 492), (620, 717)], [(647, 519), (599, 735)], [(690, 534), (689, 672)]]]


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


layers = [len([-90, -37.5, -15, 0, 15, 37.5, 90]) + 1, 4, 3, 5]

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
    startAngle = 10

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
        self.vision = self.Vision()[0]
        self.nn_inputs = self.vision + [self.speed]
        self.fitness = 0
        self.nextCP = 0
        self.runAgent = True
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

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

    def ResetAgent(self):
        sa = random.uniform(-Agent.startAngle, Agent.startAngle)
        self.dir = sa
        self.angle = sa
        self.speed = 0
        self.fitness = 0
        self.nextCP = 0
        self.runAgent = True
        self.pos = pygame.Vector2(track[2][0], track[2][1])

    def AgentDeath(self):
        if trainMode:
            self.runAgent = False
        else:
            self.ResetAgent()

    def TrackCollisions(self):
        for walls in range(2):
            for wall in range(len(track[walls]) - 1):

                coll = BoxCollision(self.carCorners, (track[walls][wall], track[walls][wall + 1]))
                if coll:
                    self.fitness -= 1
                    self.AgentDeath()

    def TrackCheckpoints(self, draw):
        coll = BoxCollision(self.carCorners, track[3][self.nextCP])
        if draw:
            pygame.draw.line(screen, "green", track[3][self.nextCP][0], track[3][self.nextCP][1], 1)
        if coll:
            self.fitness += 1
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
    def UpdateAgent(Agent, inputs):
        Agent.ApplyVelocity()
        Agent.ApplyDirection()
        Agent.Controls(inputs)
        Agent.TrackCheckpoints(True)
        Agent.TrackCollisions()
        Agent.BorderCollisions()

        Agent.DriftTrail(10 * Agent.size, 5 * Agent.size)
        Agent.DrawAngle(50, False)
        Agent.DrawCar()



trainer = Trainer(Agent)
trainer.Set_NN_Info(layers, 0.1, 0.2, "Tanh")
trainer.Set_Run_Info(Agent.UpdateAgent, Agent.OutputToInput, "nn_inputs")
trainer.Initialize_Agents(10)





wait = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    dt = clock.tick(60) / 1000
    screen.fill([120, 120, 110])
    keys = [pygame.key.get_pressed()[pygame.K_w], pygame.key.get_pressed()[pygame.K_s], pygame.key.get_pressed()[pygame.K_d], pygame.key.get_pressed()[pygame.K_a], pygame.key.get_pressed()[pygame.K_SPACE]]
    DrawTrack(track, False)
    trainer.Run_Agents()
    pygame.display.flip()

pygame.quit()
