m4_dnl  These are the pages that are served by the CMS.
m4_dnl  The last field is the version number. Please bump it
m4_dnl  by one if you're the primary author, and synchronize
m4_dnl  it in translations when the translation is up to date.

m4_dnl  "menu_name" is the short name of the page, which is
m4_dnl  typically listed in sidebar menus.

insert([index], [|strproject|], [Splash-Seite],
[
    |tabsplashlanguages|
])

insert([adddocument], [Dokument hinzufügen], [],
[
    |tabeditdoc|
])

insert([users], [Liste der Benutzer], [],
[
    |tabletters|
    |tabusers|
])

insert([sessions], [Benutzersitzungen], [],
[
    |tabsessions|
])

insert([my], [Meine Homepage], [],
[
    <p>Dies ist Ihre persönliche Homepage.

    <p>Und dies sind die Dokumente an denen sie mitarbeiten:

    <p>|session_user_docs|
])

insert([home], [|strproject|], [Home], 
[
    <p>Willkommen zu |strproject|.

    <p>Diese Web-Site basiert auf einer Vorabversion des
    Dokumentenverwaltungssystems Lampadas welches im Rahmen des
    <a href="http://www.tldp.org">Linux-Dokumentations-Projekts</a>
    entwickelt wird.

    <p>Diese Vorführinstallation bietet die folgenden 
    Benutzerkonten. Melden Sie sich mit diesen Namen an,
    um die Anwendungen mit verschiedenen Rollen und Berechtigungen
    zu sehen.

    <ul>
        <li>sysadmin - SUPERUSER, administriert das System.</li>
        <li>admin - Web-Manager, verwaltet die Inhalte.</li>
        <li>english - Englisch sprechender Benutzer.</li>
        <li>french - Französisch sprechender Benutzer.</li>
        <li>german - Deutsch sprechender Benutzer.</li>
        <li>korean - Koreanisch sprechender Benutzer.</li>
    </ul>

    <p>Alle diese Konten benutzen das Kennwort "password".
    Sie können einen dieser Namen ausprobieren oder auch ein 
    eigenes Benutzerkonto anlegen (oben, rechts, der 
    Link "Benutzerkonto anlegen").
])

insert([doctable], [Dokumente durchsehen], [],
[
	|tabdocs|
])

insert([search], [Suche], [],
[
    |tabsearch|
])

insert([recentnews], [Neuigkeiten], [],
[
    |tabrecentnews|
])

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
])

insert([staff], [Projektteam], [],
[
    Führen Sie hier die Mitglieder Ihres Projekteams an.
])

insert([contribute], [Mitarbeit bei |strproject|],
    [Mitarbeit bei |strprojectshort|],
[
    Als Mitglied der Lampadas-Gemeinde arbeiten Sie mit
    hunderten oder gar tausenden Anderen zusammen an Dokumentation
    die über's Netz weltweit veröffentlicht wird.

    <p>Lampadas soll weltweite Mitarbeit so einfach wie möglich machen.
    Wir können viele Arten von Hilfe brauchen.
    Nach aufsteigendem Aufwand sortiert:

    <ul>
    <li>Bewerten Sie Dokumentation

    <p>Jedes Dokument hat eine von den Lesern vergebene Bewertung auf
    einer Skala von 1 bis 10. Durch diese Beurteilung können wir
    uns auf verbesserungsbedürftige Dokumente konzentrieren.
    </li>

    <li>Melden Sie Fehler

    <p>Schicken Sie uns jeden gefunden Fehler, egal in welchem Dokument.
    </li>
    
    <li>Übersetzen Sie Dokumentation

    <p>Übersetzer sind rar und werden von uns sehr geschätzt.
    Unser Ziel ist es, die gesamte Dokumentation in so vielen Sprachen wie
    möglich anzubieten.
    </li>

    <li>Schreiben Sie ein Handbuch

    <p>Gute Autoren mit solidem technischen Wissen sind herzlich
    eingeladen unsere Sammlung um ein neues Dokument zu bereichern.
    Lampadas stellt einige Werkzeuge für Autoren zur Verfügung.
    </li>
    
    <li>Helfen Sie Lampadas

    <p>Programmierer und Übersetzer können uns an der
    Weiterentwicklung der Software hinter Lampadas helfen.

    <p>Das Lampadas-Systems kann Meldungen in verschiedenen Sprachen
    anzeigen. Übersetzer für weitere Sprachen werden dringend
    benötigt.
    </li>

    </ul>
])

