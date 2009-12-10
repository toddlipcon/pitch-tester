#!/usr/bin/python

from tempfile import NamedTemporaryFile
import subprocess
import random
import optparse
import time
import sys

TEMPLATE=file("test.csd").read()
VALID_ANSWERS = ['<', '=', '>']

def parse_opts():
  parser = optparse.OptionParser()
  parser.add_option('-f', '--center-freq', dest="center_freq",
                    default=440,
                    type=float,
                    help="center frequency")
  parser.add_option('-c', '--cents-diff', dest="cents_diff",
                    default=10,
                    type=float,
                    help="cents to change pitch")
  parser.add_option("-i", "--interval", dest="interval",
                    default=0,
                    type=int,
                    help="interval (half steps)")
  parser.add_option("-v", "--vary", dest="vary_center",
                    default=0,
                    type=int,
                    help="vary first tone (half steps)")
  parser.add_option('-t', "--vary-tone", dest="vary_insts",
                    default=False,
                    action="store_true",
                    help="Vary instruments")
  options,args = parser.parse_args()
  if len(args) > 0:
    options.print_help()
    sys.exit(1)
  return options


def play_tones(freq_a, freq_b, vary_insts=False):
  subst = (TEMPLATE
    .replace('@FREQ1', str(freq_a))
    .replace("@FREQ2", str(freq_b))
    .replace('@INST1', "1")
    .replace('@INST2', vary_insts and "2" or "1"))
  with NamedTemporaryFile(suffix=".csd") as f:
    f.write(subst)
    f.flush()
    subprocess.check_call(["/usr/bin/csound", f.name],
                          stderr=file("/dev/null"))
    f.close()

def get_correct_response(freq_a, freq_b):
  if freq_a < freq_b:
    return '>'
  elif freq_a == freq_b:
    return '='
  elif freq_a > freq_b:
    return '<'

def run_test(center_freq, cents_diff, interval, vary_insts=False):
  target_freq = center_freq * pow(2, float(interval)/12.0)
  choices = [target_freq,
             target_freq*pow(2, float(cents_diff)/1200),
             target_freq*pow(2, -float(cents_diff)/1200)]
  freq_a = center_freq
  freq_b = random.choice(choices)
  correct = get_correct_response(target_freq, freq_b)

  repeat = True
  while repeat:
    repeat = False
    play_tones(freq_a, freq_b, vary_insts=vary_insts)
    answer = raw_input("<|=|> ?").strip()
    if answer == correct:
      print "Right!"
    elif answer in VALID_ANSWERS:
      print "Incorrect. Correct was: " + correct
      print "Playing correct..."
      play_tones(freq_a, target_freq)
      time.sleep(0.5)
      print "OK. Moving on....\n"

    else:
      repeat = True

def main():
  options = parse_opts()
  while True:
    varied = options.center_freq * \
      pow(2, float(random.randint(0, options.vary_center))/12)
    run_test(center_freq=varied,
             cents_diff=options.cents_diff,
             interval=options.interval,
             vary_insts=options.vary_insts)

if __name__ == "__main__":
  main()
