import itertools
import random

import mido


def generate_chain_v2(num_states, order=2):
    """
    >>> generate_chain_v2(num_states=2, order=3)
    {
        ((0, 0), 0): 0.28494308534904395,
        ((0, 0), 1): 0.3313206033195829,
        ((0, 0), 2): 0.38373631133137304,
        ((0, 1), 0): 0.3391475885535857,
        ...
    }
    ((prev2, prev1), next): prob    
    """
    states = list(range(num_states))
    histories = list(itertools.product(*[states] * order))
    d = {}
    for hist in histories:
        freqs = [random.random() for s in states]
        tot = sum(freqs)
        probs = [f / tot for f in freqs]
        d.update({(hist, s): p for s, p in enumerate(probs)})
    return d


def generate_chain(num_states, order=2):
    """
    >>> generate_chain(num_states=3, order=2)
    {
        (0, 0): ([0, 1, 2], [0.7327870398594072, 0.21593138486562874, 0.05128157527496412]),
        (0, 1): ([0, 1, 2], [0.5487415773422673, 0.07647795810376425, 0.37478046455396846]),    
        ...
    }
    ((prev2, prev1): ([next_case1, next_case2, ...], [prob1, prob2, ...])  # sum(probs) = 1
    """
    states = list(range(num_states))
    histories = list(itertools.product(*[states] * order))
    d = {}
    for hist in histories:
        freqs = [random.random() for s in states]
        tot = sum(freqs)
        probs = [f / tot for f in freqs]
        d[hist] = (states, probs)
    return d


def generate_series(chain, num_states, order, init, length):
    """
    >>> generate_series(c, 3, 2, (0, 1), 20)
    [0, 1, 1, 2, 0, 1, 0, 2, 2, 1, 1, 1, 1, 1, 1, 0, 2, 2, 2, 1, 2, 0]
    """
    series = [] + list(init)
    hist = init
    for k in range(length):
        states, probs = chain[hist]
        next_state = random.choices(states, probs)[0]
        series.append(next_state)
        hist = hist[1:] + (next_state, )
    return series


def generate_melody_01():
    scale = {0: 0, 1: 5, 2: 7}
    chain = generate_chain(num_states=3, order=2)
    series = generate_series(chain=chain, num_states=3, order=2, init=(0, 1), length=20)
    melody = [60 + scale[key] for key in series]
    return melody


if __name__ == '__main__':
    messages = []
    duration = 480

    melody = generate_melody_01()
    for note in melody:
        messages.append(mido.Message('note_on', note=note, velocity=100, time=0))
        messages.append(mido.Message('note_off', note=note, velocity=100, time=duration))

    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    for msg in messages:
        track.append(msg)

    mid.save('new_song.mid')    