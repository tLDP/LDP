m4_dnl  These are the pages that are served by the CMS.
m4_dnl  The last field is the version number. Please bump it
m4_dnl  by one if you're the primary author, and synchronize
m4_dnl  it in translations when the translation is up to date.

insert([index], [|strproject|], [Splash Page],
[
    |tabsplashlanguages|
], 1)

insert([adddocument], [Add Document], [],
[
    |tabeditdoc|
], 1)

insert([users], [User List], [],
[
    |tabletters|
    |tabusers|
], 1)

insert([sessions], [User Sessions], [],
[
    |tabsessions|
], 1)

insert([my], [My Home], [],
[
    <p>This is your personal home page.</p>

    <p>This table lists documents you have volunteered to contribute to:</p>

    <p>|session_user_docs|</p>
], 1)

insert([home], [|strprojectshort| Home Page], [Home], 
[
    <p>Welcome to |strproject|.</p>

    <p>This site is based on a development version of the
    Lampadas Document Management System from
    <a href="http://www.tldp.org">The Linux Documentation Project</a></p>

    <p>This is <i><b>alpha quality</b></i> code, updated from the cvs tree
    very frequently, whenever there are significant features or
    bugfixes available.
    This happens at least once a day and sometimes
    several times a day.
    The system is fairly stable, although some half-
    implemented features will cause ugly error dumps.</p>
    
    <p>This demo site is populated with data from the LDPDB.
    If you had an account on the LDPDB, you have one here.
    However, because passwords on the LDPDB are stored only in
    hashed form, I was unable to port them over, and you\'ve been
    given a new password. To get it, click the "Mail Password"
    link and your new password will be mailed to your address
    of record.</p>

    <p>There are also a set of additional test users.
    Log in as one of them to see the site through their eyes.
    The pages change depending on your access level.
    These users\'passwords are "password".</p>

    <ul>
        <li>sysadmin - the SUPERUSER, who manages the system.</li>
        <li>admin - the Site Administrator, who manages the content.</li>
        <li>french - a French-speaking user.</li>
        <li>german - a German-speaking user.</li>
        <li>korean - a Korean-speaking user.</li>
    </ul>

    <p>We greatly appreciate your comments, bug reports or questions.
    You can reach David Merrill at
    <a href="mailto:david@lupercalia.net">david@lupercalia.net</a>.
    If you want to help build Lampadas, it is a really fun and exciting
    project.
    You can find out more about it by reading the
    <a href="http://www.lupercalia.net/lampadas/">Lampadas Developer\'s
    Guide</a>.</p>
], 1)

insert([doctable], [Browse Documents], [],
[
    |tabdocs|
], 1)

insert([document_list], [Document List], [],
[
    |tabdocs_block|
], 1)    

insert([search], [Search], [],
[
    |tabsearch|
], 1)

insert([news], [Latest News], [],
[
    |tabrecentnews|
], 1)

insert([staff], [Staff], [],
[
    List the members of your project\'s staff here.
], 1)

insert([contribute], [Contributing to |strproject|], [Contributing to |strprojectshort|],
[
    <p>As a member of this Lampadas community, you can collaborate with
    hundreds or even thousands of others to produce documentation,
    which can then be shared with others all around the world over the
    Web.
    
    <p>We\'ve designed the Lampadas system to make contributing simple and easy.
    Here are some ways you can help, roughly in order of difficulty or
    commitment required:

    <ul>
    <li>Rate Documents

    <p>Each document has a "rating", on a scale of 1 to 10, which tells you
    what other readers think of it.
    We use this rating to improve our documents, for focusing our attention
    on the documents you\'ve identified as neednig improvement.
    </li>

    <li>Report a Bug

    <p>If you find an error in any document, file a bug report.
    </li>
    
    <li>Translate a Document

    <p>Translators are always in short supply, and we value them very much.
    Our goal is to provide all of our documentation in as many languages
    as possible, allowing people all over the world to take advantage of it.
    </li>

    <li>Write a Document

    <p>If you are a good writer with solid technical knowledge,
    write a new document and contribute it to the collection.
    Lampadas has several tools that will help you.
    </li>
    
    <li>Help Lampadas

    <p>If you have programming or translating skills, you can help to develop
    the platform upon which this site is based.

    <p>The Lampadas System itself can be localized to display in several
    languages. Translators are needed to translate it into additional
    languages.
    </li>
    </ul>
], 1)

insert([unmaintained], [Unmaintained Documents], [],
[
    <p>If you wish to become the maintainer for one of these unmaintained
    documents, please follow these steps:

    <ul>
        <li>Contact the original author. If not listed, consult the document.
        Make sure the author no longer wishes to maintain the document in question.

        <li>Determine if a more up-to-date copy of the document exists, outside
        of what is available here. The best way to do this is through the
        former maintainer. If you can, secure a copy of the most recent
        version and submit it here.

        <li>Inform the site administrator that you would like to maintain the
        document. The administrator will assign you the necessary rights so
        you can begin maintaining it.

        <li>Update the document, adding yourself as the current maintainer.
        Be sure that you continue to credit all former maintainers.
    </ul>

    <p>It is possible that a document could be listed here erroneously.
    If you find an error, please notify the site administrator right away
    so we can correct the problem.
    
    <p>|tabunmaintained|
], 1)

