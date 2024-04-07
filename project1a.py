# Luis Octavo
# 3010U - Course Project
# Corinth game (コリントゲーム) in Python

# packages
import pygame
import random
# integrate pymunk into pygame
import pymunk.pygame_util
from pymunk import Vec2d

# Since pymunk and pygame use different coordinate systems
pymunk.pygame_util.positive_y_is_up = False

# Constants
WIDTH = 1200
HEIGHT = 900
FPS = 60
# Coefficients
CO_ELASTICITY = 0.8
CO_FRICTION = 0.4

TIMER = pygame.time.Clock()
springForce = 1800

# ---------------------------------------------------------------------- #
# Pygame initialization
pygame.init()
pygame.font.init()
gameFont = pygame.font.SysFont("Helvetica", 30)
gameFont2 = pygame.font.SysFont("Helvetica", 15)
screen = pygame.display.set_mode([WIDTH, HEIGHT])
# integrate pymunk here
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Text
titleTextSurface = gameFont.render("Corinth's Game", True, (170, 255, 170))
# Instruction Text
instructionTextSurface1 = gameFont2.render("Press Q or E to change spring strength", True, (255, 170, 170))
instructionTextSurface2 = gameFont2.render("Press R to spawn the ball. Press Space to launch.", True, (255, 170, 170))
instructionTextSurface3 = gameFont2.render("Press P to Reset Game", True, (255, 170, 170))

# Debug
debugTextSurface = gameFont2.render("Debug Mode" , True, (255, 255, 255))

# Pymunk initiliaztion
space = pymunk.Space()
space.gravity = 0, 2000

# Ball bearing constants
BEARING_ELASTICITY = 0
BEARING_FRICTION = 0.001

# Changing ball texture
...

# Ball storage (for reset and removal)
balls = []

# Create ball Function
def createBall(space, spawnPoint):
    # Make global (for spring)
    global ballBody, ballShape

    ballMass = 1
    ballRadius = 15
    # moment of intertia
    ballMoE = pymunk.moment_for_circle(ballMass, 0, ballRadius)
    ballBody = pymunk.Body(ballMass, ballMoE)
    ballBody.position = spawnPoint
    ballShape = pymunk.Circle(ballBody, ballRadius)
    ballShape.elasticity = CO_ELASTICITY
    ballShape.friction = BEARING_FRICTION
    ballShape.color = (128, 128, 128, 255)
    space.add(ballBody, ballShape)
    balls.append(ballShape)

# Create initial balls

# Board Creation
# ---------------------------------------------------------------------- #
# Floor
floor = pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 20)
floor.elasticity = CO_ELASTICITY
floor.friction = CO_FRICTION
space.add(floor)

# Ceiling
ceiling = pymunk.Segment(space.static_body, (0, 0), (WIDTH, 0), 5)
ceiling.elasticity = CO_ELASTICITY
ceiling.friction = CO_FRICTION
space.add(ceiling)

# "Curve"
# Needs to be thicker to prevent ball passthrough
curve = pymunk
curve = pymunk.Segment(space.static_body, (600, 0), (800, 200), 6)
space.add(curve)

# Scoreboard Barrier
barrier = pymunk.Segment(space.static_body, (800, 0), (800, HEIGHT), 5)
barrier.elasticity = CO_ELASTICITY
barrier.friction = CO_FRICTION
space.add(barrier)

# Walls
wallLeft = pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), 5)
wallLeft.elasticity = CO_ELASTICITY
wallLeft.friction = CO_FRICTION
space.add(wallLeft)

wallRight = pymunk.Segment(space.static_body, (0, WIDTH), (WIDTH, HEIGHT), 5)
wallRight.elasticity = CO_ELASTICITY
wallRight.friction = CO_FRICTION
space.add(wallRight)

# Static Dots
def createDots(radius, dotsPerRow, distancePerDot, height, offset=-5):
    for x in range(dotsPerRow):
        staticBallRadius = radius
        staticBallBody = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        staticBallBody.position = (distancePerDot * x + offset, height)
        staticBallShape = pymunk.Circle(staticBallBody, staticBallRadius)
        staticBallShape.elasticity = 0.75
        staticBallShape.friction = 0.2
        staticBallShape.color = (255, 100, 0, 255)
        space.add(staticBallBody, staticBallShape)

