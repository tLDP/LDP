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
          <td class="center" width="100%" colspan="2">|blkheader|</td>
          <td></td>
        </tr>
        <tr>
          <td class="sidebarleft" valign="top">
            |navmenus|
            <p>|navcollections|
            <p>|navtopics|
            <p>|navtypes|
            <p>|navlanguages|
          </td>
          <td class="center body" width="100%" valign="top">|body|</td>
          <td class="sidebarright" valign="top">
            |navlogin|
            <p>|navsessions|
          </td>
        </tr>
        <tr>
          <td colspan="3">|blkfooter|</td>
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
        <tr>
          <td colspan="2">|blkfooter|</td>
        </tr>
      </table>
    </body>
    </html>
])