insert([maint_wanted], [New Maintainer Wanted], [],
[
    |tabmaint_wanted|
], 1)

insert([pending], [Pending Documents], [],
[
    |tabpending|
], 1)

insert([wishlist], [Wishlist Documents], [],
[
    |tabwishlist|
], 1)

insert([resources], [Other Resources], [],
[
    <ul>
        <li><a href="http://www.dictionary.com">Dictionary.com</a>, an online dictionary.
        <li><a href="http://www.thesaurus.com">Thesaurus.com</a>, an online thesaurus.
        <li><a href="http://www.webopedia.com">Webopedia.com</a>, an online dictionary
            and search engine for computer and internet technology.
    </ul>
], 1)

insert([maillists], [Mailing Lists], [],
[
    List your project\'s mailing lists here.
], 1)

insert([about], [About |strproject|], [About |strprojectshort|],
[
    Replace this text with information about your project.
], 1)

m4_dnl There is a alt.fan.dune_Frequently_Asked_Questions_(FAQ)
m4_dnl It provides some hints on translated version - at least it
m4_dnl tells title and publisher of the books.
m4_dnl
m4_dnl http://ftp.kreonet.re.kr/pub/docs/usenet-by-hierarchy/alt/fan/dune/
m4_dnl
insert([lampadas], [About Lampadas], [],
[
    <p>This website is based on version |version| of the Lampadas
    Documentation Management System,
    a Free Software (GPL) platform developed by
    <a href="http://www.tldp.org">The Linux Documentation Project</a>.
    
    <p>Lampadas is a powerful, flexible platform designed to support
    large documentation projects such as the LDP.
    It provides an interactive environment for writing, managing,
    publishing and reading documentation.

    <p>Lampadas creates a collaborative community which
    includes authors, editors, technical experts, and readers all working
    together to produce documentation, and to share information with
    each other.

    <h1>Why Lampadas?</h1>

    <p>Fans of Frank Herbert\'s Dune series will recognize Lampadas
    as the name of the Bene Gesserit teaching planet, which plays a
    role in the final book,
    Chapterhouse: Dune.
    Before the planet can be destroyed by hordes of Honored Matres,
    Reverend Mother Lucilla orders the planet to share Other Memory,
    two by two then four by four, until all the students hold within
    them the composite knowledge and memories of the entire planet.
    After the planet is annihilated by the Honored Matres, the precious
    knowledge is carried back to the Bene Gesserit Chapterhouse by the
    lone holder of the precious cargo, Rebecca.

    <p>Herbert apparently took the name from the city of Lampadas,
    which was an ancient seat of learning and scholarship.
    Also, the word lampadas is the accusative form of the word
    "Torch" in ancient Greek.

    <p>In all of these senses, Lampadas seems an appropriate name for
    this project, which is created to facilitate sharing information
    from many people and many sources, and disseminating it widely to others.
], 1)

insert([copyright], [Copyright Statment], [],
[
    <p>Lampadas is Copyright 2000, 2001, 2002 by David C. Merrill.

    <p>Individual documents are copyrighted by their authors,
    and comments are owned by the poster.

    <p>We disclaim any responsibility for contents which are posted by
    users of the site.
    In using the site, you might be exposed to profanity, pornography,
    or anything else.
    Anything of this nature which is reported to us, or anything which
    you can demonstrate to be posted here in violation of copyright law,
    will be removed promptly upon request.

    <p>Lampadas is made available under the terms of the GNU General Public
    License (GPL). A copy is available online at
    <a href="http://www.gnu.org/licenses/gpl.html"
      >www.gnu.org/licenses/gpl.html</a>.

    <p>We do our best to provide accurate information, but we do not provide
    any warranty or guarantees as to accuracy, completeness, or anything else.
    In fact, we make no warranty or guarantee of anything at all.

    <p>Use of information, downloads, software, and any other resource on this
    website is <i>entirely at your own risk</i>.
    We recommend you back up your system on a regular basis, and immediately
    before making nontrivial changes to it.

    <p>Linux is a trademark of Linus Torvalds. TLDP is a trademark of
    <a href="http://www.tldp.org">The Linux Documentation Project</a>.
    All other trademarks are the trademarks of their respective owners.

    <p>Unless you expressly state otherwise, by writing a comment,
    a bug report or a document annotation or other reader feedback you
    agree to release it into the Public Domain.
    This is so authors are free to integrate your comments into their
    documentation regardless of the document\'s license.
], 1)

