insert([newdocument], [Add Document], [],
[
    |tabeditdoc|
])

insert([admin], [Admin Page], [],
[
    <p>Admin tools.
])

insert([users], [User List], [],
[
    |tabusers|
])

insert([sysadmin], [Sysadmin Page], [],
[
    <p>Sysadmin tools.
])

insert([my], [My Home], [],
[
    <p>This is your personal home page.

    <p>This table lists documents you have volunteered to contribute to:

    |session_user_docs|
])

insert([home], [|strproject|], [Home], 
[
    <p>Welcome to |strproject|.

    <p>This site is based on a development version of the
    Lampadas Document Management System from
    <a href="http://www.tldp.org">The Linux Documentation Project</a>
])

insert([doctable], [DocTable], [],
[
    |tabdocs|
])

insert([news], [Latest News], [],
[
    |tabrecentnews|
])

insert([staff], [Staff], [],
[
    List the members of your project\'s staff here.
])

insert([contribute], [Contributing to |strproject|], [Contributing to |strprojectshort|],
[
    As a member of this Lampadas community, you can collaborate with
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
    languages. It is currently available in:

    <ul>
    <li>English</li>
    <li>French</li>
    <li>German</li>
    </ul>
    </li>

    </ul>
])

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
    
    |tabunmaintained|
])

insert([maint_wanted], [New Maintainer Wanted], [],
[
    |tabmaint_wanted|
])

insert([pending], [Pending Documents], [],
[
    |tabpending|
])

insert([wishlist], [Wishlist Documents], [],
[
    |tabwishlist|
])

insert([resources], [Other Resources], [],
[
    <ul>
        <li><a href="http://www.dictionary.com">Dictionary.com</a>, an online dictionary.
        <li><a href="http://www.thesaurus.com">Thesaurus.com</a>, an online thesaurus.
        <li><a href="http://www.webopedia.com">Webopedia.com</a>, an online dictionary
            and search engine for computer and internet technology.
    </ul>
])

insert([maillists], [Mailing Lists], [],
[
    List your project\'s mailing lists here.
])

insert([about], [About |strproject|], [About |strprojectshort|],
[
    Replace this text with information about your project.
])

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
    Reverend Mother Lucia orders the planet to share Other Memory,
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
])

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
])

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
])

insert([sitemap], [Site Map], [],
[
    |tabsitemap|
])

insert([newuser], [New User], [],
[
    <p>To create a new user account, fill out this form.
    <p>
    <form name="newuser" action="data/save/newuser" method=GET>
        <table class="form">
            <tr>
                <td align=right>*Username</td>
                <td><input type=text name=username size=20></input></td>
            </tr>
            <tr>
                <td align=right>*Enter your email address.<br>
		  Your password will be mailed to this address,
		  so it must be valid.</td>
                <td><input type=text name=email size=20></input></td>
            </tr>
            <tr>
                <td align=right>First Name</td>
                <td><input type=text name=first_name size=20></input></td>
            </tr>
            <tr>
                <td align=right>Middle Name</td>
                <td><input type=text name=middle_name size=20></input></td>
            </tr>
            <tr>
                <td align=right>Surname</td>
                <td><input type=text name=surname size=20></input></td>
            </tr>
            <tr>
                <td colspan=2 align=center><input type=submit
		  value="Create Account!"></td>
            </tr>
        </table
    </form>
    <p>*Required Fields
])

insert([mailpass], [Mail Password], [],
[
    <p>Please enter your username or email address to have your
    password mailed to you.
])

insert([topic], [View Topic], [],
[
    |tabsubtopics|
])

insert([subtopic], [View Subtopic], [],
[
    |tabsubtopic|
    |tabsubtopicdocs|
])

insert([editdoc], [Edit Document Meta-data], [Edit Document Meta-data],
[
    |tabeditdoc|
    |tabdocfiles|
    |tabdocusers|
    |tabdocversions|
    |tabdoctopics|
    |tabdocnotes|
    |tabdocerrors|
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
])

insert([user_exists], [User Exists], [],
[
    <p>That username is already taken. Please select another username and try again.
])

insert([username_required], [Username Required] [],
[
    <p>Username is a required field. Please enter a username and try again.
])

insert([email_exists], [Email Exists], [],
[
    <p>That email address is already in the database.
    If you already have an account but have forgotten your password,
    you can have it <a href="mailpass">mailed</a> to you.
])

insert([account_created], [Account Created], [],
[
    <p>Your account has been created, and your password has been mailed to you.
    Please check your email.
])

insert([user], [|user.name|], [],
[
    |tabuser|
])

insert([logged_in], [Logged In], [],
[
    <p>You have been logged into the system.
])

insert([logged_out], [Logged Out], [],
[
    <p>You have been logged out of the system.
])

insert([type], [|type.name|], [],
[
    |tabtypedocs|
])

insert([cvslog], [CVS Log], [],
[
    |tabcvslog|
])

