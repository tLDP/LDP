insert([newdocument], [Dokument hinzufügen], [],
[
    |tabeditdoc|
])

insert([admin], [Administration], [],
[
    <p>Werkzeuge für Administratoren.
])

insert([users], [Liste der Benutzer], [],
[
    |tabusers|
])

insert([sysadmin], [System-Administration], [],
[
    <p>Werkzeuge für System-Administratoren.
])

insert([my], [Meine Homepage], [],
[
    <p>Dies ist Ihre persönliche Homepage.

    <p>Und dies sind die Dokumente an denen sie mitarbeiten:

    |session_user_docs|
])

insert([home], [|strproject|], [Home], 
[
    <p>Willkommen zu |strproject|.

    <p>Diese Web-Site basiert auf einer Vorabversion des
    Dokumentenverwaltungssystems Lampadas welches im Rahmen des
    <a href="http://www.tldp.org">Linux-Dokumentations-Projekts</a>
    entwickelt wird.
])

insert([doctable], [DocTable], [],
[
    |tabdocs|
])

insert([news], [Neuigkeiten], [],
[
    |tabrecentnews|
])

insert([staff], [Team], [],
[
    Führen Sie hier die Mitglieder Ihres Projekteams an.
])

insert([contribute], [Mitarbeit bei |strproject|],
    [Mitarbeit bei |strprojectshort|],
[
    Als Mitglied der Lampadas-Gemeinde arbeiten Sie mit
    hunderten oder gar tausenden Anderen zusammen an Dokumentation
    die über\'s Netz weltweit veröffentlicht wird.

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
    benötigt. Momentan ist Lampadas verfügbar in:

    <ul>
    <li>Englisch</li>
    <li>Französisch</li>
    <li>Deutsch</li>
    </ul>
    </li>

    </ul>
])

insert([unmaintained], [Nicht mehr gewartete Dokumente], [],
[
    |tabunmaintained|
])

insert([maint_wanted], [Instandhalter gesucht], [],
[
    |tabmaint_wanted|
])

insert([wishlist], [Dokumentwunschliste], [],
[
    |tabwishlist|
])

insert([pending], [Dokumentwarteschlange], [],
[
    |tabpending|
])

insert([resources], [Andere Hilfsmittel], [],
[
    <ul>
        m4_dnl holy penguin droppings, it's a meta command!
        <li>Insert some resources for German authors.
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
        <table class="form">
            <tr>
                <td align=right>*Benutzername</td>
                <td><input type=text name=username size=20></input></td>
            </tr>
            <tr>
                <td align=right>*Ihre E-Mailadresse.
		<br>Da Ihr Kennwort zu dieser Adresse geschickt wird,
		muss sie gültig sein.</td>
                <td><input type=text name=email size=20></input></td>
            </tr>
            <tr>
                <td align=right>Vorname</td>
                <td><input type=text name=first_name size=20></input></td>
            </tr>
            <tr>
                <td align=right>Zweiter Vorname</td>
                <td><input type=text name=middle_name size=20></input></td>
            </tr>
            <tr>
                <td align=right>Nachname</td>
                <td><input type=text name=surname size=20></input></td>
            </tr>
            <tr>
                <td colspan=2 align=center>
		<input type=submit value="Anlegen!"></td>
            </tr>
        </table
    </form>
    <p>*Unbedingt erforderlich
])

insert([mailpass], [Kennwort schicken], [],
[
    <p>Bitte geben Sie Benutzernamen oder E-Mailaddresse an.
    Wir schicken Ihnen anschließend Ihr Kennwort per E-Mail.
])

insert([topic], [Liste der Themen], [],
[
    |tabsubtopics|
])

insert([subtopic], [Liste der Unterthemen], [],
[
    |tabsubtopic|
    |tabsubtopicdocs|
])

insert([editdoc], [Metadaten eines Dokuments ändern], [Metadaten ändern],
[
    |tabeditdoc|
    |tabdocfiles|
    |tabdocusers|
    |tabdocversions|
    |tabdoctopics|
    |tabdocnotes|
    |tabdocerrors|
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

insert([user], [|user.name|], [],
[
    |tabuser|
])

insert([logged_in], [Angemeldet], [],
[
    <p>Sie wurden im System angemeldet.
])

insert([logged_out], [Abgemeldet], [],
[
    <p>Sie wurden im System abgemeldet.
])

insert([type], [|type.name|], [],
[
    |tabtypedocs|
])

insert([cvslog], [CVS Log], [],
[
    |tabcvslog|
])
