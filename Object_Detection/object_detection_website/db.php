<?php
// db.php: Database connection configuration

$host = 'localhost';
$user = 'root';
$password = '';
$database = 'object_detection';

$conn = new mysqli($host, $user, $password, $database);

if ($conn->connect_error) {
    die("Database connection failed: " . $conn->connect_error);
}
?>
