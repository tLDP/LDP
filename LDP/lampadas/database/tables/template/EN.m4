insert(blank,
[|body|])

insert(splash,
[
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    |blkhead|
    <body>
      |body|
    </body>
    </html>
])

insert(index,
[
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    |blkhead|
    <body>
      <table class="layout" width="100%">
        <tr>
          <td class="sidebarleft">|blklogo|</td>
          <td class="center" width="100%">|blkheader|</td>
        </tr>
      </table>
      <table class="layout" width="100%">
        <tr>
          <td class="sidebarleft" valign="top">
            |navmenus|
            <p>|navcollections|
            <p>|navtopics|
            <p>|navtypes|
            <p>|navlanguages|
          </td>
          <td class="center body" width="100%" valign="top">
            |body|
            |tabedit_this_page|
          </td>
          <td class="sidebarright" valign="top">
            |navlogin|
            <p>|navsessions|
          </td>
        </tr>
      </table>
      <table class="layout" width="100%'>
        <tr>
          <td>|blkfooter|</td>
        </tr>
      </table>
    </body>
    </html>
])

insert(default,
[
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    |blkhead|
    <body>
      <table class="layout" width="100%">
        <tr>
          <td class="sidebarleft">|blklogo|</td>
          <td class="center" width="100%">|blkheader|</td>
        </tr>
      </table>
      <table>
        <tr>
          <td class="sidebarleft" valign="top">
            |navmenus|
            <p>|navcollections|
            <p>|navtopics|
            <p>|navtypes|
            <p>|navlanguages|
          </td>
          <td class="center body" width="100%" valign="top">|body|</td>
        </tr>
      </table>
      <table class="layout" width="100%">
        <tr>
          <td>|blkfooter|</td>
        </tr>
      </table>
    </body>
    </html>
])

