#!/usr/bin/python

from tempfile import NamedTemporaryFile
import subprocess
import random
import optparse
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
  options,args = parser.parse_args()
  if len(args) > 0:
    options.print_help()
    sys.exit(1)
  return options


def play_tones(freq_a, freq_b):
  subst = TEMPLATE.replace('@FREQ1', str(freq_a)).replace("@FREQ2", str(freq_b))
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

def run_test(center_freq, cents_diff):
  choices = [center_freq,
             center_freq*pow(2, float(cents_diff)/1200),
             center_freq*pow(2, -float(cents_diff)/1200)]
  freq_a = center_freq
  freq_b = random.choice(choices)
  correct = get_correct_response(freq_a, freq_b)

  repeat = True
  while repeat:
    repeat = False
    play_tones(freq_a, freq_b)
    answer = raw_input("<|=|> ?").strip()
    if answer == correct:
      print "Right!"
    elif answer in VALID_ANSWERS:
      print "Incorrect. Correct was: " + correct
    else:
      repeat = True

def main():
  options = parse_opts()
  while True:
    run_test(center_freq=options.center_freq,
             cents_diff=options.cents_diff)

if __name__ == "__main__":
  main()
