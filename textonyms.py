from collections import defaultdict
import urllib.request
import json
import math

CH2NUM = {ch: str(num) for num, chars in enumerate('abc def ghi jkl mno pqrs tuv wxyz'.split(), 2) for ch in chars}
URL = 'https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-usa-no-swears.txt'
URL2 = 'https://raw.githubusercontent.com/quinnj/Rosetta-Julia/master/unixdict.txt'

def getwords(url):
 return urllib.request.urlopen(url).read().decode("utf-8").lower().split()

def word_to_num(word):
    return ''.join(CH2NUM[ch] for ch in word)

def mapnum2words(words):
    number2words = defaultdict(list)
    reject = 0
    for word in words:
        try:
            key = word_to_num(word)
            if word not in number2words[key]:
                number2words[key].append(word)
        except KeyError:
            # Reject words with non a-z e.g. '10th'
            reject += 1
    return dict(number2words), reject

def longest_synonyms(num2words):
    longest = ''
    for key in num2words:
        if len(key) > len(longest) and len(num2words[key]) > 1:
            longest = key 

    print('\n', 'longest synonyms', longest, len(longest), 'letters long maps to:', num2words[longest])

def different_in_letters(num2words):
    gt_four_letters = []
    for i in num2words:
        if len(i) > 3 and len(num2words[i]) > 1:
            gt_four_letters.append(num2words[i])

    # print(gt_four_letters)

    for words in gt_four_letters:
        for i_word in words:
            for j_word in words:
                diff_letters = 0
                index = 0
                for char in j_word:
                    if char != i_word[index]:
                        diff_letters += 1
                    index += 1
                if diff_letters > 3:
                    print(i_word, j_word, 'have a difference of', diff_letters)

def longest_combo(num2words):
    longest = ['1']

    for num in num2words:
        if len(num) > len(longest[0]):
            longest = [num]
        elif len(num) == len(longest[0]):
            longest.append(num)
    
    print('the longest number is %i digits' % (len(longest[0])))
    for num in longest:
        print('\t', num, 'maps to: ', num2words[num])

def get_svg_line(x1,x2,y1,y2):
    return ('<line x1="%i" x2="%i" y1="%i" y2="%i" stroke="black"></line>' % (x1,x2,y1,y2))

def get_keystrokes(combo):
    keystrokes = ''
    prev = [False, False]
    occurences = {}

    for num in combo:
        if num not in occurences:
            occurences[num] = 0
        occurences[num] += 1

    for num in combo:
        r = occurences[num] * 5
        occurences[num] -= 1
        x = 20 + (((int(num) - 1)%3) * 40)
        y = 20 + math.floor((int(num) -1)/3) * 40
        if prev[0] and prev[1]:
            keystrokes += get_svg_line(x, prev[0], y, prev[1])
        keystrokes += ('<circle fill="%s" cx="%i" cy="%i" data-digit="%s" r="%i"></circle>' % ('#fff', x, y, num, r))
        prev = [x, y]
    
    for num in occurences:
        x = 20 + (((int(num) - 1)%3) * 40)
        y = 20 + math.floor((int(num) -1)/3) * 40
        r = 5
        fill = '#fff'
        if num == combo[0]:
            fill = 'orangered'
        keystrokes += ('<circle fill="%s" cx="%i" cy="%i" data-digit="%s" r="%i"></circle>' % (fill, x, y, num, r))

    return '<g>%s</g>' % keystrokes

def get_graphic(combo, include_labels = False):
    labels = ''
    if include_labels:
        labels = '<text x="60" y="13">abc</text><text x="100" y="13">def</text><text x="20" y="52">ghi</text><text x="60" y="52">jkl</text><text x="100" y="52">mno</text><text x="20" y="92">pqrs</text><text x="60" y="92">tuv</text><text x="100" y="92">wxyz</text>'

    return '<div class="combo-graphic"><svg height="120" width="120"><g>' + labels + get_svg_line(40,40,0,120) + get_svg_line(80,80,0,120) + get_svg_line(0,120,40,40) + get_svg_line(0,120,80,80) + get_keystrokes(combo) + '</g></svg></div>'                

if __name__ == '__main__':
    words = list(set(getwords(URL) + getwords(URL2) + ['goats']))
    print("Read %i words from %r and %r" % (len(words), URL, URL2))
    wordset = set(words)
    num2words, reject = mapnum2words(words)
    morethan1word = sum(1 for w in num2words if len(num2words[w]) > 1)
    maxwordpernum = max(len(values) for values in num2words.values())
    print("""
There are {0} words in {1} and {2} which can be represented by the Textonyms mapping.
They require {3} digit combinations to represent them.
{4} digit combinations represent Textonyms.\
""".format(len(words) - reject, URL, URL2, len(num2words), morethan1word))

    w = open('./data/words.json', 'w')
    json.dump(num2words, w, indent=4, ensure_ascii=False)
    w.close()

    longest_synonyms(num2words)
    different_in_letters(num2words)
    longest_combo(num2words)

    page_name = '2'
    page_default = '<!DOCTYPE html><html lang="en"><head><meta http-equiv="Content-Type"content="text/html; charset=UTF-8" /><title>textonyms</title><meta property="og:title" content="t9 textonyms" /><link rel="shortcut icon" href="./favicon.png"></link><meta name="viewport" content="width=device-width,initial-scale=0.8"><meta property="og:image" content="./favicon.png"><link rel="stylesheet" href="./client/main.css" /><body><main>'
    page_html = page_default
    page_html += '<header>' + get_graphic(word_to_num('textonyms'), True) + '<div><h1>' + word_to_num('textonyms') + '</h1><h2>t9 textonyms</h2></div></header>'
    index_html = '<ul>'
    for combo in sorted(num2words.keys()):
        # if combo[0] != page_name:
        #     page_html += '</main></body></head></html>'

        #     w = open('./' + page_name + '.html', 'w')
        #     w.write(page_html)
        #     w.close()

        #     index_html += '<li><a href="./' + page_name + '.html">' + page_name + '</a></li>'

        #     page_name = combo[0]
        #     page_html = page_default

        if len(num2words[combo]) > 1:
            page_html += '<section><div class="combo-header">' + get_graphic(combo) + '<h2>' + str(combo) + '</h2></div>'
            for word in num2words[combo]:
                page_html += '<p>' + word + '</p>'
            page_html += '</section>'

    # page_html = page_default
    # page_html += index_html
    # page_html += '</ul></main></body></head></html>'

    w = open('./index.html', 'w')
    w.write(page_html)
    w.close()

    print("\nThe numbers mapping to the most words map to %i words each:" % maxwordpernum)
    maxwpn = sorted((key, val) for key, val in num2words.items() if len(val) == maxwordpernum)
    for num, wrds in maxwpn:
        print("  %s maps to: %s" % (num, ', '.join(wrds)))