# tunniplaan.arti.ee lehe lähtekood

Siin on siis selle lehe lähtekood. Kood ise on üsna vähe confitav aga peaks olema
üsna kergelt mõistetav. http://tunniplaan.arti.ee/blog lehelt võib leid ka mõninga
kirjelduse selle kohta kuidas siin olev kood on kokku pandud.

## kuidas jooksutada seda koodi

### setup

kõige pealt oleks vaja keskond üles seada, selleks oleks vaja linuxiga masinat
kus on peale installitud Python 3 koos setup toolsi ning git'iga. Seejärel tuleks
käima lasta need käsud:

    git clone https://github.com/arti95/tunniplaan.arti.ee.git  # kloonime repo
    python3 -m venv venv       # tekitame virtualenvi venv kausta
    source venv/bin/activate   # käivitame venv'i
    pip install flask          # veebi osa jaoks
    pip install beautifulsoup4 # html'i parsemiseks

peale selle on vaja veebist tunniplaanide alla laadimiseks veel ka `imagemagick`
pakist `convert` käsku millega eemaldatakse `.png` failidelt läbipaistvus ja
`swftools` pakist on vaja `swfrender` käsku millega `.swf` flash failidest
tehakse `.png` failid.

### kasutamine (tunniplaanide sikutamine)

kõigepealt oleks vaja `static/img/` kausta tunniplaanid tekitada
kindel kataloogi puu mis peaks välja nägema selline

[Imgur](http://i.imgur.com/OoRdgcF.png)

selleks tuleks kasutada `vmg_tunniplaan.py` ja `vmok_tunniplaan.py` skripte
mis käivitumisel tõmbavad kooli kodukalt alla tunniplaanid ning panevad need
sinna kaustadesse õiges.

### kasutamine (veeb)

veebi osa käivitamiseks developeri reziimis piisab lihtaslt `python3 main.py`
käivitamisest seal samas kaustas

uwsgi kasutamiseks tasub uurida enda veebiserveri ja uwsgi dokumentatsiooni, et
see korralikult avalikus netis tööle saada
