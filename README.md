If you use this work please cite my work:
```
@article{soleymani2023protinteract,
  title={ProtInteract: A deep learning framework for predicting protein--protein interactions},
  author={Soleymani, Farzan and Paquet, Eric and Viktor, Herna Lydia and Michalowski, Wojtek and Spinello, Davide},
  journal={Computational and Structural Biotechnology Journal},
  volume={21},
  pages={1324--1348},
  year={2023},
  publisher={Elsevier}
}
```

```
@article{soleymani2022protein,
  title={Protein--protein interaction prediction with deep learning: A comprehensive review},
  author={Soleymani, Farzan and Paquet, Eric and Viktor, Herna and Michalowski, Wojtek and Spinello, Davide},
  journal={Computational and Structural Biotechnology Journal},
  volume={20},
  pages={5316--5341},
  year={2022},
  publisher={Elsevier}
}
```


### ProtInteract Datasets 

The following links can download the datasets used to train the [ProtInteract framework](https://www.sciencedirect.com/science/article/pii/S2001037023000296?via%3Dihub) for protein-protein interaction. These datasets are retrieved from the [STRING database][1].

1- The ["Protein_Sequences"][2] contains amino acid sequences of Homo sapiens, Mus musculus, E.coli, S.cerevisiae, D.melanogaster and C.elegans organisms available on the STRING database. 

2- The ["PPI_datasets"][3] contains protein-protein interaction sets of Homo sapiens, Mus musculus, E.coli, S.cerevisiae, D.melanogaster and C.elegans organisms available on the STRING database, with their respective interaction score.

3 - The ["Negatome_2.0"][4] contains the experimentally curated PPI pertaining to Homo sapiens and Mus musculus organisms.

The processed datasets for this work is available [here][5]. This dataset contains protein interactions under three scenarios, 2-classes, 3-classes and 5-classes.





```
docker build --no-cache -f Dockerfile -t data_processing .
```

```
docker run --rm -it data_processing
```





[1]: https://string-db.org/cgi/download?sessionId=bJBREVNlU0b2

[2]: https://uottawa-my.sharepoint.com/personal/fsole078_uottawa_ca/_layouts/15/guestaccess.aspx?docid=0d3ffd65e49a04259ae5a2e4e96ef87d6&authkey=AQTpiIB0l1M9JoPtHIrXNGM&e=j5nhev

[3]: https://uottawa-my.sharepoint.com/personal/fsole078_uottawa_ca/_layouts/15/guestaccess.aspx?docid=09cc4a4734ad145a0a768b9169a2eb4d5&authkey=AUJ-1i3A4SF5QWvoFf9F7pc&e=wUs7sW

[4]: https://uottawa-my.sharepoint.com/personal/fsole078_uottawa_ca/_layouts/15/guestaccess.aspx?docid=0de7633725541482192b2b2f397e14418&authkey=AefFpc6dRwI0nswW9O6zar4&e=HRaGac

[5]: https://uottawa-my.sharepoint.com/personal/fsole078_uottawa_ca/_layouts/15/guestaccess.aspx?share=ETkhLgX7-PdCrMOgex-yhzoBEtrAtcugGOu97ucliP98lw&e=GKEZ73