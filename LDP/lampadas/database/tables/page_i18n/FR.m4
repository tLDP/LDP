insert([admin], [Admin Page], [],
[
    <p>Admin tools.
])

insert([sysadmin], [Sysadmin Page], [],
[
    <p>Sysadmin tools.
])

insert([my], [My Home], [],
[
    |session_user_docs|
])

insert([home], [|strproject|], [Home],
[
	<p>Ce syst&egrave;me est en cours de d&eacute;veloppement. Son code est modifi&eacute; en permanence ce qui le rend instable.

	<p>Merci de ne pas envoyer de rapport de bogue pour le moment
])

insert([doctable], [Table des docs], [Table des docs],
[
	|tabdocs|
])

insert([news], [|strproject| News], [|strprojectshort| News],
[
	|tabrecentnews|
])

insert([contribute], [Contribuer &agrave; Lampadas], [Contribuer &agrave; Lampadas],
[
	En tant que membre de ce syst&egrave;me, vous b&eacute;n&eacute;ficiez du travail de plusieurs centaines d\'utilisateurs de Linux, qui ont b&eacute;n&eacute;volement contribu&eacute; &agrave; cr&eacute;er cette &eacute;norme biblioth&egrave;que &eacute;lectronique.

	<p>Nous sommes s&ucric;rs que vous souhaiteriez apporter votre pierre &agrave; l\'&eacute;difice aussi avons-nous con&ccedil;u Lampadas pour que vous puissiez ais&eacute;ment participer. Voici plusieurs fa&ccedil;ons d\'aider, class&eacute;es par ordre de difficult&eacute;:

	<ul>
	<li>Noter les documents

	<p>Chaque document est not&eacute;, sur une &eacute;chelle de 1 &agrave; 10, qui vous informe de l\'opinion qu\'en ont eu les autres lecteurs. Cette note nous permet de concentrer nos efforts sur l\'am&eacute;lioration des documents dont vous nous dites qu\'ils en ont le plus besoin.</li>

	<li>Signaler une erreur

	<p>Si vous trouvez une erreur dans un document, signalez-l&agrave;.

	</li>

	<li>Traduire un document
	<p>Les traducteurs sont toujours tr&egrave;s recherch&eacute;s, car notre but est d\'offrir notre documentation dans le plus grand nombre de langues possibles pour que tous puissent en profiter.
	</li>
	<li>Tranduire Lampadas
	<p>Le syst&egrave;me Lampadas peut &ecirc;tre localis&eacute; pour que chacun puisse l\'utiliser dans sa langue de pr&eacute;dilection. Il est actuellement disponible en:
	<ul>
	<li>Anglais</li>
	<li>Fran&ccedil;ais</li>
	</ul>
	</li>
	<li>Ecrire un document
	<p>Si vous avez une comp&eacute;tence particuli&egrave;re, n\'h&eacute;sitez pas &agrave; &eacute;crire un nouveau document pour que nous le publions. Lampadas propose plusieurs outils pour vous faciliter cette tâche.
	</li>
	</ul>
])

insert([about], [A propos de |strproject|], [A propos de |strprojectshort|],
[
	Remplacez ce texte par la description de votre projet.
])

insert([lampadas], [A propos de Lampadas], [A propos de Lampadas],
[
	<p>Lampadas est un syst&egrave;me de r&eacute;daction, gestion, publication et lecture de documentaion.

	<p>Une fois enregistr&eacute; dans Lampadas, vous devenez membre d\'une communaut&eacute; 
	incluant auteurs, &eacute;diteurs, experts techniques et lecteurs,
	qui collaborent et partagent des informations.

])

insert([copyright], [Le Copyright], [Le Copyright],
[
	Copyright 2002 David Merrill.
])

insert([privacy], [Confidentialit&eacute;], [Confidentialit&eacute;],
[
	Confidentialit&eacute;
])

insert([newuser], [New User], [],
[
    <p>To create a new user account, fill out this form.
    <p>
    <form name="newuser" action="adduser" method=GET>
        <table class="form">
            <tr>
                <td align=right>*Username</td>
                <td><input type=text name=username size=20></input></td>
            </tr>
            <tr>
                <td align=right>*Enter your email address.<br>Your password will be mailed to this address, so it must be valid.</td>
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
                <td colspan=2 align=center><input type=submit value="Create Account!"></td>
            </tr>
        </table
    </form>
    <p>*Required Fields
])

insert([topic], [View Topic], [View Topic],
[
    |tabsubtopics|
])

insert([subtopic], [View Subtopic], [],
[
    |tabsubtopic|
    |tabsubtopicdocs|
])

insert([editdoc], [M&eacute;ta-donn&eacute;es du doc], [M&eacute;ta-donn&eacute;es du doc],
[
	|tabeditdoc|
])

insert([404], [Introuvable], [Introuvable],
[
	Introuvable
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

insert([user], [|user_name|], [],
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
