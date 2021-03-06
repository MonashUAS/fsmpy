from .. import FSM as FSMBase
from .. import set_logger
from std_msgs.msg import String
import rospy

'''
A subclass of FSM specificly for ROS applications.

ros.FSM initialises a ROS node and sets the fsmpy logger to rosout.
'''
class FSM(FSMBase):
	'''
	name:			the name of the FSM used in logging
	topic:			the topic to publish the state string too
	save_file=None:	path to a file to be used for storing the current state stack

	All other arguments are passed through to the call to rospy.init_node.
	'''
	def __init__(self, name, topic, *args, **kw):
		if 'save_file' in kw:
			save_file = kw.pop('save_file')
		else:
			save_file = None
		rospy.init_node(*args, **kw)
		set_logger("rosout")
		self.__pub = rospy.Publisher(topic, String, queue_size=2, latch=True)
		super(FSM, self).__init__(name, save_file=save_file)

	### Method Overrides ###

	def on_transition(self, next_state):
		self.__pub.publish(next_state.name)
		self.loginfo("Transitioned to State '%s'"%(next_state.name))

	def delay(self):
		rospy.sleep(self.delay_duraton)
		if rospy.is_shutdown():
			self.logfatal("ROS shutdown")

	### / Method Overrides ###
