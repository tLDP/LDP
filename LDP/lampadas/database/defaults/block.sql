DELETE FROM block_i18n;
DELETE FROM block;

INSERT INTO block (block_code) VALUES ('header');
INSERT INTO block (block_code) VALUES ('footer');

INSERT INTO block_i18n (block_code, lang, block) VALUES ('header', 'EN',
'
<center>
<a href="home">Home</a> \\|
<a href="about">About |projectshort|</a>
</center>
');

INSERT INTO block_i18n (block_code, lang, block) VALUES ('header', 'FR',
'
<center>
<a href="home">Chez Moi</a> \\|
<a href="about">About |projectshort|</a>
</center>
');

INSERT INTO block_i18n (block_code, lang, block) VALUES ('footer', 'EN',
'
<center>
<a href="copyright">Copyright</a> \\|
<a href="privacy">Privacy</a> \\|
<a href="lampadas">About Lampadas</a>
<p>
<a href="/EN/|page|">English</a> \\|
<a href="/FR/|page|">French</a>
</center>
');

INSERT INTO block_i18n (block_code, lang, block) VALUES ('footer', 'FR',
'
<center>
<a href="copyright">Le Copyright</a> \\|
<a href="privacy">Le Privacy</a> \\|
<a href="lampadas">Le About Lampadas</a>
<p>
<a href="/EN/|page|">L''Anglais</a> \\|
<a href="/FR/|page|">Fran&ccedil;ais</a>
</center>
');
