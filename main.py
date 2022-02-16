from robot import Robot

def main():

	try:
		robot = Robot(interface='/dev/input/js0', connecting_using_ds4drv=False)
		robot.listen()
		# robot.start()
			
	except (KeyboardInterrupt, SystemExit):
		robot.shutdown()


if __name__ == "__main__":
	main()
