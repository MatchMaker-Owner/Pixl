#Models.py

"""
Models should contain player model, enemy model, obstacles, stage object for saving to mysql
Character model should contain damage integration and differentiation
Enemy object and player object are derived from character model.
Sword, shield, gun, bow, arrow, crystal, everything should have a model.

"""
class Attribute:
    def _init_(self, base, power):
        self.base = base
        self.power = power
    
    def _integrate(self):
        """Integrates attribute considering base as variable"""
        self.power += 1
        self.base /= self.power
    
    def _differentiate(self):
        """Differentiates attribute considering base as variable"""
        self.base *= self.power
        self.power -= 1
        
    def _value(self):
        return base ** power

class Character:
    """Basic object containing redundant code from player and enemy classes. Player and enemy classes have their separate movement code not declared here"""
    
    def _init_(self, damage_vals, defense_vals, ):
        self.Damage = Attribute(damage_vals)
        self.Defense = Attribute(defense_vals)
        
    def _powerup(self, boost):
        if boost["type"] == "Damage":
            self.Damage.integrate()
        
        elif boost["type"] == "Defense":
            self.Defense.integrate()
    
    def _damage(self, Defender):
        damage = self.Damage._value() - Defender.Defense._value()
        if damage > 0:
            Defender.hp -= damage
            
    #No need for a defense function as its functionality is redundant with _damage() function
    
class Player:
    """
    Height, Width -> For making character rect
    Position -> For helping in movement
    Self-sacrifice: A move using lifeforce to unleash an exponential damage
    """
    
    def _init_(self, x, y):
        self.height = 20
        self.width = 10
        
        self.step_x = 5
        self.step_y = 5 #Pixels moved whenever up or down key is pressed
        
        self.rect = pygame.Rect(x, y, self.height, self.width)
        self.hp = 100
        self.inventory = []
        
        #Attributes
        self.Damage = Attribute(2, 2)
        self.Defense = Attribute(3, 2)
        
        
    def _move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.step_x
            
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            
        # Keep player on screen
        self.rect.clamp_ip(screen.get_rect())
        
    def _da
    
            
            