insert([unmaintained], [Nicht mehr gewartete Dokumente], [],
[
    <p>Wenn Sie die Wartung eines dieser verwaisten Dokumente
    übernehmen wollen, folgen Sie bitte diesem Ablauf:

    <ul>
        <li>Nehmen Sie mit dem ursprünglichen Autor Konkakt auf.
	Informationen dazu sollte entweder hier oder im betroffenen
	Dokument zu finden sein. Stellen Sie sicher, dass der Autor
	das Dokument nicht mehr länger betreuen will.

        <li>Stellen Sie bitte fest, ob von dem Dokument eine neuere
	Version existiert. Die Daten an dieser Stelle können veraltet
	sein.  Der einfachste Weg zu dieser Anwtort führt über den
	Autor bzw. letzten Instandhalter des Dokuments. Wenn möglich
	verschaffen Sie sich eine Kopie und veröffentlichen Sie hier.

        <li>Informieren Sie bitte den Administrator dieser Web-Site,
	dass Sie das Dokument übernehmen wollen. Der Administrator
	wird Ihnen dann die nötigen Zugriffsrechte geben.

        <li>Bringen Sie das Dokument auf den letzten Stand.
	Tragen Sie sich selbst als aktuellen Instandhalter ein.
	Bitte bewahren Sie alle Information über frühere Autoren.
    </ul>

    <p>Es ist durchaus möglich, dass ein Dokument irrtümlicherweise
    hier aufgeführt wird. Bitte benachrichtigen Sie den Administrator
    dieser Web-Site wenn Sie einen Fehler finden, damit wir das Problem
    beheben können.
    
    <p>|tabunmaintained|
])

insert([maint_wanted], [Instandhalter gesucht], [],
[
    |tabmaint_wanted|
])

insert([wishlist], [Wunschliste], [],
[
    |tabwishlist|
])

insert([pending], [Dokumente in Arbeit], [],
[
    |tabpending|
])

insert([resources], [Andere Hilfsmittel], [],
[
    <ul>
	<li><a href="http://www.tu-harburg.de/dlhp/"
	  >Deutschen Linux HOWTO Projekt</a></li>
        <li><a href="http://www.leo.org/">Link Everything Online</a></li>
	<li><a href="http://www.ids-mannheim.de/grammis/reform/inhalt.html"
	  >Deutsche Rechtschreibung: Regeln und Wörterverzeichnis</a></li>
        <li><a href="http://home.t-online.de/home/lerch/neolog.htm"
	  >Deutsche Wörter sind schön!</a></li>
    </ul>
])

insert([maillists], [Mailing-Listen], [],
[
    Führen Sie hier die Mailing-Listen Ihres Projekts an.
])

insert([about], [Über |strproject|], [Über |strprojectshort|],
[
    Ersetzen Sie diesen Text mit Angaben über Ihr Projekt.
])

