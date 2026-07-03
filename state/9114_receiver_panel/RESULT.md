# H_9114 -- Receiver-PANEL referent-agreement -- RESULT

**VERDICT: 🟠 PARTIAL — beaters=['claude-fable-5', 'sonnet', 'haiku'] b2(agr)=False b3(consensus)=False; agreement=0.5952380952380953 vs 0.6904761904761905**

- responders: ['claude-fable-5', 'haiku', 'sonnet'] · receivers-beating-shuffle(t>=4): ['claude-fable-5', 'sonnet', 'haiku']
- mean inter-receiver agreement (real, t>=4) = 0.5952380952380953 · shuffle = 0.6904761904761905
- consensus acc (t>=4) = 0.750 · best single receiver = 0.821
- receivers = ['claude-fable-5', 'sonnet', 'haiku'] (heterogeneous theta, all outside anima closure) · emits FROZEN engine-native (H_9111)
- tier = PANEL-CONSENSUS-DIRECTIONAL if 🟢 else DIRECTIONAL-on-external-oracle

## real arm
  t=8B: acc={'claude-fable-5': 0.857, 'sonnet': 0.857, 'haiku': 0.714} consensus=0.857 agreement=0.8095238095238096
  t=4B: acc={'claude-fable-5': 0.786, 'sonnet': 0.571, 'haiku': 0.214} consensus=0.643 agreement=0.38095238095238093
## shuffle arm
  t=8B: acc={'claude-fable-5': 0.0, 'sonnet': 0.0, 'haiku': 0.071} consensus=0.000 agreement=0.8095238095238094
  t=4B: acc={'claude-fable-5': 0.0, 'sonnet': 0.0, 'haiku': None} consensus=0.000 agreement=0.5714285714285714
