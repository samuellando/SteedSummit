import pygame

class DrawGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.bg = None

    def draw(self, surface):
        if self.bg is not None:
            self.clear(surface, self.bg)
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sorted(sprites, key=lambda x : x.rect.y + x.rect.height):
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []

class CollisionGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)