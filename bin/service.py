#!venv/bin/python

import argparse
import datetime
import logging
import os
import signal
import subprocess
import sys

script_dir = os.path.dirname(__file__)

logs_dir = os.path.join(script_dir, "..", "logs")
today = datetime.date.today().strftime("%Y-%m-%d")
log_path = os.path.join(logs_dir, "{}.log".format(today))

pid_path = os.path.join(script_dir, "") #TODO


def parse_args():
	argp = argparse.ArgumentParser()
	argp.add_argument("cmd", choices=["start", "status", "stop", "restart"])
	return argp.parse_args()


def get_pid():
	"""
	Get the PID of this app if it's running, return None otherwise.

	The app is running if the PID is stored in {}, and if that process still
	runs.
	""".format(pid_path)

	try:
		with open(pid_path) as pid_file:
			pid = pid_file.read()
	except OSError:
		return None
	else:
		pid = int(pid)

	# os.kill has a misleading name - we're just checking if process is running
	try:
		os.kill(pid, 0)
	except ProcessLookupError:
		return None

	return pid


def start():
	logging.info("Starting ...")


def status():
	pid = get_pid()
	if pid:
		logging.info("Running with PID %d", pid)
	else:
		logging.info("Not running")
		sys.exit(1)


def stop():
	pid = get_pid()

	if not pid:
		logging.error("Not running")
		sys.exit(1)

	logging.info("Stopping process running with PID %d...", pid)
	os.kill(pid, signal.SIGHUP)
	os.remove(pid_path)
	logging.info("Stopped")

if __name__ == "__main__":

	logging.basicConfig(
		level=logging.DEBUG, stream=sys.stderr,
		format="%(asctime)s\t%(levelname)s\t%(message)s"
	)

	if not os.path.exists(logs_dir):
		os.makedirs(logs_dir)

	args = parse_args()
	if args.cmd == "start":
		start()
	elif args.cmd == "status":
		status()
	elif args.cmd == "stop":
		stop()
	elif args.cmd == "restart":
		stop()
		start()
	else:
		raise ValueError()
