#!/usr/bin/python3
#######################################################################
# Quick script to generate .tsv files from Grew output, as with the
# GREW match platform
#######################################################################

import argparse, json, os.path, re

def parse_conllu(conllu_file):
    
    def write_buff():
        nonlocal d, sent_id, buff
        if not sent_id:
            # Create GREW-style sent_id
            sent_id = '{}_{:0>5}'.format( 
                os.path.basename(conllu_file),
                len(d.keys()) + 1
            )
        d[sent_id] = buff
        sent_id, buff = '', {}
    
    with open(conllu_file, 'r', encoding='utf-8') as f:
        buff, d, sent_id = {}, {}, ''
        for line in f.readlines():
            # Empty line: write contents to dictionary
            if line.isspace() and buff: write_buff() # Empty line, write buffer
            # Line contains a sentence_id
            m = re.match(r'#\s*sent_id\s*=\s*([^\n]*)', line)
            if m: sent_id = m.group(1)
            # Line contains token
            m = re.match(r'([0-9\-\.]+)\t([^\t]+)\t', line)
            if m: buff[m.group(1)] = m.group(2) # ID, WORD entry in dictionary
        if buff: write_buff() # just in case file doesn't end with an empty line
    return d
            
def parse_json(json_file):
    with open(json_file) as f:
        return json.load(f)
        
def main(conllu, json, pivot, output=''):
    
    def write_hit(hit):
        nonlocal text, pivot
        sid = hit['sent_id']  # ID from json file
        l = [sid] 
        try:
            sentence = text[sid]
        except KeyError:
            # If we can't match the sentence ID, just return the matching SID
            l.append('ID not in file')
            return l
        try:
            pivot_id = hit['matching']['nodes'][pivot]
        except KeyError:
            l.append('Pivot not in JSON')
            return l
        s_keys = list(sentence.keys())
        s_values = list(sentence.values())
        try:
            pivot_ix = s_keys.index(pivot_id)
        except ValueError:
            l.append('Pivot ID not in text')
            return l
        try:
            l += [' '.join(s_values[:pivot_ix]),
                s_values[pivot_ix],
                ' '.join(s_values[pivot_ix + 1:])
            ]
        except IndexError: # pivot is last word in sentence
            l += [
                ' '.join(s_values[:pivot_ix]),
                s_values[pivot_ix],
                ''
            ]
        return l
    
    text = parse_conllu(conllu)
    hits = parse_json(json)
    if not output: output = json[:-4] + 'tsv' # Default outfile simply replaces the JSON extension with .tsv
    with open(output, 'w', encoding='utf-8') as f:
        for hit in hits:
            f.write('\t'.join(write_hit(hit)) + '\n')
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description = \
        'Converts grew grep JSON file into a .tsv file.'
    )
    parser.add_argument('--conllu', help='Source CONLLU file.', required=True)
    parser.add_argument('--json', help='JSON file with matches.', required=True)
    parser.add_argument('--pivot', help='Name of pivot node.', required=True)
    parser.add_argument('--output', help='Output file.')
    kwargs = vars(parser.parse_args())
    main(**kwargs)
    
