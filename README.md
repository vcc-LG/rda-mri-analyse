# rda-mri-analyse
Code to batch analyse multiple .rda files and store in Sqlite db

Place your RDA files in the ```data/``` directory and run main.py. It will use [Tarquin](http://tarquin.sourceforge.net/) to analyse the files and store the results in the ```output/``` directory. It will also dump the concentration data in a SQLite database, located in the ```database.``` directory. 

Future work will be to integrate this into a web app to allow users to more easily interact with and analyse the MRS data.
