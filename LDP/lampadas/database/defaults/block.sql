DELETE FROM block_i18n;
DELETE FROM block;

INSERT INTO block (block_code) VALUES ('header');
INSERT INTO block (block_code) VALUES ('footer');

INSERT INTO block_i18n (block_code, lang, block) VALUES ('header', 'EN',
'
<table class="header" style="width:100%">
<tr><th>|project| Lampadas System</th></tr>
</table>

<table class="title">
<tr><td><h1>|title|</h1></td></tr>
</table>
');

INSERT INTO block_i18n (block_code, lang, block) VALUES ('header', 'FR',
'
<table class="header" style="width:100%">
<tr><th>|project| Syst&egrave;me Lampadas</th></tr>
</table>

<table class="title">
<tr><td><h1>|title|</h1></td></tr>
</table>
');

INSERT INTO block_i18n (block_code, lang, block) VALUES ('footer', 'EN',
'
<table class="footer" style="width:100%">
<tr><td>
<center>
<a href="copyright">Copyright</a> \\|
<a href="privacy">Privacy</a> \\|
<a href="lampadas">About Lampadas</a>
<p>
<a href="/EN/|page|">English</a> \\|
<a href="/FR/|page|">French</a>
</center>
</td></tr>
</table>
');

INSERT INTO block_i18n (block_code, lang, block) VALUES ('footer', 'FR',
'
<table class="footer" style="width:100%">
<tr><td>
<center>
<a href="copyright">Copyright</a> \\|
<a href="privacy">Confidentialit&eacute;</a> \\|
<a href="lampadas">A propos de Lampadas</a>
<p>
<a href="/EN/|page|">Anglais</a> \\|
<a href="/FR/|page|">Fran&ccedil;ais</a>
</center>
</td></tr>
</table>
');
