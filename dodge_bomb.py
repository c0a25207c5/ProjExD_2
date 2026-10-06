import time
import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA={
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんまたは爆弾のRect
    戻り値：タプル[横方向、縦方向]
    画面内ではtrue、画面外ではFalse
    """
    yoko,tate = True,True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko, tate


def gameovrer(screen: pg.Surface) -> None:
    """
    ゲームオーバー関数
    引数：screen
    戻り値：screenにゲームオーバー画像をbildした画像
    五秒後に閉じる
    """
    go_img = pg.Surface((WIDTH,HEIGHT))  # ゲームオーバー背景のサーフェス
    pg.draw.rect(go_img,(0,0,0),(0,0,1600,900))
    go_img.set_alpha(100)

    go_font = pg.font.Font(None,80)  # 文字の作成
    go_txt = go_font.render("Game Over",True, (255,255,255))
    txt_rct = go_txt.get_rect()
    txt_rct.center = WIDTH/2,HEIGHT/2
    go_img.blit(go_txt,txt_rct)

    kk2_img = pg.image.load("fig/8.png")  # こうかとんの画像作成
    kk2_rct1 = kk2_img.get_rect()  # こうかとんをゲームオーバー画像へ貼り付け（1匹目）
    kk2_rct1.center = WIDTH/2+200,HEIGHT/2
    go_img.blit(kk2_img,kk2_rct1)

    kk2_rct2 = kk2_img.get_rect()# こうかとんをゲームオーバー画像へ貼り付け（2匹目）
    kk2_rct2.center = WIDTH/2-200,HEIGHT/2
    go_img.blit(kk2_img,kk2_rct2)

    go_rct = go_img.get_rect()
    go_rct.center = WIDTH/2,HEIGHT/2
    screen.blit(go_img,go_rct)
    
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface],list[int]]:
    """
    爆弾を拡大、加速させる関数
    引数：なし
    戻り値：１０段階の拡大するタプルと加速するタプル
    """
    bb_imgs = []
    for r in range(1,11):  # 大きさリストの作成
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255,0,0), (10*r,10*r), 10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)

    bb_accs = [a for a in range(1,11)]  # 加速度リストの作成
    return bb_imgs, bb_accs



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))  # 爆弾の作成
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy = +5,+5
    clock = pg.time.Clock()
    tmr = 0

    bb_imgs,bb_accs = init_bb_imgs()  # タプルを取得
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  # kkとbbのRectが重なっていたら
            gameovrer(screen)
            print("game over")
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        bb_img = bb_imgs[min(tmr//500,9)]  # 段階に応じた大きさの変更
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        avx = vx*bb_accs[min(tmr//500,9)]  # 段階に応じた加速度の変更
        avy = vy*bb_accs[min(tmr//500,9)]
        bb_rct.move_ip(avx,avy)

        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0]+= tpl[0]  # 横方向
                sum_mv[1]+= tpl[1]  # 縦方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):  # こうかとんがどこかからはみ出ている場合
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx,vy)  # 爆弾の移動
        yoko,tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出た場合
            vx *=-1
        if not tate:  # 縦方向にはみ出た場合
            vy *=-1
        screen.blit(bb_img, bb_rct)  # 爆弾の表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
