#引入必要的库以及包

import pygame,random
import os

snakeColor = (0x4c, 0xaf, 0x50)
# 蛇身颜色
foodColor = (0x00, 0x8c, 0xba)
#食物颜色
bgColor = (0x00, 0x00, 0x00)
# 背景颜色
headColor = (0xdd, 0x33, 0)
#头部颜色
clock = pygame.time.Clock()
# 定义计时器
FPS = 30
# 屏幕刷新频率

hardLevel = list (range(2, int(FPS/2), 2))
#设置难度等级
hardness = hardLevel[0]
#初始难度

D_LEFT, D_RIGHT, D_UP, D_DOWN = 0, 1, 2, 3
#设置运动方向

cubeWidth = 20
#小方块宽度
counter = 0
#设置计数器
width = 600

height = 600
#定义长和宽
direction = D_RIGHT
#初始方向向右
left, top = 300, 300
#设置方块初始位置
gridWidth, gridHeight = width //cubeWidth, height // cubeWidth
#网格数目

running = True
#定义运行标志函数
pygame.init()
# 初始化pygame
screen = pygame.display.set_mode((600, 600), 0, 32)
# 创建窗口
pygame.display.set_caption("SUPER SNAKE by Fingal Yu")
# 窗口标题
pygame.mixer.init()
#初始化准备载入音乐

baseFolder = os.path.dirname(__file__)
#根目录为当前文件夹
musicFolder =  os.path.join(baseFolder,'music')
#存放音乐的文件夹
backMusic = pygame.mixer.music.load(os.path.join(musicFolder,'back.mp3'))
#背景音乐

imgFolder = os.path.join(baseFolder,'images')
#图片文件夹
backImg = pygame.image.load(os.path.join(imgFolder, 'back.jpg'))
#背景图片
snakeHeadImg = pygame.image.load(os.path.join(imgFolder, 'head.png'))
#蛇头图片
snakeHeadImg.set_colorkey(bgColor)
#头部背景
foodImg = pygame.image.load(os.path.join(imgFolder, 'orb2.png'))
#食物图片

background = pygame.transform.scale(backImg, (width, height))

food = pygame.transform.scale(foodImg, (cubeWidth, cubeWidth))
#调整背景及食物的大小
pygame.mixer.music.set_volume(0.3)
#调节音量
pygame.mixer.music.play(loops=-1)
#无限循环音乐


snake_body = []
#蛇身，每次身体加长就将身体的位置加到列表末尾
snake_body.append((int(gridWidth / 2)* cubeWidth, int(gridHeight / 2) * cubeWidth))
#贪吃蛇头部

def drawGrids():
    for i in range(gridWidth):
        pygame.draw.line(screen,(0x00,0x00,0x00),(i * cubeWidth, 0),(i * cubeWidth, 600))
    for i in range(gridHeight):
        pygame.draw.line(screen,(0x00,0x00,0x00),(0, i * cubeWidth),(600, i * cubeWidth))
#划出表格

def drawBody(direction=D_LEFT):
    for b in snake_body[1:]:
        screen.blit(food , b)
    #根据吃了多少食物加多少节
    if direction == D_LEFT:
        rot = 0
    elif direction == D_RIGHT:
        rot = 180
    elif direction == D_UP:
        rot = 270
    elif direction == D_DOWN:
        rot = 90
    #根据按键方向变化改变头部变化方向
    newHeadImg = pygame.transform.rotate(snakeHeadImg, rot)

    head = pygame.transform.scale(newHeadImg , (cubeWidth , cubeWidth))
    #转动头部方向
    screen.blit(head, snake_body[0])

food_pos = None
#记录食物位置
def generateFood():
    while True:
        pos = (random.randint(0, gridWidth - 1),
               random.randint(0, gridHeight - 1))

        # 如果当前位置没有小蛇的身体，我们就跳出循环，返回食物的位置
        if not (pos[0] * cubeWidth, pos[1] * cubeWidth) in snake_body:
            return pos#随机生成食物的函数
def drawFood():
    screen.blit(food, (food_pos[0] * cubeWidth,
                       food_pos[1] * cubeWidth, cubeWidth, cubeWidth))
    #画出食物主体
def grow():
    if snake_body[0][0] == food_pos[0] * cubeWidth and \
            snake_body[0][1] == food_pos[1] * cubeWidth:
        return True
    return False

food_pos = generateFood()
drawFood()
while running:
    clock.tick(FPS)
    # 游戏主循环
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # 有键盘按键呗按下
            if event.key ==pygame.K_RIGHT:

                direction = D_RIGHT
            elif event.key == pygame.K_LEFT:

                direction = D_LEFT
            elif event.key == pygame.K_UP:
                direction = D_UP

            elif event.key == pygame.K_DOWN:
                direction = D_DOWN

        if counter % int(FPS / 15)  == 0:
            #判断计数器是否符合要求，符合则移动
            last_pos = snake_body[-1]
            # 保存尾部位置以更新增长

            for i in range(len(snake_body) -1, 0, -1):
                snake_body[i] = snake_body[i - 1]

            if direction ==D_UP:
                snake_body[0] = ( snake_body[0][0], snake_body[0][1] - cubeWidth)

            elif direction ==D_DOWN:
                snake_body[0] = ( snake_body[0][0], snake_body[0][1] + cubeWidth)

            elif direction ==D_LEFT:
                snake_body[0] = ( snake_body[0][0] - cubeWidth, snake_body[0][1] )

            elif direction ==D_RIGHT:
                snake_body[0] = ( snake_body[0][0] + cubeWidth, snake_body[0][1])
                # 限制小蛇的活动范围
            if snake_body[0][0] < 0 or snake_body[0][0] >= 600 or \
                    snake_body[0][1] < 0 or snake_body[0][1] >= 600:
                # 超出屏幕之外游戏结束
                running = False

            # 限制小蛇不能碰到自己的身体
            for sb in snake_body[1:]:
                # 身体的其他部位如果和蛇头（snake_body[0]）重合就死亡
                if sb == snake_body[0]:
                    running = False

            got_food = grow()

            if got_food:
                food_pos = generateFood()
                snake_body.append(last_pos)
            #如果吃到食物则增长长度
                hardness = hardLevel[min(int(len(snake_body) / 10), len(hardLevel) - 1)]

    screen.blit(background, (0,0))
    # 将背景色填充
    drawGrids()
    # 画出网格
    drawBody(direction)
    #画出蛇身
    drawFood()
    #画出食物
    counter += 1
    # 计数器+1
    pygame.display.update()
    # 刷新画面
pygame.quit()

