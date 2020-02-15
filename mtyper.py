#!/usr/bin/env python3

import os
import sys
import pygame
import random
from typing import Tuple

class MtyperApp:
    imageExtensions = ['.png', '.jpg', '.tif', '.tiff', '.svg']

    def __init__(self) -> None:
        resourcesPath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'resources')

        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.display.set_caption("mtyper")
        pygame.key.set_repeat(0)
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.font = pygame.font.SysFont('DejaVu Sans Mono', 75)
        self.clock = pygame.time.Clock()

        self.wordItems = []
        for item in os.scandir(os.path.join(resourcesPath, 'words')):
            if item.is_file() and \
                    (os.path.splitext(item.name)[1].lower() in \
                        MtyperApp.imageExtensions):
                self.wordItems.append(
                    (os.path.splitext(item.name)[0], item.path))

        for item in self.wordItems:
            print(item)

        self.soundPing = pygame.mixer.Sound(
                os.path.join(resourcesPath, 'sounds/ping.wav'))
        self.soundKey = pygame.mixer.Sound(
                os.path.join(resourcesPath, 'sounds/keypress.wav'))

    def resizeImage(
            self,
            img: pygame.Surface,
            maxDim: Tuple[int, int]=(800, 600)) -> pygame.Surface:
        rect = img.get_rect()
        if (rect.width > maxDim[0]) or (rect.height > maxDim[1]):
            ratio = rect.width / rect.height
            if rect.width > rect.height:
                newDim = (maxDim[0], int(maxDim[0] / ratio))
            else:
                newDim = (int(maxDim[1] * ratio), maxDim[1])
            resized = pygame.transform.scale(img, newDim)
        else:
            resized = img

        return resized

    def run(self) -> pygame.Surface:
        running = True
        current = None
        words = []
        screenSize = self.screen.get_size()
        imgPosCenter = (int(screenSize[0] / 2), int(screenSize[1] * 0.35))
        wordPosCenter = (int(screenSize[0] / 2), int(screenSize[1] * 0.80))

        while running:
            # load the word to be typed
            if len(words) == 0:
                words = [item for item in self.wordItems]
                random.shuffle(words)

            if current is None:
                current = words.pop()
                (wordString, wordImgPath) = current
                wordImg = self.resizeImage(pygame.image.load(wordImgPath))
                targetLetters = [l for l in wordString]
                typedLetters = []

            # process events/ input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    if key == 'escape':
                        running = False
                    elif (key == 'return') or (key == 'space'):
                        if targetLetters == typedLetters:
                            current = None
                            self.soundPing.play()
                    elif len(typedLetters) < len(targetLetters):
                        index = len(typedLetters)
                        target = targetLetters[index]
                        actual = event.unicode
                        if target.lower() == actual.lower():
                            typedLetters.append(targetLetters[index])
                            self.soundKey.play()

            # draw the image, target and typed letters
            self.screen.fill((255, 255, 255))
            self.screen.blit(
                wordImg,
                (   int(imgPosCenter[0] - (0.5 * wordImg.get_rect().width)),
                    int(imgPosCenter[1] - (0.5 * wordImg.get_rect().height)) ))
            wordSurface = self.font.render(
                    ''.join(targetLetters).upper(), True, (100, 100, 100))
            wordCoord = \
                (   int(wordPosCenter[0] -
                        (0.5 * wordSurface.get_rect().width)),
                    int(wordPosCenter[1] -
                        (0.5 * wordSurface.get_rect().height))  )
            self.screen.blit( wordSurface, wordCoord)
            self.screen.blit(
                self.font.render(
                    ''.join(typedLetters).upper(),
                    True,
                    (103, 169, 207)),
                wordCoord)

            pygame.display.update()
            self.clock.tick(60)

        sys.exit(0)


if __name__ == '__main__':
    app = MtyperApp()
    app.run()

