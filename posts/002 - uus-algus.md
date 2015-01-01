---
title: Uus algus
slug: uus-algus
date: katse nr 2 &mdash; 23. aprill 2014
---

2014-nda aasta aprillikuu lõpupoole otsustasin selle mobiilse tunniplaani 
rakenduse projekti uuesti ellu äratada ning ka lõpuni viia siis toimunud 
võrgurakendused kooli tundide raames.

Kuna ma tollel hetkel enda esimest katset enam üles ei leidnud siis otsustasin 
uuesti nullist alustada.

Algust sai tehtud `vmok_tunniplaan.py` failiga mille eesmärk on Väike-Maarja
Õppekeskuse kodulehelt üles otsida hetkel üleval olevad tunniplaanid ning need 
siis alla laadida ja need `.png` piltideks teisendada.

Eesmärk sai jaotatud mitmeks väiksemaks probleemiks, et neid kergem lahendada oleks
1. HTML koodist tunniplaanide nimekirja välja lugemine
2. Tunniplaani allalaadimine
3. Flash `.swf` failide lugemine ja nendest `.png` piltide loomine
4. Piltide salvestamine loogilisse kaustapuuse.

Esimene probleem on õnneks üsna kergelt lahendatav kuna programmeerimiskeeles
[Python][1], mida ma otsustasin kasutada terve selle projekti jaoks,
on olemas üks teek nimega [Beautiful Soup][2] millega on üsna lihtne 
HTML koodist ennast läbi närida. Lisaks sai ka kasutatud [requests][3] teeki
mis muudab HTTP käskude saatmise serverile palju palju kergemaks.

<script src="https://gist.github.com/arti95/6fb56a63ad90ae349725.js"></script>

[1]: https://www.python.org/ "Python programeerimiskeele koduleht"
[2]: http://www.crummy.com/software/BeautifulSoup/ "Beautiful Soup Python teegi koduleht"
[3]: http://docs.python-requests.org/ "Requests: HTTP for Humans"

