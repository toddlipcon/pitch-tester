<CsoundSynthesizer>
<CsOptions>
-odac -d -B4096 -b1024
</CsOptions>
<CsInstruments>

instr 1  
  a1 oscil 3000, p4, p5
  out a1
endin

</CsInstruments>

<CsScore>
f1 0 16384  10 1 .5 .333333 .25 .2 .166667 .142857 
f2 0 16384  10 1 ;.5 .333333  .25 .2 .166667 .142857 
i1 0 0.75 @FREQ1 1
i1 0.75 1.5 @FREQ2 2
</CsScore>

</CsoundSynthesizer>
