#!/usr/bin/env python3

import os
import sys
import pygame
import random

class MtyperApp:
    def __init__(self):
        resourcesPath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'resources')

        pygame.init()
        pygame.display.set_caption("mtyper")
        pygame.key.set_repeat(0)
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.SysFont('DejaVu Sans Mono', 75)
        self.clock = pygame.time.Clock()

        self.wordItems = []
        for item in os.scandir(resourcesPath):
            if (item.is_file() and os.path.splitext(item.name)[1] == '.png'):
                self.wordItems.append(
                    (os.path.splitext(item.name)[0], item.path))

        for item in self.wordItems:
            print(item)

    def run(self):
        running = True
        current = None
        words = []

        while running:
            # load the word to be typed
            if len(words) is 0:
                words = [item for item in self.wordItems]
                random.shuffle(words)
            if current is None:
                current = words.pop()
                (wordString, wordImgPath) = current
                wordImg = pygame.image.load(wordImgPath)
                wordImg = pygame.transform.scale(
                    pygame.image.load(wordImgPath), (200, 200))
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
                    elif len(typedLetters) < len(targetLetters):
                        index = len(typedLetters)
                        target = targetLetters[index]
                        actual = event.unicode
                        if target.lower() == actual.lower():
                            typedLetters.append(targetLetters[index])

            # draw the image, target and typed letters
            self.screen.fill((255, 255, 255))
            self.screen.blit(wordImg, (50, 50))
            for i, letter in enumerate(targetLetters):
                if i < len(typedLetters):
                    color = (103, 169, 207)
                else:
                    color = (100, 100, 100)
                self.screen.blit(
                    self.font.render(letter.upper(), True, color),
                    (50 + i * 50, 400))

            pygame.display.update()
            self.clock.tick(60)


        sys.exit(0)


if __name__ == '__main__':
    app = MtyperApp()
    app.run()

