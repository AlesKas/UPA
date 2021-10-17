package com.company;
import java.net.*;
import java.sql.*;
import java.util.Arrays;
import java.util.Locale;
import java.util.Optional;
import java.io.*;
import java.io.BufferedReader;

import static java.lang.Integer.parseInt;

public class Main {

    public static void main(String[] args) throws Exception {
        //DB configuration - TODO adapt to FIT VUT DB
        String jdbc_Url = "jdbc:mysql://localhost:3306/upa";
        String jdbc_Driver = "com.mysql.cj.jdbc.Driver";
        String db_name = "UPA_proj1";
        String username = "root";
        String password = "";
        Connection conn = null;

        //Check jdbc driver
        try {
            Class.forName(jdbc_Driver);
        } catch (ClassNotFoundException ex) {
            System.out.println("Driver Failed To Load");
            System.out.println(ex.getMessage());
        }
        //Connect to xampp server
        try {
            conn = DriverManager.getConnection(jdbc_Url, username, password);
        } catch (SQLException ex) {
            System.out.println("Failed To Connect To Server Successfully");
            System.out.println(ex.getMessage());
        }

        //Download csv files TODO - hard download?
        String url_string1 = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/zakladni-prehled.csv";
        String url_string2 = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.csv";
        String url_string3 = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/vyleceni.csv";
        String url_string4 = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv";
        String url_string5 = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv";
        String url_string6 = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv";
        String url_string7 = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-nakazeni-vyleceni-umrti.csv";
        String url_string8 = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/orp.csv";
        String url_string9 = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/obce.csv";
        String url_string10 = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/mestske-casti.csv";
        String url_string11 = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/incidence-7-14-cr.csv";
        String url_string12 = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/incidence-7-14-kraje.csv";
        String url_string13 = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/incidence-7-14-okresy.csv";
        String[] url_arr = {url_string1, url_string2, url_string3, url_string4, url_string5, url_string6, url_string7, url_string8, url_string9, url_string10, url_string11, url_string12, url_string13};

        //Table query
        //String table_zakladni_prehled = "CREATE TABLE zakladni_prehled ("+ "id INT(64) NOT NULL AUTO_INCREMENT," + "datum DATE,"+ "provedene_testy_celkem INT(64),"+ "potvrzene_pripady_celkem INT(64),"+ "aktivni_pripady INT(64),"+ "vyleceni INT(64),"+ "umrti INT(64),"+ "aktualne_hospitalizovani INT(64)," + "provedene_testy_vcerejsi_den INT(64),"+ "potvrzene_pripady_vcerejsi_den INT(64),"+ "potvrzene_pripady_dnesni_den INT(64),"+ "provedene_testy_vcerejsi_den_datum DATE,"+ "PRIMARY KEY(id))";
        String table_osoby = "CREATE TABLE IF NOT EXISTS osoby (id INT(64) NOT NULL AUTO_INCREMENT,"+ "datum DATE," + "vek INT(64),"+ "pohlavi VARCHAR(2), "+ "kraj_nuts_kod VARCHAR(20), "+ "okres_lau_kod VARCHAR(20), "+ "nakaza_v_zahranici BIT, "+ "nakaza_zeme_csu_kod VARCHAR(20), "+ "PRIMARY KEY(id))";
        String table_vyleceni = "CREATE TABLE IF NOT EXISTS vyleceni (datum DATE," + "vek INT(64),"+ "pohlavi VARCHAR(2), "+ "kraj_nuts_kod VARCHAR(20), "+ "okres_lau_kod VARCHAR(20))";
        String table_umrti = "CREATE TABLE IF NOT EXISTS umrti ("+ "id INT(64) NOT NULL AUTO_INCREMENT,"+ "datum DATE," + "vek INT(64),"+ "pohlavi VARCHAR(2), "+ "kraj_nuts_kod VARCHAR(20), "+ "okres_lau_kod VARCHAR(20), "+ "PRIMARY KEY(id))";
        String table_hospitalizace = "CREATE TABLE IF NOT EXISTS hospitalizace ("+ "id INT(64) NOT NULL AUTO_INCREMENT,"+ "datum DATE," + "pacient_prvni_zaznam INT(64),"+ "kum_pacient_prvni_zaznam INT(64),"+ "pocet_hosp INT(64),"+ "stav_bez_priznaku INT(64),"+ "stav_lehky INT(64),"+ "stav_stredni INT(64),"+ "stav_tezky INT(64),"+ "jip INT(64),"+ "kyslik INT(64),"+ "hfno INT(64),"+ "upv INT(64),"+ "ecmo INT(64),"+ "tezky_upv_ecmo INT(64),"+ "umrti INT(64),"+ "kum_umrti INT(64),"+ "PRIMARY KEY(id))";
        String table_nakazeni_vyleceni_umrti_testy = "CREATE TABLE IF NOT EXISTS nakazeni_vyleceni_umrti_testy ("+ "id INT(64) NOT NULL AUTO_INCREMENT,"+ "datum DATE," + "kumulativni_pocet_nakazenych INT(64),"+ "kumulativni_pocet_vylecenych INT(64),"+ "kumulativni_pocet_umrti INT(64),"+ "kumulativni_pocet_testu INT(64),"+ "kumulativni_pocet_ag_testu INT(64),"+ "prirustkovy_pocet_nakazenych INT(64),"+ "prirustkovy_pocet_vylecenych INT(64),"+ "prirustkovy_pocet_umrti INT(64),"+ "prirustkovy_pocet_provedenych_testu INT(64),"+ "prirustkovy_pocet_provedenych_ag_testu INT(64),"+ "PRIMARY KEY(id))";
        String table_kraj_okres_nakazeni_vyleceni_umrti = "CREATE TABLE IF NOT EXISTS kraj_okres_nakazeni_vyleceni_umrti ("+ "id INT(64) NOT NULL AUTO_INCREMENT,"+ "datum DATE," + "kraj_nuts_kod VARCHAR(20), "+ "okres_lau_kod VARCHAR(20), "+ "kumulativni_pocet_nakazenych INT(64),"+ "kumulativni_pocet_vylecenych INT(64),"+ "kumulativni_pocet_umrti INT(64),"+ "PRIMARY KEY(id))";
        String table_orp = "CREATE TABLE IF NOT EXISTS orp ("+ "id INT(64) NOT NULL AUTO_INCREMENT,"+ "den VARCHAR(20), "+ "datum DATE," + "orp_kod VARCHAR(20),"+ "orp_nazev VARCHAR(20), "+ "incidence_7 INT(64), "+ "incidence_65_7 INT(64), "+ "incidence_75_7 INT(64), "+ "prevalence INT(64), "+ "prevalence_65 INT(64), "+ "prevalence_75 INT(64), "+ "aktualni_pocet_hospitalizovanych_osob INT(64), "+ "nove_hosp_7 INT(64)," + "testy_7 INT(64), " + "PRIMARY KEY(id))";
        String table_obce = "CREATE TABLE IF NOT EXISTS obce ("+ "id INT(64) NOT NULL AUTO_INCREMENT,"+ "den VARCHAR(20), "+ "datum DATE," + "kraj_nuts_kod VARCHAR(20), "+ "kraj_nazev VARCHAR(20), " + "okres_lau_kod VARCHAR(20), " + "okres_nazev VARCHAR(20), " + "orp_kod INT(64),"+ "orp_nazev VARCHAR(20), "+ "obec_kod INT(64),"+ "obec_nazev VARCHAR(20), "+ "nove_pripady INT(64), "+ "aktivni_pripady INT(64), "+ "nove_pripady_65 INT(64), "+ "nove_pripady_7_dni INT(64), "+ "nove_pripady_14_dni INT(64), "+"PRIMARY KEY(id))";
        String table_mestske_casti = "CREATE TABLE IF NOT EXISTS mestske_casti ("+ "id INT(64) NOT NULL AUTO_INCREMENT,"+ "den VARCHAR(20), "+ "datum DATE," + "okres_nuts_kod VARCHAR(20), " + "orp_kod INT(64),"+ "orp_nazev VARCHAR(20), "+ "mc_kod INT(64),"+ "nove_pripady INT(64), "+ "aktivni_pripady INT(64), "+ "nove_pripady_65 INT(64), "+ "nove_pripady_7_dni INT(64), "+ "nove_pripady_14_dni INT(64), "+ "zemreli INT(64), "+ "vyleceni INT(64), "+ "PRIMARY KEY(id))";
        String table_incidence_7_14_cr = "CREATE TABLE IF NOT EXISTS incidence_7_14_cr ("+ "id INT(64) NOT NULL AUTO_INCREMENT,"+ "datum DATE," + "incidence_7 INT(64),"+ "incidence_14 INT(64), "+ "incidence_7_100000 FLOAT( 10, 2 ), " + "incidence_14_100000 FLOAT( 10, 2 ), "+ "PRIMARY KEY(id))";
        String table_incidence_7_14_kraje = "CREATE TABLE IF NOT EXISTS incidence_7_14_kraje ("+ "id INT(64) NOT NULL AUTO_INCREMENT,"+ "datum DATE,"  + "kraj_nuts_kod VARCHAR(20), "+ "kraj_nazev VARCHAR(20), " + "incidence_7 INT(64),"+ "incidence_14 INT(64), "+ "incidence_7_100000 FLOAT(8,4), "+ "incidence_14_100000 FLOAT(8,4), "+ "PRIMARY KEY(id))";
        String table_incidence_7_14_okresy = "CREATE TABLE IF NOT EXISTS incidence_7_14_okresy ("+ "id INT(64) NOT NULL AUTO_INCREMENT,"+ "datum DATE,"  + "okres_lau_kod VARCHAR(20), "+ "okres_nazev VARCHAR(20), " + "incidence_7 INT(64),"+ "incidence_14 INT(64), "+ "incidence_7_100000 FLOAT(8,4), "+ "incidence_14_100000 FLOAT(8,4), "+ "PRIMARY KEY(id))";
        String[] table_arrs = {table_osoby, table_vyleceni, table_umrti, table_hospitalizace, table_nakazeni_vyleceni_umrti_testy, table_kraj_okres_nakazeni_vyleceni_umrti, table_orp, table_obce, table_mestske_casti, table_incidence_7_14_cr, table_incidence_7_14_kraje, table_incidence_7_14_okresy};

        //Inserts query
        //String insert_into_zakladni_prehled = "insert into zakladni_prehled (datum, provedene_testy_celkem, potvrzene_pripady_celkem, aktivni_pripady, vyleceni, umrti, aktualne_hospitalizovani, provedene_testy_vcerejsi_den, potvrzene_pripady_vcerejsi_den, potvrzene_pripady_dnesni_den, provedene_testy_vcerejsi_den_datum) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        String insert_into_osoby = "insert into osoby (datum, vek, pohlavi, kraj_nuts_kod, okres_lau_kod, nakaza_v_zahranici, nakaza_zeme_csu_kod) values (?, ?, ?, ?, ?, ?, ?)";
        String insert_into_vyleceni = "insert into vyleceni (datum, vek, pohlavi, kraj_nuts_kod, okres_lau_kod) values (?, ?, ?, ?, ?)";
        String insert_into_umrti = "insert into umrti (datum, vek, pohlavi, kraj_nuts_kod, okres_lau_kod) values (?, ?, ?, ?, ?)";
        String insert_into_hospitalizace = "insert into hospitalizace (datum, pacient_prvni_zaznam, kum_pacient_prvni_zaznam, pocet_hosp, stav_bez_priznaku, stav_lehky, stav_stredni, stav_tezky, jip, kyslik, hfno, upv, ecmo, tezky_upv_ecmo, umrti, kum_umrti) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        String insert_into_nakazeni_vyleceni_umrti_testy = "insert into nakazeni_vyleceni_umrti_testy (datum, kumulativni_pocet_nakazenych, kumulativni_pocet_vylecenych, kumulativni_pocet_umrti, kumulativni_pocet_testu, kumulativni_pocet_ag_testu, prirustkovy_pocet_nakazenych, prirustkovy_pocet_vylecenych, prirustkovy_pocet_umrti, prirustkovy_pocet_provedenych_testu, prirustkovy_pocet_provedenych_ag_testu) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        String insert_into_kraj_okres_nakazeni_vyleceni_umrti = "insert into kraj_okres_nakazeni_vyleceni_umrti (datum, kraj_nuts_kod, okres_lau_kod, kumulativni_pocet_nakazenych, kumulativni_pocet_vylecenych, kumulativni_pocet_umrti) values (?, ?, ?, ?, ?, ?)";
        String insert_into_orp = "insert into orp (den, datum, orp_kod, orp_nazev, incidence_7, incidence_65_7, incidence_75_7, prevalence, prevalence_65, prevalence_75, aktualni_pocet_hospitalizovanych_osob, nove_hosp_7, testy_7) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        String insert_into_obce = "insert into obce (den, datum, kraj_nuts_kod, kraj_nazev, okres_lau_kod, okres_nazev, orp_kod, orp_nazev, obec_kod, obec_nazev, nove_pripady, aktivni_pripady, nove_pripady_65, nove_pripady_7_dni, nove_pripady_14_dni) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        String insert_into_mestske_casti = "insert into mestske_casti (den, datum, okres_nuts_kod, orp_kod, orp_nazev, mc_kod, nove_pripady, aktivni_pripady, nove_pripady_65, nove_pripady_7_dni, nove_pripady_14_dni, zemreli, vyleceni) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        String insert_into_incidence_7_14_cr = "insert into incidence_7_14_cr (datum, incidence_7, incidence_14, incidence_7_100000, incidence_14_100000) values (?, ?, ?, ?, ?)";
        String insert_into_incidence_7_14_kraje = "insert into incidence_7_14_kraje (datum, kraj_nuts_kod, kraj_nazev, incidence_7, incidence_14, incidence_7_100000, incidence_14_100000) values (?, ?, ?, ?, ?, ?, ?)";
        String insert_into_incidence_7_14_okresy = "insert into incidence_7_14_okresy (datum, okres_lau_kod, okres_nazev, incidence_7, incidence_14, incidence_7_100000, incidence_14_100000) values (?, ?, ?, ?, ?, ?, ?)";
        String[] insert_arrs = {insert_into_osoby, insert_into_vyleceni, insert_into_umrti, insert_into_hospitalizace, insert_into_nakazeni_vyleceni_umrti_testy, insert_into_kraj_okres_nakazeni_vyleceni_umrti, insert_into_orp, insert_into_obce, insert_into_mestske_casti, insert_into_incidence_7_14_cr, insert_into_incidence_7_14_kraje, insert_into_incidence_7_14_okresy};

        try{
            conn = DriverManager.getConnection(jdbc_Url, username, password);
            conn.setAutoCommit(false);

            //Create DB
            Statement statement_create_db = conn.createStatement();
            statement_create_db.executeUpdate("CREATE DATABASE IF NOT EXISTS " + db_name);

            //Create Tables in DB
            Statement statement_create_table = null;
            for (String one_table : table_arrs){
                statement_create_table = conn.createStatement();
                statement_create_table.executeUpdate(one_table);
            }

            //Insert data to tables
            for (String one_url : url_arr){
                //Extract csv file from url
                String csv_name = one_url.substring(52, one_url.length() - 4);

               //Search suitable insert command for csv file
               for (String one_insert : insert_arrs){

                   //Match csv file and insert
                   if (one_insert.toLowerCase().contains(csv_name)){

                       PreparedStatement statement_insert_data = conn.prepareStatement(one_insert);

                       //Open csv file
                       URL url = new URL(one_url);
                       BufferedReader read = new BufferedReader(new InputStreamReader(url.openStream()));
                       String one_line;
                       String[] data = null;
                       int colum_counter = 0;
                       boolean first_line = true;

                       FIRST_LOOP:
                       while ((one_line = read.readLine()) != null) {
                           System.out.println(csv_name);
                           //Skip the header
                           if (first_line){
                               //Counting number of columns
                               String[] column_split = one_line.split(",");
                               colum_counter = column_split.length;
                               first_line = false;
                               continue;
                           }

                           data = one_line.split(",");

                           //Skip line with missing data
                           if (data.length != colum_counter){
                               continue;
                           }

                           for (int i = 0; i < data.length; i++){
                               if(data[i].isEmpty() || data[i] == null) {
                                   continue FIRST_LOOP;
                               }
                           }

                           switch (csv_name){
                               case "vyleceni":
                                   Date sql_date =Date.valueOf(data[0]);
                                   statement_insert_data.setDate(1, sql_date);
                                   statement_insert_data.setInt(2, parseInt(data[1]));
                                   statement_insert_data.setString(3, data[2]);
                                   statement_insert_data.setString(4, data[3]);
                                   statement_insert_data.setString(5, data[4]);
                                   statement_insert_data.addBatch();
                                   break;
                               case "osoby": break; //TODO insert statements
                               case "zakladni_prehled": break; //TODO insert statements
                               case "umrti": break; //TODO insert statements
                               case "hospitalizace": break; //TODO insert statements
                               case "nakazeni_vyleceni_umrti_testy": break; //TODO insert statements
                               case "kraj_okres_nakazeni_vyleceni_umrti": break; //TODO insert statements
                               case "orp": break; //TODO insert statements
                               case "obce": break; //TODO insert statements
                               case "mestske_casti": break; //TODO insert statements
                               case "incidence_7_14_cr": break; //TODO insert statements
                               case "incidence_7_14_kraje": break; //TODO insert statements
                               case "incidence_7_14_okresy": break; //TODO insert statements
                               default:
                                   //System.out.println("No such db.");
                           }
                       }
                       System.out.println("Zde 1");
                       statement_insert_data.executeBatch();
                       System.out.println("Zde 2");
                       conn.commit();
                       System.out.println("Zde 3");
                       read.close();
                       System.out.println("Zde 4");
                   }
               }
            }

            System.out.println("Zde 5");
            statement_create_table.close();
            System.out.println("Zde 6");
            statement_create_db.close();
            System.out.println("Zde 7");
            conn.close();
            System.out.println("Zde 8");

        } catch (Exception e){
            System.out.println("rrr");
        }
    }
}