insert([lampadas], [Über Lampadas], [],
[
    <p>Diese Web-Site basiert auf Version |version| des
    Dokumentenverwaltungssystems Lampadas. Sie wird im Rahmen des
    <a href="http://www.tldp.org">Linux-Dokumentations-Projekts</a>
    entwickelt und ist freie Software (GPL).
    
    <p>Lampadas ist eine mächtige und flexible Plattform, ausgelegt
    für große Projekte wie LDP. Es bietet eine interaktive
    Umgebung um Dokumentation zu schreiben, zu verwalten,
    zu veröffentlichen und zu lesen.

    <p>Lampadas schafft eine Gemeinschaft von Autoren, Redakteuren,
    technische Experten und Lesern die zusammen Dokumente erarbeiten
    und Wissen austauschen.

    <h1>Warum Lampadas?</h1>

    <p>In Frank Herberts Saga um den "Wüstenplanet" (eng. "Dune") ist
    Lampadas der Ausbildungsplanet der Bene Gesserit. Er spielt eine
    wesentliche Rolle im letzten Band "Die Ordensburg des Wüstenplaneten"
    (eng. "Chapterhouse: Dune").

    Vor der Zerstörung des Planeten durch die Horden der Geehrten
    Matres läßt die Ehrwürdige Mutter Lucilla die Bewohner ihr
    Wissen in einem übersinnlichen Gedächtnis teilen. Erst zu zweit,
    dann zu viert - bis alle Schüler die gesamte Erfahrung und Erinnerung
    des Planeten in sich halten.
    Nach der Vernichtung dieser Welt wird das wertvolle Wissen
    durch die alleinige Inhaberin Rebecca zur Ordensburg der Bene
    Gesserit zurückgebracht.

    <p>Herbert entlehnte den Namen anscheinend von der antiken Stadt
    Lampadas, ein Ort des Wissens und der Lehre.
    Ausserdem ist "Lampadas" die Akusativform des altgriechischen
    Wortes für Fackel.

    <p>In jeder dieser Bedeutungen ist Lampadas ein angemessener Name
    für ein Projekt, dass geschaffen wurde, um Informationen zwischen
    vielen Menschen auszutauschen und zu verbreiten.
])

insert([copyright], [Copyright], [],
[
    <p>Lampadas is Copyright 2000, 2001, 2002 by David C. Merrill.

    <p>Die Rechte an einzelnen Dokumenten liegen bei deren Autoren.
    Kommentare sind geistiges Eigentum ihrer Verfasser.

    <p>Wir bestreiten jede Verantwortung für Inhalte die durch
    Benutzer dieser Web-Site veröffentlicht werden.
    Die Benutzung dieser Web-Site kann Sie mit Fäkalsprache,
    Gotteslästerung, Pornographie und ähnlichen Dingen konfrontieren.
    Alle Inhalte dieser Art sowie alle belegten Urheberrechtsverletzungen
    werden von uns prompt entfernt - wenn wir davon Kenntnis erlangen.

    <p>Die Lampadas Software wird unter den Bedingungen der GNU General
    Public License (GPL) veröffentlich.
    Eine Kopie der GPL ist online verfügbar unter
    <a href="http://www.gnu.org/licenses/gpl.html"
      >www.gnu.org/licenses/gpl.html</a>.

    <p>Wir bemühen uns, genaue Information zu liefern. Aber wir
    garantieren weder Genauigkeit, Vollständigkeit oder irgend
    eine andere Eigenschaft. Genau genommen geben wir keinerlei
    Garantie oder Sicherheit für irgend etwas. 

    <p>Die Benutzung von Informationen, Downloads, Software oder
    irgend einer anderen Ressource dieser Web-Site geschieht
    <i>auf eigene Gefahr</i>.
    Wir empfehlen Datensicherung ihres Systems nicht nur regelmäßig
    sondern auch vor jeder nicht-trivialen Änderungen durchzuführen.

    <p>Linux ist ein eingetragenes Warenzeichen von Linus Torvalds.
    TLDP ist ein eingetragenes Warenzeichen von
    <a href="http://www.tldp.org">Das Linux-Dokumentations-Projekt</a>.
    Alle anderen Warenzeichen gehören ihren Eigentümern.

    <p>Sofern Sie es nicht ausdrücklich anders erklären,
    fallen alle Kommentare, Fehlerberichte, Anmerkungen zu Dokumenten
    oder andere Formen der Leserrückmeldung die Sie hier veröffentlichen
    in öffentlichen Besitz ("public domain").
    Diese Bestimmung ermöglicht es den Autoren, ihre Kommentare
    unabhängig von den Lizenzbestimmungen des betreffenden Dokuments
    in die Dokumentation aufzunehmen.
])