# Adding more extra variables for bouncability
# Radius, Dots per row, distance per dot, height (inverse), offset (optional)
#createDots(7, 15, 50, 250)
createDots(7, 9, 80, 300, 0)
createDots(7, 10, 80, 350, -35)
createDots(7, 9, 80, 400, 0)
createDots(7, 10, 80, 450, -35)
createDots(7, 9, 80, 500, 0)
createDots(7, 10, 80, 550, -35)
createDots(7, 9, 80, 600, 0)

# TODO
# Propellers

# Segments
def createBottomSegments(segmentHeight, thickness):
    for x in range(16):
        segment = pymunk.Segment(space.static_body, (x * 50, HEIGHT), (x * 50, segmentHeight), thickness)
        # NOTE: Elasticity must be high to prevent ball from standing on the top of the segment
        segment.elasticity = 0.9
        segment.friction = CO_FRICTION
        space.add(segment)

createBottomSegments(700, 5)

# Spring Ejection System
# NOTE: integrated in pygame loop
catapult = pymunk.Segment(space.static_body, (750, HEIGHT), (750, 250), 5)
catapult.elasticity = 0.0
catapult.friction = CO_FRICTION
space.add(catapult)

# Spring adjustment booleans
adjustingUp = False
adjustingDown = False

# ---------------------------------------------------------------------- #
# Pygame loop
run = True

# Initial ball
createBall(space, (775, 810))

while run:
    
    # Since the spring force will be dynamic, the text will stay here so it can get updated in real time
    normalizedSpringForce = ( ( springForce - (1600) ) / (2600 - (1600)) ) * (100 - 0) + 0
    springTextSurface = gameFont.render("Spring Strength: " + str(round(normalizedSpringForce, 2)) + "%", True, (255, 255, 255, 255))

    # Debug text
    ballsAmountSurface = gameFont2.render("Balls Used: " + str(len(balls)), True, (255, 255, 255, 255))
    rawSpringSurface = gameFont2.render("Raw Spring Force: " + str(springForce), True, (255, 255, 255, 255))

    # Background
    screen.fill(pygame.Color('black'))
    

    # Events
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            exit()

        # Mouse button spawn (deprecated)
        #if event.type == pygame.MOUSEBUTTONDOWN:
        #    if event.button == 1:
                
                #print(balls)
                #springForce += 10
        #    if event.button == 2:
        #        if (len(balls) >= 2):
        #            

            
        # Spring adjustment system / Launch system
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q :
                adjustingDown = True
            elif event.key == pygame.K_e:
                adjustingUp = True
            
            # Launch Ball
            elif event.key == pygame.K_SPACE:
                if (ballBody.position.x > 765 and ballBody.position.y > 820):
                        ballBody.apply_impulse_at_local_point((Vec2d.unit() * -springForce), (0, 0))
                           
            elif event.key == pygame.K_r:
                createBall(space, (775, 810))

            # Reset
            elif event.key == pygame.K_p:
                for ball in balls: 
                    space.remove(ball.body, ball)
                    balls.remove(ball)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q :
                adjustingDown = False
            elif event.key == pygame.K_e:
                adjustingUp = False
                

    space.step(1 / FPS)
    space.debug_draw(draw_options)

    if adjustingUp:
        springForce += 10
    if adjustingDown:
        springForce -= 10

    # Spring force floor/ceiling
    if springForce < 1700:
        springForce = 1700
    elif springForce > 2600:
        springForce = 2600

    # Text display
    screen.blit(titleTextSurface, (850, 70))
    screen.blit(springTextSurface, (850, 100))
    screen.blit(instructionTextSurface1, (850, 200))
    screen.blit(instructionTextSurface2, (850, 220))
    screen.blit(instructionTextSurface3, (850, 240))

    # Advanced Mode
    screen.blit(debugTextSurface, (850, 380))
    screen.blit(ballsAmountSurface, (850, 400))
    screen.blit(rawSpringSurface, (850, 420))

    pygame.display.flip()
    TIMER.tick(FPS)   