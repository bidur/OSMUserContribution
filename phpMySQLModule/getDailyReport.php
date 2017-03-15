<?php
include('mysqlConnect.php');

$conn = new mysqli($server, $user, $password);  
mysqli_select_db($conn, 'osm_contributions');  

$setSql = "SELECT `username`, `created_year`,`created_month`, sum(`building_created`), sum(`building_modified`),sum(`building_deleted`), sum(`node_created`),sum(`node_modified`), sum(`node_deleted`) FROM `contributions` where  `created_year`='2017' group by `username`,`created_month`,`created_day`";
$setRec = mysqli_query($conn,$setSql);

$columnHeader ='';
#$columnHeader = "SN"."\t"."User Name"."\t"."Year"."\t"."Month"."\t"."Day"."\t"."Total Changes"."\t";
$columnHeader = "SN"."\t"."User Name"."\t"."Year"."\t"."building_created"."\t"."building_modified"."\t"."building_deleted"."\t"."node_created"."\t"."node_modified"."\t"."node_deleted"."\t";


$setData='';
$i=0;

while($rec = mysqli_fetch_row($setRec))  
{
  $rowData = '"' . ++$i . '"' . "\t";
  foreach($rec as $value)       
  {
    $value = '"' . $value . '"' . "\t";
    $rowData .= $value;
  }
  $setData .= trim($rowData)."\n";
}


header("Content-type: application/octet-stream");
header("Content-Disposition: attachment; filename=osmDailyReoprt.xls");
header("Pragma: no-cache");
header("Expires: 0");

echo ucwords($columnHeader)."\n".$setData."\n";

?>

