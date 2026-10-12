# Mesure des limites — semaine 4

Machine : Windows 11, Intel64 Family 6 Model 170, 15.37 GiB RAM, Python 3.12.6.

| Taille du flux | Distincts réels | Mémoire set exact | Temps exact | Mémoire FM | Temps FM | Ratio FM/réel |
|---:|---:|---:|---:|---:|---:|---:|
| 100,000 | 36,702 | 3.9 MB | 0.25 s | 4.4 KB | 8.92 s | 1.15× |
| 200,000 | 73,410 | 5.8 MB | 0.53 s | 4.4 KB | 18.90 s | 1.15× |
| 400,000 | 146,970 | 11.6 MB | 1.11 s | 4.4 KB | 36.18 s | 0.58× |
| 1,600,000 | 587,625 | 46.6 MB | 4.54 s | 4.4 KB | 142.32 s | 1.15× |

L'ensemble exact passe d'environ 3.9 MB à 46.6 MB sur un facteur 16 de flux,
soit une croissance approximativement linéaire (environ 28 bytes par élément
du flux ici). FM reste à 4.4 KB : sa mémoire dépend des 16 hashes, pas de la
longueur du flux. Ses ratios oscillent entre 0.58× et 1.15×; cette imprécision
est le prix de la mémoire bornée.

Le set exact est resté utilisable jusqu'à 1.6 million dans cette mesure. Le
run complet est devenu pénible à ce point (plus de deux minutes), mais à cause
du calcul FM en Python, non pas par manque de RAM. Une estimation à un facteur
deux peut suffire à surveiller une tendance de visiteurs; elle ne convient pas
à une facture, un quota, ou une décision de conformité nécessitant un nombre
exact.
