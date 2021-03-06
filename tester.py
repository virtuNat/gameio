#!/usr/bin/env python
"garbage.py"
import sys
import pygame as pg
import random
import asyncio

# Allowed events to pass
GLOBAL_CONFIG = [pg.ACTIVEEVENT, pg.KEYUP, pg.KEYDOWN]
# Allowed keys to work
KEY_CONFIG = {pg.K_SPACE: 'clear'}

class ExitGame (Exception):
	"Called to exit the game."

class Grid:
	"Object Example"
	def __init__ (self, owner):
		self.owner = owner
		self.lines = 0

	async def clear (self):
		"Tells you it's clearing lines."
		self.lines = random.randint(1, 4)
		print("About to clear {} lines".format(self.lines))
		for line in range(self.lines):
			await asyncio.sleep(0)
			print("Clearing line #{}".format(line + 1))
		self.lines = 0
		self.owner.clearing = False

class Game:
	"Game Instance Example"
	def __init__ (self):
		self.grid = Grid(self)
		self.clearing = False
		self.x = 0

	async def _eval_events (self, event_pumper):
		for event in next(event_pumper):
			if event.type is pg.KEYDOWN:
				action = KEY_CONFIG[event.key]
				if action == 'clear':
					self.clearing = True

	async def _eval_logic (self):
		"Dummy logic code. Randomly generates a number."
		if self.clearing:
			await self.grid.clear()
		else:
			self.x = random.randint(0, 10)

	def display (self, screen):
		"Dummy display code. Does nothing but flash a number."
		surf = pg.Surface(screen.get_size())
		surf.fill(pg.Color(0x000000FF))
		screen.blit(surf, (0, 0))
		screen.blit(
			pg.font.SysFont(None, 25).render(
				'{}'.format(self.x), 0, pg.Color(0xFFFFFFFF)
				),
			(0, 0)
			)
		pg.display.flip()

	async def run (self, owner):
		await self._eval_events(owner.event_pumper)
		await self._eval_logic()
		self.display(owner.screen)
		
class Testris:
	"Some High-Level Execution thingy? What is this called again?"

	STATES = {'game': Game()}

	pg.init()
	screen = pg.display.set_mode((800, 600))
	loop = asyncio.get_event_loop()
	clock = pg.time.Clock()

	def __init__ (self):
		self.state = 'game'
		self.event_pumper = self._pump_events()
		
	@property
	def state (self):
		return self.STATES[self._state]

	@state.setter
	def state(self, value):
		self._state = value

	def exit (self, status=0):
		self.loop.close()
		pg.quit()
		sys.exit(status)

	def _pump_events (self):
		"Prunes commands for the running code to execute."
		while True:
			events = [ ]
			for event in pg.event.get():
				if event.type is pg.QUIT:
					self.exit()
				elif event.type in GLOBAL_CONFIG:
					events.append(event)
			yield events

	def run (self):
		"How to get this to loop?"
		try:
			while True:
				self.loop.run_until_complete(
					self.state.run(self)
					)
				self.clock.tick(30)
		except (ExitGame, KeyboardInterrupt):
			pass
		finally:
			self.exit()
			

if __name__ == '__main__':
	Testris().run()
