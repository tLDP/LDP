insert([test], [Test Page],
[
Test Page
])

insert([404], [Not Found],
[
    Not Found
])

insert([home], [Lampadas], 
[
    <p>This is a development system. The code is being edited constantly,
    so the site breaks from time to time.

    <p>Please do not send me bug reports at this time.
])

insert([lampadas], [About Lampadas],
[
    <p>Lampadas is an interactive environment for writing, managing, publishing and reading documentation.

    <p>As a Lampadas member, you are part of a collaborative community which includes authors, editors, technical experts, and readers all working together to document the Linux system, and to share information with each other.

    <p>See <a href="contribute">Contributing to Lampadas</a>.

    <h2>Why Lampadas?</h2>

    <p>Fans of Frank Herbert's Dune series will recognize Lampadas as the name of the Bene Gesserit teaching planet, which plays a role in the final book, Chapterhouse: Dune. Before the planet can be destroyed by hordes of Honored Matres, Reverend Mother Lucia orders the planet to share Other Memory, two by two then four by four, until all the students hold within them the composite knowledge and memories of the entire planet. After the planet is annihilated by the Honored Matres, the precious knowledge is carried back to the Bene Gesserit Chapterhouse by the lone holder of the precious cargo, Rebecca.

    <p>Herbert apparently took the name from the city of Lampadas, which was an ancient seat of learning and scholarship. Also, the word lampadas is the accusative form of the word "Torch" in ancient Greek.

    <p>In all of these senses, Lampadas seems an appropriate name for this project, which is created to facilitate sharing information from many people and many sources, and disseminating it widely to others.
])

insert([copyright], [Copyright],
[
    Lampadas is Copyright 2000, 2001, 2002 by David C. Merrill. Individual documents are copyrighted by their authors, and comments are owned by the poster.

    <p>We disclaim any responsibility for contents which are posted by users of the site. In using the site, you might be exposed to profanity, pornography, or anything else. Anything of this nature which is reported to us, or anything which you can demonstrate to be posted here in violation of copyright law, will be removed promptly upon request.

    <p>Lampadas is made available under the terms of the GNU General Public License (GPL). A copy is available online at <a href="http://www.gnu.org/licenses/gpl.html">www.gnu.org/licenses/gpl.html</a>.

    <p>We do our best to provide accurate information, but we do not provide any warranty or guarantees as to accuracy, completeness, or anything else. In fact, we make no warranty or guarantee of anything at all.

    <p>Use of information, downloads, software, and any other resource on this website is <i>entirely at your own risk</i>. We recommend you back up your system on a regular basis, and immediately before making nontrivial changes to it.

    <p>Linux is a trademark of Linus Torvalds. TLDP is a trademark of The Linux Documentation Project. All other trademarks are the trademarks of their respective owners.

    <p>Unless you expressly state otherwise, by writing a comment, a bug report or a document annotation or other reader feedback you agree to release it into the Public Domain. This is so authors are free to integrate your comments into their documentation regardless of the document's license.
])

insert([contribute], [Contributing to Lampadas],
[
    As a member of this Lampadas System, you benefit from the work of hundreds of Linux users who have given freely of their time and knowledge to create the enormous LDP document collection. We're sure that you would like to give a little back in return, and help make us even better.
    We've designed the Lampadas system to make giving back simple and easy. Here are some ways you can help, roughly in order of difficulty or commitment required:

    <ul>
    <li>Rate Documents

    <p>Each document has a "rating", on a scale of 1 to 10, which tells you what other readers think of it. We use this rating to improve our documents, for focusing our attention on the documents you've identified as neednig improvement.</li>

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
])

insert([privacy], [Privacy Policy],
[
    Replace this text with your official privacy policy.
])

insert([about], [About |project|],
[
    Replace this text with information about your project.
])

insert([doctable], [DocTable],
[
    |tabdocstable|
])

insert([editdoc], [Document Meta-data],
[
    |tabeditdoc|
])

insert([downloads], [Downloads],
[
    <p>Along with the many HOWTOs, Guides and other documents published by the
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
])
