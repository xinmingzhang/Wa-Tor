# controls:
# p for pause
# i for information
# 9 for replay
# 1,2 for speed
# 3,4 for fish production frequency
# 5,6 for shark production frequency
# 7,8 for shark energy
# SCREEN_RECT and SQUARE_LENGTH can also be changed manually

import pygame as pg
import random

SCREEN_RECT = pg.Rect(0,0,800,600)

SQUARE_LENGTH = 10

assert SCREEN_RECT.width % SQUARE_LENGTH == 0, 'please change another number ^v^'
assert SCREEN_RECT.height % SQUARE_LENGTH == 0 , 'please change another number ^v^'

FISH_COLOR = (0,255,0)
SHARK_COLOR = (255,0,0)
SPACE_COLOR = (0,0,255)


FISH_REPRODUCE_TIME = 2
SHARK_REPRODUCE_TIME = 3
SHARK_ENERGY = 2


MAX_NUMBER = (SCREEN_RECT.width/SQUARE_LENGTH) * (SCREEN_RECT.height/SQUARE_LENGTH)

def print_text(surface,position,text,size,colour):
    font = pg.font.get_default_font()
    font_layer = pg.font.Font(font,size)
    font_surface = font_layer.render(text,True,colour)
    surface.blit(font_surface,position)
    return surface

class Space(pg.sprite.Sprite):
    def __init__(self,pos,*group):
        super(Space, self).__init__(*group)
        self.name = 'space'
        self.image = pg.Surface((SQUARE_LENGTH,SQUARE_LENGTH))
        self.image.fill(SPACE_COLOR)        
        self.rect = self.image.get_rect(topleft = pos)


class Fish(pg.sprite.Sprite):
    def __init__(self, pos, age, *group):
        super(Fish, self).__init__(*group)
        self.name = 'fish'
        self.age = age
        self.image = pg.Surface((SQUARE_LENGTH,SQUARE_LENGTH))
        self.image.fill(FISH_COLOR)        
        self.rect = self.image.get_rect(topleft = pos)
        self.rebirth = FISH_REPRODUCE_TIME

    def next_pos(self,sprites_dict):

        neighbour = []

        upper_sprite_pos = (self.rect.x , (self.rect.y-SQUARE_LENGTH)%SCREEN_RECT.height)
        if sprites_dict[upper_sprite_pos].name == 'space':
            neighbour.append(upper_sprite_pos)

        bottom_sprite_pos = (self.rect.x , (self.rect.y+SQUARE_LENGTH)%SCREEN_RECT.height)
        if sprites_dict[bottom_sprite_pos].name == 'space':
            neighbour.append(bottom_sprite_pos)

        left_sprite_pos = ((self.rect.x - SQUARE_LENGTH)%SCREEN_RECT.width , self.rect.y)
        if sprites_dict[left_sprite_pos].name == 'space':
            neighbour.append(left_sprite_pos)

        right_sprite_pos = ((self.rect.x + SQUARE_LENGTH)%SCREEN_RECT.width , self.rect.y)
        if sprites_dict[right_sprite_pos].name == 'space':
            neighbour.append(right_sprite_pos)

        if len(neighbour) >= 1:
            pos = tuple(random.choice(neighbour))
        else:
            pos = tuple(self.rect.topleft)
        return pos


    def update(self, game):
        pos = self.next_pos(game.sprites_dict)
        if pos == self.rect.topleft:
            pass
        else:
            game.sprites_dict[self.rect.topleft].kill()
            game.sprites_dict[pos].kill()
            if self.age >= self.rebirth:
                game.sprites_dict[pos] = Fish(pos, 0, game.fishes)
                game.sprites_dict[self.rect.topleft] = Fish(self.rect.topleft,0,game.fishes)
            else:
                game.sprites_dict[pos] = Fish(pos, self.age+1, game.fishes)
                game.sprites_dict[self.rect.topleft] = Space(self.rect.topleft,game.spaces)


