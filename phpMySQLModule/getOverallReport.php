<?php
include('mysqlConnect.php');

$conn = new mysqli($server, $user, $password);

mysqli_select_db($conn, 'osm_contributions');  

$setSql = "SELECT `username`, `created_year`, sum(`total_changes`) FROM `contributions`  where `created_year`='2017' group by `username`";
$setRec = mysqli_query($conn,$setSql);

$columnHeader ='';
$columnHeader = "SN"."\t"."User Name"."\t"."Year"."\t"."Total Changes"."\t";


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
header("Content-Disposition: attachment; filename=osmOverallReoprt.xls");
header("Pragma: no-cache");
header("Expires: 0");

echo ucwords($columnHeader)."\n".$setData."\n";

?>

