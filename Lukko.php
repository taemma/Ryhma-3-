<?php

        class Lukko extends CI_Model {

              /*  function __construct(){

                parent::__construct();
                $this->load->database();

                }*/

                function lukontila(){
                        $this->load->database();

                        $query = $this->db->query("SELECT * FROM logi ORDER BY id DESC");

                        $query->result_array();
                        return $query->result_array();
                }
                function atmtila(){

                        $query = $this->db->query('SELECT DISTINCT id,msg,aika  FROM lukontila ORDER BY id DESC LIMIT 1');

                        $query->result_array();
                        return $query->result_array();
                        /*$this->db->replace('lukontila');*/
                }

        }
?>
