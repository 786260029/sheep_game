import pygame
import random
from collections import Counter
import time

# 初始化 Pygame
pygame.init()
# 倒计时时间（毫秒）
countdown_time = 30000

# 获取开始时间
start_ticks = pygame.time.get_ticks()
# 定义常量
WIDTH, HEIGHT = 1360, 900
BAG_WIDTH,BAG_HEIGHT=150,800
TILE_SIZE = 80
#ROWS, COLS = 6, 6
FPS = 30

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
itemCount=5

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("羊了个羊小游戏")

# 加载图案图片
patterns = [pygame.image.load(f"{i}.png") for i in range(1, 8)]
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]
menu=pygame.image.load("menu.png")
menu=pygame.transform.scale(menu, (WIDTH, HEIGHT))
background=pygame.image.load("4b566dc7d61bb8e362381985002266d.png")
background=pygame.transform.scale(background, (WIDTH, HEIGHT))
start_game=pygame.image.load("easy.png")
start_game=pygame.transform.scale(start_game, (300, 150))
storee=pygame.image.load("hard.png")
storee=pygame.transform.scale(storee, (300, 150))

# 创建游戏板
selected = []
board = [[0 for _ in range(22)] for _ in range(22)]
def seed(ROWS, COLS):
    total=ROWS*COLS/3
    for i in range(0,int(total)):
        fruit_type=random.randint(1,7)
        for j in range(0,3):
            while(True):
                x=random.randint(1,ROWS)
                y=random.randint(1,COLS)
                if(board[x][y]==0):
                    break
            board[x][y]=fruit_type
    selected.clear()

def draw_board(ROWS, COLS):
    #screen.blit(background, (0, 0))
    # 遍历棋盘的每一行
    for row in range(1,ROWS+1):
        # 遍历棋盘的每一列
        for col in range(1,COLS+1):
            # 如果当前位置不为0，则绘制图案
            if (board[row][col]!=0):
                a=board[row][col]
                screen.blit(patterns[a-1], (col * TILE_SIZE, row * TILE_SIZE))
    # 遍历选中的图案
    for i in range(1,len(selected)+1):
        # 绘制选中的图案
        screen.blit(patterns[selected[i - 1][1]-1], (i * BAG_WIDTH, BAG_HEIGHT))

def check_match(total):
    cgf=[]
    cgf.clear()
    for i in selected:
        cgf.append(i[1])
    lwj=Counter(cgf)
    for i,j in lwj.items():
        if j == 3 :
            k=0
            while (k<len(selected)) :
                if i == selected[k][1] :
                    selected.pop(k)
                else :
                    k += 1
            total -= 3
            #print(i,j)
    return total

def lose_interface():
    #失败界面自己做
    game_over=pygame.image.load("20240915212559.png")
    game_over=pygame.transform.scale(game_over, (WIDTH, HEIGHT))
    screen.blit(game_over, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)
    print("You Lose!!")
    return

def win_interface():
    game_win=pygame.image.load("OIP.png")
    game_win=pygame.transform.scale(game_win, (WIDTH, HEIGHT))
    screen.blit(game_win, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)
    print("You Win!!")
    return
# 主游戏循环
def game_interface(ROWS, COLS):
    seed(ROWS, COLS)
    start_time = time.time()
    total=COLS*ROWS
    running = True
    while running:
        
        totalScore=0
        clock.tick(FPS)
        #playSurface=pygame.display.set_mode((WIDTH,HEIGHT))
        color = (75, 223, 225)
        s="mission "+str(itemCount-4)
        color = (238, 175, 65)  # 设置文本颜色为红色
        s="mission "+str(itemCount-4)  # 将itemCount-4转换为字符串，并拼接成字符串s
        # 使用字体对象渲染文本，返回一个Surface对象
        text=font.render(s,True,color)
        screen.blit(text,(5,45))
        color = (241, 69, 158)
        text=font.render("score: "+str(totalScore),True,color)
        screen.blit(text,(5,65))
        # 遍历pygame事件
        for event in pygame.event.get():
            # 如果事件类型为退出
            if event.type == pygame.QUIT:
                # 停止运行
                running = False
            # 如果事件类型为鼠标点击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标点击位置
                x, y = event.pos
                #print(x,y)
                # 计算点击位置对应的行列
                col, row = x // TILE_SIZE, y // TILE_SIZE
                # 如果点击位置在棋盘范围内
                if(col<=COLS and row<=ROWS):
                    # 如果点击位置已经有棋子
                    if board[row][col] !=0:
                        # 将点击位置和棋子添加到选中列表
                        selected.append([(row, col),board[row][col]])
                        # 将点击位置置为空
                        board[row][col]=0
                    # 如果选中列表中已经有超过2个棋子
                    if len(selected) > 2:
                        # 检查是否有匹配的棋子
                        total=check_match(total)
                        if(total):
                            totalScore =totalScore+1
                    # 如果选中列表中已经有超过7个棋子
                    if len(selected) >7:
                        # 显示失败界面
                        lose_interface()
                        # 返回
                        return
        #screen.fill(BG_COLOR)
        screen.blit(background, (0, 0))
        draw_board(ROWS, COLS)
        current_ticks = pygame.time.get_ticks()
        elapsed_time = current_ticks - start_ticks
        remaining_time = max(0, countdown_time - elapsed_time)

        # 格式化倒计时时间
        minutes = int(remaining_time // 60000)
        seconds = int((remaining_time % 60000) // 1000)
        time_str = f"{minutes:02d}:{seconds:02d}"

        # 渲染倒计时文本
        text = font.render(time_str, True, (255, 255, 255))
        text_rect = text.get_rect(center=(950, 240))
        screen.blit(text, text_rect)
        pygame.display.flip()
        if(remaining_time==0):
            lose_interface()
            return
        if(total==0):
            win_interface()
            return

def menu_interface():
    running = True
    while running:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                #print(event.pos)
                if(x>=550 and x<=850 and y>=200 and y<=350):
                    ROWS, COLS = 6,6
                    game_interface(ROWS, COLS)
                    running=False
                    
                if(x>=550 and x<=850 and y>=500 and y<=650):
                    ROWS, COLS = 9,9
                    game_interface(ROWS, COLS)
                    running=False

                
        screen.blit(menu, (0, 0))
        screen.blit(start_game,(550,200))
        screen.blit(storee,(550,500))

        pygame.display.flip()

menu_interface()
pygame.quit()
#sys.exit()