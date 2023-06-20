import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1000, 600
delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    # こうかとんSurface（kk_img）からこうかとんRect（kk_rct）を抽出する
    go_img = pg.image.load("ex02/fig/8.png")
    go_img = pg.transform.rotozoom(go_img, 0, 2.0)
    # ゲームオーバー時に表示する画像
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20, 20))  # 練習１
    bd_img.set_colorkey((0, 0, 0))  # 黒い部分を透明にする
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    # 爆弾Surface（bd_img）から爆弾Rect（bd_rct）を抽出する
    bd_rct = bd_img.get_rect()
    # 爆弾Rectの中心座標を乱数で指定する
    bd_rct.center = x, y 
    vx, vy = +5, +5  # 練習２
    gameover_check = False
    # ゲームオーバーの判定 ゲームオーバー時にTrue

    clock = pg.time.Clock()
    tmr = 0
    after_go_time_count = 0
    #ゲームオーバー後に経過した時間を記録する変数
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bd_rct):  # 練習５
            gameover_check = True
            if after_go_time_count == 0:
                go_time = tmr
                # ゲームオーバー時に時間を記録する
            after_go_time_count = tmr
            """
            ゲームオーバー時の時間を記録する。time_countは増加
            していき、80フレーム経過したら(go_timeとtime_count
            の差が80以上になったら)画面を閉じる
            """
            if (after_go_time_count - go_time) >= 80:
                print("ゲームオーバー")
                return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 合計移動量
        for k, mv in delta.items():
            if key_lst[k] and not gameover_check:
                #ゲームオーバー時でないときキーが押されたら 
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
 
        screen.blit(bg_img, [0, 0])

        if not gameover_check:
            # 通常時
            screen.blit(kk_img, kk_rct)

            bd_rct.move_ip(vx, vy)  # 練習２
            yoko, tate = check_bound(bd_rct)
            if not yoko:
                vx *= -1
            if not tate:
                vy *= -1
            screen.blit(bd_img, bd_rct)
        if gameover_check:
            # ゲームオーバー時
            screen.blit(go_img, kk_rct)
            # ゲームオーバー時に画像を切り替える

        pg.display.update()
        tmr += 1
        clock.tick(50)

        if vx < 15:
            """
            爆弾の加速
            速度が15になるまで1フレームに0.1ずつ加速
            """
            if vx > 0:
                vx += 0.1
            else:
                vx -= 0.1
            if vy > 0:
                vy += 0.1
            else:
                vy -= 0.1

        if after_go_time_count != 0:
            after_go_time_count += 1
            # ゲームオーバー後に経過した時間を記録する

def check_bound(rect: pg.rect) -> tuple[bool, bool]:
    """
    こうかとん、爆弾が画面内or画面外かを判定する関数
    引数：こうかとんor爆弾Rect
    戻り値：横方向、縦方向の判定結果タプル(True:画面内/False:画面外)
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  #横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  #縦方向判定
        tate = False
    return yoko, tate

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()