m4_dnl  These are the pages that are served by the CMS.
m4_dnl  The last field is the version number. Please bump it
m4_dnl  by one if you're the primary author, and synchronize
m4_dnl  it in translations when the translation is up to date.

insert([index], [|strproject|], [Splash Page],
[
    |tabsplashlanguages|
], 0)

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

insert([my], [My Home Page], [],
[
    <p>This is your personal home page.

    <p>This table lists documents you have volunteered to contribute to:

    <p>|session_user_docs|
], 1)

insert([home], [|strproject|], [Home],
[
	<p>Ce système est en cours de développement. Son code est modifié en permanence ce qui le rend instable.

	<p>Merci de ne pas envoyer de rapport de bogue pour le moment

    <p>This demo site provides the following users. Log in as one of
    them to see the site through their eyes!

    <ul>
        <li>sysadmin - the SUPERUSER, who manages the system.</li>
        <li>admin - the Site Administrator, who manages the content.</li>
        <li>english - an English-speaking user.</li>
        <li>french - a French-speaking user.</li>
        <li>german - a German-speaking user.</li>
        <li>korean - a Korean-speaking user.</li>
    </ul>

    <p>All of these accounts use the password &quot;password&quot;.
    Log in as one of them, and check it out, or create your own
    account using the "Create Account" link to the right.
], 1)

insert([doctable], [Browse Documents], [],
[
	|tabdocs|z
], 1)

insert([search], [Search], [],
[
    |tabsearch|
], 0)

insert([recentnews], [|strproject| News], [|strprojectshort| News],
[
	|tabrecentnews|
], 1)

insert([stats], [Current Statistics], [],
[
    |tabpub_status_stats|
    <p>|tabdoc_error_stats|
    <p>|tablint_time_stats|
    <p>|tabmirror_time_stats|
    <p>|tabpub_time_stats|
    <p>|tabdoc_format_stats|
    <p>|tabdoc_dtd_stats|
    <p>|tabdoc_lang_stats|
], 1)

insert([staff], [Staff], [],
[
    List the members of your project\'s staff here.
], 1)

insert([contribute], [Contribuer à Lampadas], [Contribuer à Lampadas],
[
	En tant que membre de ce système, vous bénéficiez du travail de plusieurs centaines d\'utilisateurs de Linux, qui ont bénévolement contribué à créer cette énorme bibliothèque électronique.

	<p>Nous sommes sûrs que vous souhaiteriez apporter votre pierre à l\'édifice aussi avons-nous conçu Lampadas pour que vous puissiez aisément participer. Voici plusieurs façons d\'aider, classées par ordre de difficulté:

	<ul>
	<li>Noter les documents

	<p>Chaque document est noté, sur une échelle de 1 à 10, qui vous informe de l\'opinion qu\'en ont eu les autres lecteurs. Cette note nous permet de concentrer nos efforts sur l\'amélioration des documents dont vous nous dites qu\'ils en ont le plus besoin.</li>

	<li>Signaler une erreur

	<p>Si vous trouvez une erreur dans un document, signalez-là.

	</li>

	<li>Traduire un document
	<p>Les traducteurs sont toujours très recherchés, car notre
    but est d\'offrir notre documentation dans le plus grand nombre de langues
    possibles pour que tous puissent en profiter.
	</li>

	<li>Tranduire Lampadas
	<p>Le système Lampadas peut être localisé pour que chacun
    puisse l\'utiliser dans sa langue de prédilection.
	</li>
	
    <li>Ecrire un document
	<p>Si vous avez une compétence particulière, n\'hésitez pas à écrire un nouveau document pour que nous le publions. Lampadas propose plusieurs outils pour vous faciliter cette tâche.
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
], 0)

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
        <li>Insert some resources for French authors.
    </ul>
], 1)

insert([maillists], [Mailing Lists], [],
[
    List your project\'s mailing lists here.
], 1)

insert([about], [A propos de |strproject|], [A propos de |strprojectshort|],
[
	Remplacez ce texte par la description de votre projet.
], 1)

insert([lampadas], [A propos de Lampadas], [A propos de Lampadas],
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

insert([copyright], [Le Copyright], [Le Copyright],
[
	Copyright 2002 David Merrill.
], 1)

insert([privacy], [Confidentialité], [Confidentialité],
[
	Confidentialité
], 1)

insert([sitemap], [Site Map], [],
[
    |tabsitemap|
], 1)

insert([newuser], [New User], [],
[
    <p>To create a new user account, fill out this form.
    <p>
    <form name="newuser" action="adduser" method=GET>
        <table class="box">
            <tr>
                <td class="label">*Username</td>
                <td><input type=text name=username size=20></input></td>
            </tr>
            <tr>
                <td class="label">*Enter your email address.<br>Your password will be mailed to this address, so it must be valid.</td>
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
                <td colspan=2 align=center><input type=submit value="Create Account!"></td>
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
	|tabeditdoc|
    <p>|tabdocerrors|
    <p>|tabdocfiles|
    <p>|tabdocfileerrors|
    <p>|tabdocusers|
    <p>|tabdocversions|
    <p>|tabdoctopics|
    <p>|tabdocnotes|
    <p>|tabdoctranslations|
], 2])

insert([document_main], [|doc.title|], [],
[
    |tabdocument_tabs|
    |tabeditdoc|
    <p>|tabdocerrors|
])

insert([document_files], [|doc.title|], [],
[
    |tabdocument_tabs|
    |tabdocfiles|
    <p>|tabdocfileerrors|
])

insert([document_users], [|doc.title|], [],
[
    |tabdocument_tabs|
    |tabdocusers|
])

insert([document_revs], [|doc.title|], [],
[
    |tabdocument_tabs|
    |tabdocversions|
])

insert([document_topics], [|doc.title|], [],
[
    |tabdocument_tabs|
    |tabdoctopics|
])

insert([document_notes], [|doc.title|], [],
[
    |tabdocument_tabs|
    |tabdocnotes|
])

insert([document_translation], [|doc.title|], [],
[
    |tabdocument_tabs|
    |tabdoctranslations|
])

insert([document_admin], [|doc.title|], [],
[
    |blkdocument_nav_bar|
    |tabdocadmin|
])

insert([news_edit], [Edit News], [],
[
    |tabnewsitem|
])

insert([page_edit], [Edit Web Page], [],
[
    |tabpage|
])

insert([string_edit], [Edit String], [],
[
    |tabstring|
])

insert([404], [Introuvable], [Introuvable],
[
	Introuvable
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
], 1)

insert([file_report], [File Report], [],
[
    |tabfile_report|
], 1)

insert([errors], [Error List], [],
[
    |taberrors|
], 0)

insert([collection], [|collection.name|], [],
[
    |tabcollection|
], 1)

insert([news], [News List], [],
[
    |tabnews|
], 1)

insert([addnews], [Add News], [],
[
    |tabnewsitem|
], 1)

insert([pages], [Web Page List], [],
[
    |tabpages|
], 1)

insert([addpage], [Add Web Page], [],
[
    |tabpage|
], 1)

insert([strings], [String List], [],
[
    |tabstrings|
], 1)

insert([addstring], [Add String], [],
[
    |tabstring|
], 1)
