#!/usr/bin/python

import string

LABEL_ORDER = ['folder contents', 'contents', 'view', 'edit', 'local roles', 'properties', 'state']

def unique_options(a_sequence):
    """Eliminates duplicate items in manage_options tuples,
       and canonicalizes their order."""

    # Turn the tuple of dictionaries into a single dictionary
    # indexed by the uppercased label.
    a_list = list(a_sequence)
    dict = {}
    for action in a_list:
        label = action['label']
        dict[string.upper(label)] = action

    # Move the dictionary items into the result set
    # in the same order as they appear in LABEL_ORDER.
    results = []
    for label in LABEL_ORDER:
        uc_label = string.upper(label)
        if dict.has_key(uc_label):
            results.append(dict[uc_label])
            del dict[uc_label]

    # Append any remaining items to the result set.
    for key in dict.keys():
        item = dict[key]
        results.append(item)

    # Turn it back into a tuple before returning.
    results = tuple(results)
    print 'results: ', results
    return results

