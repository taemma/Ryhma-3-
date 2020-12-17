<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Welcome extends CI_Controller {

        /**
         * Index Page for this controller.
         *
         * Maps to the following URL
         *              http://example.com/index.php/welcome
         *      - or -
         *              http://example.com/index.php/welcome/index
         *      - or -
         * Since this controller is set as the default controller in
         * config/routes.php, it's displayed at http://example.com/
         *
         * So any other public methods not prefixed with an underscore will
         * map to /index.php/welcome/<method_name>
         * @see https://codeigniter.com/user_guide/general/urls.html
         */
        public function index()
        {
                /*$sub = escapeshellcmd('/var/www/html/paho.mqtt.python/examples/sub_to_db_ATM.py');
                $output = shell_exec($sub);*/
               /* $this->sub();*/
                $this->load->model('Lukko');
                $data['taulukko'] = $this->Lukko->lukontila();
                $tila['atm'] = $this->Lukko->atmtila();
                $taulu = $tila + $data;
                $this->load->view('myindexview', $taulu);
        }
        function sub()
        {
                /*system('/etc/python2.7 /var/www/html/paho.mqtt.python/examples/sub_to_db_ATM.py > /dev/null 2>/dev/null &');*/
                $subba = escapeshellcmd('/var/www/html/paho.mqtt.python/examples/publish_auki.py');
                $output = shell_exec($subba);
                /*echo $output;/*
                system('sudo -r root -S  python /var/www/html/paho.mqtt.python/examples/sub_to_db_ATM.py');
                system('sudo -r root -S  python /var/www/html/paho.mqtt.python/examples/sub_to_nappi.py');
                system('sudo -r root -S  python /var/www/html/paho.mqtt.python/examples/sub_to_db_rasp.py');
*/
        }




}
