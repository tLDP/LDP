DELETE FROM page_i18n;
DELETE FROM page;

INSERT INTO page (page_code, template_code) VALUES ('test',		'default');
INSERT INTO page (page_code, template_code) VALUES ('home',		'default');
INSERT INTO page (page_code, template_code) VALUES ('lampadas',		'default');
INSERT INTO page (page_code, template_code) VALUES ('copyright',	'default');
INSERT INTO page (page_code, template_code) VALUES ('contribute',	'default');
INSERT INTO page (page_code, template_code) VALUES ('privacy',		'default');
INSERT INTO page (page_code, template_code) VALUES ('about',		'default');
INSERT INTO page (page_code, template_code) VALUES ('doctable',		'default');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('test', 'EN', 'Test Page',
'Test Page');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('test', 'FR', 'Le Test Page',
'Test Page');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('home', 'EN', 'Lampadas',
'
<h2>Welcome to the Lampadas System.</h2>

<p>This is a development system. The code is being edited constantly,
so the site breaks from time to time.

<p>Please do not send me bug reports at this time.
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('home', 'FR', 'Le Lampadas',
'
Le Lampadas
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('lampadas', 'EN', 'About Lampadas',
'
<p>Lampadas is an interactive environment for writing, managing, publishing and reading documentation.

<p>As a Lampadas member, you are part of a collaborative community which includes authors, editors, technical experts, and readers all working together to document the Linux system, and to share information with each other.

<p>See "How to Help".

<h2>Why Lampadas?</h2>

<p>Fans of Frank Herbert''s Dune series will recognize Lampadas as the name of the Bene Gesserit teaching planet, which plays a role in the final book, Chapterhouse: Dune. Before the planet can be destroyed by hordes of Honored Matres, Reverend Mother Lucia orders the planet to share Other Memory, two by two then four by four, until all the students hold within them the composite knowledge and memories of the entire planet. After the planet is annihilated by the Honored Matres, the precious knowledge is carried back to the Bene Gesserit Chapterhouse by the lone holder of the precious cargo, Rebecca.

<p>Herbert apparently took the name from the city of Lampadas, which was an ancient seat of learning and scholarship. Also, the word lampadas is the accusative form of the word "Torch" in ancient Greek.

<p>In all of these senses, Lampadas seems an appropriate name for this project, which is created to facilitate sharing information from many people and many sources, and disseminating it widely to others.
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('lampadas', 'FR', 'Le About Lampadas',
'
Le About Lampadas
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
Le Copyright
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

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('contribute', 'FR', 'Le Contributing to Lampadas',
'
Le Contributing
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('privacy', 'EN', 'Privacy Policy',
'
Replace this text with your official privacy policy.
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('privacy', 'FR', 'Le Privacy Policy',
'
Le Privacy Policy
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('about', 'EN', 'About |project|',
'
Replace this text with information about your project.
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('about', 'FR', 'Le About |project|',
'
Le About Project
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('doctable', 'EN', 'DocTable',
'
|tabdoctable|
');

INSERT INTO page_i18n (page_code, lang, title, page) VALUES ('doctable', 'FR', 'Le DocTable',
'
Le DocTable goes here...
');

