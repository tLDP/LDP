DELETE FROM block_i18n;
DELETE FROM block;

INSERT INTO block (block_code) VALUES ('header');
INSERT INTO block (block_code) VALUES ('footer');

INSERT INTO block_i18n (block_code, lang, block) VALUES ('header', 'EN',
'
<h1><center>
<a href="home">Home</a>
<a href="about">About</a>
</center></h1>
');

INSERT INTO block_i18n (block_code, lang, block) VALUES ('footer', 'EN',
'
<h1><center>
<a href="copyright">Copyright</a>
<a href="privacy">Privacy</a>
</center></h1>
');
