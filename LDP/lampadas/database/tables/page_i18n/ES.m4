insert([404], [Error 404, Página No Encontrada], [Error], [<p>Disculpa, pero la página que has solicitado no exite.
Si vienes de otro sitio, por favor notifica al webmaster del sitio
acerca de que el vínculo es incorrecto o ha caducado. 
<p>Si vienes de otra página del sistema Lampadas, posiblemente
has encontrado un error.
Si crees que ese es el caso, por favor envía un archivo
de reporte de error a los desarolladores de Lampadas.])
insert([about], [Acerca de |strproject|], [Acerca de |strprojectshort|], [Reemplaza este texto con información de tu proyecto.])
insert([account_created], [Account Created], [], [<p>Your account has been created, and your password has been mailed to you.
Please check your email.
])
insert([adddocument], [Add Document], [Add Document], [|tabeditdoc|])
insert([addnews], [|stradd_news|], [|stradd_news|], [|tabnewsitem|])
insert([addpage], [Agregar Página Web], [Agregar Página Web], [|tabpage|])
insert([addstring], [Agregar Cadena], [Agregar Cadena], [|tabstring|])
insert([adduser], [Agregar Usuario], [Agregar Usuario], [|tabuser|])
insert([collection], [|collection.name|], [], [|tabcollection|
])
insert([contribute], [Contribuyendo con |strproject|], [Contribuyendo con |strprojectshort|], [<p>As a member of this Lampadas community, you can collaborate with
hundreds or even thousands of others to produce documentation,
which can then be shared with others all around the world over the
Web.
<p>We've designed the Lampadas system to make contributing simple and easy.
Here are some ways you can help, roughly in order of difficulty or
commitment required:
<ul>
<li>Rate Documents
<p>Each document has a "rating", on a scale of 1 to 10, which tells you
what other readers think of it.
We use this rating to improve our documents, for focusing our attention
on the documents you've identified as neednig improvement.
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
</ul>])
insert([copyright], [Copyright], [Copyright], [<p>Lampadas está bajo  Copyright 2000, 2001, 2002 por David C. Merrill.
<p>
Individual documents are copyrighted by their authors,
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
documentation regardless of the document's license.])
insert([doctable], [Tabla de Documentos], [Tabla de Documentos], [|tabdocs|])
insert([document], [|doc.title|], [|doc.title|], [|blkdocument_nav_bar|
|tabeditdoc|
<p>|tabdocerrors|
<p>|tabeditdocfiles|
<p>|tabdocfileerrors|
<p>|tabeditdocusers|
<p>|tabeditdocversions|
<p>|tabeditdoctopics|
<p>|tabeditdocnotes|
<p>|tabdoctranslations|])
insert([document_admin], [|doc.title|], [], [|blkdocument_nav_bar|
|tabdocadmin|
])
insert([document_deleted], [Document Deleted], [Document Deleted], [The document has been deleted from the database.])
insert([document_errors], [|doc.title|], [|doc.title|], [|blkdocument_nav_bar|
|tabdocerrors|
<p>|tabdocfileerrors|])
insert([document_files], [|doc.title|], [|doc.title|], [|blkdocument_nav_bar|
<p>|tabfile_metadata|
<p>|tabeditdocfiles|])
insert([document_main], [|doc.title|], [|doc.title|], [|tabdocument_tabs|
|tabeditdoc|])
insert([document_notes], [|doc.title|], [|doc.title|], [|blkdocument_nav_bar|
|tabeditdocnotes|])
insert([document_revs], [|doc.title|], [|doc.title|], [|blkdocument_nav_bar|
|tabeditdocversions|])
insert([document_topics], [|doc.title|], [|doc.title|], [|blkdocument_nav_bar|
|tabeditdoctopics|])
insert([document_translation], [|doc.title|], [], [|blkdocument_nav_bar|
|tabdoctranslations|
])
insert([document_users], [|doc.title|], [|doc.title|], [|blkdocument_nav_bar|
|tabeditdocusers|])
insert([email_exists], [Email Exists], [], [<p>That email address is already in the database.
If you already have an account but have forgotten your password,
you can have it <a href="mailpass">mailed</a> to you.
])
insert([errors], [Lista de Errores], [Lista de Errores], [|taberrors|])
insert([file_report], [File Report], [], [|tabfile_report|
])
insert([home], [|strprojectshort| Página Principal], [Principal], [<p>¡Bienvenido a |strproject|¡.</p>

<p>Este sitio es un demo del 
<a href="|uri.base|lampadas|uri.lang_ext|">
Sistema de Manejo de Documentos
Lampadas </a> que está siendo
desarollado por
<a href="mailto:david@lupercalia.net">David Merrill</a> y otros del <a href="http://www.tldp.org">
Proyecto de Documentación Linux</a>, con
soporte y asistencia
del 
<a href="http://developer.gnome.org/projects/gdp/">
Proyecto
de Documentación
Gnome</a>.</p>

<p>Lampadas 
permanece bajo desarollo. Si ocurre algún error, por favor repórtalo en la
<a href="http://bugzilla.gnome.org/enter_bug.cgi?product=lampadas">
base de datos
Gnome Bugzilla</a>. Los desarolladores posiblemente estén interesados en la  <a href="http://www.lampadas.org/doc/740/index.html">
Guía de Desarolladores Lampadas</a>,
que explica como trabaja el sistema.

<p>Hay muchas maneras de buscar en los documentos que esán publicados aquí. Selecciona uno de ellos de los men&uacute;s de navegación a la izquierda.

<p>|tabrecentnews|])
insert([index], [|strproject|], [Splash Page], [|tabsplashlanguages|
])
insert([lampadas], [About Lampadas], [About Lampadas], [<p>This website is based on version |version| of the Lampadas Documentation Management System, a Free Software (GPL) platform developed by David Merrill (<a href="mailto:david@lupercalia.net">david@lupercalia.net</a>)
and others at <a href="http://www.tldp.org">The Linux Documentation Project</a>.

<p>Lampadas is a powerful, flexible platform designed to support large documentation projects such as the LDP. It provides an interactive environment for writing, managing, publishing and reading documentation.

<p>The system is being adopted by the LDP and by the Gnome Documentation Project.

<p>Lampadas is intended to facilitate a more collaborative process, with authors, editors, technical experts, and readers working together to produce documentation, and to share information with each other. The idea is that for documentation to improve at the same rate as other Free Software projects, we also need to start taking advantage of the strength of Open Source, namely massive parallelism.

<p>Of course, very little of this vision is available in the code running on this server.
We're still in the way to version 1.0, and 1.0 is all about getting the core features implemented in a sane and flexible way. Version 1.0 is the basic infrastructure.

<p>This is <i><b>alpha quality</b></i> code, so you get the standard disclaimer: if it breaks, you get to keep both pieces. That said, the system is fairly stable, most of the time, but it is not production grade quite yet. It is also being actively hacked, so sometimes is it less stable than other times.

<h1>About This Demo Site</h1>

<p>This demo site is populated with data from the LDP Database (LDPDB). If you had an account on the LDPDB, you have one here. However, because passwords on the LDPDB are stored only in
hashed form, I was unable to port them over, and you've been given a new password. To get it, click the "Mail Password" link on the home page and your new password will be mailed to your
address of record.</p>

<h1>Reporting Bugs</h1>

<p>We greatly appreciate your comments, bug reports or questions. You can reach David Merrill at <a href="mailto:david@lupercalia.net">david@lupercalia.net</a>
if you have comments or questions.

<p>Bugs should be reported in the Gnome Bugzilla database at <a href="http://bugzilla.gnome.org">bugzilla.gnome.org</a>.
If you file a bug, be sure to file it against the Lampadas project.

<h1>Building Lampadas</h1>

<p>If you want to help build Lampadas, it is a really fun and exciting project. You can find out more about it by reading the <a href="http://www.lupercalia.net/lampadas/">Lampadas Developer's Guide</a> (temporarily down).</p>

<h1>Why Lampadas?</h1>

<p>Fans of Frank Herbert's Dune series will recognize Lampadas as the name of the Bene Gesserit teaching planet, which plays a
role in the final book, <i>Chapterhouse: Dune</i>. Before the planet can be destroyed by hordes of Honored Matres, Reverend Mother Lucilla orders the planet to share Other Memory, two by two then four by four, until all the students hold within them the composite knowledge and memories of the entire planet. After the planet is annihilated by the Honored Matres, the precious knowledge is carried back to the Bene Gesserit Chapterhouse by the lone holder of the precious cargo, Rebecca.

<p>Herbert apparently took the name from the city of Lampadas, which was an ancient seat of learning and scholarship. Also, the word lampadas is the accusative form of the word
"Torch" in ancient Greek.

<p>In all of these senses, Lampadas seems an appropriate name for this project, which is created to facilitate sharing information
from many people and many sources, and disseminating it widely to others.])
insert([logged_in], [Logged In], [], [<p>You have been logged into the system.
])
insert([logged_out], [Logged Out], [], [<p>You have been logged out of the system.
])
insert([maillists], [Listas de Correo], [Listas de Correo], [Lista aquí las listas de correo de tu proyecto.])
insert([mailpass], [Mail Password], [], [<p>Please enter your email address to have your
password mailed to you.
<p>|tabmailpass|
])
insert([maint_wanted], [Se Busca Responsable de Mantenimiento], [Se Busca Responsable de Mantenimiento], [|tabmaint_wanted|])
insert([my], [Mi Página Personal], [Mi Página Personal], [<p>Esta es tu página personal.</p>
<p>Esta tabla lista todos los documentos en los que te has ofrecido de voluntario para contribuir:</p></p>
<p>|session_user_docs|</p>])
insert([news], [Lista de Noticias], [Lista de Noticias], [|tabnews|])
insert([news_edit], [Edit News], [], [|tabnewsitem|
])
insert([newuser], [New User], [], [<p>To create a new user account, fill out this form.
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
])
insert([omf], [OpenSource Meta-data Framework XML Output], [OMF XML Output], [|tabomf|])
insert([page_edit], [Edit Web Page], [Edit Web Page], [|tabpage|])
insert([pages], [Lista de Páginas Web], [Lista de Páginas Web], [|tabpages|])
insert([password_mailed], [Password Mailed], [], [<p>Your password has been mailed to you.
If you continue to have problems logging in, please write
the site administrator for assistance.
])
insert([pending], [Documentos Pendientes], [Documentos Pendientes], [|tabpending|])
insert([privacy], [Política de Privacidad], [Política de Privacidad], [<p>Nuestro cometido es ayudarte a mantener tu privacidad mientras estás en línea. Puedes usar este sitio sin divulgar información personal. 
<p>Como sea, debido a la naturaleza del sistema, algunas características requieren registrarse.
Para registrarte, debes proveer tu dirección de email. Requerímos
una dirección de email para prevenir ciertos tipos de Ataque de Denegación de Servicio (Denial of Service, DoS). Toda la demás información es opcional.
<p>Tu información es usada sólmante en la operación de este sitio. Ninguna información personal tuya será divulgada a una tercera persona.
<p>No te mandaremos basura a tu mail o te agregaremos a ninguna lista de correo sin tu consentimiento.])
insert([recentnews], [Noticias Recientes], [Noticias Recientes], [|tabrecentnews|])
insert([resources], [Otros Recursos], [Otros Recursos], [Próximamente recursos en español
<ul>
<li><a href="http://www.dictionary.com">Dictionary.com</a>, an online dictionary.
<li><a href="http://www.thesaurus.com">Thesaurus.com</a>, an online thesaurus.
<li><a href="http://www.webopedia.com">Webopedia.com</a>, an online dictionary
and search engine for computer and internet technology.
</ul>])
insert([search], [Search], [Search], [|tabsearch|])
insert([sessions], [Sesiones de Usuarios], [Sesiones de Usuarios], [|tabsessions|])
insert([sitemap], [Mapa del Sitio], [Mapa del Sitio], [|tabsitemap|])
insert([sourcefile], [Source File], [Source File], [|tabfile_reports|
<p>|tabfile_metadata|])
insert([staff], [Miembros], [Miembros], [Lista a los miembros del grupo de tu proyecto aquí.])
insert([stats], [Estadísticas Actuales], [Estadísticas Actuales], [<h1>Estadísticas Globales de Documentos</h1>
|tabpub_status_stats|
<p>Estas estadísticas incluyen todos los documentos en la base de datos, sin tener en cuenta su estado.
<p>|tabdoc_format_stats|
<p>|tabdoc_dtd_stats|
<p>|tabdoc_lang_stats|
<p><hr>
<h1>Estadísticas de Publicado</h1>
<p>Estas estadísticas muestran el estado del sistema de publicación de documentos.
<p>La primera tabla indica cuándo Lintadas (el revisor de errores de Lampadas) fue ejecutado sobre cada documento.
<p>|tablint_time_stats|
<p><hr>
<p>Esta tabla indica cuándo los documentos fueron puestos en mirrors satisfactoriamente:
<p>|tabmirror_time_stats|
<p><hr>
<p>Esta tabla indica cuándo los documentos fueron publicados satisfactoriamente:
<p>|tabpub_time_stats|
<p><hr>
<p>Esta tabla indica que errores en el documento han sido identificados por Lintadas, ya sea durante el proceso de mirror o durante la publicación:
<p>|tabdoc_error_stats|
<h1>Estadísticas de Documentos Publicados</h1>
<p>El resto de estas estadísticas sólo reportan documentos que han sido publicados satisfactoriamente.
<p>La siguiente tabla da estadísticas en muchos documentos meta-datos:
<p>|tabpub_doc_format_stats|
<p>|tabpub_doc_dtd_stats|
<p>|tabpub_doc_lang_stats|])
insert([string_edit], [Editar Cadena], [Editar Cadena], [|tabstring|], [1.0])
insert([strings], [Lista de Cadenas], [Lista de Cadenas], [|tabstrings|])
insert([topic], [View Topic], [], [|tabtopics|
<p>|tabtopicdocs|
])
insert([type], [|type.name|], [], [|tabtypedocs|
])
insert([unmaintained], [Documentos sin Mantenimiento], [Documentos sin Mantenimiento], [<p>Si quieres mantener uno de esos documentos sin mantenimiento, por favor sigue estos pasos:
<ul>
<li>Contacta al autor original. Si no está listado, consulta el documento.
Asegúrate que el autor ya no desea mantener el document en cuestión. 
<li>Determina si existe una copia más actual del documento, aparte de 
la que esta disponible aquí. La mejor manera de hacer esto es a través
de la persona que mantenía antes el documento. Si puedes, asegura una copia 
de la versión más reciente y envíala aquí.
<li>Informa al administrador del sitio que quieres mantener el documento.
El  administrador te asignará los derechos necesarios así puedes
empezar a mantenerlo.
<li>Actualiza el documento, agregándote como la persona responsable de su mantenimiento. Asegúrate de continuar acreditando a todos las personas anteriores responsables del mantenimiento del documento.
</ul>
<p>Es posible que un documento pueda ser listado aquí de manera errónea. 
Si encuentras un error, por favor notifícalo al administrador del sitio
en el momento, así podremos corregir el problema.
<p>|tabunmaintained|])
insert([user], [|user.username| - |user.name|], [], [|tabuser|
<p>|user.docs|
])
insert([user_exists], [User Exists], [], [<p>That username is already taken. Please select another username and try again.
])
insert([username_required], [Username Required], [<p>Username is a required field. Please enter a username and try again.
], [1])
insert([users], [Lista de Usuarios], [Lista de Usuarios], [|tabletters|
|tabusers|])
insert([view_document], [|doc.title|], [|doc.title|], [|tabviewdoc|
<p>|tabdocerrors|
<p>|tabviewdocfiles|
<p>|tabviewdocfileerrors|
<p>|tabviewdocusers|
<p>|tabviewdocversions|
<p>|tabviewdoctopics|
<p>|tabviewdocnotes|
<p>|tabdoctranslations|])
insert([wishlist], [Documentos Pendientes], [Documentos Pendientes], [|tabwishlist|])
