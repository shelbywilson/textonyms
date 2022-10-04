# T9 textonyms

[https://shelby.cool/textonyms](https://shelby.cool/textonyms)

A compilation/thesaurus of [words that share the same T9 keystrokes](https://en.wikipedia.org/wiki/Predictive_text#Textonyms).

<img width="373" alt="Textonyms 25483 (alive, chive) and 25569 (allow, alloy)" src="https://user-images.githubusercontent.com/5523024/193935681-2cbb36eb-1768-4779-b5ca-16cdd876a6fa.png">

## textonyms.py
Modified from [Rosetta Code](https://rosettacode.org/wiki/Textonyms#Python).

`python textonyms.py` will translate a set of words to T9 keystrokes and filter for digit combinations with multiple possible words. It will then generate index.html with svg diagrams of keystrokes from this dictionary.