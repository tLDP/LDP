DELETE FROM block_i18n;
DELETE FROM block;

INSERT INTO block (block_code) VALUES ('header');
INSERT INTO block (block_code) VALUES ('footer');

INSERT INTO block_i18n (block_code, lang, block) VALUES ('header', 'EN',
'
<center>
<a href="home">Home</a>
<a href="about">About</a>
</center>
');

INSERT INTO block_i18n (block_code, lang, block) VALUES ('footer', 'EN',
'
<center>
<a href="copyright">Copyright</a>
<a href="privacy">Privacy</a>
</center>
');