class Shark(pg.sprite.Sprite):
    def __init__(self,pos,age,energy,*group):
        super(Shark, self).__init__(*group)
        self.name = 'shark'
        self.age = age
        self.energy = energy
        if self.energy >= SHARK_ENERGY:
            self.energy = SHARK_ENERGY
        self.image = pg.Surface((SQUARE_LENGTH,SQUARE_LENGTH))
        self.image.fill(SHARK_COLOR)        
        self.rect = self.image.get_rect(topleft = (pos))
        self.rebirth = SHARK_REPRODUCE_TIME

    def next_pos(self,sprites_dict):
        fishes = []
        spaces = []

        upper_sprite_pos = (self.rect.x , (self.rect.y-SQUARE_LENGTH)%SCREEN_RECT.height)
        if sprites_dict[upper_sprite_pos].name== 'fish':
            fishes.append(upper_sprite_pos)
        elif sprites_dict[upper_sprite_pos].name == 'space':
            spaces.append(upper_sprite_pos)

        bottom_sprite_pos = (self.rect.x , (self.rect.y+SQUARE_LENGTH)%SCREEN_RECT.height)
        if sprites_dict[bottom_sprite_pos].name == 'fish':
            fishes.append(bottom_sprite_pos)
        elif sprites_dict[bottom_sprite_pos].name == 'space':
            spaces.append(bottom_sprite_pos)

        left_sprite_pos = ((self.rect.x - SQUARE_LENGTH)%SCREEN_RECT.width , self.rect.y)
        if sprites_dict[left_sprite_pos].name == 'fish':
            fishes.append(left_sprite_pos)
        elif sprites_dict[left_sprite_pos].name == 'space':
            spaces.append(left_sprite_pos)

        right_sprite_pos = ((self.rect.x + SQUARE_LENGTH)%SCREEN_RECT.width , self.rect.y)
        if sprites_dict[right_sprite_pos].name == 'fish':
            fishes.append(right_sprite_pos)
        elif sprites_dict[right_sprite_pos].name == 'space':
            spaces.append(right_sprite_pos)

        if len(fishes) >= 1:
            pos = tuple(random.choice(fishes))
        elif len(spaces) >= 1:
            pos = tuple(random.choice(spaces))
        else:
            pos = tuple(self.rect.topleft)

        return pos

    def update(self,game):
        self.energy -= 1
        if self.energy <= 0:
            game.sprites_dict[self.rect.topleft].kill()
            game.sprites_dict[self.rect.topleft] = Space(self.rect.topleft, game.spaces)
        else:        
            pos = self.next_pos(game.sprites_dict)
            if pos == self.rect.topleft:
                pass
            else:
                if game.sprites_dict[pos].name == 'fish':
                    self.energy += 1
                    game.sprites_dict[self.rect.topleft].kill()
                    game.sprites_dict[pos].kill()
                    if self.age > self.rebirth:
                        game.sprites_dict[self.rect.topleft] = Shark(self.rect.topleft,0,SHARK_ENERGY,game.sharks)
                        game.sprites_dict[pos] = Shark(pos,0,SHARK_ENERGY,game.sharks)
                    else:
                        game.sprites_dict[self.rect.topleft] = Space(self.rect.topleft,game.spaces)
                        game.sprites_dict[pos] = Shark(pos,self.age + 1,self.energy,game.sharks)
                elif game.sprites_dict[pos].name == 'space':
                    game.sprites_dict[self.rect.topleft].kill()
                    game.sprites_dict[pos].kill()
                    if self.age > self.rebirth:
                        game.sprites_dict[self.rect.topleft] = Shark(self.rect.topleft,0,SHARK_ENERGY,game.sharks)
                        game.sprites_dict[pos] = Shark(pos,0,SHARK_ENERGY,game.sharks)
                    else:
                        game.sprites_dict[self.rect.topleft] = Space(self.rect.topleft,game.spaces)
                        game.sprites_dict[pos] = Shark(pos,self.age + 1,self.energy,game.sharks)
                else:
                    print('ok, this section need modified')