insert([privacy], [Datenschutz], [],
[
    <p>Wir unterstützen Sie bei der Wahrung Ihrer Privatsphäre im Internet.
    Sie können diese Web-Site ohne Preisgabe persönlicher Angaben
    benutzen.
    
    <p>Allerdings machen technische Gründe bei einigen Funktionen
    eine Registrierung notwendig.

    Diese Registrierung erfordert die Angabe eine E-Mailadresse. 
    Wir benötigen sie um bestimmte Arten eines "denial of service attack"
    (DoS) zu vereiteln. Alle anderen Angaben sind optional.

    <p>Ihre Daten werden nur zum Betrieb dieser Web-Site verwendet.
    Keinerlei persönliche Daten werden jemals Dritten bekanntgegeben.
    
    <p>Ohne Ihre Zustimmung werden wir Ihnen weder unverlangten
    Werbe-E-Mails schicken ("spam") noch Sie bei E-Mailverteilern eintragen.
])

m4_dnl FIXME: there has to be German expression for it
insert([sitemap], [Site Map], [],
[
    |tabsitemap|
])

insert([newuser], [Neue Benutzer], [],
[
    <p>Füllen Sie bitte dieses Formular aus,
    um ein neues Benutzerkonto anzulegen.
    
    <p>
    <form name="newuser" action="data/save/newuser" method=GET>
        <table class="box">
            <tr>
                <td class="label">*Benutzername</td>
                <td><input type=text name=username size=20></input></td>
            </tr>
            <tr>
                <td class="label">**Ihre E-Mailadresse</td>
                <td><input type=text name=email size=20></input></td>
            </tr>
            <tr>
                <td class="label">Vorname</td>
                <td><input type=text name=first_name size=20></input></td>
            </tr>
            <tr>
                <td class="label">Zweiter Vorname</td>
                <td><input type=text name=middle_name size=20></input></td>
            </tr>
            <tr>
                <td class="label">Nachname</td>
                <td><input type=text name=surname size=20></input></td>
            </tr>
            <tr>
                <td colspan=2 align=center>
		<input type=submit value="Anlegen!"></td>
            </tr>
        </table
    </form>
    <p>* Unbedingt erforderlich
    <br>** Da Ihr Kennwort zu dieser Adresse geschickt wird,
    muss sie gültig sein.
])

insert([mailpass], [Kennwort schicken], [],
[
    <p>Bitte geben Sie E-Mailaddresse an.
    Wir schicken Ihnen anschließend Ihr Kennwort per E-Mail.

    <p>|tabmailpass|
])

insert([topic], [View Topic], [],
[
    |tabtopics|
    <p>|tabtopicdocs|
])

insert([document], [|doc.title|], [],
[
    |blkdocument_nav_bar|
    |tabeditdoc|
    <p>|tabeditdocfiles|
    <p>|tabdocfileerrors|
    <p>|tabeditdocusers|
    <p>|tabeditdocversions|
    <p>|tabeditdoctopics|
    <p>|tabeditdocnotes|
    <p>|tabdoctranslations|
])

insert([document_main], [|doc.title|], [],
[
    |blkdocument_nav_bar|
    |tabeditdoc|
])

insert([document_files], [|doc.title|], [],
[
    |blkdocument_nav_bar|
    <p>|tabfile_metadata|
    <p>|tabeditdocfiles|
])

insert([document_users], [|doc.title|], [],
[
    |blkdocument_nav_bar|
    |tabeditdocusers|
])

insert([document_revs], [|doc.title|], [],
[
    |blkdocument_nav_bar|
    |tabeditdocversions|
])

insert([document_topics], [|doc.title|], [],
[
    |blkdocument_nav_bar|
    |tabeditdoctopics|
])

insert([document_notes], [|doc.title|], [],
[
    |blkdocument_nav_bar|
    |tabeditdocnotes|
])

insert([document_translation], [|doc.title|], [],
[
    |blkdocument_nav_bar|
    |tabdoctranslations|
])