insert([privacy], [Privacy Policy], [],
[
    <p>We are committed to helping you maintain your privacy while online.
    You can use this site without divulging any personal information.
    
    <p>However, due to the nature of the system, some features require
    registration.
    To register, you must provide your email address.
    We require an email address to prevent certain types of Denial of
    Service (DoS) attacks. All other information is completely optional.
    
    <p>Your information is used only in the operation of this website.
    No personal information about you will ever be disclosed to any third
    party.
    
    <p>We will not spam you or add you to any mailing lists without
    your consent.
], 1)

insert([sitemap], [Site Map], [],
[
    |tabsitemap|
], 1)

insert([newuser], [New User], [],
[
    <p>To create a new user account, fill out this form.
    <p>
    <form name="newuser" action="data/save/newaccount" method=GET>
        <table class="box">
            <tr>
                <td class="label">*Username</td>
                <td><input type=text name=username size=20></input></td>
            </tr>
            <tr>
                <td class="label">*Enter your email address.<br>
		  Your password will be mailed to this address,
		  so it must be valid.</td>
                <td><input type=text name=email size=20></input></td>
            </tr>
            <tr>
                <td class="label">First Name</td>
                <td><input type=text name=first_name size=20></input></td>
            </tr>
            <tr>
                <td class="label">Middle Name</td>
                <td><input type=text name=middle_name size=20></input></td>
            </tr>
            <tr>
                <td class="label">Surname</td>
                <td><input type=text name=surname size=20></input></td>
            </tr>
            <tr>
                <td colspan=2 align=center><input type=submit
		  value="Create Account!"></td>
            </tr>
        </table
    </form>
    <p>*Required Fields
], 1)

insert([mailpass], [Mail Password], [],
[
    <p>Please enter your email address to have your
    password mailed to you.

    <p>|tabmailpass|
], 1)

insert([topic], [View Topic], [],
[
    |tabtopics|
    <p>|tabtopicdocs|
], 1)

insert([document], [|doc.title|], [],
[
    |blkdocument_tabs|
    |tabeditdoc|
    <p>|tabdocerrors|
    <p>|tabdocfiles|
    <p>|tabdocfileerrors|
    <p>|tabdocusers|
    <p>|tabdocversions|
    <p>|tabdoctopics|
    <p>|tabdocnotes|
    <p>|tabdoctranslations|
], 2)

insert([document_main], [|doc.title|], [],
[
    |blkdocument_tabs|
    |tabeditdoc|
    <p>|tabdocerrors|
])

insert([document_files], [|doc.title|], [],
[
    |blkdocument_tabs|
    |tabdocfiles|
    <p>|tabdocfileerrors|
])

insert([document_users], [|doc.title|], [],
[
    |blkdocument_tabs|
    |tabdocusers|
])

insert([document_revs], [|doc.title|], [],
[
    |blkdocument_tabs|
    |tabdocversions|
])

insert([document_topics], [|doc.title|], [],
[
    |blkdocument_tabs|
    |tabdoctopics|
])

insert([document_notes], [|doc.title|], [],
[
    |blkdocument_tabs|
    |tabdocnotes|
])

insert([document_translation], [|doc.title|], [],
[
    |blkdocument_tabs|
    |tabdoctranslations|
])

insert([404], [Error 404, Page Not Found], Error,
[
    <p>I\'m sorry, but the page you requested does not exist.
    If you came here from another website, please notify the webmaster
    of that site that their link is incorrect or out of date.

    <p>If you came here from another page on this Lampadas system,
    you have probably found a bug.
    If you believe that to be the case, please file a bug report for
    the Lampadas developers.
], 1)

insert([user_exists], [User Exists], [],
[
    <p>That username is already taken. Please select another username and try again.
], 1)

insert([username_required], [Username Required] [],
[
    <p>Username is a required field. Please enter a username and try again.
], 1)

insert([email_exists], [Email Exists], [],
[
    <p>That email address is already in the database.
    If you already have an account but have forgotten your password,
    you can have it <a href="mailpass">mailed</a> to you.
], 1)

insert([account_created], [Account Created], [],
[
    <p>Your account has been created, and your password has been mailed to you.
    Please check your email.
], 1)

insert([password_mailed], [Password Mailed], [],
[
    <p>Your password has been mailed to you.
    If you continue to have problems logging in, please write
    the site administrator for assistance.
], 1)

insert([user], [|user.username| - |user.name|], [],
[
    |tabuser|
    <p>|user.docs|
], 1)

insert([adduser], [Add User], [Add User],
[
    |tabuser|
], 1)

insert([logged_in], [Logged In], [],
[
    <p>You have been logged into the system.
], 1)

insert([logged_out], [Logged Out], [],
[
    <p>You have been logged out of the system.
], 1)

insert([type], [|type.name|], [],
[
    |tabtypedocs|
], 1)

insert([sourcefile], [Source File], [],
[
    |tabfile_reports|
], 3)

insert([file_report], [File Report], [],
[
    |tabfile_report|
], 2)

insert([errors], [Error List], [],
[
    |taberrors|
], 1)
