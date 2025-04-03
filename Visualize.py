
import math
import pygame
import time
time.sleep(5)
BLACK=(0,0,0)
BLUE=(0,0,255)
CYAN=(0,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
WHITE=(255,255,255)
RES = WIDTH, HEIGHT = 800, 800
pygame.init()
clock=pygame.time.Clock()
sc= pygame.display.set_mode(RES)
pygame.display.set_caption("GRAPH VISUALIZATION")

#[0,1,7,8,14,15,21,22,28,29,35,36,42,43]:
nodes={
    0:[45],
    1:[6],
    2:[49],
    3:[7],
    4:[9],
    5:[8],
    6:[1],
    7:[3],
    8:[5],
    9:[4],
    10:[12],
    #11:[16],
    12:[10],
    13:[18],
    14:[16],
    15:[20],
    16:[14],
    17:[22],
    18:[13],
    19:[21],
    20:[15],
    21:[19],
    22:[17],
    23:[25],
    24:[27],
    25:[23],
    26:[31],
    27:[24],
    28:[30],
    29:[32],
    30:[28],
    31:[26],
    32:[29],
    33:[36],
    #34:[39],
    35:[38],
    36:[33],
    37:[42],
    38:[35],
    39:[41],
    #40:[45],
    41:[39],
    42:[37],
    43:[46],
    44:[48],
    45:[0],
    46:[43],
    #47:[49],
    48:[44],
    49:[2],
}
def dist(c1,c2):
    return math.sqrt(((c1[0]-c2[0])**2)+((c1[1]-c2[1])**2))

def midp(c1,c2):
    return (((c1[0]+c2[0])/2),(c1[1]+c2[1])/2)


coord=[(400,12),(446,15),(490,24),(536,37),(581,59),(621,83),(663,117),(694,150),(721,186),(746,227),(763,270),(778,319),(785,372),  (785,428),(778,481),(763,530),(746,573),(721,614),(694,650),(663,683),(621,717),(581,741),(536,763),(490,776),(446,785),(400,788),(354, 785), (310, 776), (264, 763), (219, 741), (179, 717), (137, 683), (106, 650), (79, 614), (54, 573), (37, 530), (22, 481), (15, 428), (15, 372), (22, 319), (37, 270), (54, 227), (79, 186), (106, 150), (137, 117), (179, 83), (219, 59), (264, 37), (310, 24), (354, 15)]


Agent= [43, 42, 41, 40, 39, 40, 39, 40, 39, 38, 39, 41, 42, 43, 44, 48, 49, 2, 3, 4, 9]
prey=[5, 4, 9, 4, 9, 8, 5, 6, 7, 8, 9, 8, 9, 4, 9, 8, 5, 8, 5, 8, 9]
pred=[3, 2, 49, 48, 44, 43, 42, 41, 42, 37, 38, 39, 40, 41, 42, 43, 44, 48, 47, 48]

run=True
for s in range(len(Agent)-1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    sc.fill(BLACK)
    pygame.draw.circle(sc,BLACK,(400,400),388,2)
    pygame.draw.circle(sc,WHITE,(400,400),386)

    for j in nodes.keys():
        pygame.draw.circle(sc,BLACK,midp(coord[j],coord[nodes[j][0]]),dist(coord[j],coord[nodes[j][0]])/2,2)




    coord=[(400,12),(446,15),(490,24),(536,37),(581,59),(621,83),(663,117),(694,150),(721,186),(746,227),(763,270),(778,319),(785,372),  (785,428),(778,481),(763,530),(746,573),(721,614),(694,650),(663,683),(621,717),(581,741),(536,763),(490,776),(446,785),(400,788),(354, 785), (310, 776), (264, 763), (219, 741), (179, 717), (137, 683), (106, 650), (79, 614), (54, 573), (37, 530), (22, 481), (15, 428), (15, 372), (22, 319), (37, 270), (54, 227), (79, 186), (106, 150), (137, 117), (179, 83), (219, 59), (264, 37), (310, 24), (354, 15)]
    for i in range(len(coord)):
        color=CYAN
        if i==pred[s]:
            color=RED
        if i==prey[s]:
            color=GREEN
        if i==Agent[s]:
            color=BLUE
        # if i in [0,1,7,8,14,15,21,22,28,29,35,36,42,43]:
        #     color=RED


        pygame.draw.circle(sc,color,coord[i],12)



    
    pygame.display.update()
    clock.tick(1)


pygame.quit()
quit()