insert([document_admin], [|doc.title|], [],
[
    |blkdocument_nav_bar|
    |tabdocadmin|
])

insert([document_errors], [|doc.title|], [],
[
    |blkdocument_nav_bar|
    |tabdocerrors|
    <p>|tabdocfileerrors|
])

insert([view_document], [|doc.title|], [],
[
    |tabviewdoc|
    <p>|tabdocerrors|
    <p>|tabviewdocfiles|
    <p>|tabviewdocfileerrors|
    <p>|tabviewdocusers|
    <p>|tabviewdocversions|
    <p>|tabviewdoctopics|
    <p>|tabviewdocnotes|
    <p>|tabdoctranslations|
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

insert([404], [Fehler 404, Seite nicht gefunden], Fehler,
[
    <p>Die angeforderte Seite existiert leider nicht.
    Sollten Sie einem Link von einer anderen Web-Site gefolgt sein,
    informieren Sie bitte den dortigen Webmaster, dass der Link
    falsch bzw. veraltet ist.

    <p>Wenn Sie von einer anderen Seite innerhalb des Lampadas-Systems
    kommen, haben Sie wahrscheinlich einen Software-Fehler gefunden.
    In diesem Fall schicken Sie bitte einen Fehlerbericht an die 
    Lampadas-Entwickler.
])

insert([user_exists], [Benutzername bereits vorhanden], [],
[
    <p>Dieser Benutzername wird bereits verwendet. Wählen Sie bitte einen
    anderen Namen und probieren Sie es erneut.
])

insert([username_required], [Benutzername erforderlich] [],
[
    <p>Das Feld "Benutzername" ist zwingend notwendig.
    Tragen Sie bitte einen Namen ein und probieren Sie es erneut.
])

insert([email_exists], [E-Mailadresse bereits vorhanden], [],
[
    <p>Diese E-Mailadresse gibt es bereits in der Datenbank.
    Wenn Sie bereits über Benutzerkonto verfügen, aber Ihr Kennwort
    vergessen haben, können Sie es sich <a href="mailpass">schicken</a>
    lassen.
])

insert([account_created], [Benutzerkonto angelegt], [],
[
    <p>Ihr Benutzerkonto wurde angelegt und das Kennwort per E-Mail
    zugeschickt. Bitte warten Sie auf den Erhalt der E-Mail.
])

insert([password_mailed], [Kennwort wurde zugeschickt], [],
[
    <p>Ihr Kennwort wurde Ihnen per E-Mail zugeschickt.
    Bitte benachrichtigen Sie den Administrator dieser Web-Site
    wenn Sie noch weiter Probleme bei der Anmeldung haben.
])

insert([user], [|user.username| - |user.name|], [],
[
    |tabuser|
    <p>|user.docs|
])

insert([adduser], [Add User], [Add User],
[
    |tabuser|
])

insert([logged_in], [Angemeldet], [],
[
    <p>Sie sind im System angemeldet.
])

insert([logged_out], [Abgemeldet], [],
[
    <p>Sie sind im System abgemeldet.
])

insert([type], [|type.name|], [],
[
    |tabtypedocs|
])

insert([sourcefile], [Quelldatei], [],
[
    |tabfile_metadata|
    <p>|tabfile_reports|
])

insert([file_report], [Report einer Datei], [],
[
    |tabfile_report|
])

insert([errors], [Liste der Fehler], [],
[
    |taberrors|
])

insert([collection], [|collection.name|], [],
[
    |tabcollection|
])

insert([news], [News List], [],
[
    |tabnews|
])

insert([addnews], [Add News], [],
[
    |tabnewsitem|
])

insert([pages], [Web Page List], [],
[
    |tabpages|
])

insert([addpage], [Add Web Page], [],
[
    |tabpage|
])

insert([strings], [String List], [],
[
    |tabstrings|
])

insert([addstring], [Add String], [],
[
    |tabstring|
])

insert([omf], [OpenSource Meta-data Framework XML Output], [OMF XML Output],
[|tabomf|])


