# adapted from https://gist.github.com/cliffano/9868180
import os
import sys
import datetime
import time
import json
from json import JSONEncoder

now = datetime.datetime.now()

class CallbackModule(object):
  def json_log(self, res, host):
    pid = self.pid
    log_dir = datetime.datetime.strftime(datetime.datetime.now(), "logs/%s/%%Y/%%m/%%d" % self.play)
    log_filename = "%s/%s-%d.json" % (log_dir, now.strftime("%s"), pid)
    if type(res) == type(dict()):
      if 'verbose_override' not in res:
        res.update({"host": host, "pid": pid, "play": self.play, "task": self.task })
        combined_json  = json.dumps(res, sort_keys=True)
	try:
		os.makedirs(log_dir)
	except Exception as e:
		if e.errno != 17:
			print >>sys.stderr, e
        with file(log_filename, "a") as f:
		f.write("%s\n" % combined_json)


  def on_any(self, *args, **kwargs):
    pass

  def runner_on_failed(self, host, res, ignore_errors=False):
    self.json_log(res, host)

  def runner_on_ok(self, host, res):
    self.json_log(res, host)

  def runner_on_error(self, host, msg):
    pass

  def runner_on_skipped(self, host, item=None):
    pass

  def runner_on_unreachable(self, host, res):
    self.json_log(res, host)

  def runner_on_no_hosts(self):
    pass

  def runner_on_async_poll(self, host, res, jid, clock):
    self.json_log(res, host)

  def runner_on_async_ok(self, host, res, jid):
    self.json_log(res, host)

  def runner_on_async_failed(self, host, res, jid):
    self.json_log(res, host)

  def playbook_on_start(self):
    pass

  def playbook_on_notify(self, host, handler):
    pass

  def playbook_on_no_hosts_matched(self):
    pass

  def playbook_on_no_hosts_remaining(self):
    pass

  def playbook_on_task_start(self, name, is_conditional):

    if '|' in name:
      (self.play, self.task) = map(lambda s: s.strip(), name.split('|'))
    else:
      self.play = None
      self.task = name

  def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
    pass

  def playbook_on_setup(self):
    pass

  def playbook_on_import_for_host(self, host, imported_file):
    pass

  def playbook_on_not_import_for_host(self, host, missing_file):
    pass

  def playbook_on_play_start(self, pattern):
    self.pid = os.getpid()

  def playbook_on_stats(self, stats):
    pass
