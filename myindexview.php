<!DOCTYPE HTML>
<html>

<head>
<h1 style="text-align:center"> Face lock </h1>

<script>
function startTime() {
  var today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  m = checkTime(m);
  s = checkTime(s);
  document.getElementById('txt').innerHTML =
  h + ":" + m + ":" + s;
  var t = setTimeout(startTime, 500);
}
function checkTime(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
}
</script>
</head>


<body onload="startTime()">

<div id="txt"></div>



<body>

<h2>Tämänhetkinen lukon tila:</h2>


        <table align="left">

                <tr>
                        <th>Tila</th>
                        <th>Aika</th>
                </tr>
                <?php
                        foreach($atm as $value){
                                echo "<tr>
                                   <td>".$value['msg']."</td>
                                   <td>".$value['aika']."</td>
                                </tr>";
                        }
                ?>


        </table>
<br><br>
<br><br>
<br><br>
Tila 1 = Lukko on auki
<br><br>
Tila 0 = Lukko on kiinni
<br><br>


  <div style="height:100px;overflow:auto">
        <table border="1"
               align="right">
                <caption>Tapahtumahistoria</caption>
                <tr>
                        <th>ID</th>
                        <th>Topic</th>
                        <th>Message</th>
                        <th>Time</th>
                </tr>
                <?php
                        foreach($taulukko as $key => $value){
                                echo "<tr>
                                  <td>".$value['id']."</td>
                                   <td>".$value['tila']."</td>
                                   <td>".$value['msg']."</td>
                                   <td>".$value['aika']."</td>
                                </tr>";
                        }
                ?>

        </table>
  </div>
<br><br>
<?php
        if(array_key_exists('Auki', $_POST)) {
            Auki();
        }
        else if(array_key_exists('kiinni', $_POST)) {
            kiinni();
        }
        function Auki() {
            echo "Lukko aukaistaan";
            $open = escapeshellcmd('/var/www/html/paho.mqtt.python/examples/publish_auki.py');
            $output = shell_exec($open);
            echo $output;
        }
        function kiinni() {
            echo "Lukko suljetaan";
            $close = escapeshellcmd('/var/www/html/paho.mqtt.python/examples/publish_kiinni.py');
            $output = shell_exec($close);
            echo $output;
        }
    ?>

    <form method="post">
        <input type="submit" name="Auki"
                class="button" value="auki" />

        <input type="submit" name="kiinni"
                class="button" value="kiinni" />
    </form>

</body>
</html>
