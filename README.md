Inżynieria języka naturalnego
=============================

Kod programu na którym opiera się projekt.

Grupa zajęciowa
---------------

Rok akademicki 2014/2015

Semestr zimowy

Śr. 13:15

Autorzy
-------

* Jacek Miszczak (179158)
* Filip Malczak (179326)

Dev Notes
---------

> Zawartość tego i kolejnych rozdziałów nie powinna być brana pod uwagę przy ocenie; są to jedynie prywatne notatki.

1. Tym razem w komentarzach i dokumentach używajmy j. polskiego. Jakby nie patrzeć, nim się zajmujemy... Klasy i
zmienne - klasycznie, po angielsku ~F
2. Dla ujednolicenia używajmy terminów "question class" (qc) i "expected answer type" (eat) zamiast "klasa pytania"
i "oczekiwany typ odpowiedzi" (OTO) ~F
3. Proszę o dodawanie takiej formułki na górę każdego modułu, na rzecz wygody na linuksie:

> \#!/usr/bin/python2

> \# -*- coding: UTF-8 -*-

4. w module main jedyne co się zmienia to moduł z pakietu question_classification. Jeśli piszemy skrypty, to wystawiamy
z nich funkcję main przyjmującą sys.argv która zostanie tam (w main.py) wywołana. ~F

5. Pliki z danymi wrzucamy na repo, nie są aż tak duże. Wyjątkiem od tego, póki co, jest leksykon nazw własnych - on ma
60 MB, tym nie będziemy gita katować. Nalezy go dociągnąć z http://nlp.pwr.wroc.pl/download/ner/nelexicon-v1.7z
rozpakować i wrzucić do <repo_root>/data