# 1024 Spiders

Some 1024 spiders, crawl xp1024 porn information and magnet-links and insert them into the database.

* Python 3.6
* MySQL 8.0

## Deploy

### Clone & Install

```
git clone git@github.com:huihut/1024Spiders.git
cd 1024Spiders && pip install -r requirements.txt
```

### Configure

* No_Json

    Configure your database, request_header, save_path, etc. in the source code.

* With_Json

    1. `mv config_template.json config.json` ( [config_template.json](config_template.json) )
    2. Configure your database, request_header, save_path, etc. in the `config.json`.

### Run front-end process

```
python TorrentSpider_AsianNomosaic_DB.py
```

### Run background process

```
nohup python -u TorrentSpider_AsianNomosaic_DB.py > TorrentSpider_AsianNomosaic_DB.log 2>&1 &
```

## Database

```mysql
mysql> show tables;
+-------------------------+
| Tables_in_torrent       |
+-------------------------+
| AsianNomosaic           |
| AsianNomosaicPictures   |
| EuropeAmerica           |
| EuropeAmericaPictures   |
| JapaneseCavalry         |
| JapaneseCavalryPictures |
+-------------------------+
6 rows in set (0.01 sec)

mysql> desc AsianNomosaic;
+---------+-----------+------+-----+---------+----------------+
| Field   | Type      | Null | Key | Default | Extra          |
+---------+-----------+------+-----+---------+----------------+
| id      | int(11)   | NO   | PRI | NULL    | auto_increment |     # porn id
| data    | char(10)  | YES  |     | NULL    |                |     # porn date
| name    | char(255) | NO   |     | NULL    |                |     # porn name
| summary | text      | YES  |     | NULL    |                |     # porn introduction
| magnet  | char(255) | NO   |     | NULL    |                |     # porn magnet-link
+---------+-----------+------+-----+---------+----------------+
5 rows in set (0.00 sec)

mysql> desc AsianNomosaicPictures;
+-------+-----------+------+-----+---------+----------------+
| Field | Type      | Null | Key | Default | Extra          |
+-------+-----------+------+-----+---------+----------------+
| id    | int(11)   | NO   | PRI | NULL    | auto_increment |       # picture id
| an_id | int(11)   | NO   |     | NULL    |                |       # porn id
| name  | char(255) | NO   |     | NULL    |                |       # picture name
+-------+-----------+------+-----+---------+----------------+
3 rows in set (0.00 sec)
```