# [tunniplaan.arti.ee](http://tunniplaan.arti.ee/) lehe lähtekood

Siin on siis selle lehe lähtekood. Kood ise on üsna vähe confitav, aga peaks olema
üsna kergelt mõistetav. http://tunniplaan.arti.ee/blog lehelt võib leid ka mõninga
kirjelduse selle kohta, kuidas siinolev kood on kokku pandud.

## Kuidas jooksutada seda koodi?

### Setup

Kõigepealt oleks vaja keskond üles seada, selleks oleks vaja linuxiga masinat,
kuhu on installitud Python 3 koos setup tools'i ning git'iga. Seejärel tuleks
käima lasta järgmised käsud:

    git clone https://github.com/arti95/tunniplaan.arti.ee.git  # kloonime repo
    cd tunniplaan.arti.ee      # siseneme sinna kausta
    python3 -m venv venv       # tekitame virtualenvi venv kausta
    source venv/bin/activate   # käivitame venv'i
    pip install flask          # veebi osa jaoks
    pip install beautifulsoup4 # html'i parsemiseks

Peale selle on vaja veebist tunniplaanide allalaadimiseks veel ka `imagemagick`
pakist `convert` käsku, millega eemaldatakse `.png` failidelt läbipaistvus ja
`swftools` pakist on vaja `swfrender` käsku, millega `.swf` flash failidest
tehakse `.png` failid.

### Kasutamine (tunniplaanide sikutamine)

Kõigepealt oleks vaja `static/img/` kausta kataloogipuu tunniplaanidega, mis
peaks välja nägema selline:

![kataloogi puu](http://i.imgur.com/OoRdgcF.png)

Selleks tuleks kasutada `vmg_tunniplaan.py` ja `vmok_tunniplaan.py` skripte,
mis käivitamisel tõmbavad kooli kodukalt alla tunniplaanid ning paigutavad need
õigetesse kaustadesse.

### Kasutamine (veeb)

Veebiosa käivitamiseks, developeri režiimis, piisab lihtsalt `python3 main.py`
käivitamisest sealsamas kaustas

[uWSGI](http://uwsgi-docs.readthedocs.org) kasutamiseks tasub uurida enda 
veebiserveri ja uwsgi dokumentatsiooni, et see avalikus Internetis korralikult
tööle saada