class Game(object):
    def __init__(self):
        self.screen = pg.display.set_mode(SCREEN_RECT.size)
        self.fishes = pg.sprite.Group()
        self.sharks = pg.sprite.Group()
        self.spaces = pg.sprite.Group()
        self.sprites_dict = {}

        for i in range(0,SCREEN_RECT.width,SQUARE_LENGTH):
            for j in range(0,SCREEN_RECT.height,SQUARE_LENGTH):
                seed = random.randint(0,2)
                if seed == 0:
                    self.sprites_dict[(i,j)] = Fish((i,j),0,self.fishes)
                elif seed == 1:
                    self.sprites_dict[(i,j)] = Shark((i,j),0,SHARK_ENERGY,self.sharks)
                elif seed == 2:
                    self.sprites_dict[(i,j)] = Space((i,j),self.spaces)
                else:
                    pass

        self.done = False
        self.pause = False
        self.show_information = False
        self.clock = pg.time.Clock()
        self.fps = 20.0

        self.curve_start_point = 0
        self.fish_list = []
        self.shark_list = []


    def event_loop(self):
        global FISH_REPRODUCE_TIME,SHARK_REPRODUCE_TIME,SHARK_ENERGY
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.pause = not self.pause
                elif event.key == pg.K_i:
                    self.show_information = not self.show_information
                elif event.key == pg.K_1:
                    self.fps -= 2
                    if self.fps <= 2:
                        self.fps = 1
                elif event.key == pg.K_2:
                    self.fps += 2
                    if self.fps >= 100:
                        self.fps = 100
                elif event.key == pg.K_3:
                    FISH_REPRODUCE_TIME -= 1
                    if FISH_REPRODUCE_TIME <= 1:
                        FISH_REPRODUCE_TIME = 1
                elif event.key == pg.K_4:
                    FISH_REPRODUCE_TIME += 1
                elif event.key == pg.K_5:
                    SHARK_REPRODUCE_TIME -= 1
                    if SHARK_REPRODUCE_TIME <= 1:
                        SHARK_REPRODUCE_TIME = 1
                elif event.key == pg.K_6:
                    SHARK_REPRODUCE_TIME += 1
                elif event.key == pg.K_7:
                    SHARK_ENERGY -= 1
                    if SHARK_ENERGY <= 1:
                        SHARK_ENERGY = 1
                elif event.key == pg.K_8:
                    SHARK_ENERGY += 1
                elif event.key == pg.K_9:
                    self.__init__()



            if event.type == pg.KEYUP:
                if event.type ==pg.K_ESCAPE:
                    self.done = True

            self.keys = pg.key.get_pressed()


    def curve_information(self,fish_number,shark_number):
        number_f = SCREEN_RECT.height - fish_number/4.0/MAX_NUMBER*SCREEN_RECT.height
        number_s = SCREEN_RECT.height - shark_number/4.0/MAX_NUMBER*SCREEN_RECT.height

        self.curve_start_point += 1
        self.fish_list.append((self.curve_start_point,number_f))
        self.shark_list.append((self.curve_start_point,number_s))

        if self.curve_start_point >= SCREEN_RECT.width:
            self.fish_list = []
            self.shark_list = []
            self.curve_start_point = 0
        if len(self.fish_list) >= 2:
            pg.draw.lines(self.screen,FISH_COLOR,False,self.fish_list,1)
            print_text(self.screen,self.fish_list[-1],'fish_number {}'.format(len(self.fishes)),int(SCREEN_RECT.height/50),FISH_COLOR)
        if len(self.shark_list) >= 2:
            pg.draw.lines(self.screen,SHARK_COLOR,False,self.shark_list,1)
            print_text(self.screen,self.shark_list[-1],'shark_number {}'.format(len(self.sharks)),int(SCREEN_RECT.height/50),SHARK_COLOR)
        

    def draw(self):

        self.screen.fill((255,255,255))
        self.spaces.draw(self.screen)
        self.fishes.draw(self.screen)
        self.sharks.draw(self.screen)
        if self.show_information:
            pg.draw.rect(self.screen,(0,0,255),(0,SCREEN_RECT.height/4.0*3,SCREEN_RECT.width,SCREEN_RECT.height/4.0))
            self.curve_information(len(self.fishes),len(self.sharks))
            print_text(self.screen,(0,SCREEN_RECT.height/4.0*3),'Fishes',int(SCREEN_RECT.height/20),FISH_COLOR)
            print_text(self.screen, (0, SCREEN_RECT.height / 20.0 * 18), 'Sharks', int(SCREEN_RECT.height / 20),
                       SHARK_COLOR)

            print_text(self.screen, (SCREEN_RECT.width/5.0, SCREEN_RECT.height / 4.0 * 3), 'fish reproduction frequency :{:.2f} s [3, 4]'.format(FISH_REPRODUCE_TIME/1.0/self.fps), int(SCREEN_RECT.height / 40), FISH_COLOR)
            print_text(self.screen, (SCREEN_RECT.width / 5.0 * 3, SCREEN_RECT.height / 4.0 * 3),
               'game speed :{} fps [press 1, 2 to adjust]'.format(self.fps), int(SCREEN_RECT.height / 40),
               FISH_COLOR)
            print_text(self.screen, (SCREEN_RECT.width / 5.0, SCREEN_RECT.height / 40.0 * 36),
               'shark reproduction frequency :{:.2f} s [5, 6]'.format(SHARK_REPRODUCE_TIME/1.0/self.fps), int(SCREEN_RECT.height / 40),
               SHARK_COLOR)

            print_text(self.screen, (SCREEN_RECT.width / 5.0 * 3, SCREEN_RECT.height / 40 * 36),
                       'shark death frequency :{:.2f} s [7, 8]'.format(SHARK_ENERGY/1.0/self.fps),
                       int(SCREEN_RECT.height / 40), SHARK_COLOR)




    def update(self):
        if not self.pause:
            self.spaces.update()
            self.fishes.update(self)
            self.sharks.update(self)

    def run(self):
        while not self.done:
            pg.init()
            self.event_loop()
            self.draw()
            self.clock.tick(self.fps)
            fps = self.clock.get_fps()
            if self.pause:
                pg.display.set_caption('Wa-Tor Pause')
            else:
                pg.display.set_caption('Wa-Tor FPS{:.2f}'.format(fps))
                self.update()
            pg.display.update()
        pg.quit()


if __name__ == '__main__':
    game = Game()
    game.run()



    
        
