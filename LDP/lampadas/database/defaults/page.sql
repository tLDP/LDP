DELETE FROM page_i18n;
DELETE FROM page;

INSERT INTO page (page_code, section_code, template_code) VALUES ('test',	'test',		'default');
INSERT INTO page (page_code, section_code, template_code) VALUES ('404',	NULL,		'default');
INSERT INTO page (page_code, section_code, template_code) VALUES ('home',	'main',		'default');
INSERT INTO page (page_code, section_code, template_code) VALUES ('lampadas',	NULL,		'default');
INSERT INTO page (page_code, section_code, template_code) VALUES ('copyright',	NULL,		'default');
INSERT INTO page (page_code, section_code, template_code) VALUES ('contribute',	'main',		'default');
INSERT INTO page (page_code, section_code, template_code) VALUES ('privacy',	NULL,		'default');
INSERT INTO page (page_code, section_code, template_code) VALUES ('about',	NULL,		'default');
INSERT INTO page (page_code, section_code, template_code) VALUES ('doctable',	NULL,		'default');
INSERT INTO page (page_code, section_code, template_code) VALUES ('editdoc',	NULL,		'default');


INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('test', 'EN', 'Test Page',
'Test Page');
INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('test', 'FR', 'Page de Test',
'Page de Test');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('404', 'EN', 'Not Found',
'Not Found');
INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('404', 'FR', 'Introuvable',
'Introuvable');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('home', 'EN', 'Lampadas',
'
<p>This is a development system. The code is being edited constantly,
so the site breaks from time to time.

<p>Please do not send me bug reports at this time.
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('home', 'FR', 'Le Lampadas',
'
<p>Ce syst&egrave;me est en cours de d&eacute;veloppement. Son code est modifi&eacute; en permanence ce qui le rend instable.

<p>Merci de ne pas envoyer de rapport de bogue pour le moment
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('lampadas', 'EN', 'About Lampadas',
'
<p>Lampadas is an interactive environment for writing, managing, publishing and reading documentation.

<p>As a Lampadas member, you are part of a collaborative community which includes authors, editors, technical experts, and readers all working together to document the Linux system, and to share information with each other.

<p>See <a href="contribute">Contributing to Lampadas</a>.

<h2>Why Lampadas?</h2>

<p>Fans of Frank Herbert''s Dune series will recognize Lampadas as the name of the Bene Gesserit teaching planet, which plays a role in the final book, Chapterhouse: Dune. Before the planet can be destroyed by hordes of Honored Matres, Reverend Mother Lucia orders the planet to share Other Memory, two by two then four by four, until all the students hold within them the composite knowledge and memories of the entire planet. After the planet is annihilated by the Honored Matres, the precious knowledge is carried back to the Bene Gesserit Chapterhouse by the lone holder of the precious cargo, Rebecca.

<p>Herbert apparently took the name from the city of Lampadas, which was an ancient seat of learning and scholarship. Also, the word lampadas is the accusative form of the word "Torch" in ancient Greek.

<p>In all of these senses, Lampadas seems an appropriate name for this project, which is created to facilitate sharing information from many people and many sources, and disseminating it widely to others.
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('lampadas', 'FR', 'A propos de Lampadas',
'
<p>Lampadas est un syst&egrave;me de r&eacute;daction, gestion, publication et lecture de documentaion.

<p>Une fois enregistr&eacute; dans Lampadas, vous devenez membre d''une communaut&eacute; incluant auteurs, &eacute;diteurs, experts techniques et lecteurs, qui collaborent et partagent des informations.


<p>See <a href="contribute">Contribuer &agrave; Lampadas</a>.

<p>...
');


INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('copyright', 'EN', 'Copyright',
'Lampadas is Copyright 2000, 2001, 2002 by David C. Merrill. Individual documents are copyrighted by their authors, and comments are owned by the poster.

<p>We disclaim any responsibility for contents which are posted by users of the site. In using the site, you might be exposed to profanity, pornography, or anything else. Anything of this nature which is reported to us, or anything which you can demonstrate to be posted here in violation of copyright law, will be removed promptly upon request.

<p>Lampadas is made available under the terms of the GNU General Public License (GPL). A copy is available online at <a href="http://www.gnu.org/licenses/gpl.html">www.gnu.org/licenses/gpl.html</a>.

<p>We do our best to provide accurate information, but we do not provide any warranty or guarantees as to accuracy, completeness, or anything else. In fact, we make no warranty or guarantee of anything at all.

<p>Use of information, downloads, software, and any other resource on this website is <i>entirely at your own risk</i>. We recommend you back up your system on a regular basis, and immediately before making nontrivial changes to it.

<p>Linux is a trademark of Linus Torvalds. TLDP is a trademark of The Linux Documentation Project. All other trademarks are the trademarks of their respective owners.

<p>Unless you expressly state otherwise, by writing a comment, a bug report or a document annotation or other reader feedback you agree to release it into the Public Domain. This is so authors are free to integrate your comments into their documentation regardless of the document''s license.
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('copyright', 'FR', 'Le Copyright',
'
Copyright 2002 David Merrill.
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('contribute', 'EN', 'Contributing to Lampadas',
'
As a member of this Lampadas System, you benefit from the work of hundreds of Linux users who have given freely of their time and knowledge to create the enormous LDP document collection. We''re sure that you would like to give a little back in return, and help make us even better.

We''ve designed the Lampadas system to make giving back simple and easy. Here are some ways you can help, roughly in order of difficulty or commitment required:

<ul>
<li>Rate Documents

<p>Each document has a "rating", on a scale of 1 to 10, which tells you what other readers think of it. We use this rating to improve our documents, for focusing our attention on the documents you''ve identified as neednig improvement.</li>

<li>Report a Bug

<p>If you find an error in any document, file a bug report.
</li>

<li>Translate a Document

<p>Translators are always in short supply, and we value them very much. Our goal is to provide all of our documentation in as many languages as possible, allowing people all over the world to take advantage of it.
</li>

<li>Translate Lampadas

<p>The Lampadas System itself can be localized to display in several languages. Translators are needed to translate it into additional languages. It is currently available in:

<ul>
<li>English</li>
</ul>
</li>

<li>Write a Document

<p>If you are a good writer with solid technical knowledge, write a new document and contribute it to the collection. Lampadas has several tools that will help you.</li>
</ul>
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('contribute', 'FR', 'Contribuer &agrave; Lampadas',
'
En tant que membre de ce syst&egrave;me, vous b&eacute;n&eacute;ficiez du travail de plusieurs centaines d''utilisateurs de Linux, qui ont b&eacute;n&eacute;volement contribu&eacute; &agrave; cr&eacute;er cette &eacute;norme biblioth&egrave;que &eacute;lectronique.

Nous sommes s&ucric;rs que vous souhaiteriez apporter votre pierre &agrave; l''&eacute;difice aussi avons-nous con&ccedil;u Lampadas pour que vous puissiez ais&eacute;ment participer. Voici plusieurs fa&ccedil;ons d''aider, class&eacute;es par ordre de difficult&eacute;:

<ul>
<li>Noter les documents

<p>Chaque document est not&eacute;, sur une &eacute;chelle de 1 &agrave; 10, qui vous informe de l''opinion qu''en ont eu les autres lecteurs. Cette note nous permet de concentrer nos efforts sur l''am&eacute;lioration des documents dont vous nous dites qu''ils en ont le plus besoin.</li>

<li>Signaler une erreur

<p>Si vous trouvez une erreur dans un document, signalez-l&agrave;.

</li>

<li>Traduire un document

<p>Les traducteurs sont toujours tr&egrave;s recherch&eacute;s, car notre but est d''offrir notre documentation dans le plus grand nombre de langues possibles pour que tous puissent en profiter.
</li>

<li>Tranduire Lampadas

<p>Le syst&egrave;me Lampadas peut &ecirc;tre localis&eacute; pour que chacun puisse l''utiliser dans sa langue de pr&eacute;dilection. Il est actuellement disponible en:

<ul>
<li>Anglais</li>
<li>Fran&ccedil;ais</li>
</ul>
</li>

<li>Ecrire un document

<p>Si vous avez une comp&eacute;tence particuli&egrave;re, n''h&eacute;sitez pas &agrave; &eacute;crire un nouveau document pour que nous le publions. Lampadas propose plusieurs outils pour vous faciliter cette tâche.
</li>

</ul>
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('privacy', 'EN', 'Privacy Policy',
'
Replace this text with your official privacy policy.
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('privacy', 'FR', 'Confidentialit&eacute;',
'
Confidentialit&eacute;
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('about', 'EN', 'About |project|',
'
Replace this text with information about your project.
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('about', 'FR', 'A propos de |project|',
'
Remplacez ce texte par la description de votre projet
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('doctable', 'EN', 'DocTable',
'
|tabdocstable|
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('doctable', 'FR', 'Table des docs',
'
|tabdocstable|
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('editdoc', 'EN', 'Document Meta-data',
'
|tabeditdoc|
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('editdoc', 'FR', 'M&eacute;ta-donn&eacute;es du doc',
'
|tabeditdoc|
');















INSERT INTO page (page_code, section_code, template_code) VALUES ('downloads',	'misc',		'default');


INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('downloads', 'EN', 'Downloads',
'
<p>
Along with the many HOWTOs, Guides and other documents published by the
LDP, we also develop tools and utilities for working with documentation.
These tools are all available under the GPL.
</p>

<hr>

<p>
<strong>db2omf</strong>
</p>
<p>
Db2omf is a conversion utility that reads a DocBook file (either XML or SGML),
and writes out an <a href="http://www.ibiblio.org/osrt/omf/">OMF</a> file.
The OMF file is suitable for submission to a
<a href="http://scrollkeeper.sourceforge.net">ScrollKeeper</a> database.
</p>

<ul>
<p>
<li><a href="db2omf-0.4.tar.gz">Version 0.4</a> (tarred and gzipped package, 11k)</li>
<li><a href="db2omf-0.5.tar.gz">Version 0.5</a> (tarred and gzipped package, 11k)</li>
</ul>

<p>
<strong>texi2db</strong>
</p>
<p>
Texi2db is a conversion utility that converts
<a href="http://www.texinfo.org">GNU Texinfo</a> source files
into DocBook XML.
</p>
<ul>

<p>
<li><a href="texi2db-0.3.tar.gz">Version 0.3</a> (tarred and gzipped package, 23k)</li>
<li><a href="texi2db-0.4.tar.gz">Version 0.4</a> (tarred and gzipped package, 24k)</li>
<li><a href="texi2db-0.4.1.tar.gz">Version 0.4.1</a> (tarred and gzipped package, 24k)</li>

</ul>

<p>
<strong>wt2db</strong>
</p>
<p>
Wt2db is a conversion utility that converts
<a href="http://www.tldp.org/HOWTO/WikiText-HOWTO/index.html">WikiText</a>
source files into DocBook XML/SGML.
</p>

<ul>
<p>
<li><a href="wt2db-0.3.tar.gz">Version 0.3</a> (tarred and gzipped package, 12k)</li>
</ul>
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('downloads', 'FR', 'T&eacute;l&eacute;chargement',
'
<p>
En plus des HOWTOs, Guides et autres documents que nous publions, nous d&eacute;veloppons des outils pour ceux qui produisent de la documentaion. Ces programmes sont disponibles sous licence GPL.
</p>

<hr>

<p>
<strong>db2omf</strong>
</p>
<p>
Db2omf lit un fichier DocBook (XML ou SGML),
et produit un fichier <a href="http://www.ibiblio.org/osrt/omf/">OMF</a> qui peut 
&ecirc;tre ajout&eacute; &agrave; une base
<a href="http://scrollkeeper.sourceforge.net">ScrollKeeper</a>.
</p>

<ul>
<p>
<li><a href="db2omf-0.4.tar.gz">Version 0.4</a> (archive tar.gz, 11k)</li>
<li><a href="db2omf-0.5.tar.gz">Version 0.5</a> (archive tar.gz, 11k)</li>
</ul>

<p>
<strong>texi2db</strong>
</p>
<p>
Texi2db convertit un fichier
<a href="http://www.texinfo.org">GNU Texinfo</a> en un fichier DocBook XML.
</p>
<ul>

<p>
<li><a href="texi2db-0.3.tar.gz">Version 0.3</a> (archive tar.gz, 23k)</li>
<li><a href="texi2db-0.4.tar.gz">Version 0.4</a> (archive tar.gz, 24k)</li>
<li><a href="texi2db-0.4.1.tar.gz">Version 0.4.1</a> (archive tar.gz, 24k)</li>

</ul>

<p>
<strong>wt2db</strong>
</p>
<p>
Wt2db convertit un fichier
<a href="http://www.tldp.org/HOWTO/WikiText-HOWTO/index.html">WikiText</a>
en un fichier DocBook XML/SGML.
</p>

<ul>
<p>
<li><a href="wt2db-0.3.tar.gz">Version 0.3</a> (archive tar.gz, 12k)</li>
</ul>
');
