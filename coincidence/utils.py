def walkdown(path, *_sequences):
    sequences = [seq for seq in _sequences if seq]   #grab nonempty sequences
    if not sequences:
        return [path]
    result = []
    for index, sequence in enumerate(sequences):
        result.extend(walkdown(path + [sequence[0]], sequence[1:],
                               *[seq for i, seq in enumerate(sequences) if i != index]))
    return result

def intermerge(*sequences):
    """Merge all given sequences in all possible variations,
    retaining the original order of every sequence"""
    return walkdown([], *sequences)