#!/usr/bin/python
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from math import pi, sin, cos

class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		#Disable Mouse
		self.disableMouse()
		#Environment

		#Load the 3D environment file
		self.scene = self.loader.loadModel("environment")
		#Set the parent obj to the render object
		self.scene.reparentTo(self.render)

		#Position and scale the environment
		self.scene.setScale(0.25, 0.25, 0.25)
		self.scene.setPos(-8, 42, 0)

		#Camera Task
		#Call self.spinCameraTask on each frame
		self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
		self.z = 0

		#Actor
		#Load Actor anomated object, associate a dict with actions
		self.pandaActor = Actor("panda-model",{'walk' : 'panda-walk4'})
		#Set scale of model
		self.pandaActor.setScale(0.005,0.005,0.005)
		#Set the parent obj to the render object
		self.pandaActor.reparentTo(self.render)
		#Loop the animation "walk"
		self.pandaActor.loop('walk')

		"""
		Create 4 intervals for the panda
		posInterval(seconds,endPos,startPos)
		startPos -------------> endPos
		            seconds
		"""
		pandaPosInterval1 = self.pandaActor.posInterval(13,Point3(0,-10,0),startPos=Point3(0,10,0))
		pandaPosInterval2 = self.pandaActor.posInterval(13,Point3(0,10,0),startPos=Point3(0,-10,0))
		pandaHprInterval1 = self.pandaActor.hprInterval(3,Point3(180,0,0),startHpr=Point3(0,10,0))
		pandaHprInterval2 = self.pandaActor.hprInterval(3,Point3(0,0,0),startHpr=Point3(180,0,0))

		#Create the sequence of intervals
		self.pandaPace = Sequence(pandaPosInterval1,pandaHprInterval1,pandaPosInterval2,pandaHprInterval2,name='pandaPace')
		self.pandaPace.loop()
	def spinCameraTask(self, task):
		angleDegrees = task.time * 6.0
		angleRadians = angleDegrees * (pi / 180.0)
		self.z += 1
		z_rad = self.z * (pi / 180.0)
		self.camera.setPos(50.0 * sin(angleRadians), -50.0 * cos(angleRadians), 2*sin(z_rad) + 10)
		self.camera.setHpr(angleDegrees, 0, 0)
		return Task.cont
app = MyApp()
app.run()