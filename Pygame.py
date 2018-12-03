#引入必要的库以及包
import pygame,random
import os

running = True
#定义运行标志函数
pygame.init()
# 初始化pygame
screen = pygame.display.set_mode((600, 600), 0, 32)
# 创建窗口
pygame.display.set_caption("SUPER SNAKE by Fingal Yu")
# 窗口标题
snakeColor = (0x4c, 0xaf, 0x50)
# 蛇身颜色
foodColor = (0x00, 0x8c, 0xba)
#食物颜色
bgColor = (0x55, 0x55, 0x55)
# 背景颜色
clock = pygame.time.Clock()
# 定义计时器
FPS = 36
# 屏幕刷新频率

D_LEFT, D_RIGHT, D_UP, D_DOWN = 0, 1, 2, 3
#设置运动方向
cubeWidth = 20
#小方块宽度
counter = 0
#设置计数器

direction = D_RIGHT
#初始方向向右
left, top = 300, 300
#设置方块初始位置
gridWidth, gridHeight = 600 //cubeWidth, 600 // cubeWidth
#网格数目
def drawGrids():
    for i in range(gridWidth):
        pygame.draw.line(screen,(0x00,0x00,0x00),(i * cubeWidth, 0),(i * cubeWidth, 600))
    for i in range(gridHeight):
        pygame.draw.line(screen,(0x00,0x00,0x00),(0, i * cubeWidth),(600, i * cubeWidth))

snake_body = []
#蛇身，每次身体加长就将身体的位置加到列表末尾
snake_body.append((int(gridWidth / 2)* cubeWidth, int(gridHeight / 2) * cubeWidth))
#贪吃蛇头部

def drawBody():
    for b in snake_body:
        pygame.draw.rect(screen, snakeColor,(b[0],b[1], cubeWidth, cubeWidth))
#打印蛇身的函数

food_pos = None
#记录食物位置
def generateFood():
    return (random.randint(0,gridWidth - 1), random.randint(0, gridHeight - 1))
#随机生成食物的函数
def drawFood():
    pygame.draw.rect(screen, foodColor, (food_pos[0] * cubeWidth, food_pos[1] * cubeWidth, cubeWidth, cubeWidth))
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
        if counter % int(FPS / 12)  == 0:
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

    screen.fill(bgColor)
    # 将背景色填充
    drawGrids()
    # 画出网格
    drawBody()
    #画出蛇身
    drawFood()
    #画出食物
    counter += 1
    # 计数器+1
    pygame.display.update()
    # 刷新画面
pygame.quit()

