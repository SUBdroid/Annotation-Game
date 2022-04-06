import pygame
import pygame.freetype
import random
import os 
from pygame.locals import *
import time


"""Defining the location of the image so that they can be fetched during image loading during the game"""
# image_loc = os.path.join(os.getcwd(),os.path.join("model_datasets",os.path.join("coco_general","train2017")))
image_loc = os.path.join(os.getcwd(),"Objected_Detected_Images")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)


def data_loader():
    """
    Selects 100 examples from COCO Train data
    """
    dic_loc = os.path.join(os.getcwd(),os.path.join("model_datasets",os.path.join("coco_general","data_dictionary_train")))
    f_dic = open(dic_loc).read().split("\n")
    examples = []
    text = []
    images = []
    for i in range(50):
        matter = f_dic[random.randint(0,len(f_dic)-1)]
        sp = matter.split("\t")
        while len(sp)!=2 or (matter in examples) or len(sp[0].split())==0 or (".jpg" not in sp[1]):
            matter = f_dic[random.randint(0,len(f_dic)-1)]
            sp = matter.split("\t")
        # print(sp)
        text.append(sp[0])
        images.append(sp[1])
        examples.append(matter)
    return examples,text,images


class GameScene:
    FONT = None

    def __init__(self, text, next_scene):
        self.background = pygame.Surface((1600,1000))
        self.background.fill(pygame.Color('lightgrey'))

        if text:
            if GameScene.FONT == None:
                GameScene.FONT = pygame.freetype.SysFont(None, 28)
            GameScene.FONT.render_to(self.background, (120, 180), text, pygame.Color('black'))
            GameScene.FONT.render_to(self.background, (119, 179), text, pygame.Color('white'))

        self.next_scene = next_scene

    def start(self):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return self.next_scene


class GameScene1:
    FONT = None

    def __init__(self, text, image, next_scene):
        self.background = pygame.Surface((1600,1000))
        self.background.fill(pygame.Color('black'))
        self.image_flag = False

        if text:
            if GameScene1.FONT == None:
                GameScene1.FONT = pygame.freetype.SysFont(None, 28)
            GameScene.FONT.render_to(self.background, (120, 180), text, pygame.Color('black'))
            GameScene.FONT.render_to(self.background, (119, 179), text, pygame.Color('white'))
        
        if image:
            self.Image = pygame.image.load(image).convert()
            self.image_flag = True
            self.file_obj = open("multimodality_confidence","a")
        
        if not image:
            self.file_obj = open("text_confidence","a")

        self.next_scene = next_scene
        self.input_text = 'Enter the confidence in range of 1-5.'
        self.confidence = '0'
        font = pygame.font.SysFont(None, 48)
        self.inp = font.render(self.input_text, True, RED)
        self.rect = self.inp.get_rect()
        self.rect.topleft = (20, 20)
        self.cursor = Rect(self.rect.topright, (3, self.rect.height))
  

    def start(self):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.inp, self.rect)
        if self.image_flag:
            screen.blit(self.Image, (200,300))


    def update(self, events, dt):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.file_obj.write(str(self.confidence))
                    self.file_obj.write("\n")
                    self.file_obj.close()
                    return self.next_scene
                else:
                    self.confidence = event.unicode

def main():
    f_multi = open("multimodality_confidence","w")
    f_texts = open("text_confidence","w")

    pygame.init()
    screen = pygame.display.set_mode((1600, 1000))
    clock = pygame.time.Clock()
    dt = 0
    scenes = {
        'TITLE': GameScene('Press space to begin. Press Return key to navigate through the sentences','GAME'),
        'GAME': GameScene('Press [SPACE] for next sentence','BREAK'),
        'BREAK': GameScene('Press [SPACE] to continue to the next sentence', 'GAME'),
    }
    scene = scenes['TITLE'] #Starts with the title
    
    corp,captions,image_names = data_loader()
    text_list = captions+captions
    image_list = image_names+image_names
    
    counter = 0 #count the number of sentences shown
    w_counter = 0 #keeps track of the index of the words to be displayed in the window
    curr_sent_len = 0  

    SENT_DONE = True
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

        next_scene = scene.update(events, dt)
        
        if next_scene:
            if next_scene=="GAME":
                if SENT_DONE:
                    # f_ile = open("text_confidence","a")
                    # f_ile.write("<new_sentence>")
                    # f_ile.close()
                    toss = counter%2
                    if toss==0:
                        print("mode: text-only")
                        text = text_list[counter] #the actual sentence                        
                        image = None
                        SENT_DONE = False
                        f_ile = open("text_confidence","a")
                        f_ile.write(text)
                        f_ile.write("\n")
                        f_ile.close()
    
                    elif toss==1:
                        print("mode: multimodal")
                        text = text_list[counter] #the actual sentence 
                        image = os.path.join(image_loc,image_list[counter])
                        SENT_DONE = False
                        f_ile = open("multimodality_confidence","a")
                        f_ile.write(text)
                        f_ile.write("\t")
                        f_ile.write(image_list[counter])
                        f_ile.write("\n")
                        f_ile.close()

                    
                        
                print("Present sentence: %s"%text)
                print("Present image: %s"%image)
                

                sent = text.split()
                curr_sent_len = len(sent) 
                
                if counter!=len(corp):
                    if w_counter == curr_sent_len+1:
                        w_counter = 0
                        counter+=1
                        SENT_DONE = True
                        scene = GameScene("Sentence complete! Press [SPACEBAR] to proceed.",'BREAK')
                    else:
                        sentence_context = []
                        for w_ind in range(w_counter):
                            sentence_context.append(sent[w_ind])
                        text_to_fill = " ".join(sentence_context)
                        scene = GameScene1(text_to_fill,image, 'GAME')
                        w_counter += 1              
                else:
                    scene = GameScene1("Experiment over",image, 'RESULT')
            elif next_scene=="RESULT":
                break
            else:
                scene = scenes[next_scene]
            scene.start()

        scene.draw(screen)

        pygame.display.flip()
        pygame.display.set_caption("Annotation Interface")
        dt = clock.tick(60)

if __name__ == '__main__':
    main()